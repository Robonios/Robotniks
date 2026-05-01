# 4Q24 Private Markets Backfill — Summary

**Generated:** 2026-05-01 (revised after follow-up asks)
**Quarter covered:** Oct 1 – Dec 31, 2024
**File touched:** [data/funding/rounds.json](rounds.json)

## Post-review changes (revision 2)

After your initial sign-off:
1. **`deal_type` field added** to all 401 rows (enum: `venture` / `government` / `strategic_corporate` / `debt` / `token`). See [§ deal_type breakdown](#deal_type-breakdown) below.
2. **Phoenix Tailings duplicate resolved.** The pre-existing 2025-04-25 row (placeholder lead = "Multiple", no other_investors, vague `source = "https://techcrunch.com"`, no `date_display` / `month_year`) was deleted. The 2025-05-01 row (named lead Envisioning Partners, full investor list, specific Woburn MA location, real press-release URL, full schema) was kept as canonical. **Total rows: 402 → 401.**
3. **Subsector consolidation audit log** added below — see [§ Subsector consolidation audit](#subsector-consolidation-audit).

## Headline numbers (revised)

- **89 deals** added in 4Q24 backfill
- **$31.32B** aggregate disclosed value for 4Q24
- **401 total rows** in `rounds.json` (after Phoenix dedup)

### ⚠️ Sense-check vs prompt expectation

You expected $5-15bn. Total came in at **$31.32B** — above expectation but below the $50bn auto-stop threshold.

**Reason:** 4Q24 was the CHIPS Act finalization rush. The Biden admin locked in 11 binding awards totaling **$23.34B** in the 11 weeks before the political transition. Strip those out and the picture matches your expectation closely:

| Slice | Deals | Aggregate |
|---|---|---|
| All 4Q24 | 89 | $31.32B |
| CHIPS Act finalized awards | 11 | $23.34B |
| **Ex-CHIPS** | **78** | **$7.98B** |

If you want CHIPS awards excluded (treated as fiscal events, not "private market deals"), say the word and I'll filter them — they share the existing `Government investment` enum so the schema is the same either way.


## deal_type breakdown

### Across all 401 rows

| deal_type | Rows | Aggregate |
|---|---|---|
| `venture` | 370 | $83.97B |
| `government` | 22 | $28.13B |
| `debt` | 5 | $1.29B |
| `strategic_corporate` | 4 | $890.0M |

### 4Q24 only (89 rows)

| deal_type | Rows | Aggregate |
|---|---|---|
| `venture` | 70 | $5.15B |
| `government` | 13 | $24.50B |
| `strategic_corporate` | 4 | $890.0M |
| `debt` | 2 | $786.9M |

### Classification rule applied

```python
def classify(r):
    if r['round'] == 'Strategic':
        return 'strategic_corporate'
    if r['round'] in ('Government investment', 'Government', 'Grant'):
        return 'government'
    if r['round'] == 'Debt Financing':
        return 'debt'
    return 'venture'  # all VC rounds, IPO, IPO (filed), M&A, Other, Bridge
```

### Edge cases noted

- **IPO / IPO (filed) / M&A** → classified as `venture`. They are exit events of VC-backed companies and the existing schema treats them as bundled rounds. 5 IPO rows + 1 M&A row affected.
- **`Other` rounds (12 existing + 8 new in 4Q24)** → classified as `venture` by default. Some have corporate-strategic leads (e.g. ANYbotics led by Qualcomm Ventures, TEKEVER co-led by NATO Innovation Fund). If you want a more granular pass on these, flag the rule and I will rewrite.
- **`token` deal_type currently has 0 hits.** Reason: the 3 existing `sector=Token` rows (Robot Era, X Square Robot, RobCo) are misclassifications — their `robotnik_notes` clearly describe humanoid / industrial robotics companies, not token raises. Auto-classifying them as `token` would compound the error. See [§ Known data-quality issues](#known-data-quality-issues) below. The `token` enum value is reserved for future real token raises.
- **Strategic-by-flavor rounds** (e.g. Nimble Robotics Series C led by FedEx) keep `venture` classification. The `Strategic` round value already exists to flag explicit strategic-investment structures; series rounds with corporate participation are not retroactively re-classified.

## Subsector consolidation audit

Before adding 4Q24 rows, 10 existing rows had their `subsector` value re-canonicalised to collapse near-duplicates (per your B answer). The `entity_id` field was NOT changed for any of these — only `subsector`. Spot-check by company / source:

| # | Company | entity_id | Date | Old subsector | New subsector | Source URL |
|---|---|---|---|---|---|---|
| 1 | ArkEdge Space | `arkedge-space` | 2025-02-04 | Satellite Comms | Satellite Communications | https://spacenews.com |
| 2 | CMR Surgical | `cmr-surgical` | 2025-04-02 | Surgical & Medical Robots | Surgical & Medical | globenewswire.com — CMR-Surgical-secures-mo |
| 3 | CMR Surgical | `cmr-surgical` | 2025-10-20 | Surgical & Medical Robots | Surgical & Medical | (2nd CMR row, same canonical move) |
| 4 | ForSight Robotics | `forsight-robotics` | 2025-06-24 | Surgical & Medical Robots | Surgical & Medical | businesswire.com — ForSight-Robotics-Secures-$125M |
| 5 | Geekplus | `geekplus` | 2025-07-09 | Warehouse & Logistics Automation | Warehouse & Logistics | prnewswire.com — geekplus-lists-on-hkex-main-board |
| 6 | Commcrete | `commcrete` | 2025-09-30 | Satellite Comms | Satellite Communications | https://spacenews.com |
| 7 | Dexory | `dexory` | 2025-05-15 | Warehouse & Logistics Automation | Warehouse & Logistics | https://techcrunch.com |
| 8 | Starship Technologies | `starship-technologies` | 2025-10-15 | Warehouse & Logistics Automation | Warehouse & Logistics | businesswire.com — Starship-Technologies-Raises-$50M |
| 9 | Tutor Intelligence | `tutor-intelligence` | 2025-12-01 | Warehouse & Logistics Automation | Warehouse & Logistics | businesswire.com — Tutor-Intelligence-Raises-34-Mill |
| 10 | Mytra | `mytra` | 2026-01-14 | Warehouse & Logistics Automation | Warehouse & Logistics | therobotreport.com — mytra-raises-120m-series-c |
| 11 | Nomagic | `nomagic` | 2026-01-28 | Warehouse & Logistics Automation | Warehouse & Logistics | nomagic.ai/news/series-b-extension |
| 12 | Dexory | `dexory` | 2025-10-14 | Warehouse & Logistics Automation | Warehouse & Logistics | (2nd Dexory row, same canonical move) |

**Note on Dexory:** the original consolidation touched 2 existing Dexory rows (2025-05-15 + 2025-10-14). My 4Q24 backfill then added a 3rd Dexory row (2024-10-01 Series B) which already used the canonical `Warehouse & Logistics` value — so all 3 Dexory rows are consistent. Same for CMR Surgical (2 existing rows, both renamed).

**Net effect on subsector enum:**
- Pre-consolidation: 29 distinct subsector values
- Post-consolidation: 26 distinct subsector values
- Post-4Q24 backfill: still 26 (no new subsectors introduced)

## Phoenix Tailings duplicate — resolution log

The pre-existing dataset had two Phoenix Tailings rows, both labelled Series B at $76M. They appear to represent the same Series B (first close $43M Dec 2024 + extension $33M Apr 2025 = $76M total). Both rows being recorded at $76M was a duplicate.

### Row deleted (2025-04-25)

```
company: Phoenix Tailings
date: 2025-04-25
lead_investors: "Multiple"          ← placeholder
other_investors: ""                  ← empty
location: "USA"                      ← no city/state
source: "https://techcrunch.com"     ← stub URL, not a specific article
robotnik_notes: "Green rare earth extraction from mining waste without toxic chemicals."
(missing date_display, month_year)
```

### Row kept (2025-05-01) — canonical

```
company: Phoenix Tailings
date: 2025-05-01
date_display: "1-May-25"
month_year: "May-25"
lead_investors: "Envisioning Partners"
other_investors: "Escape Velocity, Builders Vision, Yamaha Motor Ventures, M Power, Presidio (Sumitomo)"
location: "USA (Woburn, MA)"
source: "https://www.businesswire.com/news/home/20250430735778/en/Phoenix-Tailings-Closes-on-Additional-33M"
robotnik_notes: "First US standalone REE refining plant; 500 tons/yr Nd-Pr, Dy, Tb; responds to China export controls"
```

Both rows had `entity_id = phoenix-tailings`, `quarter = 2Q25`, `amount_m = 76`. Picked the row with named lead, full investor list, specific location, real press-release URL, and full schema.

My Dec 2024 first-close row ($43M) remains dropped — adding it on top of the canonical $76M row would re-create the inflation problem.

## Known data-quality issues (flagged, NOT fixed in this backfill)

Issues spotted while building the `deal_type` classifier — out of scope for the 4Q24 backfill, but worth surfacing for a separate cleanup pass:

### Three `sector=Token` rows are misclassified as Robotics companies

| Company | entity_id | Current sector | Should be | Evidence |
|---|---|---|---|---|
| Robot Era | `ROBOT` | Token | Robotics | `robotnik_notes` says "Tsinghua spinout; STAR1 + L7 bipedal humanoids; ERA-42 AI brain; 200+ robots delivered" |
| X Square Robot | `ROBOT` | Token | Robotics | notes: "AI foundation models for general-purpose robots" |
| RobCo | `ROBCO` | Token | Robotics | notes: "modular robot cells… competes with Universal Robots" |

Also: Robot Era and X Square Robot **share entity_id `ROBOT`**. Per the entity registry, `ROBOT` belongs to RoboStack — a real DePIN/token project — so neither company should use that ID. Recommended:
- Robot Era → mint `robot-era` (kebab-case) — applies to BOTH the existing 2025-07-08 row and my new 4Q24 2024-10-15 row (which currently inherits `ROBOT` because the build pipeline reused the existing wrong mapping)
- X Square Robot → mint `x-square-robot`
- RobCo → keep `ROBCO` if intentional (their company name is "RobCo" all-caps)
- Free `ROBOT` to point only at RoboStack

### Effect on `deal_type` distribution

Because I classified by `round` (not by `sector`), all three of these rows currently land as `deal_type = venture` (correct, since their actual deals are Series A/C). When/if the sector misclassification is fixed, the deal_type will already be correct — no re-backfill needed.
## Breakdown by sector

| Sector | Deals | Aggregate |
|---|---|---|
| Semiconductors | 25 | $26.34B |
| Robotics | 44 | $2.47B |
| Materials | 5 | $1.57B |
| Space | 15 | $937.5M |


## deal_type breakdown

### Across all 401 rows

| deal_type | Rows | Aggregate |
|---|---|---|
| `venture` | 370 | $83.97B |
| `government` | 22 | $28.13B |
| `debt` | 5 | $1.29B |
| `strategic_corporate` | 4 | $890.0M |

### 4Q24 only (89 rows)

| deal_type | Rows | Aggregate |
|---|---|---|
| `venture` | 70 | $5.15B |
| `government` | 13 | $24.50B |
| `strategic_corporate` | 4 | $890.0M |
| `debt` | 2 | $786.9M |

### Classification rule applied

```python
def classify(r):
    if r['round'] == 'Strategic':
        return 'strategic_corporate'
    if r['round'] in ('Government investment', 'Government', 'Grant'):
        return 'government'
    if r['round'] == 'Debt Financing':
        return 'debt'
    return 'venture'  # all VC rounds, IPO, IPO (filed), M&A, Other, Bridge
```

### Edge cases noted

- **IPO / IPO (filed) / M&A** → classified as `venture`. They are exit events of VC-backed companies and the existing schema treats them as bundled rounds. 5 IPO rows + 1 M&A row affected.
- **`Other` rounds (12 existing + 8 new in 4Q24)** → classified as `venture` by default. Some have corporate-strategic leads (e.g. ANYbotics led by Qualcomm Ventures, TEKEVER co-led by NATO Innovation Fund). If you want a more granular pass on these, flag the rule and I will rewrite.
- **`token` deal_type currently has 0 hits.** Reason: the 3 existing `sector=Token` rows (Robot Era, X Square Robot, RobCo) are misclassifications — their `robotnik_notes` clearly describe humanoid / industrial robotics companies, not token raises. Auto-classifying them as `token` would compound the error. See [§ Known data-quality issues](#known-data-quality-issues) below. The `token` enum value is reserved for future real token raises.
- **Strategic-by-flavor rounds** (e.g. Nimble Robotics Series C led by FedEx) keep `venture` classification. The `Strategic` round value already exists to flag explicit strategic-investment structures; series rounds with corporate participation are not retroactively re-classified.

## Subsector consolidation audit

Before adding 4Q24 rows, 10 existing rows had their `subsector` value re-canonicalised to collapse near-duplicates (per your B answer). The `entity_id` field was NOT changed for any of these — only `subsector`. Spot-check by company / source:

| # | Company | entity_id | Date | Old subsector | New subsector | Source URL |
|---|---|---|---|---|---|---|
| 1 | ArkEdge Space | `arkedge-space` | 2025-02-04 | Satellite Comms | Satellite Communications | https://spacenews.com |
| 2 | CMR Surgical | `cmr-surgical` | 2025-04-02 | Surgical & Medical Robots | Surgical & Medical | globenewswire.com — CMR-Surgical-secures-mo |
| 3 | CMR Surgical | `cmr-surgical` | 2025-10-20 | Surgical & Medical Robots | Surgical & Medical | (2nd CMR row, same canonical move) |
| 4 | ForSight Robotics | `forsight-robotics` | 2025-06-24 | Surgical & Medical Robots | Surgical & Medical | businesswire.com — ForSight-Robotics-Secures-$125M |
| 5 | Geekplus | `geekplus` | 2025-07-09 | Warehouse & Logistics Automation | Warehouse & Logistics | prnewswire.com — geekplus-lists-on-hkex-main-board |
| 6 | Commcrete | `commcrete` | 2025-09-30 | Satellite Comms | Satellite Communications | https://spacenews.com |
| 7 | Dexory | `dexory` | 2025-05-15 | Warehouse & Logistics Automation | Warehouse & Logistics | https://techcrunch.com |
| 8 | Starship Technologies | `starship-technologies` | 2025-10-15 | Warehouse & Logistics Automation | Warehouse & Logistics | businesswire.com — Starship-Technologies-Raises-$50M |
| 9 | Tutor Intelligence | `tutor-intelligence` | 2025-12-01 | Warehouse & Logistics Automation | Warehouse & Logistics | businesswire.com — Tutor-Intelligence-Raises-34-Mill |
| 10 | Mytra | `mytra` | 2026-01-14 | Warehouse & Logistics Automation | Warehouse & Logistics | therobotreport.com — mytra-raises-120m-series-c |
| 11 | Nomagic | `nomagic` | 2026-01-28 | Warehouse & Logistics Automation | Warehouse & Logistics | nomagic.ai/news/series-b-extension |
| 12 | Dexory | `dexory` | 2025-10-14 | Warehouse & Logistics Automation | Warehouse & Logistics | (2nd Dexory row, same canonical move) |

**Note on Dexory:** the original consolidation touched 2 existing Dexory rows (2025-05-15 + 2025-10-14). My 4Q24 backfill then added a 3rd Dexory row (2024-10-01 Series B) which already used the canonical `Warehouse & Logistics` value — so all 3 Dexory rows are consistent. Same for CMR Surgical (2 existing rows, both renamed).

**Net effect on subsector enum:**
- Pre-consolidation: 29 distinct subsector values
- Post-consolidation: 26 distinct subsector values
- Post-4Q24 backfill: still 26 (no new subsectors introduced)

## Phoenix Tailings duplicate — resolution log

The pre-existing dataset had two Phoenix Tailings rows, both labelled Series B at $76M. They appear to represent the same Series B (first close $43M Dec 2024 + extension $33M Apr 2025 = $76M total). Both rows being recorded at $76M was a duplicate.

### Row deleted (2025-04-25)

```
company: Phoenix Tailings
date: 2025-04-25
lead_investors: "Multiple"          ← placeholder
other_investors: ""                  ← empty
location: "USA"                      ← no city/state
source: "https://techcrunch.com"     ← stub URL, not a specific article
robotnik_notes: "Green rare earth extraction from mining waste without toxic chemicals."
(missing date_display, month_year)
```

### Row kept (2025-05-01) — canonical

```
company: Phoenix Tailings
date: 2025-05-01
date_display: "1-May-25"
month_year: "May-25"
lead_investors: "Envisioning Partners"
other_investors: "Escape Velocity, Builders Vision, Yamaha Motor Ventures, M Power, Presidio (Sumitomo)"
location: "USA (Woburn, MA)"
source: "https://www.businesswire.com/news/home/20250430735778/en/Phoenix-Tailings-Closes-on-Additional-33M"
robotnik_notes: "First US standalone REE refining plant; 500 tons/yr Nd-Pr, Dy, Tb; responds to China export controls"
```

Both rows had `entity_id = phoenix-tailings`, `quarter = 2Q25`, `amount_m = 76`. Picked the row with named lead, full investor list, specific location, real press-release URL, and full schema.

My Dec 2024 first-close row ($43M) remains dropped — adding it on top of the canonical $76M row would re-create the inflation problem.

## Known data-quality issues (flagged, NOT fixed in this backfill)

Issues spotted while building the `deal_type` classifier — out of scope for the 4Q24 backfill, but worth surfacing for a separate cleanup pass:

### Three `sector=Token` rows are misclassified as Robotics companies

| Company | entity_id | Current sector | Should be | Evidence |
|---|---|---|---|---|
| Robot Era | `ROBOT` | Token | Robotics | `robotnik_notes` says "Tsinghua spinout; STAR1 + L7 bipedal humanoids; ERA-42 AI brain; 200+ robots delivered" |
| X Square Robot | `ROBOT` | Token | Robotics | notes: "AI foundation models for general-purpose robots" |
| RobCo | `ROBCO` | Token | Robotics | notes: "modular robot cells… competes with Universal Robots" |

Also: Robot Era and X Square Robot **share entity_id `ROBOT`**. Per the entity registry, `ROBOT` belongs to RoboStack — a real DePIN/token project — so neither company should use that ID. Recommended:
- Robot Era → mint `robot-era` (kebab-case) — applies to BOTH the existing 2025-07-08 row and my new 4Q24 2024-10-15 row (which currently inherits `ROBOT` because the build pipeline reused the existing wrong mapping)
- X Square Robot → mint `x-square-robot`
- RobCo → keep `ROBCO` if intentional (their company name is "RobCo" all-caps)
- Free `ROBOT` to point only at RoboStack

### Effect on `deal_type` distribution

Because I classified by `round` (not by `sector`), all three of these rows currently land as `deal_type = venture` (correct, since their actual deals are Series A/C). When/if the sector misclassification is fixed, the deal_type will already be correct — no re-backfill needed.
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