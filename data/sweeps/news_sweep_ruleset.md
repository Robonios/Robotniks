# Ruleset 1: News Sweep

**Frequency:** Daily (weekdays), End of Week Briefing (Sundays)
**Output file:** `data/news/robotnik_news.csv`
**Automation level:** Fully automated with Claude API for summaries and Robotnik's notes.

## Purpose

Identify, catalogue, and tag news items relevant to the Robotnik frontier technology stack. Feed the daily briefing, populate the news page, and enrich the entity knowledge base for RAG.

## Source List

### Tier 1 — Primary (check daily)
- Reuters (technology, industrials, space sections)
- Bloomberg (semiconductors, technology, industrials)
- Financial Times (technology, companies)
- The Elec (Korean semiconductor supply chain)
- DigiTimes (Taiwanese semiconductor supply chain)
- SemiAnalysis (semiconductor deep analysis)
- EE News Europe / EE Times (electronics industry)
- SpaceNews (space industry)
- The Robot Report (robotics industry)

### Tier 2 — Secondary (check daily, lower priority)
- TechCrunch (funding, startups — robotics/space/AI hardware)
- Nikkei Asia (Japanese semiconductor and robotics)
- SCMP (China technology, export controls)
- Defense One / Breaking Defense (space/defense crossover)
- Mining.com / Fastmarkets (critical materials, rare earths)

### Tier 3 — Company direct (check when flagged)
- SEC filings (EDGAR — 10-K, 10-Q, 8-K for US-listed entities)
- Company press releases / investor relations pages
- Exchange announcements (for IPOs, delistings)

## Inclusion Criteria

A news item is **in scope** if it meets ANY of the following:
- It directly mentions a Robotnik universe entity
- It covers a sector or subsector in Robotnik's taxonomy
- It relates to the frontier technology dependency chain
- It reports a funding round, acquisition, IPO, or strategic partnership
- It covers commodity price movements or supply disruptions for materials in the taxonomy

A news item is **out of scope** if:
- It is pure consumer tech with no supply chain relevance
- It is general market commentary with no frontier tech specificity
- It is a duplicate (same story, different source)

## Cataloguing Protocol

| Field | How to populate |
|-------|----------------|
| ID | Sequential: NEWS-YYYYMMDD-001, NEWS-YYYYMMDD-002, etc. |
| Entity IDs | Auto: run entity matcher against title + summary. |
| Type | `news_item` / `breaking` / `daily_briefing` |
| Title | Original headline, unedited. |
| Date | YYYY-MM-DD |
| Sector(s) | From Robotnik taxonomy. Comma-separated. |
| Subsector(s) | From Robotnik taxonomy. Comma-separated. |
| Summary | Auto-generated: 1-2 sentence factual summary. |
| Source name | Publisher name. |
| Source type | wire_service / trade_publication / company_announcement / blog / social / other |
| URL | Direct link. |
| Tags | From standard vocabulary (see taxonomy.json). |
| Robotnik's notes | Auto-generated: cross-sector intelligence in Robotnik's voice. |

## Daily Briefing Protocol

**Weekdays:**
- Heading: `DAILY BRIEFING // [Date]`
- Opening: `Tovarishch, [N] signals detected today:`
- Body: 5-7 signal items across multiple sectors, each 2-3 sentences with cross-sector dependency analysis.

**Weekends:**
- No briefing Saturday
- Sunday: `END OF WEEK BRIEFING // [Date]` covering Friday + weekend developments

## Pipeline Requirements

`scripts/fetch_news.py` must:
1. Fetch RSS items from Tier 1 and Tier 2 sources
2. Deduplicate against existing catalogue (match on URL)
3. Run entity matcher on title + summary
4. Auto-populate all fields
5. MERGE new items into existing catalogue — never overwrite
