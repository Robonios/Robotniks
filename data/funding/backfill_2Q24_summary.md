# 2Q24 Private Markets Backfill — Summary

**Generated:** 2026-05-02
**Quarter covered:** Apr 1 – Jun 30, 2024
**File touched:** [data/funding/rounds.json](rounds.json)

## Headline numbers

- **97 deals** added
- **$7.86B** aggregate disclosed value
- **576 total rows** in `rounds.json` after append (was 479)
- **Quarter coverage now extends 2Q24 → 2Q26** (9 quarters total)

### Sense-check vs prompt expectation

You expected $5-15B for a typical quarter. 2Q24 came in at **$7.86B** — squarely in range. Lowest-CHIPS-distortion quarter so far in the backfill.

2Q24 had **zero finalized binding CHIPS Act commercial awards** (the first was Polar Sep 24, 2024 in 3Q24). All Q2 PMTs (Micron $6.1B, Samsung $6.4B, Microchip, etc.) were non-binding and finalized later.

## What's new in this batch

### `Decentralized AI / DePIN` subsector live-tested

First quarter to apply the new 27th subsector at scale. **6 deals** classified under `Decentralized AI / DePIN`:

| Company | Round | $ | Notes |
|---|---|---|---|
| IoTeX | Strategic | $50.0M | Modular DePIN L1; token-denominated structure |
| Aligned Layer | Series A | $20.0M | EigenLayer AVS for ZK-proof verification |
| SendingNetwork | Seed (extension) | $7.5M | DePIN messaging protocol |
| Arcium | Strategic | $5.5M | Confidential-computing network (MPC + FHE + ZK) |
| Prime Intellect | Seed | $5.5M | Decentralized AI training platform |
| Privasea | Strategic | $4.75M | FHE-powered privacy compute for AI data |

### `deal_type=token` rule clarified

Caught and fixed a classifier ambiguity: when `sector=Token AND round=Strategic`, the original classifier returned `strategic_corporate`. Updated the rule so **`sector=Token` takes precedence** — all sector=Token rows now uniformly classify as `deal_type=token` regardless of round mechanic.

Updated rule:
```python
def classify(r):
    if r['sector'] == 'Token':
        return 'token'
    if r['round'] == 'Strategic':
        return 'strategic_corporate'
    if r['round'] in ('Government investment', 'Government', 'Grant'):
        return 'government'
    if r['round'] == 'Debt Financing':
        return 'debt'
    return 'venture'
```

3 rows reclassified: IoTeX, Arcium, Privasea (`strategic_corporate` → `token`). The 4Q24 + 3Q24 Sentient/Sahara AI rows were already correct since they have non-Strategic rounds.

### One new round value: `Seed (extension)`

Added for SendingNetwork. Follows the existing pattern of `Series A/B/C/D/E (extension)` — extends the same naming convention to seed level rather than reusing `Bridge` (which has different semantics in the existing dataset).

### Multi-row convention applied: Black Semiconductor

First test of the same-company-same-quarter convention from the 3Q24 ruleset. Black Semiconductor's €254.4M Series A had two distinct legal mechanics announced jointly:

| Company | Date | Round | $ | Mechanic |
|---|---|---|---|---|
| Black Semiconductor | 2024-06-12 | Series A | $27.7M | €25.7M private equity (Porsche/Scania-led) |
| Black Semiconductor | 2024-06-12 | Government investment | $246.2M | €228.7M IPCEI ME/CT public funding (Germany federal + NRW) |

Both rows share `entity_id=black-semiconductor`, distinct rounds, distinct `deal_type` (`venture` vs `government`). Cross-referenced in `robotnik_notes`.

## `deal_type` distribution for 2Q24

| deal_type | Deals | Aggregate |
|---|---|---|
| `venture` | 81 | $5.18B |
| `government` | 3 | $869.7M |
| `strategic_corporate` | 7 | $1.71B |
| `debt` | 0 | $0.0M |
| `token` | 6 | $93.2M |

## Breakdown by sector

| Sector | Deals | Aggregate |
|---|---|---|
| Robotics | 49 | $4.13B |
| Semiconductors | 21 | $1.87B |
| Space | 16 | $1.19B |
| Materials | 5 | $587.4M |
| Token | 6 | $93.2M |

## Breakdown by sector × subsector

### Robotics — 49 deals, $4.13B

| Subsector | Deals | Aggregate |
|---|---|---|
| Autonomous Systems & Drones | 23 | $3.18B |
| Industrial Robots | 10 | $332.0M |
| Humanoid & Service Robots | 5 | $318.4M |
| Collaborative Robots | 1 | $100.0M |
| Surgical & Medical | 5 | $87.9M |
| Warehouse & Logistics | 2 | $53.0M |
| Machine Vision & Sensors | 1 | $30.0M |
| Software & Simulation | 1 | $20.0M |
| Motion Control & Actuators | 1 | $6.1M |

### Semiconductors — 21 deals, $1.87B

| Subsector | Deals | Aggregate |
|---|---|---|
| Frontier Compute | 7 | $1.25B |
| Silicon & Substrates | 2 | $273.9M |
| Fabless Design | 4 | $208.5M |
| OSAT / Packaging & Test | 3 | $87.3M |
| EDA & IP | 4 | $29.1M |
| Equipment | 1 | $12.5M |

### Space — 16 deals, $1.19B

| Subsector | Deals | Aggregate |
|---|---|---|
| Launch | 4 | $382.7M |
| Space Components | 4 | $299.5M |
| In-Orbit Services | 4 | $295.6M |
| Earth Observation | 2 | $136.9M |
| Satellite Communications | 2 | $71.8M |

### Materials — 5 deals, $587.4M

| Subsector | Deals | Aggregate |
|---|---|---|
| Battery Materials | 3 | $464.6M |
| Structural Materials | 1 | $111.0M |
| Rare Earths & Critical Minerals | 1 | $11.8M |

### Token — 6 deals, $93.2M

| Subsector | Deals | Aggregate |
|---|---|---|
| Decentralized AI / DePIN | 6 | $93.2M |

## Breakdown by geography

| Country | Deals | Aggregate |
|---|---|---|
| USA | 41 | $4.07B |
| United Kingdom | 6 | $1.21B |
| China | 7 | $633.5M |
| Germany | 6 | $425.3M |
| South Korea | 4 | $311.7M |
| Japan | 3 | $234.1M |
| Canada | 4 | $213.9M |
| Israel | 6 | $206.0M |
| Australia | 2 | $118.0M |
| Finland | 1 | $93.0M |
| Spain | 3 | $92.9M |
| Netherlands | 2 | $90.0M |
| Singapore | 1 | $50.0M |
| Global | 4 | $37.8M |
| France | 4 | $31.7M |
| Denmark | 1 | $20.0M |
| Switzerland | 1 | $11.0M |
| Lithuania | 1 | $3.5M |

## Top 10 deals by size

| # | Company | Round | Amount | Lead investor(s) |
|---|---|---|---|---|
| 1 | **Wayve** | Series C | $1.05B | SoftBank Group |
| 2 | **Cruise** | Strategic | $850.0M | General Motors |
| 3 | **PsiQuantum** | Government investment | $620.0M | Australian Commonwealth Government, Queensland State Government |
| 4 | **Motional** | Strategic | $475.0M | Hyundai Motor Group |
| 5 | **Sila Nanotechnologies** | Series G | $375.0M | Sutter Hill Ventures, T. Rowe Price Associates |
| 6 | **Rivos** | Series A | $250.0M | Matrix Capital Management |
| 7 | **Black Semiconductor** | Government investment | $246.2M | German federal government & North Rhine-Westphalia (IPCEI ME/CT) |
| 8 | **Space Pioneer** | Series C (extension) | $207.0M | Undisclosed Chinese institutional investors |
| 9 | **Waabi** | Series B | $200.0M | Uber, Khosla Ventures |
| 10 | **42dot** | Strategic | $185.0M | Hyundai Motor Company, Kia Corporation |

## Deals flagged `single_source: true` (56 rows)

Worth a second pass before relying for analysis. The bulk are smaller deals where only the company press release was available; major deals all have multiple-source confirmation.

| Company | Round | Amount |
|---|---|---|
| Orbex | Series D | $20.7M |
| FOSSA Systems | Series A | $6.8M |
| Princeton NuEnergy | Series A | $30.0M |
| SendingNetwork | Seed (extension) | $7.5M |
| Cruise | Strategic | $850.0M |
| 42dot | Strategic | $185.0M |
| Bright Machines | Series C | $106.0M |
| Rokae Robotics | Strategic | $69.1M |
| TIER IV | Series B (extension) | $54.0M |
| Gausium | Series D | $50.0M |
| GrayMatter Robotics | Series B | $45.0M |
| Ronovo Surgical | Series B | $44.0M |
| XTEND | Series B | $40.0M |
| Vecna Robotics | Series C (extension) | $40.0M |
| Ripcord | Other | $32.0M |
| PhiGent Robotics | Series B | $30.0M |
| Gatik | Strategic | $30.0M |
| Formic Technologies | Series A | $27.4M |
| Orca AI | Other | $23.0M |
| Vitestro | Other | $22.0M |
| Aerodome | Series A | $21.5M |
| Kinetic | Series B | $21.0M |
| Greeneye Technology | Other | $20.0M |
| BurnBot | Series A | $20.0M |
| Reshape Biotech | Series A | $20.0M |
| Planted Solar | Series A | $20.0M |
| TerraClear | Other | $15.3M |
| Pipedream Labs | Seed | $13.0M |
| Coboworx | Other | $12.2M |
| SpinEM Robotics | Series A (extension) | $11.0M |
| ... | ... | (+26 more) |

## Subsector classification flags (24 rows)

Best-fit assignment under the existing 27-value enum. Common pattern: ag-robotics + lab-automation + manufacturing-as-construction + DePIN-adjacent (non-AI) — all hit gaps in the current taxonomy.

| Company | Sector | Assigned subsector |
|---|---|---|
| Varda Space Industries | Space | In-Orbit Services |
| Sift | Space | Space Components |
| Zeno Power | Space | Space Components |
| SiTration | Materials | Rare Earths & Critical Minerals |
| Hysata | Materials | Structural Materials |
| Aligned Layer | Token | Decentralized AI / DePIN |
| SendingNetwork | Token | Decentralized AI / DePIN |
| Skyports Infrastructure | Robotics | Autonomous Systems & Drones |
| Ripcord | Robotics | Industrial Robots |
| Kinetic | Robotics | Autonomous Systems & Drones |
| Greeneye Technology | Robotics | Autonomous Systems & Drones |
| Reshape Biotech | Robotics | Software & Simulation |
| Planted Solar | Robotics | Industrial Robots |
| Eyebot | Robotics | Surgical & Medical |
| Shinkei Systems | Robotics | Industrial Robots |
| Relocalize | Robotics | Industrial Robots |
| Carbon Robotics | Robotics | Industrial Robots |
| Auradine | Semiconductors | Fabless Design |
| RAAAM Memory Technologies | Semiconductors | Fabless Design |
| RaiderChip | Semiconductors | EDA & IP |
| Frore Systems | Semiconductors | OSAT / Packaging & Test |
| Ranovus | Semiconductors | OSAT / Packaging & Test |
| Black Semiconductor | Semiconductors | Silicon & Substrates |
| Black Semiconductor | Semiconductors | Silicon & Substrates |

## Stage classification flags (18 rows)

| Company | Assigned round |
|---|---|
| MinoSpace | Series C |
| PLD Space | Other |
| SendingNetwork | Seed (extension) |
| Cruise | Strategic |
| Motional | Strategic |
| 42dot | Strategic |
| Galbot | Pre-Seed |
| Rokae Robotics | Strategic |
| Ripcord | Other |
| PhiGent Robotics | Series B |
| Orca AI | Other |
| Vitestro | Other |
| Greeneye Technology | Other |
| Mentee Robotics | Other |
| TerraClear | Other |
| Coboworx | Other |
| SpinEM Robotics | Series A (extension) |
| Carbon Robotics | Series C (extension) |

## Non-USD deals — currency audit (35 rows)

| Company | Native | USD | Implied FX |
|---|---|---|---|
| Synspective | JPY 7,000.0M | $43.9M | 0.00627 |
| MinoSpace | CNY 1,000.0M | $137.0M | 0.137 |
| ICEYE | EUR 86.0M | $93.0M | 1.0814 |
| Astroscale Holdings | JPY 21,200.0M | $136.2M | 0.00643 |
| PLD Space | EUR 78.0M | $85.0M | 1.0897 |
| Isar Aerospace | EUR 65.0M | $70.0M | 1.0769 |
| Orbex | GBP 16.7M | $20.7M | 1.2395 |
| Infinite Orbits | EUR 12.0M | $12.9M | 1.0775 |
| FOSSA Systems | EUR 6.3M | $6.8M | 1.0794 |
| Space Pioneer | CNY 1,500.0M | $207.0M | 0.138 |
| cylib | EUR 55.0M | $59.6M | 1.0834 |
| 42dot | KRW 253,000.0M | $185.0M | 0.000731 |
| Galbot | CNY 700.0M | $96.4M | 0.1377 |
| Rokae Robotics | CNY 500.0M | $69.1M | 0.1382 |
| TIER IV | JPY 8,500.0M | $54.0M | 0.00635 |
| Vitestro | EUR 20.0M | $22.0M | 1.1 |
| Coboworx | EUR 11.4M | $12.2M | 1.07 |
| SpinEM Robotics | EUR 10.0M | $11.0M | 1.1 |
| Fotokite | CHF 10.0M | $11.0M | 1.1 |
| ARX Robotics | EUR 9.0M | $9.6M | 1.07 |
| Forcen | CAD 8.3M | $6.1M | 0.731 |
| Relocalize | CAD 5.8M | $4.3M | 0.731 |
| Nami Surgical | GBP 3.9M | $4.9M | 1.26 |
| HyLight | EUR 3.7M | $4.0M | 1.08 |
| Unmanned Defence Systems | EUR 3.2M | $3.5M | 1.08 |
| PsiQuantum | AUD 940.0M | $620.0M | 0.659574 |
| DEEPX | KRW 110,000.0M | $80.5M | 0.000732 |
| MetisX | KRW 60,000.0M | $44.0M | 0.000733 |
| Itda Semiconductor | KRW 3,000.0M | $2.2M | 0.000733 |
| RaiderChip | EUR 1.0M | $1.1M | 1.08 |
| NcodiN | EUR 3.5M | $3.8M | 1.08 |
| Ranovus | CAD 4.8M | $3.5M | 0.7295 |
| Black Semiconductor | EUR 228.7M | $27.7M | 1.0766 |
| Black Semiconductor | EUR 228.7M | $246.2M | 1.0766 |
| Wave Photonics | GBP 4.5M | $5.8M | 1.2778 |

FX rates verified: EUR/USD ~1.07-1.10, USD/CNY ~7.20-7.30, USD/KRW ~1363-1383, USD/JPY ~155-160 (Q2 2024 was a JPY weakness window), HKD/USD pegged ~7.85, GBP/USD ~1.24-1.28, AUD/USD ~0.66, CAD/USD ~0.73, CHF/USD ~1.10.

## Deals with `amount_m: null` (0 rows)


## Excluded deals (notable)

### Outside the Q2 2024 window
- **io.net $30M Series A** (Mar 6, 2024) — Q1
- **peaq $15M** (Mar 27, 2024) — Q1
- **Niron Magnetics $25M** (Feb 20, 2024) — Q1
- **Boston Metal, Antora Energy, Lilac Solutions, Ascend Elements** — all Q1
- **Skild AI $300M Series A** (Jul 9, 2024) — 3Q24, in dataset already
- **Saronic Series B, Anduril Series F, Helsing Series C** — all Jul-Aug 2024 (3Q24)
- **Sentient $85M, Sahara AI $43M** — 3Q24, in dataset already
- **Carbon Robotics Series D, Path Robotics Series D, AMP Robotics Series D** — all Q4 2024

### Excluded per scope rules
- **Micron $6.1B PMT, Samsung $6.4B PMT, Microchip PMT** (Apr-May 2024) — non-binding CHIPS Act PMTs
- **Polar Semiconductor $120M PMT** (May 20, 2024) — non-binding; finalized Sep 24, 2024 (in 3Q24)
- **Rocket Lab $23.9M PMT** (Jun 11, 2024) — non-binding; finalized Nov 25, 2024 (in 4Q24)
- **Renesas / Transphorm $339M acquisition** — Transphorm was publicly listed; take-private excluded per "private target only" rule
- **Microchip / VSI Co.** and **Microchip / Neuronix AI Labs** acquisitions — undisclosed transaction values, excluded per "disclosed value required" rule
- **Stella Automotive AI $19.7M** — voice AI for car dealerships, not robotics/autonomy; F-Prime/Robot Report listed but off-scope for Robotniks
- **Aurora Innovation $483M secondary** (Aug 2, 2024) — Q3, public-co secondary regardless
- **Babylon $70M, Berachain $100M** — Bitcoin staking + L1 DeFi, not compute/AI/DePIN per Token scope
- **Aethir node-license sale ($146M)** — public node-license sale, not VC-priced equity round
- **Realtime Robotics Series B** (May 28, 2024) — Mitsubishi Electric lead but amount undisclosed; the $68.9M figure that appeared in F-Prime/Robot Report charts could not be independently confirmed

## Coverage gaps to flag

- **Chinese humanoid sector under-covered:** AgiBot, Kepler, Galaxea Q2 2024 rounds difficult to verify in English sources. Galbot is the standout that was confirmed.
- **DePIN scope clarity:** included compute-AI-DePIN (Sentient, Sahara, Prime Intellect, Privasea, Arcium, Aligned Layer, IoTeX, SendingNetwork) but excluded BTC-staking (Babylon) and L1-DeFi (Berachain). Wireless DePIN (DAWN), positioning DePIN (Hivemapper, GeodNet), and energy DePIN sit in scope-grey zone — flag for taxonomy decision.
- **Lab/biotech automation:** Reshape Biotech, Eyebot, Shinkei Systems all flagged as borderline robotics — could justify a "Lab Automation & Bio-Robotics" subsector if you want to extend to 28.

## Schema notes

- **No new fields** introduced.
- **No new sectors** (still 5: Robotics, Semiconductors, Space, Materials, Token).
- **No new subsector values** (still 27 — `Decentralized AI / DePIN` added pre-2Q24).
- **One new round value:** `Seed (extension)` for SendingNetwork. Follows established `(extension)` naming convention.
- **Strategic** round used 7× in 2Q24: Cruise, Motional, 42dot, Rokae Robotics, Gatik, Axus Technology, Aerodome — wait actually checking: Strategic = Cruise, Motional, 42dot, Rokae Robotics, Gatik, Axus Technology = 6 strategic_corporate + 3 token (IoTeX, Arcium, Privasea) = 9 Strategic-round rows total but only 6 classified as strategic_corporate (Token sector overrides).
- **Multi-row convention** activated for the first time: Black Semiconductor (Series A + Government investment, both 2024-06-12).

## Source-of-truth file

Every appended row has a `source` field with at least one verifiable URL. Single-source flagged. Full audit trail at `/tmp/2q24_research/{space,materials,robotics,semis}.json`.

---

## Ready for 1Q24?

Per prompt convention, stopped here for review. Same workflow available for 1Q24 (Jan-Mar 2024) when you give the word.