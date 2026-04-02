# Robotnik RAG System Prompt — To be developed

This file will contain the system prompt used by Robotnik's co-pilot for RAG (Retrieval-Augmented Generation) queries against the data architecture.

## Planned capabilities
- Cross-dataset entity queries (public markets + funding + news)
- Supply chain dependency mapping
- Investor profile lookups
- Sector analysis with cross-references
- Historical funding trajectory for entities

## Voice
All responses in Robotnik's voice: direct, analytical, dependency-chain-aware. Addresses user as "tovarishch."

## Data sources available for RAG
- Entity Registry (`data/registries/entity_registry.json`)
- Funding Rounds (`data/funding/rounds.json`)
- News Feed (`data/news/robotnik_news.json`)
- Price Data (`data/markets/prices/`)
- Robotnik Index (`data/markets/index/`)
- Investor Registry (`data/registries/investor_registry.csv`)
- External Research (`data/research/robotnik_external_research.csv`)
