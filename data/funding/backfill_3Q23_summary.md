# 3Q23 Backfill Summary

**Window:** July 1 – September 30, 2023
**Rows added:** 118
**Cumulative dataset:** 903 rows across 12 quarters (3Q23–2Q26)

## Aggregate (two views)

| View | Deals | Disclosed |
|------|------:|----------:|
| **Headline** (all deal types) | 118 | **$31,307.8M** |
| **True venture** (ex-IPO/M&A/government/strategic/debt/token) | 86 | **$9,317.1M** |

Headline is dominated by three macro events: ARM Holdings IPO ($4.87B), ESMC TSMC/Bosch/Infineon/NXP JV ($3.85B strategic), and Eutelsat–OneWeb M&A combination ($3.4B). Like 4Q24's CHIPS Act PMTs, these drag the headline well above the underlying venture pace. **The "true venture" line is the cleaner number for cross-quarter pacing comparisons.**

## Sector breakdown (headline / venture-only)

| Sector | Headline deals | Headline $ | True venture deals | True venture $ |
|--------|--------------:|-----------:|-------------------:|---------------:|
| Semiconductors | 30 | $16,736.6M | 18 | $596.4M |
| Materials | 13 | $6,556.5M | 12 | $5,356.5M |
| Space | 16 | $4,370.4M | 11 | $801.4M |
| Robotics | 58 | $3,619.4M | 45 | $2,562.8M |
| Token | 1 | $25.0M | 0 | $0.0M |
| **Total** | **118** | **$31,307.8M** | **86** | **$9,317.1M** |

## Deal type distribution

| Type | Deals | Disclosed | % of headline |
|------|------:|----------:|--------------:|
| Venture (incl. IPO/M&A by classifier convention) | 93 | $21,390.1M | 68% |
| Strategic corporate | 14 | $8,069.0M | 26% |
| Debt | 7 | $1,666.1M | 5% |
| Government | 3 | $157.6M | 0.5% |
| Token | 1 | $25.0M | 0.1% |

> **Note:** Per existing classifier convention, IPO and M&A rounds are classified as `venture` deal_type. The "true venture" aggregate above strips those out for cleaner cross-quarter trend analysis.

## Top 20 deals

| Company | Date | Sector | Round | Amount |
|---------|------|--------|-------|-------:|
| Arm Holdings | 2023-09-14 | Semiconductors | IPO | $4,870.0M |
| ESMC (TSMC/Bosch/Infineon/NXP JV) | 2023-08-08 | Semiconductors | Strategic | $3,850.0M |
| Eutelsat OneWeb (combination) | 2023-09-28 | Space | M&A | $3,400.0M |
| Hua Hong Semiconductor | 2023-08-07 | Semiconductors | IPO | $2,950.0M |
| GTA Semiconductor | 2023-09-07 | Semiconductors | Strategic | $1,850.0M |
| Runpeng Semiconductor | 2023-08-14 | Semiconductors | Strategic | $1,700.0M |
| H2 Green Steel (Stegra) | 2023-09-07 | Materials | Series B | $1,607.0M |
| Northvolt | 2023-08-22 | Materials | Debt Financing | $1,200.0M |
| Stack AV | 2023-09-07 | Robotics | Series A | $1,000.0M |
| Redwood Materials | 2023-08-29 | Materials | Series D | $1,000.0M |
| Verkor | 2023-09-14 | Materials | Series C | $916.0M |
| Hithium Energy Storage | 2023-07-05 | Materials | Series C | $622.0M |
| Ascend Elements | 2023-09-11 | Materials | Series D | $542.0M |
| Berkshire Grey | 2023-07-21 | Robotics | M&A | $375.0M |
| Tower Semiconductor | 2023-08-16 | Semiconductors | M&A | $353.0M |
| Axiom Space | 2023-08-21 | Space | Series C | $350.0M |
| Sierra Space | 2023-09-26 | Space | Series B | $290.0M |
| Boston Metal | 2023-09-06 | Materials | Series C | $262.0M |
| iRobot | 2023-07-24 | Robotics | Debt Financing | $200.0M |
| Lyten | 2023-09-12 | Materials | Series B | $200.0M |

## Top subsectors by disclosed capital

| Sector / Subsector | Deals | Disclosed |
|--------------------|------:|----------:|
| Semiconductors / Foundry | 6 | $10,813.2M |
| Semiconductors / Fabless Design | 8 | $4,990.5M |
| Materials / Battery Materials | 10 | $4,638.5M |
| Space / Satellite Communications | 2 | $3,515.0M |
| Materials / Structural Materials | 2 | $1,869.0M |
| Robotics / Autonomous Systems & Drones | 17 | $1,726.5M |
| Space / In-Orbit Services | 5 | $700.4M |
| Robotics / Humanoid & Service Robots | 10 | $649.3M |
| Robotics / Warehouse & Logistics | 8 | $608.5M |
| Semiconductors / Frontier Compute | 8 | $563.6M |

## Geography (top 10)

| Country | Deals |
|---------|------:|
| USA | 46 |
| China | 28 |
| Germany | 7 |
| South Korea | 5 |
| France | 5 |
| Japan | 4 |
| Israel | 4 |
| United Kingdom | 3 |
| Italy | 3 |
| Netherlands | 3 |

## Monthly cadence

| Month | Deals |
|-------|------:|
| July 2023 | 38 |
| August 2023 | 38 |
| September 2023 | 42 |

## IPO / M&A inventory (7 deals, $12,073M)

| Company | Round | Amount |
|---------|-------|-------:|
| Arm Holdings | IPO | $4,870.0M |
| Eutelsat OneWeb | M&A | $3,400.0M |
| Hua Hong Semiconductor | IPO | $2,950.0M |
| Berkshire Grey | M&A | $375.0M |
| Tower Semiconductor | M&A | $353.0M |
| MACOM / Wolfspeed RF | M&A | $125.0M |
| RoboSense | IPO (filed) | undisclosed |

## Schema additions (with user approval)

One new round value:
- `Pre-Series B` — for Ronovo Surgical $27.4M (consistent with Pre-Series A and Pre-Series C precedent)

## FX coverage

51 of 118 rows (43%) are non-USD with full FX capture:
- CNY: 25 (China — semis foundry, robotics AVs, materials)
- EUR: 18 (Germany H2 Green Steel, France Aledia, etc.)
- KRW: 4 (Korean semis Sapeon Korea, robotics)
- JPY: 2 (Telexistence, GITAI)
- CHF: 1
- GBP: 1

## Triage decisions (13 drops)

### A. Token sector (5 drops)
Per "equity in crypto co → classify by tech sector OR drop if doesn't fit our 5 sectors" rule:

| Company | Amount | Reason |
|---------|-------:|--------|
| RISC Zero | $40.0M | zkVM software, not Frontier Compute hardware |
| Flashbots | $60.0M | MEV/SUAVE software, not Frontier Compute hardware |
| BitGo | $100.0M | Crypto custody, doesn't fit any of our 5 sectors |
| Friend.tech | undisclosed | Consumer social platform, not DePIN/AI |
| ZetaChain | $27.0M | Cross-chain L1 messaging, not the frontier thesis |

### B. Public secondaries at already-listed cos (6 drops)
Post-IPO public market events out of scope for private deals dataset:

| Company | Ticker | Round | Amount |
|---------|--------|-------|-------:|
| Aurora Innovation | NASDAQ:AUR | Public + PIPE | $820.0M |
| PROCEPT BioRobotics | NASDAQ:PRCT | Public secondary | $150.0M |
| Vicarious Surgical | NASDAQ:RBOT | Public follow-on | $45.0M |
| Innoviz Technologies | NASDAQ:INVZ | Public offering | $65.0M |
| Ehang | NASDAQ:EH | Public secondary | $23.0M |
| Asensus Surgical | NASDAQ:ASXC | Registered direct | $10.0M |

### C. Below-threshold drops (2)

| Company | Amount | Reason |
|---------|-------:|--------|
| PierSight Space | $0.6M | Below $3M space minimum |
| Astrape Networks | $1.7M | Below $5M robotics minimum, not flagship |

### D. Round reclassifications

12 rows the agent labeled "Other" reclassified by inspection:
- NEURA Robotics → Strategic (Lingotto/Exor lead)
- Northvolt → Debt Financing (convertible note)
- Kodiak Robotics → Bridge (convertible)
- Imagry → Bridge (convertible)
- Aledia → Strategic (existing investors + French sovereign)
- Suzhou Aijiwei Robot → Government investment (local-government-aligned)
- Figure → Strategic (Intel Capital add-on)
- Treeswift → Seed
- Robocon → Strategic (Korean pre-IPO style)
- Q-Bot → Seed
- Serve Robotics → Bridge (pre-merger)
- Intuition Robotics → Strategic (Toyota's Woven Capital led)

## Notable themes

- **Foundry dominates by capital, fabless dominates by deal count.** Foundry spend was concentrated in 6 mega-events ($10.8B): Hua Hong's IPO, ESMC JV, GTA Semiconductor, Runpeng, Hua Hong Wuxi, plus smaller. Fabless saw 8 rounds across $5.0B incl. ARM IPO. Strip ARM and ESMC and Hua Hong and the underlying private semis venture pace is just **$596M across 18 deals** — thin even by 2023 standards.
- **Materials carries the venture aggregate.** $5.36B in true venture is 57% of the quarter's true-venture total — driven by H2 Green Steel ($1.6B), Redwood ($1B), Verkor ($916M), Hithium ($622M), Ascend ($542M), Boston Metal ($262M), Lyten ($200M). 2023 was a peak year for battery-materials capital deployment ahead of the 2024–2025 cooling.
- **Robotics: AV/drones still leading subsector by deal count.** 17 rounds in Autonomous Systems & Drones ($1.73B) — Stack AV's $1B Series A (Bridgestone-anchored) was the standout. Humanoid & Service Robots had 10 rounds for $649M, including early Figure $9M Intel Capital add-on, Telexistence $170M, NEURA $55M Lingotto.
- **Eutelsat–OneWeb $3.4B M&A.** Combination of Eutelsat (GEO) and OneWeb (LEO) created a ~$3.4B equity merger; included as M&A but skews satellite communications heavily.
- **No CHIPS Act binding awards in 3Q23.** First binding CHIPS Act award (Polar Semiconductor) was Sept 2024. ESMC was a private JV announcement, not a US gov program.
- **Token sector at near-zero.** $25M from Manta Network — single deal that survived triage. Q3 2023 was the trough of the crypto winter; most "AI x crypto" activity at this point was R&D/protocol-launch, not equity rounds.

## Cumulative dataset state

| Quarter | Deals |
|---------|------:|
| 3Q23 | 118 (new) |
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
| **Total** | **903** |

1Q25 deal-count gap (36 vs neighbors 47–118) remains flagged at [audit_followups.md](audit_followups.md) for supplemental backfill consideration.

## Next: 2Q23 backfill

Same workflow — 4 parallel research agents (Robotics / Semis / Space / Materials+Tokens), 27 canonical subsectors, full round enum (now incl. Pre-Series B as well as Pre-Series A, Pre-Series C, Series F (extension), Series G (extension)), multi-row convention, FX guardrails, headline + venture-only aggregates.
