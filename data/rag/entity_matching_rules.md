# Entity Matching Rules

Documents the logic used by `scripts/match_entities.py` for entity resolution across all Robotnik datasets.

## Overview

The `EntityMatcher` class loads the entity registry and builds an inverted index of all aliases. When given text input, it returns matched entity IDs.

## How it works

1. **Registry load:** Reads `data/registries/entity_registry.json` (561 entities — 347 public, 214 private)
2. **Inverted index:** Maps every alias (lowercased) to its entity ID, sorted longest-first
3. **Greedy matching:** Scans input text for alias matches using word-boundary regex, preferring longer matches
4. **Consumed ranges:** Tracks matched character positions to prevent overlapping matches

## Ambiguous short tickers

Short tickers (2-3 chars) that are common English words require context validation:

| Ticker | Context words required nearby |
|--------|-------------------------------|
| ON | semiconductor, semi, onsemi, silicon carbide, sic, power |
| ARM | chip, semiconductor, processor, cpu, mobile, holdings, architecture |
| AI | artificial intelligence |
| MP | materials, rare earth, mining, magnet |

If none of the context words appear within 100 characters of the match, it is rejected.

## Usage

### CLI
```bash
python3 scripts/match_entities.py "TSMC expands CoWoS for NVIDIA"
# Output: ["NVDA", "TSM"]
```

### Python import
```python
from match_entities import EntityMatcher
matcher = EntityMatcher()
entities = matcher.match("text to search")
tickers_only = matcher.match_tickers_only("text to search")
```

## Where it's used

1. **News pipeline** (`scripts/fetch_news.py`) — tags news items with `mentioned_entities` and `mentioned_tickers`
2. **Funding round matching** — populates `entity_id` on funding rounds
3. **Future: RAG entity extraction** — resolves entities in user queries
