# Robotniks

Structured intelligence platform for robotics and semiconductors — like Messari, but for the physical AI stack. Tracks public markets, startup funding, supply chains, and technical milestones.

## Architecture

- **Single-file app**: Everything lives in `index.html` — HTML, CSS, and JS are all inline
- **No build tools**: No package.json, no bundler, no framework. Pure static site
- **Data pipeline**: Python fetcher scripts → JSON files → frontend reads via `fetch()`
- **Hosting**: GitHub Pages
- **Config**: `.env` file for API keys, loaded by `scripts/config.py` (no external deps)
- **Archiving**: `scripts/archive_utils.py` provides shared archive-and-filter logic for all fetchers

## Project Structure

```
Robotniks/
├── index.html              # Main site (single-file app)
├── tetris.html             # Landing/teaser page with Tetris game
├── cosmonaut-bg.png        # Background image for tetris.html
├── requirements.txt        # Python dependencies
├── .env                    # API keys (gitignored)
├── .gitignore
├── CLAUDE.md
├── .github/workflows/
│   └── fetch-data.yml      # GitHub Actions: daily prices + weekly intel
├── scripts/                # All Python fetcher scripts
│   ├── config.py           # Shared config (paths, API keys)
│   ├── archive_utils.py    # Shared archive-and-filter logic
│   ├── fetch_prices.py     # EODHD + CoinGecko (219 equities + 43 tokens)
│   ├── fetch_prices_alphavantage.py  # Legacy Alpha Vantage fetcher
│   ├── fetch_news.py       # ~30 RSS feeds
│   ├── fetch_research.py   # OpenAlex API
│   ├── fetch_filings.py    # SEC EDGAR
│   └── fetch_reports.py    # IFR/SEMI/SIA websites
├── data/                   # Live JSON data (served by GitHub Pages)
│   ├── prices/             # Price data from fetch_prices.py
│   │   ├── equities.json
│   │   ├── tokens.json
│   │   └── all_prices.json
│   ├── news.json
│   ├── research.json
│   ├── filings.json
│   ├── reports.json
│   └── prices.json         # Legacy Alpha Vantage output
└── archive/                # Historical data for co-pilot training (gitignored)
    ├── archive_news.json
    ├── archive_research.json
    ├── archive_filings.json
    └── archive_reports.json
```

## Design System

- **Font**: Roboto Mono (monospace) — ONLY font allowed, never use any other font
- **Background**: `#111318` (dark theme)
- **Yellow accent**: `#F5D921` (primary brand color)
- **CSS variables are defined in `:root` at the top of index.html**

## Key Sections

1. **Market Tracker** — table of ~20 public robotics/semi companies with real prices, filterable by sector (Semis, Robotics, Infra)
2. **Fundraising Dashboard** — startup raises with stage, amount, valuation, investors. Has CSV export
3. **Intelligence Feed** — aggregated news, research papers, SEC filings, and industry reports. Filterable by type and category. Has two subtabs:
   - **Feed** — all aggregated content with search, type filters (News/Research/Filings/Reports), and category filters (Robotics/Semis/AI-ML/Supply Chain)
   - **Robotniks Insights** — placeholder for original analysis (coming soon)
4. **Thesis** — founding thesis ("One Strategic Stack")
5. **Business Model** — free vs paid tiers
6. **Roadmap** — 10-milestone product roadmap
7. **Products** — three product cards (Market Tracker, Fundraising Dashboard, Innovation Map)
8. **Waitlist CTA** — email signup form (connected to Mailchimp)

## Data

- Market data is hardcoded in the `companies` JS array (prices as of Mar 4, 2026)
- Fundraising data is hardcoded in the `raises` JS array
- API keys stored in `.env` (not committed), loaded by `scripts/config.py`
- Price universe: 262 entities (219 equities + 43 crypto tokens) defined in `scripts/fetch_prices.py`

## Data Fetcher Scripts

All scripts live in `scripts/` and output to `data/`.

| Script | Source | Output | Dependencies |
|--------|--------|--------|-------------|
| `scripts/fetch_prices.py` | EODHD + CoinGecko | `data/prices/*.json` | stdlib only |
| `scripts/fetch_news.py` | ~30 RSS feeds | `data/news.json` | `feedparser` |
| `scripts/fetch_research.py` | OpenAlex API | `data/research.json` | stdlib only |
| `scripts/fetch_filings.py` | SEC EDGAR | `data/filings.json` | stdlib only |
| `scripts/fetch_reports.py` | IFR/SEMI/SIA websites | `data/reports.json` | `beautifulsoup4`, `lxml` |
| `scripts/fetch_prices_alphavantage.py` | Alpha Vantage API | `data/prices.json` | `requests` |
| `scripts/archive_utils.py` | (shared utility) | — | stdlib only |
| `scripts/config.py` | (shared config) | — | stdlib only |

### Content Retention Rules

- **Research**: Papers from Jan 2023 onward in live output; all papers archived
- **News**: Rolling 12-month window in live output; older items archived
- **Filings**: Most recent filing per company in live output; all filings archived
- **Reports**: All reports in live output (dates unreliable); all archived
- **Archive files** (`archive/`): Full historical data for co-pilot training. Gitignored.

### Key RSS Sources (~30 feeds in `scripts/fetch_news.py`)

Industry: The Robot Report, IEEE Spectrum Robotics, Robohub, Robotics Tomorrow, Automate.org, Automation World, SemiEngineering, EE Times, Semiconductor Today, The Elec, eeNews Europe, Electronics Weekly

Substacks: SemiAnalysis, Fabricated Knowledge, Asianometry

Business/Tech: Ars Technica, TechCrunch AI, TechCrunch Robotics, VentureBeat AI, The Verge Robotics, Supply Chain Dive

Company: NVIDIA Blog/Newsroom/Developer, Boston Dynamics, ARM Community, TSMC Newsroom

Policy: Commerce Dept

Research: arXiv Robotics (cs.RO), arXiv AI (cs.AI)

### Setup

```bash
pip install -r requirements.txt
```

### `.env` file (required, not committed)

```
OPENALEX_API_KEY=<your-key>
EODHD_API_KEY=<your-key>
COINGECKO_API_KEY=<your-key>
```

### Running fetchers

```bash
python3 scripts/fetch_prices.py     # EODHD + CoinGecko → data/prices/ (262 entities)
python3 scripts/fetch_news.py       # ~30 RSS feeds → data/news.json (150 items, 12-month window)
python3 scripts/fetch_research.py   # OpenAlex → data/research.json (200 papers, Jan 2023+)
python3 scripts/fetch_filings.py    # SEC EDGAR → data/filings.json (1 per company, ~18 entries)
python3 scripts/fetch_reports.py    # IFR/SEMI/SIA → data/reports.json (with article summaries)
```

## Dev Server

```
python3 -m http.server 8000
```

Config saved in `.claude/launch.json` as `robotniks-site`.
