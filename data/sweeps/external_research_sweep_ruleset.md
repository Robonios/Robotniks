# Ruleset 2: External Research Sweep

**Frequency:** Weekly (academic), as-published (industry reports), as-filed (company filings)
**Output file:** `data/research/robotnik_external_research.csv`
**Automation level:** Semi-automated

## Purpose

Catalogue academic papers, industry reports, and company filings relevant to the frontier stack. Internal knowledge base for RAG and original research.

## Source List

- **Academic:** OpenAlex API (primary), arXiv, IEEE Xplore, Nature/Science, Google Scholar alerts
- **Industry reports:** SEMI, IFR, Gartner/McKinsey/BCG (when public), BloombergNEF, Satellite Industry Association, USGS
- **Company filings:** SEC EDGAR, Companies House, EDINET, company IR pages

## Relevance Filtering — RIII Framework

| Level | Definition | Action |
|-------|-----------|--------|
| **Revolution** | Fundamentally new capability or paradigm shift | Catalogue — HIGH relevance |
| **Innovation** | Novel approach with clear commercial implications | Catalogue — HIGH relevance |
| **Improvement** | Incremental improvement on existing methods | SKIP |
| **Interesting** | Theoretically novel but no clear commercial pathway | SKIP |

Expected volume after filtering: ~50-100 papers per year across all sectors.

## Cataloguing Protocol

| Field | How to populate |
|-------|----------------|
| Entity IDs | Comma-separated entity registry IDs. |
| Organisation | Company, university, or research firm. |
| Type | `academic` / `industry_report` / `company_filing` / `regulatory_filing` |
| Title | Full title. |
| Date | YYYY-MM-DD |
| Sector(s) | From Robotnik taxonomy. |
| Subsector(s) | From Robotnik taxonomy. |
| Summary | 2-4 sentences: what is new, significant, and implications. |
| Authors | Author names (academic), lead analyst (reports), "N/A" (filings). |
| Source name | Journal, regulator, or publisher. |
| Relevance | `high` / `medium` / `low` |
| URL | Direct link. |
| Tags | From standard vocabulary. |
| Robotnik's notes | How does this connect to the dependency chain? |

## Weekly Sweep Protocol

Each Monday:
1. Run OpenAlex queries for past 7 days. Apply RIII filter.
2. Check industry body websites for new reports.
3. Check EDGAR for filings from Robotnik universe entities.
4. Log sweep metadata: date, items reviewed, items catalogued.
