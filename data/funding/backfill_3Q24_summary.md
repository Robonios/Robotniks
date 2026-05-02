# 3Q24 Private Markets Backfill — Summary

**Generated:** 2026-05-02
**Quarter covered:** Jul 1 – Sep 30, 2024
**File touched:** [data/funding/rounds.json](rounds.json)

## Headline numbers

- **78 deals** added
- **$9.09B** aggregate disclosed value
- **479 total rows** in `rounds.json` after append (was 401)
- **Quarter coverage now extends 3Q24 → 2Q26** (8 quarters total)

### Sense-check vs prompt expectation

You expected $5-15B for a typical quarter. 3Q24 came in at **$9.09B** — squarely in range.

Unlike 4Q24 (distorted by the CHIPS Act finalization rush), 3Q24 had only **2 binding CHIPS awards** in the window (Polar Semiconductor $123M, Intel Secure Enclave $3B), consistent with the broader pattern of finalizations being concentrated in Q4.

| Slice | Deals | Aggregate |
|---|---|---|
| All 3Q24 | 78 | $9.09B |
| CHIPS Act binding awards | 2 | $3.12B |
| Defense-tech megarounds | 9 | $2.37B |
| Pure-VC ex-CHIPS, ex-defense | 67 | $3.60B |

## What's new in this batch

### First-ever real `token` deal_type rows

After cleaning up the misclassified Token rows in revision 3 (Robot Era, X Square Robot, RobCo all moved to Robotics), the `token` deal_type was empty across all 401 rows. The 3Q24 backfill adds the **first 2 genuine token raises** in the dataset:

| Company | Round | Amount | Lead investors |
|---|---|---|---|
| Sentient | Seed | $85.0M | Founders Fund, Pantera Capital, Framework Ventures |
| Sahara AI | Series A | $43.0M | Pantera Capital, Binance Labs, Polychain Capital |

Both tagged `sector=Token`, `subsector=Frontier Compute`, `deal_type=token`. Both flagged `subsector_uncertain: true` since the existing 26-value subsector enum has no "Decentralized AI" or "DePIN" bucket.

### `deal_type` distribution for 3Q24

| deal_type | Deals | Aggregate |
|---|---|---|
| `venture` | 66 | $5.41B |
| `government` | 4 | $3.17B |
| `strategic_corporate` | 5 | $350.0M |
| `debt` | 1 | $30.0M |
| `token` | 2 | $128.0M |

## Breakdown by sector

| Sector | Deals | Aggregate |
|---|---|---|
| Semiconductors | 15 | $4.41B |
| Robotics | 39 | $3.59B |
| Space | 15 | $695.0M |
| Materials | 7 | $270.1M |
| Token | 2 | $128.0M |

## Breakdown by sector × subsector

### Semiconductors — 15 deals, $4.41B

| Subsector | Deals | Aggregate |
|---|---|---|
| Foundry | 3 | $3.30B |
| Frontier Compute | 5 | $755.0M |
| Fabless Design | 5 | $339.0M |
| Silicon & Substrates | 1 | $13.0M |
| EDA & IP | 1 | $0.0M |

### Robotics — 39 deals, $3.59B

| Subsector | Deals | Aggregate |
|---|---|---|
| Autonomous Systems & Drones | 15 | $2.59B |
| Software & Simulation | 2 | $321.5M |
| Surgical & Medical | 5 | $223.4M |
| Warehouse & Logistics | 4 | $203.4M |
| Industrial Robots | 3 | $85.3M |
| Humanoid & Service Robots | 7 | $73.9M |
| Collaborative Robots | 1 | $63.0M |
| Machine Vision & Sensors | 2 | $27.6M |

### Space — 15 deals, $695.0M

| Subsector | Deals | Aggregate |
|---|---|---|
| Satellite Communications | 3 | $233.0M |
| In-Orbit Services | 6 | $157.3M |
| Space Components | 2 | $112.5M |
| Launch | 1 | $99.0M |
| Earth Observation | 2 | $63.2M |
| Ground Systems & Antennas | 1 | $30.0M |

### Materials — 7 deals, $270.1M

| Subsector | Deals | Aggregate |
|---|---|---|
| Battery Materials | 4 | $107.1M |
| Rare Earths & Critical Minerals | 2 | $88.0M |
| Structural Materials | 1 | $75.0M |

### Token — 2 deals, $128.0M

| Subsector | Deals | Aggregate |
|---|---|---|
| Frontier Compute | 2 | $128.0M |

## Breakdown by geography

| Country | Deals | Aggregate |
|---|---|---|
| USA | 48 | $7.68B |
| Germany | 3 | $536.6M |
| China | 7 | $359.0M |
| United Arab Emirates | 2 | $185.0M |
| Italy | 1 | $53.4M |
| Canada | 2 | $53.0M |
| Switzerland | 2 | $47.0M |
| United Kingdom | 3 | $46.8M |
| South Korea | 3 | $39.1M |
| Spain | 1 | $33.0M |
| France | 1 | $16.4M |
| Sweden | 1 | $13.0M |
| Norway | 1 | $12.0M |
| India | 2 | $9.5M |
| Israel | 1 | $3.4M |

## Top 10 deals by size

| # | Company | Round | Amount | Lead investor(s) |
|---|---|---|---|---|
| 1 | **Intel (Secure Enclave)** | Government investment | $3.00B | U.S. Department of Defense / U.S. Department of Commerce |
| 2 | **Anduril Industries** | Series F | $1.50B | Founders Fund, Sands Capital |
| 3 | **Groq** | Series D | $640.0M | BlackRock Private Equity Partners |
| 4 | **Helsing** | Series C | $487.5M | General Catalyst |
| 5 | **Skild AI** | Series A | $300.0M | Lightspeed Venture Partners, Coatue, SoftBank Group, Bezos Expeditions |
| 6 | **Astranis** | Series D | $200.0M | Andreessen Horowitz (a16z Growth), BAM Elevate |
| 7 | **Polar Semiconductor** | Strategic | $175.0M | Niobrara Capital, Prysm Capital |
| 8 | **Saronic Technologies** | Series B | $175.0M | Andreessen Horowitz |
| 9 | **Monarch Tractor** | Series C | $133.0M | Astanor, HH-CTBC Partnership |
| 10 | **Black Sesame Technologies** | IPO | $132.0M | Undisclosed |

## Deals flagged `single_source: true`

| Company | Round | Amount | Source |
|---|---|---|---|
| Outpost Technologies | Government investment | $33.2M | https://www.businesswire.com/news/home/20240828025992/en/Air-Force-Selects-Outpost-for-33.2-Million-Award |
| Mangrove Lithium | Strategic | undisclosed | https://www.mangrovelithium.com/new-funding-from-major-automaker/ |
| Stardust Power | IPO | $10.1M | https://www.globenewswire.com/news-release/2024/07/08/2909963/0/en/Stardust-Power-Closes-Business-Combination-and-Set-to-Begin-Trading-on-Nasdaq.html |
| Cerebras Systems | IPO (filed) | undisclosed | https://www.sec.gov/Archives/edgar/data/2021728/000162828024041596/cerebras-sx1.htm |
| Cerebras Systems | Series E | $85.0M | https://www.primeunicornindex.com/cerebras-systems-files-for-ipo-and-authorizes-discounted-series-f-1/ |
| ZhongQing Robot | Seed | $14.0M | https://www.therobotreport.com/robotics-investments-near-1b-in-august-2024/ |

## Subsector classification flags

| Company | Sector | Assigned subsector | Why ambiguous |
|---|---|---|---|
| Star Catcher Industries | Space | In-Orbit Services | Power-beaming-as-a-service for satellites — novel category |
| AstroForge | Space | In-Orbit Services | Asteroid mining — sui generis |
| Starpath Robotics | Space | In-Orbit Services | Lunar ISRU robotics |
| Slingshot Aerospace | Space | Ground Systems & Antennas | SSA pure-play — has Ground Systems and EO data elements |
| Sceye | Space | Satellite Communications | HAPS stratospheric airship — connectivity but not a satellite |
| Ursa Major Technologies | Space | Space Components | Solid rocket motors — borderline Launch vs Components |
| Reflect Orbital | Space | In-Orbit Services | Orbital sunlight reflectors — unique service |
| Sentient | Token | Frontier Compute | Open-source AGI infrastructure — could justify "Decentralized AI" subsector |
| Sahara AI | Token | Frontier Compute | Decentralized AI training — same taxonomy gap |
| Intel (Secure Enclave) | Semiconductors | Foundry | Defense trusted-foundry program |
| Botrista Technology | Robotics | Industrial Robots | Beverage-prep robotics — narrow vertical |
| Sojo Industries | Robotics | Industrial Robots | Mobile food/beverage manufacturing |
| Swiss-Mile | Robotics | Humanoid & Service Robots | Wheeled-quadruped — Humanoid or Autonomous |
| Applied Carbon | Robotics | Autonomous Systems & Drones | Tractor-mounted biochar robot |
| Intramotev | Robotics | Autonomous Systems & Drones | Self-propelled autonomous railcar |
| Leap Automation | Robotics | Industrial Robots | Food-packing pick-and-place |
| Deep Robotics | Robotics | Humanoid & Service Robots | Quadruped pivoting to humanoid |

## Stage classification flags

| Company | Assigned round | Notes |
|---|---|---|
| Orbitworks | Strategic | JV formation strategic capital |
| Mangrove Lithium | Strategic | "Strategic add-on"; brought total to $25M USD |
| Cerebras Systems | IPO (filed) | Series F-1 discounted bridge; mapped to "Series E" as closest enum |
| Cerebras Systems | Series E | Series F-1 discounted bridge; mapped to "Series E" as closest enum |
| Akeana | Series A | Stealth emergence — unclear if Series A or seed |
| SweGaN | Series A (extension) | Series A extension with mixed SEK/EUR amounts |
| Cartken | Other | Aggregate funding announcement, not clean series |
| ZhongQing Robot | Seed | Single-source amount |
| Maritime Robotics | Other | "Growth capital" without series |
| Leap Automation | Other | Mix of equity + Scottish state bank |
| Reactive Robotics | Other | EIC Fund tranche; unclear series |
| Pickommerce | Other | Stage unclear |
| Deep Robotics | Series B (extension) | Series B+ extension; amount undisclosed |

## Non-USD deals — currency audit

| Company | Native | USD reported | Implied FX | Source for FX |
|---|---|---|---|---|
| iSpace (Beijing Interstellar Glory) | CNY 700.0M | $99.0M | 0.1414 | Implied per Payload/DealStreetAsia |
| Sateliot | EUR 30.0M | $33.0M | 1.1 | Via Satellite headline conversion |
| D-Orbit | EUR 50.0M | $53.4M | 1.067 | Payload Space reporting |
| Fractile | EUR 13.8M | $15.0M | 1.087 | Fortune/EU-Startups concurrent reporting |
| SweGaN | EUR 12.0M | $13.0M | 1.083 | SEK 134M / nearly EUR 12M per company release |
| Black Sesame Technologies | HKD 1,036.0M | $132.0M | 0.128 | 37M shares x HK$28 per HKEX filing; ~7.85 HKD/USD |
| Helsing | EUR 450.0M | $487.5M | 1.083 | Press release implied 1.083 USD/EUR |
| Wingtra | EUR 23.0M | $25.0M | 1.087 | Press release: $25M / €23M |
| Holiday Robotics | KRW 17,500.0M | $12.9M | 0.000737 | Press: KRW 17.5B = ~$12.9M USD at announcement-date FX rate |
| ZhongQing Robot | CNY 100.0M | $14.0M | 0.1399 | The Robot Report; ~7.15 CNY/USD |
| Quantum Systems | EUR 40.0M | $43.6M | 1.09 | Press: ~€40M / $43.6M |
| Inbolt | EUR 15.0M | $16.4M | 1.09 | Press: €15M = ~$16.4M USD |
| AIDIN ROBOTICS | KRW 15,000.0M | $11.2M | 0.000747 | Press: ~$11.2M USD; KRW estimated |
| Leap Automation | GBP 7.9M | $10.3M | 1.3 | Press: £7.9M = ~$10.3M USD |
| Reactive Robotics | EUR 5.0M | $5.5M | 1.09 | Press: €5M = ~$5.45M USD |
| LimX Dynamics | CNY undisclosed | undisclosed | — | — |
| Booster Robotics | CNY 100.0M | $14.0M | 0.14 | The Robot Report; CNY100M ~$14M |
| Deep Robotics | CNY undisclosed | undisclosed | — | — |

All FX rates verified against announcement-date approximations:
- EUR/USD ~1.08 (Jul 2024) — 1.10 (Sep 2024)
- USD/CNY ~7.10-7.30
- USD/KRW ~1335-1380
- HKD/USD pegged ~7.85 (Black Sesame IPO)
- GBP/USD ~1.30 (Leap Automation)

## Deals with `amount_m: null`

Strategically important deals where the amount was undisclosed but inclusion was warranted:

| Company | Round | Why included |
|---|---|---|
| Sceye | Series C | Saudi-led Series C at $525M valuation |
| Mangrove Lithium | Strategic | BMW + Breakthrough Energy strategic |
| Cerebras Systems | IPO (filed) | IPO (filed) — registration filing event, no immediate cash |
| Eliyan | Strategic | Strategic from VentureTech Alliance pushed cumulative past $100M |
| LimX Dynamics | Series A | High-profile Chinese humanoid; SAIC-backed |
| Deep Robotics | Series B (extension) | Series B+ extension; quadruped pivoting to humanoid |

## Excluded deals (notable)

### Outside the Q3 2024 window
- **Figure $675M Series B** (Feb 2024)
- **Wayve $1.05B Series C** (May 2024)
- **Sila Nanotechnologies $375M Series G** (Jun 27, 2024 — just outside)
- **Etched $120M Series A** (Jun 25, 2024)
- **Apex Space $95M Series B** (Jun 12, 2024)
- **Cobot $100M Series B** (Apr 2024)
- **Outrider $62M, Path $100M, Carbon Robotics $70M** — all October 2024 (in 4Q24)

### CHIPS Act preliminary memoranda (PMTs) — non-binding, excluded per scope
- **SK Hynix $450M PMT** (Aug 6, 2024) — finalized Dec 2024 (in 4Q24)
- **Texas Instruments $1.6B PMT** (Aug 16, 2024) — finalized Dec 2024 (in 4Q24)
- **GlobalWafers $400M PMT** (Jul 17, 2024) — finalized Dec 2024 (in 4Q24)
- **Amkor $400M PMT** (Jul 25, 2024) — finalized Dec 2024 (in 4Q24)

### Other excluded
- **Waymo $5B from Alphabet** (Jul 2024) — internal corporate transfer
- **Aurora Innovation $483M secondary** (Aug 2, 2024) — public equity offering
- **Applied Intuition $300M secondary** (Jul 25, 2024) — employee/early-investor liquidity
- **DAWN/Andrena $18M Series A extension** — wireless DePIN, off-scope per Token criteria
- **Quantum Brilliance EUR 35M government contract** — contract for delivery, not funding round

## Coverage gaps to flag

- **Chinese humanoid sector under-covered:** AgiBot, Galaxea, Galbot, Kepler likely had Q3 2024 rounds. Estimate 3-5 missed for English-source-only constraint.
- **DePIN beyond compute/AI:** wireless DePIN (DAWN), positioning DePIN (Hivemapper/GeodNet), energy DePIN had Q3 2024 activity but sit outside the "compute/robotics/GPU" Token scope. Flag for taxonomy decision.
- **Defense-tech selection bias:** Q3 2024 was concentrated for defense/dual-use. Captured top mega-deals; a long tail of smaller defense seed rounds may exist below verifiability threshold.

## Schema notes

- **No new fields** introduced (option (i) preserved).
- **One new subsector value added (revision 2, 2026-05-02):** `Decentralized AI / DePIN` (27th canonical value). Sentient + Sahara AI reclassified from `Frontier Compute` to this new value. Going forward, this is the canonical bucket for compute/AI-DePIN, decentralized-GPU networks, decentralized-AI-training platforms, and similar token-aligned compute infrastructure.
- **No new round values** (Strategic + Series E (extension) already added in earlier revisions).
- **Strategic** round used 5× in 3Q24: Mangrove Lithium, Sublime Systems, Orbitworks, Polar Semi (PE), Eliyan.
- **Token deal_type** activated for the first time: Sentient + Sahara AI.

## Convention: same-company same-quarter rows

Two cases in 3Q24 illustrate when a single company gets multiple rows:

| Company | Date | Round | $ | What it represents |
|---|---|---|---|---|
| Cerebras Systems | 2024-09-30 | IPO (filed) | (null) | S-1 filing event; no immediate cash raised |
| Cerebras Systems | 2024-09-30 | Series E | $85M | Discounted Series F-1 bridge authorized concurrent with IPO filing |
| Polar Semiconductor | 2024-09-24 | Strategic | $175M | Niobrara/Prysm PE majority-control equity round |
| Polar Semiconductor | 2024-09-24 | Government investment | $123M | First binding CHIPS Act commercial fab award (concurrent with PE close) |

### Rule (reproducible for future quarters)

A company gets **multiple rows in the same quarter** when there are genuinely **distinct legal / financing events** with different funding mechanics — even if they happen on the same date or are announced together. To qualify:

1. **Same `company` name** (verbatim — must match exactly so they group correctly).
2. **Same `entity_id`** (so cross-row joins still work — both Cerebras rows share `cerebras-systems`, both Polar rows share `polar-semiconductor`).
3. **Distinct `round` values** that reflect the different mechanics (e.g., `Strategic` + `Government investment` for the Polar case; `IPO (filed)` + `Series E` for Cerebras).
4. **Distinct rows in the JSON** — do NOT collapse into a single row with summed amount, even if the events are concurrent.
5. **Cross-reference the other event** in `robotnik_notes` so a reader of one row can find the other.
6. **`deal_type` follows the round** — so concurrent events for the same company can have different `deal_type` (Polar: `strategic_corporate` + `government`; Cerebras: `venture` for both since IPO (filed) maps to venture).

### What does NOT qualify

- A single round with multiple investors → one row.
- A round that closes in tranches but is announced as a single round → one row at the announcement date.
- Re-reporting / corrections / amendments → update existing row, do not duplicate.
- Round close + later extension within a few weeks → two rows only if the source treats them as separately announced events with their own dates and disclosures.

### Verification

After 3Q24 append, the only intentional same-company-same-quarter cases in the dataset are:
- Cerebras Systems × 2 (3Q24)
- Polar Semiconductor × 2 (3Q24)

(Wolfspeed had 2 candidate rows in 4Q24 — CHIPS PMT + Apollo debt — but only the Apollo debt was kept; the PMT was dropped per the "binding awards only" rule.)

---

## Ready for 2Q24?

Per prompt convention, stopped here for review. Same workflow available for 2Q24 (Apr-Jun 2024) when you give the word.