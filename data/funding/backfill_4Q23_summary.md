# 4Q23 Backfill Summary

**Window:** October 1 – December 31, 2023
**Rows added:** 113
**Disclosed capital:** $5,395.6M
**Cumulative dataset:** 785 rows across 11 quarters (4Q23–2Q26)

## Sector breakdown

| Sector | Deals | Disclosed |
|--------|------:|----------:|
| Robotics | 65 | $2,035.0M |
| Semiconductors | 18 | $1,582.1M |
| Materials | 12 | $763.3M |
| Space | 13 | $750.4M |
| Token | 5 | $264.8M |
| **Total** | **113** | **$5,395.6M** |

## Top subsectors by disclosed capital

| Sector / Subsector | Deals | Disclosed |
|--------------------|------:|----------:|
| Robotics / Autonomous Systems & Drones | 25 | $1,229.7M |
| Semiconductors / Power & Analog | 1 | $830.0M |
| Materials / Battery Materials | 9 | $670.3M |
| Space / Launch | 6 | $529.2M |
| Semiconductors / Frontier Compute | 11 | $505.2M |
| Token / Decentralized AI / DePIN | 5 | $264.8M |
| Robotics / Industrial Robots | 10 | $256.2M |
| Semiconductors / Foundry | 1 | $206.0M |
| Robotics / Humanoid & Service Robots | 7 | $185.7M |
| Robotics / Warehouse & Logistics | 5 | $168.6M |

## Deal type distribution

| Type | Deals | Disclosed |
|------|------:|----------:|
| Venture | 92 | $4,111.9M |
| Strategic corporate | 10 | $605.1M |
| Debt | 3 | $266.5M |
| Token | 5 | $264.8M |
| Government | 3 | $147.3M |

## Geography (top 10)

| Country | Deals |
|---------|------:|
| USA | 49 |
| China | 22 |
| Canada | 8 |
| Germany | 5 |
| India | 5 |
| Japan | 4 |
| France | 4 |
| Switzerland | 3 |
| United Kingdom | 3 |
| Israel | 2 |

## Monthly cadence

| Month | Deals |
|-------|------:|
| October 2023 | 46 |
| November 2023 | 30 |
| December 2023 | 37 |

## Top 20 deals by amount

| Company | Date | Sector | Round | Amount |
|---------|------|--------|-------|-------:|
| GaN Systems | 2023-10-24 | Semiconductors | M&A | $830.0M |
| Shield AI | 2023-12-29 | Robotics | Series F (extension) | $300.0M |
| Ola Electric | 2023-10-26 | Materials | Debt Financing | $240.0M |
| Wormhole | 2023-11-29 | Token | Strategic | $225.0M |
| Pragmatic Semiconductor | 2023-12-06 | Semiconductors | Series D | $206.0M |
| Shield AI | 2023-10-31 | Robotics | Series F | $200.0M |
| Lightmatter | 2023-12-19 | Semiconductors | Series C (extension) | $155.0M |
| Galactic Energy | 2023-12-18 | Space | Series C (extension) | $154.0M |
| Didi Autonomous Driving (Didi Woya) | 2023-10-12 | Robotics | Strategic | $149.0M |
| Ola Electric | 2023-10-26 | Materials | Strategic | $140.0M |
| GreyOrange | 2023-12-20 | Robotics | Series D (extension) | $135.0M |
| Landspace | 2023-12-25 | Space | Government investment | $123.0M |
| Element Energy | 2023-11-14 | Materials | Series B | $111.0M |
| May Mobility | 2023-11-07 | Robotics | Series D | $105.0M |
| Gecko Robotics | 2023-12-05 | Robotics | Series C (extension) | $100.0M |
| Pony.ai | 2023-10-25 | Robotics | Strategic | $100.0M |
| Photonic Inc. | 2023-11-08 | Semiconductors | Strategic | $100.0M |
| Oxford Quantum Circuits | 2023-11-27 | Semiconductors | Series B | $100.0M |
| Stoke Space | 2023-10-05 | Space | Series B | $100.0M |
| True Anomaly | 2023-12-12 | Space | Series B | $100.0M |

## Multi-row entities (legitimate concurrent events)

- **Shield AI**: Series F ($200M, Oct 31) + Series F extension ($300M, Dec 29) — back-to-back closes within the same quarter
- **Ola Electric**: Strategic equity ($140M Temasek, Oct 26) + Debt Financing ($240M SBI, Oct 26) — split per multi-row convention; pre-IPO structured deal totaling $384M

## Schema additions (with user approval)

Three new round values added to enum, all consistent with existing extension-naming patterns:
- `Pre-Series C` (Skyroot Aerospace $27.5M, Temasek-led)
- `Series F (extension)` (Shield AI $300M Dec extension)
- `Series G (extension)` (Astroscale $7.5M extension pre-IPO)

## FX coverage

47 of 113 rows (42%) are non-USD with full FX capture (`native_currency`, `native_amount`, `fx_source`, `fx_rate_used`):
- CNY: 20 rows (China robotics, AVs, launchers)
- EUR: 11 rows (German Bionic, Pasqal, D-Orbit-region competitors, etc.)
- CAD: 4 rows (Canadian quantum/space)
- JPY: 3 rows (Astroscale, Axelspace)
- INR: 3 rows (Ola, AgniKul, Skyroot)
- KRW: 2 rows
- CHF: 2 rows
- GBP: 2 rows

## Triage decisions (5 drops)

| Company | Amount | Reason |
|---------|-------:|--------|
| Epsilon Advanced Materials (EAM) | $649.9M | Indian parent corporate capex commitment for NC plant — not a fundraising event (per Nth Cycle precedent) |
| io.net | $30.0M | Same $30M as existing 1Q24 Series A row — formal announcement was March 2024 |
| D-Orbit | $53.5M | Possible duplicate of existing 2024-09-27 $53.4M Series C extension row; flagged 2024-01-11 row date for follow-up |
| Pipedream Labs | $9.43M | Round/date order inconsistent with existing 2024-04-23 Seed row — too suspicious to include without verification |
| Firefly Aerospace | $175.0M | "Series C third tranche" claim insufficiently corroborated; existing $175M Series D Nov 2024 already in dataset |

## Notable themes

- **Robotics dominated by AVs/drones.** Shield AI's two Series F closes ($500M combined), Didi Woya's $149M, May Mobility's $105M, and Pony.ai's $100M strategic together represent ~$854M in autonomous-systems capital — 42% of the sector's quarterly disclosed total.
- **GaN Systems M&A skews semis.** Infineon's $830M acquisition close represents 52% of disclosed semis capital. Excluding M&A, primary semis fundraising was a thin $752M across 17 rounds — reflecting the broader 2023 "lackluster" chip-startup funding narrative.
- **Quantum cluster.** Five quantum-adjacent rounds in semis: Photonic Inc. ($100M Microsoft/BCI), OQC ($100M Series B), Pasqal Quebec govt investment, Quandela, Nu Quantum. Quantum was disproportionately active relative to total semi-startup activity.
- **China launch megafund.** Landspace ($123M state) + Galactic Energy ($154M Series C ext) + Space Pioneer (~$98M C+) — Chinese state capital funded ~$375M of methane/reusable launcher development in a single quarter.
- **Token sector at cycle low.** $264.8M across 5 deals; Wormhole's $225M Brevan Howard-led was the largest crypto round of all of 2023 per Crunchbase Web3 tracker. Bittensor, Akash, Render, Helium had no equity rounds in the quarter.
- **No CHIPS Act binding awards.** BAE Systems Dec 11 announcement was a non-binding PMT (excluded). First binding CHIPS Act award (Polar Semiconductor) did not finalize until Sept 2024.

## Cumulative dataset state

| Quarter | Deals |
|---------|------:|
| 4Q23 | 113 (new) |
| 1Q24 | 100 |
| 2Q24 | 97 |
| 3Q24 | 78 |
| 4Q24 | 89 |
| 1Q25 | 36 |
| 2Q25 | 47 |
| 3Q25 | 62 |
| 4Q25 | 70 |
| 1Q26 | 89 |
| 2Q26 | 4 |
| **Total** | **785** |

1Q25 deal-count gap (36 vs 47–100 neighbors) flagged at [audit_followups.md](audit_followups.md) for supplemental backfill consideration.

## Next: 3Q23 backfill

Same workflow — 4 parallel research agents (Robotics, Semis, Space, Materials/Tokens), 27 canonical subsectors plus the 3 new round values approved this quarter, multi-row convention preserved, FX guardrails for non-USD deals.
