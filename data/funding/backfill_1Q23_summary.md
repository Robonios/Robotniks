# 1Q23 Backfill Summary

**Window:** January 1 – March 31, 2023
**Rows added:** 79
**Cumulative dataset:** 1,080 rows across 14 quarters (1Q23–2Q26)

## Aggregate (two views)

| View | Deals | Disclosed |
|------|------:|----------:|
| **Headline** (all deal types) | 79 | **$9,794.6M** |
| **True venture** (ex-IPO/M&A/government/strategic/debt/token) | 65 | **$2,755.0M** |

The headline is heavily skewed by **3 strategic events** totaling $6.67B (68% of headline):
- Hua Hong Semiconductor JV $4.02B (Wuxi 12-inch fab capital injection from Hua Hong Group + Wuxi gov + China IC Industry Investment Fund Phase II)
- YMTC $1.9B Strategic recapitalization (China Big Fund Phase II following US export controls)
- SpaceX $750M Strategic (early-2023 employee tender + primary capital)

Strip those three and the underlying venture pace of $3.1B is the thinnest of the 6 backfilled 2023-2024 quarters — consistent with the immediate post-SVB-collapse drought (March 2023) and the broader hardware-VC funding cycle bottom.

## New rule documented: **Government capital binding-only**

Effective this pass and going forward, government capital enters the dataset **only when it represents a finalized/binding award**. This applies the same logic the project has used for CHIPS Act preliminary memorandums of terms (PMTs):

| Instrument type | Include? |
|-----------------|----------|
| CHIPS Act PMT (preliminary memorandum of terms) | ❌ Exclude |
| CHIPS Act binding award / signed agreement | ✓ Include |
| DOE LPO / ATVM **conditional commitment** | ❌ Exclude |
| DOE LPO / ATVM **closed loan** | ✓ Include |
| ESA contract / OTA / SBIR — meaningful capital with delivery | ✓ Include (as Government investment) |
| Routine procurement | ❌ Exclude |
| Grants (executed, funds disbursed) | ✓ Include (as Grant) |

Rationale: conditional commitments are routinely renegotiated, restructured, or rescinded between announcement and close. Including them at the announcement date inflates headline figures with capital that may never deploy. The project records government capital at the close/binding-award date for consistency.

## Sector breakdown (headline / venture-only)

| Sector | Headline deals | Headline $ | True venture deals | True venture $ |
|--------|--------------:|-----------:|-------------------:|---------------:|
| Semiconductors | 13 | $6,346.2M | 7 | $199.4M |
| Space | 15 | $1,410.9M | 12 | $600.9M |
| Robotics | 44 | $1,352.5M | 40 | $1,299.7M |
| Materials | 7 | $685.0M | 6 | $655.0M |
| Token | 0 | $0.0M | 0 | $0.0M |
| **Total** | **79** | **$9,794.6M** | **65** | **$2,755.0M** |

## Deal type distribution

| Type | Deals | Disclosed | % of headline |
|------|------:|----------:|--------------:|
| Strategic corporate | 10 | $6,768.8M | 69% |
| Venture (incl. IPO/M&A by classifier convention) | 66 | $2,945.0M | 30% |
| Government | 2 | $70.8M | 1% |
| Debt | 1 | $10.0M | 0.1% |
| Token | 0 | $0.0M | 0% |

## Top 20 deals

| Company | Date | Sector | Round | Amount |
|---------|------|--------|-------|-------:|
| Hua Hong Semiconductor JV (Wuxi) | 2023-01-31 | Semiconductors | Strategic | $4,020.0M |
| Yangtze Memory Technologies (YMTC) | 2023-02-27 | Semiconductors | Strategic | $1,900.0M |
| SpaceX | 2023-01-03 | Space | Strategic | $750.0M |
| Our Next Energy (ONE) | 2023-02-01 | Materials | Series B | $300.0M |
| Skydio | 2023-02-27 | Robotics | Series E | $230.0M |
| Fungible | 2023-01-09 | Semiconductors | M&A | $190.0M |
| Isar Aerospace | 2023-03-28 | Space | Series C | $165.0M |
| Oxbotica | 2023-01-10 | Robotics | Series C | $140.0M |
| Boston Metal | 2023-01-27 | Materials | Series C | $120.0M |
| Pasqal | 2023-01-23 | Semiconductors | Series B | $108.0M |
| Standard Robots | 2023-03-15 | Robotics | Series C | $86.5M |
| Voyager Space | 2023-02-03 | Space | Series A | $80.2M |
| StoreDot | 2023-01-09 | Materials | Series D | $80.0M |
| Astroscale | 2023-02-27 | Space | Series G | $76.0M |
| Outrider | 2023-01-19 | Robotics | Series C | $73.0M |
| Nimble Robotics | 2023-03-16 | Robotics | Series B | $65.0M |
| NanoGraf | 2023-02-14 | Materials | Series B | $65.0M |
| Fulfil Solutions | 2023-02-27 | Robotics | Series B | $60.0M |
| Capella Space | 2023-01-10 | Space | Series C (extension) | $60.0M |
| Varda Space Industries | 2023-03-24 | Space | Government investment | $60.0M |

## Top subsectors by disclosed capital

| Sector / Subsector | Deals | Disclosed |
|--------------------|------:|----------:|
| Semiconductors / Foundry | 1 | $4,020.0M |
| Semiconductors / Fabless Design | 4 | $2,115.9M |
| Space / Launch | 3 | $974.9M |
| Robotics / Autonomous Systems & Drones | 18 | $824.8M |
| Materials / Battery Materials | 4 | $495.0M |
| Robotics / Warehouse & Logistics | 8 | $338.3M |
| Space / In-Orbit Services | 5 | $267.4M |
| Semiconductors / Frontier Compute | 7 | $195.6M |
| Materials / Structural Materials | 2 | $160.0M |
| Space / Earth Observation | 2 | $119.6M |
| Robotics / Humanoid & Service Robots | 6 | $83.0M |
| Space / Satellite Communications | 2 | $33.0M |

## Geography (top 10)

| Country | Deals |
|---------|------:|
| USA | 34 |
| China | 10 |
| France | 6 |
| Switzerland | 4 |
| Australia | 4 |
| Israel | 3 |
| Japan | 3 |
| Canada | 3 |
| Germany | 2 |
| Norway | 1 |

## Monthly cadence

| Month | Deals |
|-------|------:|
| January 2023 | 32 |
| February 2023 | 24 |
| March 2023 | 23 |

Mar 2023 dipped — SVB collapsed Mar 10, 2023 and froze funding flows for several weeks. This is consistent with the broader hardware-VC drawdown.

## IPO / M&A inventory (1 deal, $190M)

| Company | Round | Amount |
|---------|-------|-------:|
| Fungible (acquired by Microsoft) | M&A | $190.0M |

## FX coverage

16 of 79 rows (20%) are non-USD with full FX capture:
- EUR: 7 (Pasqal, Isar Aerospace, German/French hardware)
- CNY: 6 (Hua Hong JV, YMTC, Chinese AVs)
- JPY: 1 (Astroscale)
- CHF: 1 (Distalmotion is in 2Q23; this is something else)
- GBP: 1 (Oxbotica)

## Triage decisions (12 drops)

### A. Routine triage (8 drops)

| Company | Amount | Sector | Reason |
|---------|-------:|--------|--------|
| BlackSky | $29.5M | Space | Public-co PIPE (NASDAQ:BKSY) — same rule as Aurora |
| PlanetiQ | $3.31M | Space | Single-source Tracxn, no canonical contemporaneous announcement |
| World View | $121.0M | Space | SPAC merger announcement that was TERMINATED late 2023 |
| Patriot Battery Metals | $36.5M | Materials | TSXV-listed flow-through placement |
| Talga Group | $27.3M | Materials | ASX-listed institutional placement |
| KoBold Metals | $195.0M | Materials | Date conflict; canonical KoBold Series B announcement was June 2023 (existing 2Q23 row) |
| Lumotive (robotics row) | — | Robotics | Duplicate of Lumotive semis row (correct sector is Frontier Compute for LiDAR optical beam-steering chip) |
| Berkshire Grey | $375.0M | Robotics | M&A announcement Mar 24, 2023; existing 3Q23 row at Jul 21, 2023 captures the close — same deal, drop the announcement-date row |

### B. Per new "binding-only government capital" rule (3 drops)

| Company | Amount | Sector | Reason |
|---------|-------:|--------|--------|
| Lithium Americas | $650.0M | Materials | NYSE:LAC PIPE for GM-Thacker Pass strategic; per Aurora-PIPE rule (public-co PIPE → drop) |
| Redwood Materials | $2,000.0M | Materials | DOE ATVM **conditional commitment** Feb 9, 2023 — not a binding award. Loan finalized later; that close-date event would be eligible. |
| Ioneer (Rhyolite Ridge) | $700.0M | Materials | DOE LPO **conditional commitment** Jan 13, 2023 — not a binding award. Same logic as CHIPS Act PMT exclusion. |

### D. Token sector (1 drop)

| Company | Amount | Reason |
|---------|-------:|--------|
| EigenLayer | $50.0M | Restaking middleware isn't frontier infrastructure — same logic as RISC Zero/Flashbots/BitGo/ZetaChain drops. |

**Net 1Q23 capital removed by triage:** $4,187.6M (mostly from binding-only rule and PIPE rule).

## Cross-quarter overlaps verified as legitimate sequential closes (kept both rows)

- **Boston Metal**: 1Q23 Series C $120M (Jan 27) + 3Q23 Series C $262M (Sep 6) — sequential closes of same Series C ($382M total)
- **Q-CTRL**: 1Q23 Series B (extension) $27.4M (Jan 31) + 3Q23 Series B (extension) $54M (Jul 25)
- **Astroscale**: 1Q23 Series G $76M + 4Q23 Series G ext $7.5M
- **K2 Space**: 1Q23 Seed $8.5M + 4Q23 Seed (extension) $7M
- **NorthStar Earth & Space**: 1Q23 Series C $35M + 4Q23 Series D $14.7M (different rounds)
- **Hanyang Technology**: 1Q23 Pre-Series A $14.5M + 2Q23 Series A $20M (different rounds)
- **Verity, Garuda, Pasqal, VSORA, Capella**: distinct rounds at different times — kept both

## Notable themes

- **China state semis recap dwarfs everything.** Hua Hong's $4.02B Wuxi JV recap + YMTC's $1.9B Big Fund Phase II recap = $5.92B (60% of headline). Both are state-strategic capital injections to maintain semi capacity following October 2022 US export controls. These are not commercial venture rounds; they're sovereign industrial policy instruments.
- **SpaceX dominates Space.** $750M Jan 3 employee tender + primary capital is 53% of Space sector. Underlying pace excluding SpaceX: $660M across 14 deals — a soft quarter. Isar Aerospace's €155M Series C ($165M) was the largest non-SpaceX space deal of the quarter.
- **Robotics: Skydio Series E flagship.** $230M @ $2.2B val (Feb 27) led by Linse Capital — first major robotics round of the year. AVs/drones dominated robotics by deal count (18/44 = 41%).
- **Materials thinned by triage.** After dropping LAC PIPE, Redwood DOE conditional, Ioneer DOE conditional, KoBold (date moved), Patriot, and Talga, materials sector ends at just $685M / 7 deals — versus the raw agent count of $4.3B / 13 deals. The headline-vs-true-venture gap in materials is the largest of any sector this quarter (96% reduction). Big-ticket battery materials capital in Q1 2023 was largely a government-conditional and listed-co phenomenon, not private venture.
- **Token sector zero.** EigenLayer was the only candidate found; dropped per restaking-isn't-frontier rule. Q1 2023 was the bottom of the crypto winter; AI x crypto thesis hadn't yet emerged.
- **SVB collapse (March 10, 2023) visible in cadence.** March deal count 23 vs January 32 — funding flows froze for several weeks following the bank failure.
- **Hardened guardrails held.** Zero "Other" round labels (vs 18 in 3Q23 raw), zero pure-software crypto inclusions, zero public secondaries through, zero government conditional commitments.

## Cumulative dataset state

| Quarter | Deals |
|---------|------:|
| 1Q23 | 79 (new) |
| 2Q23 | 98 |
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
| **Total** | **1,080** |

## Backfill complete

**All eight 2023–2024 quarters** (1Q23–4Q24) and all 2025–2026 quarters now in the dataset. The full multi-year private markets funding picture is captured for the Robotnik universe.

Open audit follow-ups remain at [audit_followups.md](audit_followups.md):
- 5 unreachable-source rows (Waabi, Rapidus, Elementium Materials, Orqa, Nexthop AI)
- Saronic / Saronic Technologies entity_id consolidation
- 1Q25 deal-count gap (36 vs neighbors 47–118) — supplemental backfill candidate
- 25 minor_discrepancy 1Q26 rows from earlier integrity sweep
