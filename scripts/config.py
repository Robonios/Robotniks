"""
Shared configuration for Robotniks data fetchers.
Loads API keys from .env file — no external dependencies.
"""
import os
from pathlib import Path

# scripts/ is one level below project root
BASE_DIR = Path(__file__).parent.parent

def load_env():
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()

ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "")
OPENALEX_API_KEY = os.environ.get("OPENALEX_API_KEY", "")
EODHD_API_KEY = os.environ.get("EODHD_API_KEY", "")
COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY", "")

# Output paths — live data (served by GitHub Pages)
PRICES_JSON = BASE_DIR / "data" / "prices.json"
EQUITIES_JSON = BASE_DIR / "data" / "prices" / "equities.json"
TOKENS_JSON = BASE_DIR / "data" / "prices" / "tokens.json"
ALL_PRICES_JSON = BASE_DIR / "data" / "prices" / "all_prices.json"
NEWS_JSON = BASE_DIR / "data" / "news.json"
RESEARCH_JSON = BASE_DIR / "data" / "research.json"
FILINGS_JSON = BASE_DIR / "data" / "filings.json"
REPORTS_JSON = BASE_DIR / "data" / "reports.json"

# Archive paths — historical data for co-pilot training
NEWS_ARCHIVE_JSON = BASE_DIR / "archive" / "archive_news.json"
RESEARCH_ARCHIVE_JSON = BASE_DIR / "archive" / "archive_research.json"
FILINGS_ARCHIVE_JSON = BASE_DIR / "archive" / "archive_filings.json"
REPORTS_ARCHIVE_JSON = BASE_DIR / "archive" / "archive_reports.json"
