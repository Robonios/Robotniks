# Cross-Referencing Logic

Documents how Robotnik's datasets are linked together for cross-dataset queries.

## Primary identifiers

| Identifier | Used in | Links to |
|-----------|---------|----------|
| `entity_id` | All datasets | Entity Registry — unique per company/token |
| `investor_id` | Funding rounds, Investor Registry | Investor profiles |
| Ticker (e.g., `NVDA`) | Public markets, Entity Registry | Price data, index weights |

## Cross-reference paths

### News → Entities
- Field: `mentioned_entities` (array of entity_ids)
- Field: `mentioned_tickers` (array of public tickers)
- Populated by: Entity Matcher running on title + summary text

### Funding Rounds → Entities
- Field: `entity_id` (the funded company)
- Field: `related_tickers` (array of public companies relevant to the round)
- Field: `public_market_link` (ticker if company is public or subsidiary of public company)

### Funding Rounds → Investors
- Fields: `lead_investors`, `other_investors` (comma-separated names)
- Linked to Investor Registry via name normalisation

### Entities → Price Data
- Public entities: `eodhd_ticker` maps to price history files
- Token entities: `coingecko_id` maps to CoinGecko price data

### Entities → Robotnik Index
- Public entities with sufficient market cap are included in index weights
- Sector assignment determines which sub-index an entity appears in

## Automation rules

When a news item or research paper mentions an entity:
1. Tag the item with the entity's ID (via Entity Matcher)
2. Flag the entity's profile for potential update
3. Link the item to the entity's record for RAG retrieval

When a funding round is added:
1. Match the company to the Entity Registry (or create new private entity)
2. Extract related tickers from Robotnik's Notes (via Entity Matcher)
3. Parse investors and update Investor Registry

## Data freshness

| Dataset | Update frequency | Automation |
|---------|-----------------|------------|
| Prices | Daily (weekday pipeline) | Fully automated |
| Index | Daily (after prices) | Fully automated |
| News | Daily (RSS fetch) | Fully automated |
| Funding rounds | Quarterly sweep + weekly updates | Semi-automated |
| Entity Registry | On-demand (new companies added) | Manual + automated |
| Investor Registry | Quarterly rebuild | Automated from funding data |
| External Research | Weekly sweep | Semi-automated |
