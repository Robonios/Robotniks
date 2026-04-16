#!/usr/bin/env python3
"""
Robotnik Yahoo Finance Fetcher
==============================
Fetches daily OHLCV data from Yahoo Finance's public chart API (no key required).
Used as a per-ticker override for entities where the primary provider (EODHD)
has structural limitations — e.g. Hanwha Aerospace (012450.KS), which EODHD
caps at ₩999,999.9999.

Loud failure semantics: every error path raises an explicit exception. Do not
fall back silently — callers must decide whether to drop the ticker or abort.
"""

import json
import time
import urllib.request
import urllib.error


YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

# Range tokens supported by the Yahoo chart API.
_RANGE_FOR_OUTPUT_SIZE = {
    "full":    "10y",   # ~10 years of daily bars
    "compact": "100d",  # ~100 trading days
    "5d":      "5d",
    "1mo":     "1mo",
    "3mo":     "3mo",
    "6mo":     "6mo",
    "1y":      "1y",
    "2y":      "2y",
    "5y":      "5y",
    "10y":     "10y",
    "max":     "max",
}


class YahooFetchError(Exception):
    """Raised when Yahoo returns an error, empty data, or malformed payload."""


def _http_get_json(url, timeout=30, max_retries=3):
    """GET a Yahoo chart URL with retry on 429 / 5xx. Returns parsed JSON."""
    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Robotnik/1.0 yahoo override fetcher)",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            last_err = e
            # Rate-limit or transient server error → backoff and retry
            if e.code in (429, 500, 502, 503, 504):
                sleep_s = 2 ** attempt  # 1s, 2s, 4s
                print(f"  [yahoo] HTTP {e.code}; sleeping {sleep_s}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(sleep_s)
                continue
            raise YahooFetchError(f"HTTP {e.code} from Yahoo: {e.reason}") from e
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            last_err = e
            sleep_s = 2 ** attempt
            print(f"  [yahoo] network error {e!r}; sleeping {sleep_s}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(sleep_s)
    raise YahooFetchError(f"Yahoo request failed after {max_retries} retries: {last_err!r}")


def fetch_yahoo_daily(symbol, output_size="full"):
    """Fetch daily OHLCV for one Yahoo symbol in native currency.

    Args:
        symbol: Yahoo-format symbol, e.g. "012450.KS" for Hanwha Aerospace.
        output_size: "full" (10y), "compact" (100d), or any raw Yahoo range token.

    Returns:
        {
            "symbol":   <str>,
            "currency": <str>,     # e.g. "KRW"
            "exchange": <str>,
            "series":   { "YYYY-MM-DD": { "open": ..., "high": ..., "low": ...,
                                          "close": ..., "volume": ... }, ... }
        }

    Raises:
        YahooFetchError: on HTTP error, empty payload, or structural mismatch.
    """
    rng = _RANGE_FOR_OUTPUT_SIZE.get(output_size, output_size)
    url = (
        YAHOO_CHART_URL.format(symbol=symbol)
        + f"?interval=1d&range={rng}&events=div%2Csplit"
    )

    print(f"  [yahoo] GET {symbol} range={rng}")
    payload = _http_get_json(url)

    chart = payload.get("chart") or {}
    err = chart.get("error")
    if err:
        raise YahooFetchError(f"Yahoo error for {symbol}: {err}")

    results = chart.get("result") or []
    if not results:
        raise YahooFetchError(f"Yahoo returned empty result for {symbol}")

    r0 = results[0]
    meta = r0.get("meta") or {}
    timestamps = r0.get("timestamp") or []
    quote = ((r0.get("indicators") or {}).get("quote") or [{}])[0]
    opens = quote.get("open") or []
    highs = quote.get("high") or []
    lows = quote.get("low") or []
    closes = quote.get("close") or []
    volumes = quote.get("volume") or []

    if not timestamps or not closes:
        raise YahooFetchError(f"Yahoo returned no bars for {symbol}")

    currency = meta.get("currency") or "USD"
    exchange = meta.get("exchangeName") or ""

    # Build date-keyed series. Yahoo returns the current (possibly in-progress)
    # bar with null close if market has not yet settled; skip those rows so
    # downstream never sees a null close.
    from datetime import datetime, timezone

    series = {}
    skipped_null = 0
    for i, ts in enumerate(timestamps):
        close = closes[i] if i < len(closes) else None
        if close is None:
            skipped_null += 1
            continue
        # Yahoo timestamps are exchange-local midnight in UTC seconds.
        d = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        series[d] = {
            "open":   opens[i] if i < len(opens) else None,
            "high":   highs[i] if i < len(highs) else None,
            "low":    lows[i] if i < len(lows) else None,
            "close":  close,
            "volume": volumes[i] if i < len(volumes) else None,
        }

    if not series:
        raise YahooFetchError(
            f"Yahoo returned only null bars for {symbol} (skipped {skipped_null})"
        )

    first = min(series.keys())
    last = max(series.keys())
    print(
        f"  [yahoo] {symbol}: {len(series)} bars "
        f"({first} → {last}, {currency}, {exchange}"
        + (f", skipped {skipped_null} null)" if skipped_null else ")")
    )

    return {
        "symbol": symbol,
        "currency": currency,
        "exchange": exchange,
        "series": series,
    }


def fetch_latest_from_yahoo(symbol):
    """Compact wrapper returning the most recent close in a shape compatible
    with fetch_prices.fetch_eodhd_price().

    Returns:
        {
            "price":      <float>,   # latest close, native currency
            "date":       <str>,     # YYYY-MM-DD
            "volume":     <int|None>,
            "change_pct": <float|None>,
            "currency":   <str>,
        }

    Raises:
        YahooFetchError if Yahoo cannot deliver data.
    """
    data = fetch_yahoo_daily(symbol, output_size="compact")
    series = data["series"]
    dates = sorted(series.keys())
    latest_date = dates[-1]
    latest = series[latest_date]
    prev_close = series[dates[-2]]["close"] if len(dates) >= 2 else None
    change_pct = None
    if prev_close and prev_close != 0:
        change_pct = round((latest["close"] - prev_close) / prev_close * 100, 2)
    return {
        "price":      latest["close"],
        "date":       latest_date,
        "volume":     latest.get("volume"),
        "change_pct": change_pct,
        "currency":   data["currency"],
    }


if __name__ == "__main__":
    # Smoke test — fetch Hanwha and print a 5-row sample.
    import sys
    sym = sys.argv[1] if len(sys.argv) > 1 else "012450.KS"
    try:
        out = fetch_yahoo_daily(sym, output_size="compact")
        print(f"\nSymbol: {out['symbol']}  Currency: {out['currency']}  Exchange: {out['exchange']}")
        print(f"Total bars: {len(out['series'])}")
        last5 = sorted(out["series"].keys())[-5:]
        print(f"\nMost recent 5 trading days:")
        for d in last5:
            b = out["series"][d]
            print(f"  {d}  open={b['open']}  high={b['high']}  low={b['low']}  close={b['close']}  vol={b['volume']}")

        # Adapter test
        latest = fetch_latest_from_yahoo(sym)
        print(f"\nLatest (adapter):  {latest}")
    except YahooFetchError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
