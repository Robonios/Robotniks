#!/usr/bin/env python3
"""
Robotnik Benchmark Price Fetcher
=================================
Fetches daily price history for benchmark indices/ETFs:
  SPY  (S&P 500 proxy)
  QQQ  (NASDAQ Composite proxy)
  SOXX (PHLX Semiconductor Index proxy)
  ROBO (ROBO Global Robotics & Automation ETF)

Sources: EODHD (primary), Alpha Vantage (fallback)

Outputs:
    data/prices/benchmarks.json  — combined daily series for all benchmarks

Usage:
    python scripts/fetch_benchmarks.py
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, date, timedelta
from pathlib import Path

# ── paths ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "prices"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DATA_DIR / "benchmarks.json"

# ── load env & API keys ─────────────────────────────────────────────────
def load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()
EODHD_KEY = os.environ.get("EODHD_API_KEY", "")
AV_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "")

# ── benchmarks ───────────────────────────────────────────────────────────
BENCHMARKS = {
    "SPY": {
        "name": "S&P 500 (SPY ETF)",
        "eodhd_symbol": "SPY.US",
        "color": "#7B8794",
    },
    "QQQ": {
        "name": "NASDAQ Composite (QQQ ETF)",
        "eodhd_symbol": "QQQ.US",
        "color": "#5B9BD5",
    },
    "SOXX": {
        "name": "PHLX Semiconductor Index (SOXX ETF)",
        "eodhd_symbol": "SOXX.US",
        "color": "#E97451",
    },
    "ROBO": {
        "name": "ROBO Global Robotics & Automation ETF",
        "eodhd_symbol": "ROBO.US",
        "color": "#70AD47",
    },
}

# ── EODHD fetcher ────────────────────────────────────────────────────────
def fetch_eodhd_history(symbol, years=5):
    """Fetch daily OHLCV from EODHD for the last N years."""
    from_date = (date.today() - timedelta(days=365 * years)).isoformat()
    url = (
        "https://eodhd.com/api/eod/{symbol}"
        "?api_token={key}&fmt=json&order=a&from={from_date}"
    ).format(symbol=symbol, key=EODHD_KEY, from_date=from_date)

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Robotnik/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        if not data or not isinstance(data, list):
            return None
        # Convert to series format
        series = []
        for day in data:
            series.append({
                "date": day["date"],
                "open": day.get("open"),
                "high": day.get("high"),
                "low": day.get("low"),
                "close": day["close"],
                "volume": day.get("volume"),
            })
        return series
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        print("  EODHD error for {}: {}".format(symbol, e))
        return None


# ── Alpha Vantage fallback ───────────────────────────────────────────────
FROM_DATE = "2021-01-01"

def _av_request(url):
    """Make an Alpha Vantage API request."""
    req = urllib.request.Request(url, headers={"User-Agent": "Robotnik/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def fetch_av_history(symbol):
    """Fetch 5Y history via AV: weekly adjusted (full) + daily compact, merged."""
    if not AV_KEY:
        return None

    weekly_series = []
    daily_series = []

    # 1. Weekly adjusted — full history (free tier)
    try:
        url = ("https://www.alphavantage.co/query?"
               "function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={}&apikey={}").format(symbol, AV_KEY)
        data = _av_request(url)
        ts = data.get("Weekly Adjusted Time Series", {})
        if ts:
            for d in sorted(ts.keys()):
                if d >= FROM_DATE:
                    weekly_series.append({
                        "date": d,
                        "close": float(ts[d]["5. adjusted close"]),
                    })
            print("  AV weekly: {} weeks ({} to {})".format(
                len(weekly_series), weekly_series[0]["date"], weekly_series[-1]["date"]))
        else:
            note = data.get("Note") or data.get("Information") or data.get("Error Message")
            print("  AV weekly failed for {}: {}".format(symbol, note))
    except Exception as e:
        print("  AV weekly error for {}: {}".format(symbol, e))

    time.sleep(15)  # AV rate limit: 5 calls/min

    # 2. Daily compact — last ~100 trading days (free tier)
    try:
        url = ("https://www.alphavantage.co/query?"
               "function=TIME_SERIES_DAILY&symbol={}&outputsize=compact&apikey={}").format(symbol, AV_KEY)
        data = _av_request(url)
        ts = data.get("Time Series (Daily)", {})
        if ts:
            for d in sorted(ts.keys()):
                daily_series.append({
                    "date": d,
                    "close": float(ts[d]["4. close"]),
                })
            print("  AV daily: {} days ({} to {})".format(
                len(daily_series), daily_series[0]["date"], daily_series[-1]["date"]))
        else:
            note = data.get("Note") or data.get("Information") or data.get("Error Message")
            print("  AV daily failed for {}: {}".format(symbol, note))
    except Exception as e:
        print("  AV daily error for {}: {}".format(symbol, e))

    # 3. Merge: weekly history + daily for recent period (daily overrides overlap)
    if weekly_series and daily_series:
        daily_start = daily_series[0]["date"]
        merged = [pt for pt in weekly_series if pt["date"] < daily_start]
        merged.extend(daily_series)
        print("  Merged: {} data points ({} to {})".format(
            len(merged), merged[0]["date"], merged[-1]["date"]))
        return merged
    elif daily_series:
        return daily_series
    elif weekly_series:
        return weekly_series
    return None


# ── main ─────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("ROBOTNIK BENCHMARK PRICE FETCHER")
    print("=" * 60)

    ts = datetime.utcnow().isoformat() + "Z"
    output = {
        "fetched_at": ts,
        "base_date": "2025-03-31",
        "base_value": 1000,
        "benchmarks": {},
    }

    for ticker, info in BENCHMARKS.items():
        print("\nFetching {} ({})...".format(ticker, info["name"]))

        series = None

        # Try EODHD first
        if EODHD_KEY:
            series = fetch_eodhd_history(info["eodhd_symbol"])
            if series:
                print("  EODHD: {} data points ({} to {})".format(
                    len(series), series[0]["date"], series[-1]["date"]
                ))

        # Fallback to Alpha Vantage
        if not series and AV_KEY:
            print("  Trying Alpha Vantage fallback...")
            series = fetch_av_history(ticker)
            if series:
                print("  AV: {} data points ({} to {})".format(
                    len(series), series[0]["date"], series[-1]["date"]
                ))
            time.sleep(15)  # AV rate limit

        if series:
            output["benchmarks"][ticker] = {
                "ticker": ticker,
                "name": info["name"],
                "color": info["color"],
                "days": len(series),
                "from": series[0]["date"],
                "to": series[-1]["date"],
                "series": series,
            }
        else:
            print("  WARNING: No data for {}".format(ticker))
            output["benchmarks"][ticker] = {
                "ticker": ticker,
                "name": info["name"],
                "color": info["color"],
                "days": 0,
                "from": None,
                "to": None,
                "series": [],
            }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    total = sum(b["days"] for b in output["benchmarks"].values())
    print("\n" + "=" * 60)
    print("DONE: {} benchmarks, {} total data points".format(
        len(output["benchmarks"]), total
    ))
    print("Output: {}".format(OUTPUT_PATH))
    print("=" * 60)


if __name__ == "__main__":
    main()
