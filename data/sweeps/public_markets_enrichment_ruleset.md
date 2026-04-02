# Ruleset 3: Public Markets Enrichment Sweep

**Frequency:** Sector by sector (initial), quarterly maintenance
**Output file:** `data/markets/robotnik_public_markets.csv`
**Automation level:** Manual research with Claude assistance

## Purpose

Enrich each entity with supply chain data, relationship mapping, and strategic context. Transforms a price tracker into an intelligence platform.

## Sweep Order & Scope

**For 1Q26 report:** Top 10 entities by market cap in each sector (60 entities total).
**Post-report:** Complete remaining entities progressively.

## Per-Entity Enrichment Protocol (Equities)

Research using 10-K filings, earnings transcripts, company presentations, and industry reports.

### Fields to populate

- **Value-chain tier:** From sector taxonomy
- **Key customers (within Robotnik universe):** Up to 5, comma-separated by ticker
- **Key suppliers (within Robotnik universe):** Up to 5, comma-separated by ticker
- **Cross-sector dependencies:** 1-2 sentences
- **Bottleneck risk:** High / Medium / Low
- **Geographic concentration:** Primary manufacturing/operations locations
- **Robotnik's notes:** 2-4 sentences, strategic positioning and vulnerabilities

## Token Adaptation

Tokens remain in the same file as equities. Adapted field definitions:

| Equity field | Token interpretation |
|-------|-----------|
| Value-chain tier | Protocol function: Compute / Data / Infrastructure / Connectivity / Economy / Governance |
| Key customers | Network/chain the token operates on |
| Key suppliers | Protocol dependencies |
| Cross-sector dependencies | Frontier tech connection |
| Geographic concentration | Team/foundation location, validator distribution |

## Quality Checks (per sector)

1. All enrichment fields populated (or marked "Not disclosed" / "N/A")
2. Relationship reciprocity: A lists B as customer <-> B lists A as supplier
3. Bottleneck ratings are defensible
4. Cross-sector dependencies captured on both sides
5. Every entity has Robotnik's notes

## Maintenance

Quarterly review. Ad-hoc updates triggered by major M&A, export control changes, new entity additions, material earnings disclosures.
