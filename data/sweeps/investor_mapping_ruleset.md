# Ruleset 4: Investor & Frontier Funds Mapping

**Frequency:** Rebuilt with each funding rounds dataset update (quarterly)
**Output file:** `data/registries/robotnik_investor_registry.csv`
**Automation level:** Automated rebuild from funding data + manual enrichment for top investors

## Purpose

Structured registry of investors active in the frontier technology stack. Supports Funding Ops page, investor profile pages (premium), and "who's deploying capital where" intelligence.

## Build Protocol

### Step 1: Extract
Parse all funding rounds. Split Lead/Other investor fields. Deduplicate.

### Step 2: Normalise
Map variants to canonical names. Store aliases. Keep distinct fund vehicles separate. Flag ambiguous cases for manual review.

### Step 3: Compute metrics
Calculate all quantitative fields from the funding rounds data.

### Step 4: Identify Frontier Funds
An investor qualifies as a Frontier Fund if:
- 3+ rounds in the dataset
- Multi-sector presence OR deep single-sector concentration
- At least one round in the most recent 6 months
- Flag with `frontier_fund = true`

### Step 5: Manual enrichment
For top 20 investors by total_rounds or total_capital_participated: add HQ, AUM, website, investment thesis, and Robotnik's notes.

## Dataset Fields

| Field | Definition |
|-------|-----------|
| investor_id | Unique identifier: INV-001, INV-002, etc. |
| name | Canonical name |
| aliases | Alternative names/abbreviations |
| type | VC / CVC / PE / sovereign_wealth / family_office / accelerator / corporate / angel / government / unknown |
| total_rounds | Count of rounds participated in |
| rounds_as_lead | Count of rounds as lead investor |
| total_capital_participated | Sum of round amounts participated in |
| sectors | Distinct sectors from rounds |
| preferred_stages | Most common round stages |
| first_seen | Earliest round date |
| last_seen | Most recent round date |
| portfolio_companies | Companies invested in |
| co_investors | Investors appearing in 2+ same rounds |
| frontier_fund | true / false |
| Robotnik's notes | Strategy commentary (manual — top 20 only) |

## Duplicate Detection

After each rebuild, run similarity check on names. Flag (do not auto-merge):
- Names differing only by "Capital", "Ventures", "Partners"
- Names differing only by geography qualifier
- Abbreviated vs full names

## Maintenance

Rebuild (Steps 1-4) after each quarterly fundraising sweep. Update manual enrichment (Step 5) quarterly.
