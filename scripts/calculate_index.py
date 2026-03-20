#!/usr/bin/env python3
"""
Robotnik Composite Index Calculator

Produces a market-cap weighted index with:
- 5% single-entity cap with iterative redistribution
- Base value 1000.00 (set on first run = base date)
- 4 sub-indices: Semiconductor, Robotics, Cross-stack, Token
- Outputs: weights.json, robotnik_index.json, sub_indices.json,
           base_date.json, summary.json
"""

import json
import os
import sys
from datetime import datetime, timezone

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(SCRIPT_DIR)
INDEX_DIR  = os.path.join(ROOT_DIR, "data", "index")

MCAP_PATH    = os.path.join(INDEX_DIR, "market_caps.json")
PRICES_PATH  = os.path.join(ROOT_DIR, "data", "prices", "all_prices.json")

WEIGHTS_PATH   = os.path.join(INDEX_DIR, "weights.json")
INDEX_PATH     = os.path.join(INDEX_DIR, "robotnik_index.json")
SUB_IDX_PATH   = os.path.join(INDEX_DIR, "sub_indices.json")
BASE_DATE_PATH = os.path.join(INDEX_DIR, "base_date.json")
SUMMARY_PATH   = os.path.join(INDEX_DIR, "summary.json")

BASE_VALUE = 1000.0
CAP_LIMIT  = 0.05  # 5% max weight per entity

# sector mapping for sub-indices
SECTOR_MAP = {
    "Semiconductor": "Semiconductor",
    "Semis":         "Semiconductor",
    "Robotics":      "Robotics",
    "Cross-stack":   "Cross-stack",
    "Token":         "Token",
}


def load_json(path):
    with open(path) as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  -> {os.path.relpath(path, ROOT_DIR)}")


def compute_capped_weights(entities, cap=CAP_LIMIT):
    """
    Market-cap weighted with iterative 5% cap redistribution.
    Each entity above the cap is pinned at cap%; the excess is
    redistributed proportionally among uncapped entities. Repeat
    until no entity exceeds the cap.
    """
    total_mcap = sum(e["market_cap_usd"] for e in entities)
    if total_mcap == 0:
        return {e["ticker"]: 0.0 for e in entities}

    weights = {e["ticker"]: e["market_cap_usd"] / total_mcap for e in entities}

    for _ in range(50):  # max iterations (converges in <10)
        capped = {t: w for t, w in weights.items() if w > cap}
        if not capped:
            break

        excess = sum(w - cap for w in capped.values())
        uncapped = {t: w for t, w in weights.items() if w <= cap}
        uncapped_total = sum(uncapped.values())

        if uncapped_total == 0:
            break

        for t in capped:
            weights[t] = cap

        for t in uncapped:
            weights[t] += excess * (uncapped[t] / uncapped_total)

    return weights


def build_base_date(today_str, entities, weights, prices_by_ticker):
    """Create base_date.json on the very first run."""
    base_prices = {}
    for e in entities:
        t = e["ticker"]
        if t in prices_by_ticker:
            base_prices[t] = prices_by_ticker[t]

    base = {
        "base_date": today_str,
        "base_value": BASE_VALUE,
        "base_prices": base_prices,
        "base_weights": weights,
        "entity_count": len(entities),
    }
    save_json(BASE_DATE_PATH, base)
    return base


def calculate_index_value(weights, prices_by_ticker, base_data):
    """
    Index = base_value * sum( w_i * P_i / P_i_base )
    where w_i is the capped weight, P_i is current price,
    and P_i_base is the price on the base date.
    """
    base_prices = base_data["base_prices"]
    base_value  = base_data["base_value"]

    weighted_return = 0.0
    active_weight   = 0.0

    for ticker, weight in weights.items():
        if ticker in prices_by_ticker and ticker in base_prices:
            p_now  = prices_by_ticker[ticker]
            p_base = base_prices[ticker]
            if p_base > 0:
                weighted_return += weight * (p_now / p_base)
                active_weight   += weight

    if active_weight == 0:
        return BASE_VALUE

    # normalize by active weight so missing tickers don't drag down
    index_value = base_value * (weighted_return / active_weight)
    return round(index_value, 2)


def main():
    print("Robotnik Index Calculator")
    print("=" * 40)

    # ── load inputs ──────────────────────────────────────────────────
    mcap_data   = load_json(MCAP_PATH)
    prices_data = load_json(PRICES_PATH)

    entities = mcap_data["market_caps"]
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # build price lookup: ticker -> price (USD)
    prices_by_ticker = {}
    for p in prices_data["prices"]:
        t = p["ticker"]
        if p.get("price") is not None:
            prices_by_ticker[t] = p["price"]

    # normalize sectors
    for e in entities:
        e["sector"] = SECTOR_MAP.get(e.get("sector", ""), e.get("sector", "Other"))

    # filter to entities that have both mcap > 0 and a current price
    eligible = [e for e in entities
                if e["market_cap_usd"] > 0 and e["ticker"] in prices_by_ticker]

    print(f"  Eligible entities: {len(eligible)} / {len(entities)}")

    # ── compute capped weights ───────────────────────────────────────
    weights = compute_capped_weights(eligible)

    # verify cap
    over_cap = {t: w for t, w in weights.items() if w > CAP_LIMIT + 0.0001}
    if over_cap:
        print(f"  WARNING: {len(over_cap)} entities still over cap: {over_cap}")

    # ── weights.json ─────────────────────────────────────────────────
    weights_output = {
        "calculated_at": datetime.now(timezone.utc).isoformat() + "Z",
        "cap_limit_pct": CAP_LIMIT * 100,
        "entity_count": len(eligible),
        "weights": sorted(
            [{"ticker": e["ticker"], "name": e["name"], "sector": e["sector"],
              "market_cap_usd": e["market_cap_usd"],
              "weight_pct": round(weights[e["ticker"]] * 100, 4)}
             for e in eligible],
            key=lambda x: x["weight_pct"], reverse=True
        ),
    }
    save_json(WEIGHTS_PATH, weights_output)

    # ── base date (first run only) ───────────────────────────────────
    if os.path.exists(BASE_DATE_PATH):
        base_data = load_json(BASE_DATE_PATH)
        print(f"  Base date: {base_data['base_date']} (existing)")
    else:
        base_data = build_base_date(today_str, eligible, weights, prices_by_ticker)
        print(f"  Base date: {today_str} (NEW — first run)")

    # ── composite index ──────────────────────────────────────────────
    composite_value = calculate_index_value(weights, prices_by_ticker, base_data)

    # load existing time series or start new
    if os.path.exists(INDEX_PATH):
        index_data = load_json(INDEX_PATH)
        series = index_data.get("series", [])
    else:
        series = []

    # append or update today's entry
    today_entry = {"date": today_str, "value": composite_value}
    if series and series[-1]["date"] == today_str:
        series[-1] = today_entry
    else:
        series.append(today_entry)

    index_output = {
        "name": "Robotnik Composite Index",
        "base_date": base_data["base_date"],
        "base_value": BASE_VALUE,
        "current_value": composite_value,
        "current_date": today_str,
        "entity_count": len(eligible),
        "series": series,
    }
    save_json(INDEX_PATH, index_output)

    # ── sub-indices ──────────────────────────────────────────────────
    sub_sectors = ["Semiconductor", "Robotics", "Cross-stack", "Token"]
    sub_indices = {}

    for sector in sub_sectors:
        sector_entities = [e for e in eligible if e["sector"] == sector]
        if not sector_entities:
            continue

        sector_weights = compute_capped_weights(sector_entities)
        sector_value = calculate_index_value(sector_weights, prices_by_ticker, base_data)

        # sub-index series
        sub_key = sector.lower().replace("-", "_")
        if os.path.exists(SUB_IDX_PATH):
            existing = load_json(SUB_IDX_PATH)
            sub_series = existing.get(sub_key, {}).get("series", [])
        else:
            sub_series = []

        sub_entry = {"date": today_str, "value": sector_value}
        if sub_series and sub_series[-1]["date"] == today_str:
            sub_series[-1] = sub_entry
        else:
            sub_series.append(sub_entry)

        sub_indices[sub_key] = {
            "name": f"Robotnik {sector} Index",
            "current_value": sector_value,
            "entity_count": len(sector_entities),
            "top_5": sorted(
                [{"ticker": e["ticker"], "name": e["name"],
                  "weight_pct": round(sector_weights[e["ticker"]] * 100, 2)}
                 for e in sector_entities],
                key=lambda x: x["weight_pct"], reverse=True
            )[:5],
            "series": sub_series,
        }

    save_json(SUB_IDX_PATH, sub_indices)

    # ── summary.json ─────────────────────────────────────────────────
    # daily change (if we have >= 2 data points)
    prev_value = series[-2]["value"] if len(series) >= 2 else BASE_VALUE
    daily_change_pct = round((composite_value - prev_value) / prev_value * 100, 2) if prev_value else 0

    summary = {
        "calculated_at": datetime.now(timezone.utc).isoformat() + "Z",
        "composite": {
            "name": "Robotnik Composite Index",
            "value": composite_value,
            "daily_change_pct": daily_change_pct,
            "base_date": base_data["base_date"],
            "base_value": BASE_VALUE,
            "entities": len(eligible),
        },
        "sub_indices": {
            k: {"name": v["name"], "value": v["current_value"],
                "entities": v["entity_count"]}
            for k, v in sub_indices.items()
        },
        "top_10_weights": weights_output["weights"][:10],
    }
    save_json(SUMMARY_PATH, summary)

    # ── print summary ────────────────────────────────────────────────
    print()
    print(f"  ROBOTNIK COMPOSITE INDEX: {composite_value:,.2f}")
    print(f"  Daily change: {daily_change_pct:+.2f}%")
    print(f"  Entities: {len(eligible)}")
    print()
    for k, v in sub_indices.items():
        print(f"  {v['name']}: {v['current_value']:,.2f} ({v['entity_count']} entities)")
    print()
    print("  Top 5 weights:")
    for w in weights_output["weights"][:5]:
        print(f"    {w['ticker']:8s} {w['weight_pct']:6.2f}%  ({w['name']})")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
