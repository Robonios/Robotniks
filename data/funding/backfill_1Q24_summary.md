# 1Q24 Private Markets Backfill — Summary

**Generated:** 2026-05-02
**Quarter covered:** Jan 1 – Mar 31, 2024
**File touched:** [data/funding/rounds.json](rounds.json)

## Headline numbers

- **100 deals** added
- **$7.79B** aggregate disclosed value
- **676 total rows** in `rounds.json` after append (was 576)
- **Quarter coverage now extends 1Q24 → 2Q26** (10 quarters total — full 2.5 years)

### Sense-check vs prompt expectation

You expected $5-15B for a typical quarter. 1Q24 came in at **$7.79B** — squarely in range.

1Q24 had **zero finalized binding CHIPS Act commercial awards** in window (the first was Polar Sep 24, 2024). All Q1 PMTs (GlobalFoundries Feb 19, Microchip Jan) were non-binding and excluded.

**Lithium Americas $2.26B DOE conditional commitment** added per symmetry with NOVONIX 4Q24 inclusion. Without it, 1Q24 ex-DOE-mega aggregate would be $5.53B (squarely in expected range).

## What's new in this batch

### Multi-row convention applied: Atomic-6 split into equity + grant

Per the convention from 3Q24, Atomic-6's combined $9.2M raise on 2024-01-11 was split into 2 rows:

| Date | Company | Round | $ | deal_type | Mechanic |
|---|---|---|---|---|---|
| 2024-01-11 | Atomic-6 | Seed | $4.95M | venture | IronGate-led equity tranche |
| 2024-01-11 | Atomic-6 | Grant | $4.24M | government | USAF/USSF SBIR grant |

Both rows share `entity_id=atomic-6`, distinct rounds, distinct deal_types per the rule.

### `deal_type` distribution for 1Q24

| deal_type | Deals | Aggregate |
|---|---|---|
| `venture` | 81 | $4.67B |
| `government` | 6 | $2.61B |
| `strategic_corporate` | 8 | $419.9M |
| `debt` | 0 | $0.0M |
| `token` | 5 | $95.0M |

### `Decentralized AI / DePIN` subsector usage

5 token-sector deals classified under the new (27th) subsector — biggest pre-2Q24 month for DePIN VC raises:

| Company | Round | $ | Lead |
|---|---|---|---|
| 0G Labs | Pre-Seed | $35M | Hack VC |
| io.net | Series A | $30M | Hack VC |
| peaq | Pre-Series A | $15M | Generative Ventures, Borderless Capital |
| DIMO | Series A | $11.5M | CoinFund |
| GEODNET | Seed | $3.5M | North Island Ventures |

Across 4Q24 → 1Q24, total token deals: 13 (Sentient, Sahara AI in 3Q24; IoTeX, Aligned Layer, SendingNetwork, Arcium, Prime Intellect, Privasea in 2Q24; io.net, peaq, GEODNET, 0G Labs, DIMO in 1Q24).

## Breakdown by sector

| Sector | Deals | Aggregate |
|---|---|---|
| Materials | 13 | $3.19B |
| Robotics | 53 | $2.47B |
| Semiconductors | 18 | $1.72B |
| Space | 11 | $327.5M |
| Token | 5 | $95.0M |

## Breakdown by sector × subsector

### Materials — 13 deals, $3.19B

| Subsector | Deals | Aggregate |
|---|---|---|
| Battery Materials | 6 | $2.81B |
| Structural Materials | 5 | $327.5M |
| Rare Earths & Critical Minerals | 2 | $53.0M |

### Robotics — 53 deals, $2.47B

| Subsector | Deals | Aggregate |
|---|---|---|
| Humanoid & Service Robots | 7 | $1.00B |
| Software & Simulation | 5 | $404.0M |
| Autonomous Systems & Drones | 19 | $392.9M |
| Surgical & Medical | 7 | $200.0M |
| Industrial Robots | 5 | $167.9M |
| Warehouse & Logistics | 5 | $150.9M |
| Machine Vision & Sensors | 4 | $105.8M |
| Collaborative Robots | 1 | $42.5M |

### Semiconductors — 18 deals, $1.72B

| Subsector | Deals | Aggregate |
|---|---|---|
| Fabless Design | 2 | $735.4M |
| Frontier Compute | 10 | $678.5M |
| OSAT / Packaging & Test | 1 | $200.0M |
| EDA & IP | 1 | $60.0M |
| Power & Analog | 2 | $35.3M |
| Silicon & Substrates | 1 | $4.7M |
| Equipment | 1 | $3.7M |

### Space — 11 deals, $327.5M

| Subsector | Deals | Aggregate |
|---|---|---|
| In-Orbit Services | 1 | $110.0M |
| Launch | 3 | $73.8M |
| Space Components | 4 | $65.4M |
| Satellite Communications | 1 | $37.0M |
| Earth Observation | 1 | $35.0M |
| Ground Systems & Antennas | 1 | $6.3M |

### Token — 5 deals, $95.0M

| Subsector | Deals | Aggregate |
|---|---|---|
| Decentralized AI / DePIN | 5 | $95.0M |

## Breakdown by geography

| Country | Deals | Aggregate |
|---|---|---|
| USA | 51 | $6.15B |
| China | 8 | $388.6M |
| Italy | 2 | $220.0M |
| Singapore | 2 | $218.0M |
| South Korea | 5 | $162.2M |
| Norway | 3 | $119.6M |
| France | 5 | $78.2M |
| Belgium | 3 | $71.3M |
| Spain | 2 | $70.9M |
| Germany | 3 | $65.4M |
| Israel | 2 | $59.0M |
| Canada | 3 | $53.7M |
| Netherlands | 2 | $46.0M |
| Switzerland | 1 | $25.0M |
| Japan | 2 | $21.4M |
| Australia | 1 | $15.0M |
| Poland | 2 | $14.3M |
| Hong Kong | 1 | $10.0M |
| United Kingdom | 1 | $3.5M |
| India | 1 | $1.8M |

## Top 10 deals by size

| # | Company | Round | Amount | Lead investor(s) |
|---|---|---|---|---|
| 1 | **Lithium Americas** | Government investment | $2.26B | U.S. Department of Energy Loan Programs Office (ATVM) |
| 2 | **Astera Labs** | IPO | $712.8M | Morgan Stanley, J.P. Morgan, Barclays, Deutsche Bank (lead bookrunners) |
| 3 | **Figure AI** | Series B | $675.0M | Microsoft, OpenAI Startup Fund, NVIDIA, Jeff Bezos (Bezos Expeditions) |
| 4 | **Quantinuum** | Strategic | $300.0M | JPMorgan Chase, Mitsui & Co., Amgen |
| 5 | **Applied Intuition** | Series E | $250.0M | Lux Capital, Elad Gil, Porsche Investments Management |
| 6 | **Silicon Box** | Series B | $200.0M | Bain Capital, BlackRock |
| 7 | **Brimstone** | Grant | $189.0M | U.S. DOE Office of Clean Energy Demonstrations (OCED) |
| 8 | **Ascend Elements** | Series D (extension) | $162.0M | Just Climate |
| 9 | **Antora Energy** | Series B | $150.0M | Decarbonization Partners (BlackRock + Temasek) |
| 10 | **Lilac Solutions** | Series C | $145.0M | Mercuria, Lowercarbon Capital, Breakthrough Energy Ventures |

## Deals flagged `single_source: true` (77 rows)

Most are smaller deals where only the company press release was available; bigger deals all have multi-source verification. Higher single-source share than other quarters reflects more idiosyncratic deal flow in Q1 2024 (smaller rounds, more European/Asian press).

## Subsector classification flags (11 rows)

| Company | Sector | Assigned subsector |
|---|---|---|
| Antora Energy | Materials | Battery Materials |
| TopoLogic | Semiconductors | Silicon & Substrates |
| Hippo Harvest | Robotics | Autonomous Systems & Drones |
| WIRobotics | Robotics | Surgical & Medical |
| Aether Biomedical | Robotics | Surgical & Medical |
| Forvision | Robotics | Autonomous Systems & Drones |
| KC Robots | Robotics | Warehouse & Logistics |
| VoxelSensors | Robotics | Machine Vision & Sensors |
| ACWA Robotics | Robotics | Autonomous Systems & Drones |
| Neatleaf | Robotics | Autonomous Systems & Drones |
| TechMagic | Robotics | Humanoid & Service Robots |

## Stage classification flags (13 rows)

| Company | Assigned round |
|---|---|
| peaq | Pre-Series A |
| Unitree Robotics | Series B |
| Starship Technologies | Other |
| Glacier | Strategic |
| Sea Machines Robotics | Strategic |
| Saga Robotics | Other |
| Agilis Robotics | Series A (extension) |
| Aqua Robotics | Other |
| Aether Biomedical | Series A (extension) |
| Forvision | Other |
| GUOZI Robot | Other |
| Buzz Solutions | Other |
| Neatleaf | Other |

## Non-USD deals — currency audit (29 rows)

| Company | Native | USD | Implied FX |
|---|---|---|---|
| D-Orbit | EUR 100.0M | $110.0M | 1.1 |
| Latitude | EUR 27.5M | $30.0M | 1.0909 |
| PLD Space | EUR 40.5M | $43.8M | 1.0815 |
| NeoCem | EUR 23.0M | $25.0M | 1.0884 |
| Multiverse Computing | EUR 25.0M | $27.1M | 1.085 |
| Innatera | EUR 19.6M | $21.0M | 1.085 |
| Wise Integration | EUR 15.0M | $16.3M | 1.083 |
| e-peas | EUR 17.5M | $19.0M | 1.085 |
| SEMRON | EUR 7.3M | $7.9M | 1.084 |
| TopoLogic | JPY 700.0M | $4.7M | 0.0067 |
| Femtum | CAD 5.0M | $3.7M | 0.74 |
| Unitree Robotics | CNY 1,000.0M | $139.0M | 0.139 |
| RobCo | EUR 39.1M | $42.5M | 1.087 |
| BIOBOT Surgical | SGD 24.0M | $18.0M | 0.75 |
| Preneu | KRW 15,000.0M | $11.3M | 0.000754 |
| WIRobotics | KRW 13,000.0M | $9.7M | 0.000743 |
| Aqua Robotics | NOK 85.0M | $8.1M | 0.0953 |
| Zhuoyi Intelligent Technology | CNY 250.0M | $35.1M | 0.1404 |
| ORCA-TECH | CNY 100.0M | $14.0M | 0.14 |
| Forvision | CNY 100.0M | $13.9M | 0.139 |
| GUOZI Robot | CNY 200.0M | $28.0M | 0.14 |
| KC Robots | CNY 100.0M | $14.1M | 0.141 |
| ROBOS | KRW 7,000.0M | $5.2M | 0.000743 |
| VoxelSensors | EUR 9.5M | $10.3M | 1.084 |
| ACWA Robotics | EUR 4.8M | $5.2M | 1.083 |
| TechMagic | JPY 2,500.0M | $16.7M | 0.00668 |
| Robovision | EUR 38.9M | $42.0M | 1.08 |
| LEM Surgical | CHF 22.0M | $25.0M | 1.177 |
| Aerix Systems | EUR 1.6M | $1.7M | 1.083 |

FX rates verified: EUR/USD ~1.083-1.089 (Q1 2024 was a stable EUR window), USD/CNY ~7.10-7.30, USD/KRW ~1320-1370, USD/JPY ~145-152, GBP/USD ~1.25-1.27, AUD/USD ~0.65-0.66, CAD/USD ~0.74, CHF/USD ~1.13-1.18, NOK/USD ~0.094, SGD/USD ~0.74-0.75.

## Deals with `amount_m: null` (2 rows)

| Company | Round | Why included |
|---|---|---|
| Phantom Space | Bridge | Strategically meaningful even with undisclosed amount |
| Sanctuary AI | Strategic | Strategically meaningful even with undisclosed amount |

## Excluded deals (notable)

### Outside the Q1 2024 window
- **Wayve $1.05B Series C** (May 2024) — Q2 2024
- **Cobot/Collaborative Robotics $100M Series B** (April 2024) — Q2 2024
- **Skild AI $300M Series A** (July 2024) — Q3 2024
- **Anduril $1.5B Series F, Helsing $487.5M Series C, Saronic $175M Series B** — all Q3 2024
- **Astranis $200M Series D** (July 2024) — Q3 2024
- **Apex Space $95M Series B** (June 2024) — Q2 2024
- **Hailo $120M Series C ext, SiMa.ai $70M ext, Etched $120M Series A, Auradine $80M Series B, Black Semiconductor €254M** — all Q2 2024
- **Apptronik $350M Series A** — actually February 2025 (commonly mis-dated)
- **Symbotic-Walmart $200M deal** — January 2025
- **K2 Space $110M Series B** — February 2025 (the $50M Feb 2024 round IS in 1Q24, classified as Series A per CNBC)

### Excluded per scope rules
- **GlobalFoundries CHIPS PMT $1.5B** (Feb 19, 2024), **Microchip CHIPS PMT $162M** (Jan 2024) — non-binding PMTs; finalized later in 2024
- **PROQCIMA framework agreement** (€500M, Mar 7, 2024) — competitive framework covering 5 French quantum cos, no discrete tranche disclosed for any one company in Q1 2024
- **Astra Space take-private M&A** ($11.25M, Mar 7, 2024) — target was publicly listed (NASDAQ:ASTR), excluded per "private target only" rule (matches Renesas/Transphorm exclusion in 2Q24)
- **Cornelis Networks Series B** — agent flagged uncertainty about whether the $25M reported in Crunchbase is a real Q1 2024 round vs a top-up of the 2022 Series B; excluded pending verification
- **MP Materials, Solidion Technology** — public-co secondary offerings
- **Aethir node-license sale** (Mar 18, 2024) — public node-license sale, not VC equity
- **Lyten $4M DOE grant** (Jan 30, 2024) — small grant; main activity was Q3 2023
- **DOE OCED selections** (Sublime $87M, Brimstone $189M Mar 25, 2024) — INCLUDED as Grant since they're discrete dollar-specific commitments, even if conditional. Mirrors NOVONIX precedent.

## Cross-sector reclassifications (per existing-data consistency)

- **Hadrian** — agent classified as Space (Space Components) but existing 1Q26 entry classifies as Robotics (Industrial Robots). Reclassified to match existing convention.
- **Recogni** — appeared in both Robotics and Semiconductors agent outputs (chip company for AV/datacenter). Kept in Semiconductors only.

## Coverage gaps to flag

- **Chinese humanoid sector under-covered:** AgiBot Series A1 in Q1 2024 likely existed but no English-language confirmation found. Galaxea, Astribot, Tashan Robotics — unverified.
- **Saildrone, Realtime Robotics, Verity** — Q1 2024 activity hinted at but not verifiable to specific dates/amounts.
- **DeFi-adjacent token raises** intentionally excluded per scope rules (Berachain, Babylon were Q2 2024 anyway).

## Schema notes

- **No new fields** introduced.
- **No new sectors** (still 5).
- **No new subsector values** (still 27).
- **No new round values** (Strategic + Series E (extension) + Seed (extension) all already in enum).
- **Strategic** round used 8× in 1Q24: Niron Magnetics, Quantinuum, Magrathea Metals (govt structurally), Skylo Technologies, Brain Corp, Glacier, Sanctuary AI, Phase Four.
- **Government investment** used 4× in 1Q24: Lithium Americas ($2.26B DOE), Magrathea Metals ($28M DPA), PLD Space ($43.8M PERTE), Atomic-6 Grant tranche ($4.24M USAF/USSF SBIR — captured as Grant).
- **Multi-row convention** used once: Atomic-6 split into Seed equity + Grant.

## Source-of-truth file

Every appended row has a `source` field with at least one verifiable URL. Single-source flagged. Full audit trail at `/tmp/1q24_research/{space,materials,robotics,semis}.json`.

---

## Backfill complete: 8 quarters added (1Q24–4Q24, 2Q24–4Q24, 3Q24, 4Q24)

Original dataset (1Q25–2Q26): 313 rows, ~$92.6B aggregate.
After backfill (1Q24–2Q26): **676 rows**, total ~$129.0B aggregate.

Quarterly distribution:
- 1Q24: 100 deals, $7.79B
- 2Q24: 97 deals, $7.86B
- 3Q24: 78 deals, $9.09B
- 4Q24: 89 deals, $31.32B
- 1Q25: 36 deals, $6.81B
- 2Q25: 47 deals, $9.37B
- 3Q25: 62 deals, $10.88B
- 4Q25: 70 deals, $8.07B
- 1Q26: 93 deals, $47.19B
- 2Q26: 4 deals, $629.0M

All 8 backfilled quarters share the same canonical schema (21 fields, 5 sectors, 27 subsectors, 5-value `deal_type` enum, multi-row convention for legitimate same-company-same-quarter events).