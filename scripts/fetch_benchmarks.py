#!/usr/bin/env python3
"""
Robotnik Benchmark Price Fetcher
=================================
Fetches daily price history for benchmark indices/ETFs from EODHD:
  SPY  (S&P 500 proxy)
  QQQ  (NASDAQ Composite proxy)
  SOXX (PHLX Semiconductor Index proxy)
  ROBO (ROBO Global Robotics & Automation ETF)

Outputs:
    data/prices/benchmarks.json  — daily close series for all benchmarks

Usage:
    python scripts/fetch_benchmarks.py
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, date
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

# ── config ───────────────────────────────────────────────────────────────
FROM_DATE = "2021-01-01"
BASE_DATE = "2025-03-31"
BASE_VALUE = 1000

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
def fetch_eodhd_daily(symbol):
    """Fetch full daily OHLCV from EODHD, 2021-01-01 to today."""
    to_date = date.today().isoformat()
    url = (
        "https://eodhd.com/api/eod/{symbol}"
        "?from={from_date}&to={to_date}&period=d"
        "&api_token={key}&fmt=json"
    ).format(symbol=symbol, from_date=FROM_DATE, to_date=to_date, key=EODHD_KEY)

    req = urllib.request.Request(url, headers={"User-Agent": "Robotnik/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())

    if not data or not isinstance(data, list):
        return None

    series = []
    for day in data:
        series.append({
            "date": day["date"],
            "close": day["close"],
            "volume": day.get("volume"),
        })
    return series


# ── main ─────────────────────────────────────────────────────────────────
def main():
    if not EODHD_KEY:
        print("ERROR: EODHD_API_KEY not set")
        sys.exit(1)

    print("=" * 60)
    print("ROBOTNIK BENCHMARK PRICE FETCHER")
    print("  Source: EODHD (All-in-One)")
    print("  Range:  {} to today".format(FROM_DATE))
    print("=" * 60)

    ts = datetime.utcnow().isoformat() + "Z"
    output = {
        "fetched_at": ts,
        "source": "EODHD (eodhd.com)",
        "base_date": BASE_DATE,
        "base_value": BASE_VALUE,
        "benchmarks": {},
    }

    for ticker, info in BENCHMARKS.items():
        print("\n[{}] {} ...".format(ticker, info["eodhd_symbol"]), end=" ")
        try:
            series = fetch_eodhd_daily(info["eodhd_symbol"])
            if series:
                print("{} days ({} to {})".format(
                    len(series), series[0]["date"], series[-1]["date"]))
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
                print("NO DATA")
                output["benchmarks"][ticker] = {
                    "ticker": ticker,
                    "name": info["name"],
                    "color": info["color"],
                    "days": 0,
                    "from": None,
                    "to": None,
                    "series": [],
                }
        except Exception as e:
            print("ERROR: {}".format(e))
            output["benchmarks"][ticker] = {
                "ticker": ticker,
                "name": info["name"],
                "color": info["color"],
                "days": 0,
                "from": None,
                "to": None,
                "series": [],
                "error": str(e),
            }
        time.sleep(0.2)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    total = sum(b["days"] for b in output["benchmarks"].values())
    print("\n" + "=" * 60)
    print("DONE: {} benchmarks, {} total data points".format(
        len(output["benchmarks"]), total))
    print("Output: {}".format(OUTPUT_PATH))
    print("=" * 60)


if __name__ == "__main__":
    main()
