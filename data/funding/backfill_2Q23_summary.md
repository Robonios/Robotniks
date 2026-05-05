# 2Q23 Backfill Summary

**Window:** April 1 – June 30, 2023
**Rows added:** 98
**Cumulative dataset:** 1,001 rows across 13 quarters (2Q23–2Q26)

## Aggregate (two views)

| View | Deals | Disclosed |
|------|------:|----------:|
| **Headline** (all deal types) | 98 | **$6,369.4M** |
| **True venture** (ex-IPO/M&A/government/strategic/debt/token) | 84 | **$4,749.2M** |

Cleaner quarter than 3Q23: only 4 IPO/M&A events (~$135M) and 5 strategic corporates ($854M). The headline-vs-venture gap is much narrower than 3Q23's, where ARM IPO + ESMC JV + Eutelsat-OneWeb dominated.

## Sector breakdown (headline / venture-only)

| Sector | Headline deals | Headline $ | True venture deals | True venture $ |
|--------|--------------:|-----------:|-------------------:|---------------:|
| Robotics | 50 | $2,465.5M | 44 | $1,499.1M |
| Semiconductors | 21 | $1,703.9M | 19 | $1,658.1M |
| Materials | 9 | $1,338.4M | 7 | $938.4M |
| Space | 16 | $703.6M | 14 | $653.6M |
| Token | 2 | $158.0M | 0 | $0.0M |
| **Total** | **98** | **$6,369.4M** | **84** | **$4,749.2M** |

## Deal type distribution

| Type | Deals | Disclosed | % of headline |
|------|------:|----------:|--------------:|
| Venture (incl. IPO/M&A by classifier convention) | 88 | $4,884.5M | 77% |
| Strategic corporate | 5 | $854.4M | 13% |
| Debt | 2 | $444.0M | 7% |
| Token | 2 | $158.0M | 2% |
| Government | 1 | $28.5M | 0.4% |

## Top 20 deals

| Company | Date | Sector | Round | Amount |
|---------|------|--------|-------|-------:|
| 42dot | 2023-04-26 | Robotics | Strategic | $787.0M |
| Anhui YOFC Advanced Semiconductor (YASC) | 2023-06-28 | Semiconductors | Series A | $562.3M |
| Northvolt | 2023-06-20 | Materials | Debt Financing | $400.0M |
| Libode New Material | 2023-04-24 | Materials | Series B | $375.0M |
| SJ Semiconductor (SJSemi) | 2023-04-03 | Semiconductors | Series C | $340.0M |
| Zipline | 2023-04-28 | Robotics | Series F | $330.0M |
| Gradiant | 2023-05-17 | Materials | Series D | $225.0M |
| Astranis | 2023-04-11 | Space | Series D | $200.0M |
| KoBold Metals | 2023-06-20 | Materials | Series B | $195.0M |
| United Aircraft | 2023-06-19 | Robotics | Series D (extension) | $167.0M |
| Lightmatter | 2023-05-31 | Semiconductors | Series C | $154.0M |
| Distalmotion | 2023-04-19 | Robotics | Series E | $150.0M |
| Worldcoin (Tools for Humanity) | 2023-05-25 | Token | Series C | $115.0M |
| Celestial AI | 2023-06-27 | Semiconductors | Series B | $100.0M |
| Ursa Major | 2023-04-25 | Space | Series D | $100.0M |
| SiPearl | 2023-04-05 | Semiconductors | Series A | $98.5M |
| Kepler Communications | 2023-04-13 | Space | Series C | $92.0M |
| Tomorrow.io | 2023-06-12 | Space | Series E | $87.0M |
| Auradine | 2023-05-16 | Semiconductors | Series A | $81.0M |
| Covariant | 2023-04-04 | Robotics | Series C (extension) | $75.0M |

## Top subsectors by disclosed capital

| Sector / Subsector | Deals | Disclosed |
|--------------------|------:|----------:|
| Robotics / Autonomous Systems & Drones | 17 | $1,758.7M |
| Materials / Battery Materials | 6 | $891.4M |
| Semiconductors / Silicon & Substrates | 1 | $562.3M |
| Materials / Rare Earths & Critical Minerals | 3 | $447.0M |
| Semiconductors / Frontier Compute | 6 | $429.0M |
| Semiconductors / OSAT / Packaging & Test | 3 | $426.5M |
| Space / Satellite Communications | 3 | $312.0M |
| Robotics / Surgical & Medical | 5 | $229.4M |
| Space / Earth Observation | 5 | $160.8M |
| Semiconductors / Fabless Design | 5 | $145.1M |
| Robotics / Software & Simulation | 5 | $138.8M |
| Robotics / Humanoid & Service Robots | 5 | $126.9M |

## Geography (top 10)

| Country | Deals |
|---------|------:|
| USA | 38 |
| China | 22 |
| Germany | 5 |
| South Korea | 4 |
| Israel | 4 |
| Canada | 4 |
| Switzerland | 3 |
| India | 3 |
| France | 2 |
| Japan | 2 |

## Monthly cadence

| Month | Deals |
|-------|------:|
| April 2023 | 36 |
| May 2023 | 34 |
| June 2023 | 28 |

## IPO / M&A inventory (4 deals, ~$135M)

| Company | Round | Amount |
|---------|-------|-------:|
| ideaForge Technology | IPO | $68.0M |
| ispace | IPO | $50.0M |
| Softnautics → MosChip | M&A | $17.3M |
| Adranos → Anduril | M&A | undisclosed |

## FX coverage

40 of 98 rows (41%) are non-USD with full FX capture:
- CNY: 21 (China battery materials, semis foundry, robotics)
- EUR: 9 (German/French/Dutch hardware)
- KRW: 4 (42dot, SEMIFIVE, Korean industrial robotics)
- JPY: 2 (ispace, GITAI)
- CHF, CAD, INR, GBP: 1 each

## Triage decisions (2 drops, 1 reclassification)

### A. Drops (2)

| Company | Amount | Reason |
|---------|-------:|--------|
| Diligent Robotics | $44.3M | PitchBook + Robot Report aggregation as primary; conflicts with company's own Sept 2023 press release labeling next round as "Series B (extension)" — you don't go back from C to B-ext. Round naming likely Crunchbase mislabel. |
| Saronic Technologies | $2.5M | Single Axios local-edition source published Oct 2023 (4 months post-round) referencing Pre-Seed only as backstory. No canonical contemporaneous announcement. |

### B. Reclassification (1)

| Company | From | To | Reason |
|---------|------|-----|--------|
| Northvolt | Strategic | Debt Financing | Convertible note from IMCO + Goldman Sachs; structurally identical to existing 3Q23 BlackRock $1.2B convertible already classified as Debt Financing. |

### C. Cross-quarter sequential closes verified (kept both rows in each pair)

- **GITAI**: 2Q23 $30M Series B ext (May 24) + 3Q23 $15M Series B ext (Aug 29) = $45M total Series B
- **FERNRIDE**: 2Q23 $31M Series A (Jun 13) + 3Q23 $19M Series A ext (Sep 20) = $50M total Series A
- **Lyten**: 2Q23 Stellantis Strategic placement (May 25, undisclosed amt) + 3Q23 $200M Series B (Sept 12)
- **Northvolt**: 2Q23 $400M IMCO convertible (Jun 20) + 3Q23 $1.2B BlackRock convertible (Aug 22)

## Notable themes

- **42dot $787M dominates**. Hyundai/Kia's KRW 1.05T captive subsidiary cap raise (April 26) is by far the largest deal — comp to GM/Cruise dynamic but with tighter integration. This single deal is 12% of quarterly headline.
- **Robotics autonomous concentration.** 17 of 50 robotics deals are Autonomous Systems & Drones at $1.76B (71% of robotics capital). 42dot, Zipline ($330M), United Aircraft ($167M China eVTOL), Covariant ($75M), Wayve, Stack AV-precursor activity, Outrider, Teleo.
- **Early humanoid signal pre-boom.** Figure AI's $70M Series A (May), ANYbotics $50M Series B (May), Distalmotion $150M Series E (Apr) — quiet before the late-2023/2024 humanoid funding tsunami.
- **China silicon capacity push.** YASC ($562M SiC IDM) + SJ Semiconductor ($340M packaging foundry) + Libode ($375M battery materials) + AaltoSemi ($72.5M packaging substrates) = $1.35B of Chinese hard-tech deployment, indicative of state-backed semis localization momentum following US export controls.
- **Battery materials Northvolt era peak.** Pre-bankruptcy IMCO convertible ($400M June 20) was Northvolt's debt-stack peak before the November 2024 collapse. KoBold Metals $195M Series B (Jun 20, T. Rowe Price + a16z + Gates/Bezos-backed BEV) crossed $1.15B unicorn threshold.
- **Photonics cluster.** Lightmatter $154M + Celestial AI $100M + Ayar Labs ~$25M = $279M deployed in photonic/optical-I/O compute infrastructure within a single quarter — early signal of the AI interconnect bottleneck thesis.
- **Token sector minimal.** $158M across 2 deals (Worldcoin $115M, Gensyn $43M). Strict guardrails kept LayerZero, Story Protocol, Berachain, EigenLayer (Q1) out as either pure-software or out-of-scope; the surviving 2 cleanly fit the DePIN/Frontier Compute thesis.
- **Hardened guardrails worked.** Zero "Other" round labels (vs. 18 in 3Q23 raw), zero pure-software crypto inclusions, zero public secondaries (Aurora PIPE, Astrocast post-IPO debt all properly excluded).

## Cumulative dataset state

| Quarter | Deals |
|---------|------:|
| 2Q23 | 98 (new) |
| 3Q23 | 118 |
| 4Q23 | 113 |
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
| **Total** | **1,001** |

**Milestone:** Dataset crosses 1,000 rows.

## Next: 1Q23 backfill

Final 2023 quarter remaining. Same workflow — 4 parallel research agents (Robotics / Semis / Space / Materials+Tokens), 27 canonical subsectors, full round enum (Pre-Series A/B/C, Series F+G extensions), hardened guardrails (no "Other", no public secondaries, no pure-software crypto, no parent capex commitments), multi-row convention, FX guardrails, headline + venture-only aggregates.
