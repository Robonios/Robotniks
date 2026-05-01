# 4Q24 Private Markets Backfill — Summary

**Generated:** 2026-05-01
**Quarter covered:** Oct 1 – Dec 31, 2024
**File touched:** [data/funding/rounds.json](rounds.json)

## Headline numbers

- **89 deals** added
- **$31.32B** aggregate disclosed value

### ⚠️ Sense-check vs prompt expectation

You expected $5-15bn. Total came in at **$31.32B** — above expectation but below the $50bn auto-stop threshold.

**Reason:** 4Q24 was the CHIPS Act finalization rush. The Biden admin locked in 11 binding awards totaling **$23.34B** in the 11 weeks before the political transition. Strip those out and the picture matches your expectation closely:

| Slice | Deals | Aggregate |
|---|---|---|
| All 4Q24 | 89 | $31.32B |
| CHIPS Act finalized awards | 11 | $23.34B |
| **Ex-CHIPS** | **78** | **$7.98B** |

If you want CHIPS awards excluded (treated as fiscal events, not "private market deals"), say the word and I'll filter them — they share the existing `Government investment` enum so the schema is the same either way.

## Breakdown by sector

| Sector | Deals | Aggregate |
|---|---|---|
| Semiconductors | 25 | $26.34B |
| Robotics | 44 | $2.47B |
| Materials | 5 | $1.57B |
| Space | 15 | $937.5M |

## Breakdown by sector × subsector

### Semiconductors — 25 deals, $26.34B

| Subsector | Deals | Aggregate |
|---|---|---|
| Foundry | 5 | $20.31B |
| OSAT / Packaging & Test | 4 | $1.64B |
| Power & Analog | 1 | $1.61B |
| Frontier Compute | 8 | $1.50B |
| Silicon & Substrates | 2 | $1.16B |
| Equipment | 1 | $77.0M |
| EDA & IP | 2 | $31.1M |
| Machine Vision & Sensors | 1 | $10.0M |
| Fabless Design | 1 | $3.7M |

### Robotics — 44 deals, $2.47B

| Subsector | Deals | Aggregate |
|---|---|---|
| Autonomous Systems & Drones | 16 | $804.4M |
| Industrial Robots | 8 | $476.5M |
| Software & Simulation | 3 | $439.1M |
| Warehouse & Logistics | 9 | $385.5M |
| Surgical & Medical | 3 | $218.0M |
| Machine Vision & Sensors | 1 | $80.0M |
| Humanoid & Service Robots | 3 | $66.2M |
| Collaborative Robots | 1 | $5.0M |

### Materials — 5 deals, $1.57B

| Subsector | Deals | Aggregate |
|---|---|---|
| Battery Materials | 4 | $1.57B |
| Structural Materials | 1 | $3.0M |

### Space — 15 deals, $937.5M

| Subsector | Deals | Aggregate |
|---|---|---|
| In-Orbit Services | 6 | $418.5M |
| Launch | 1 | $175.0M |
| Satellite Communications | 2 | $147.1M |
| Earth Observation | 3 | $116.0M |
| Ground Systems & Antennas | 1 | $44.0M |
| Space Components | 2 | $36.9M |

## Breakdown by geography

| Country | Deals | Aggregate |
|---|---|---|
| USA | 58 | $29.17B |
| China | 7 | $1.28B |
| Germany | 6 | $245.7M |
| United Kingdom | 2 | $124.0M |
| Austria | 1 | $109.2M |
| Portugal | 1 | $73.8M |
| Switzerland | 2 | $72.0M |
| Finland | 1 | $65.0M |
| France | 3 | $64.0M |
| Israel | 2 | $41.0M |
| India | 1 | $24.0M |
| South Korea | 1 | $18.8M |
| Denmark | 1 | $11.4M |
| Sweden | 1 | $11.1M |
| Croatia | 1 | $6.1M |
| Canada | 1 | $3.0M |

## Top 10 deals by size

| # | Company | Round | Amount | Lead investor(s) |
|---|---|---|---|---|
| 1 | **Intel** | Government investment | $7.87B | U.S. Department of Commerce (CHIPS Act) |
| 2 | **Micron Technology** | Government investment | $6.17B | U.S. Department of Commerce (CHIPS Act) |
| 3 | **Samsung Electronics** | Government investment | $4.75B | U.S. Department of Commerce (CHIPS Act) |
| 4 | **Texas Instruments** | Government investment | $1.61B | U.S. Department of Commerce (CHIPS Act) |
| 5 | **GlobalFoundries** | Government investment | $1.50B | U.S. Department of Commerce (CHIPS Act) |
| 6 | **NOVONIX** | Government investment | $754.8M | U.S. Department of Energy Loan Programs Office (ATVM) |
| 7 | **Wolfspeed** | Debt Financing | $750.0M | Apollo Global Management |
| 8 | **SJ Semiconductor** | Strategic | $700.0M | Wuxi Chanfa Science and Technology Innovation Fund |
| 9 | **Tenstorrent** | Series D | $693.0M | Samsung Securities, AFW Partners |
| 10 | **SK hynix** | Government investment | $458.0M | U.S. Department of Commerce (CHIPS Act) |

## Deals flagged `single_source: true`

Only one verifiable public source. Worth a second pass before relying for analysis:

| Company | Round | Amount | Source |
|---|---|---|---|
| Opticore | Seed | $5.0M | https://theaiinsider.tech/2024/12/29/opticore-raises-5m-seed-funding-to-deliver-optical-gpus-for-100x-lower-energy-ai-computing/ |
| Zhuoyide Robotics | Series A | $14.0M | https://min.news/en/economy/feb9331917a6d97f04ce9ad0ab916083.html |

## Subsector classification — flagged for review

These deals fit awkwardly within the existing 26-value subsector taxonomy. The closest available label was used; if you want to add new subsectors (e.g. "Long-Duration Storage", "Agricultural Robotics", "Space Compute"), flag here:

| Company | Sector | Assigned subsector | Why ambiguous |
|---|---|---|---|
| Lumen Orbit | Space | Space Components | In-space data centres — closer to compute than space components |
| U-Space | Space | Space Components | Smallsat OEM — broader than just "components" |
| Form Energy | Materials | Battery Materials | Iron-air battery cells — more of a battery integrator than a materials company |

## Stage classification — flagged for review

Source language for the round was vague (e.g., "growth funding", "additional", "more than"). Best-fit assignment used; flagged here:

| Company | Assigned round | Notes |
|---|---|---|
| ICEYE | Series D (extension) | Company called it "growth funding extension"; classified as Series D extension based on prior round structure |
| Genesat | Strategic | Reported only as "more than 1 billion yuan" with state-aligned syndicate; classified as Strategic |
| SJ Semiconductor | Strategic | Reported as "new financing"; characterized in some reports as pre-IPO |
| Dolphin Semiconductor | Strategic | Hybrid M&A + growth investment (carve-out from Dolphin Design) |
| TEKEVER | Other | Press releases use "growth funding" — no series letter named |
| ANYbotics | Other | Sources disagree — some report Series B, others "additional funding" |
| Vecna Robotics | Other | Insider bridge round + new CEO; could be Series C or bridge |
| Brightpick | Other | Mix of equity and venture debt — not a clean series |
| FarmDroid | Other | Reported as "growth round" without series letter |
| Picnic Works | Other | Referred to as "early-stage" |
| Mantis Robotics | Other | Source did not specify stage |
| D-Fend Solutions | Other | No series letter |
| Zhuoyide Robotics | Series A | Single source naming Series A; not strongly verified |

## Non-USD deals — currency audit

Per the prompt's currency guardrail, every non-USD deal's native amount + FX rate used:

| Company | Native | USD reported | Implied FX | Source for FX |
|---|---|---|---|---|
| Constellation Technologies & Operations | EUR 9.3M | $10.1M | 1.086 | satellitetoday.com cross-ref |
| OroraTech | EUR 25.0M | $27.0M | 1.08 | satellitetoday cross-ref |
| U-Space | EUR 24.0M | $25.9M | 1.08 | spacenews.com cross-ref |
| The Exploration Company | EUR 150.0M | $160.0M | 1.067 | techcrunch cross-ref |
| Genesat | CNY 1,000.0M | $137.0M | 0.137 | spacenews.com cross-ref |
| tozero | EUR 11.0M | $11.7M | 1.0636 | TechCrunch headline conversion (Nov 11, 2024) |
| SJ Semiconductor | CNY 5,000.0M | $700.0M | 0.14 | PR Newswire press release used USD |
| Akhetonics | EUR 6.0M | $6.3M | 1.055 | TechCrunch reporting USD equivalent |
| Dolphin Semiconductor | EUR 26.0M | $28.0M | 1.077 | Implied at announcement (~1.077 EUR/USD) |
| TEKEVER | EUR 70.0M | $73.8M | 1.0552 | TechCrunch reported $74M USD equivalent for €70M |
| Robot Era | CNY 300.0M | $42.1M | 0.1405 | Robot Report October 2024 funding roundup; ~7.12 CNY/USD |
| RideFlux | KRW 26,000.0M | $18.8M | 0.000723 | Reported as $18.8M USD by The Pickool/KED |
| AirForestry | EUR 10.3M | $11.1M | 1.0925 | AirForestry press release reported $11.26M; ~1.0925 USD/EUR |
| FarmDroid | EUR 10.5M | $11.4M | 1.0905 | Robot Report October 2024 roundup; ~1.09 USD/EUR |
| Orqa | EUR 5.8M | $6.1M | 1.045 | BusinessWire press release; ~1.045 USD/EUR mid-Dec |
| GROPYUS | EUR 100.0M | $109.2M | 1.0925 | Robot Report October 2024 roundup ($106M); FoundersToday confirms ~€100M |
| MAXIEYE Automotive Technology | CNY 570.0M | $80.0M | 0.1405 | Robot Report October 2024 roundup reported $80.1M; ~7.12 CNY/USD |
| Vay Technology | EUR 34.0M | $36.9M | 1.0862 | Robot Report October 2024 roundup ($36.9M) |
| Zhuoyide Robotics | CNY 100.0M | $14.0M | 0.1405 | Robot Report October 2024 roundup ($14.1M) |

All FX rates verified against announcement-date approximations (EUR/USD ~1.05-1.09, USD/CNY ~7.12-7.30, USD/KRW ~1380, USD/JPY ~150-157). No deal was assumed to be USD without checking the source.

## Schema notes

- **No new fields** introduced (per your option (i) decision — match existing schema exactly).
- **Subsector consolidation done before backfill:** `Satellite Comms`→`Satellite Communications`, `Surgical & Medical Robots`→`Surgical & Medical`, `Warehouse & Logistics Automation`→`Warehouse & Logistics`. 10 existing rows updated; subsector enum now 26 values.
- **One new round/stage value:** `Series E (extension)` added for Skydio. Follows the existing `Series A/B/C/D (extension)` pattern; not a structural break.
- **`Strategic` round used 4×** (newly allowed per your D answer): Genesat, SJ Semiconductor, Dolphin Semiconductor, Ample.

## Excluded deals (notable)

Surfaced for transparency — these were considered and rejected for a specific reason:

- **CHIPS Act PMTs (preliminary memoranda of terms):** Wolfspeed PMT ($750M), Bosch PMT ($225M), Corning PMT ($32M), Powerex PMT ($3M). PMTs are non-binding; per your prompt's guidance to "include if Commerce Department announced binding award (not just preliminary memorandum)", these were excluded. Wolfspeed's separate $750M Apollo debt deal **is** included.
- **Phoenix Tailings Series B first close ($43M, Dec 20, 2024):** Excluded to avoid a 3-way duplicate. The existing dataset has TWO Phoenix Tailings rows (2025-04-25 and 2025-05-01, both labeled Series B at $76M) which appear to be duplicates of each other AND would conflict with the Dec 2024 first close. Recommend cleaning up the existing duplicate separately.
- **Lithium Americas $2.26B DOE loan finalization (Oct 2024):** Conditional commitment was March 2024; Oct 2024 was just financial close of a previously committed loan, not a new funding event.
- **Apple → Globalstar $1.5B commitment (Nov 1, 2024):** Globalstar is publicly listed; the deal is a strategic prepayment + 20% equity stake in a public-co subsidiary, not a private round.
- **Waymo $5.6B (Oct 2024):** Alphabet-subsidiary growth round at $45B+ valuation — corporate spin-out, not a private-startup deal in spirit. Could be re-included if you want late-stage AV deals.
- **WeRide & Pony AI IPOs (Oct/Nov 2024):** Public-market events, classified out of "private markets" scope.
- **Various Q3/Q4 boundary deals:** KoBold ($537M, Jan 2025), Stoke Space C ($260M, Jan 2025), Skild AI (Jul 2024), Groq (Sep 2024), etc. all confirmed outside the Oct–Dec 2024 window.

## Coverage gaps to flag

- **Chinese humanoid sector under-covered:** AgiBot, Galaxea, LimX Dynamics, Galbot, Kepler Exploration likely had 4Q24 rounds but most coverage is in Chinese-only sources (36Kr, etc.) without dated investor lists in English. Robot Era and Zhuoyide are included as the only ones I could verify with primary English-language sources. Estimate I missed 5-10 sub-$50M Chinese humanoid rounds.
- **DePIN tokens (4Q24):** Window was unusually quiet for compute/robotics-DePIN priced VC rounds with disclosed amounts. Most 4Q24 DePIN activity was token-side (TGEs, listings). Zero Token-sector deals included rather than fabricate.
- **No dedicated agriculture-robotics or in-space-compute subsectors:** Existing taxonomy doesn't accommodate cleanly (see "Subsector classification flagged for review" table above). Worth a separate decision if you want to extend the 26-value enum.

## Source-of-truth file

Every appended row has a `source` field with at least one verifiable URL. Multi-source verification used wherever possible — single-source flagged above. Full audit trail: each agent's output (with source URL arrays + commentary) is preserved at `/tmp/4q24_research/{space,materials,semis_raw,robotics_raw}.json` for the duration of this session.

---

## Ready for next quarter (3Q24)?

Per the prompt, I've stopped here for your review. When you're ready, the 3Q24 backfill should be straightforward — same workflow, same agents, same validation pipeline.