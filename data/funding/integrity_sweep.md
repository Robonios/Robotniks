# Robotnik Funding Dataset — Integrity Sweep

**Generated:** 2026-05-03
**Coverage:** 676 rows, 1Q24 → 2Q26 (10 quarters)
**Mode:** Read-only audit. No mutations applied.

## TL;DR

| Section | Status | Findings |
|---|---|---|
| 1. deal_type classifier drift | ✅ clean | 0 rows differ from current rule |
| 2. Token sector audit | ✅ clean | 13/13 rows are legitimate DePIN/AI projects |
| 3. entity_id collisions | ⚠️ 4 issues | 2 exact collisions + 2 near-collisions |
| 4. subsector_uncertain flags | ⚠️ informational | 55 rows flagged by agents (not persisted to schema) |
| 5. Companies in 3+ rows | ✅ all sensible | 14 companies with 3-4 rows; all show round progression |
| 6. Schema consistency | ⚠️ 15 rows | Missing `date_display` + `month_year` (all in original 1Q25-2Q26 data) |
| 7. Location anomalies | ⚠️ 2 issues | UK/United Kingdom inconsistency (29 rows); 2 empty locations |
| 8. Aggregate sanity | ⚠️ 2 outliers | 1Q25 venture-deal count is low; 1Q26 venture aggregate spike |

---

## Section 1 — `deal_type` classifier drift

Re-ran the canonical classifier across all 676 rows:

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

**Result: 0 drift.** Every stored `deal_type` matches what the classifier would assign now. The 2Q24 fix (sector=Token wins) propagated cleanly to all earlier rows.

---

## Section 2 — Token sector audit

All 13 `sector=Token` rows verified as genuine token / DePIN / decentralized-AI projects:

| idx | Company | Date | Subsector | Round | dt |
|---|---|---|---|---|---|
| 423 | Sentient | 2024-07-02 | Decentralized AI / DePIN | Seed | `token` |
| 424 | Sahara AI | 2024-08-14 | Decentralized AI / DePIN | Series A | `token` |
| 500 | IoTeX | 2024-04-02 | Decentralized AI / DePIN | Strategic | `token` |
| 501 | Aligned Layer | 2024-04-25 | Decentralized AI / DePIN | Series A | `token` |
| 502 | Arcium | 2024-05-09 | Decentralized AI / DePIN | Strategic | `token` |
| 503 | Prime Intellect | 2024-04-23 | Decentralized AI / DePIN | Seed | `token` |
| 504 | SendingNetwork | 2024-04-16 | Decentralized AI / DePIN | Seed (extension) | `token` |
| 505 | Privasea | 2024-04-03 | Decentralized AI / DePIN | Strategic | `token` |
| 600 | io.net | 2024-03-05 | Decentralized AI / DePIN | Series A | `token` |
| 601 | peaq | 2024-03-27 | Decentralized AI / DePIN | Pre-Series A | `token` |
| 602 | GEODNET | 2024-02-29 | Decentralized AI / DePIN | Seed | `token` |
| 603 | 0G Labs | 2024-03-26 | Decentralized AI / DePIN | Pre-Seed | `token` |
| 604 | DIMO | 2024-01-16 | Decentralized AI / DePIN | Series A | `token` |

**All 13 share `subsector=Decentralized AI / DePIN`** (the canonical taxonomy bucket). Robotnik notes consistently describe token mechanics, decentralized compute networks, or AI-DePIN protocols. Source URLs point to crypto-native press (CoinDesk, The Block, CoinTelegraph) or company press releases announcing token rounds.

No misclassified robotics/semis companies remaining (the Robot Era / X Square Robot / RobCo cleanup in revision 3 of 4Q24 caught all of those).

---

## Section 3 — entity_id collisions and near-collisions

### 3a. Exact collisions (same entity_id, different `company` value)

**2 cases.** Both legitimate but inconsistent.

#### `entity_id = neura-robotics` — same company, capitalization split

| idx | company | date | round | sector |
|---|---|---|---|---|
| 3 | NEURA Robotics | 2025-01-15 | Series B | Robotics |
| 270 | Neura Robotics | 2026-03-04 | Undisclosed | Robotics |

**Same company, different capitalization in `company` field.** Suggested canonical: `NEURA Robotics` (matches company's own brand convention). Mutation: rename idx=270 `Neura Robotics` → `NEURA Robotics`.

#### `entity_id = INTC` — distinct programs, same parent ticker

| idx | company | date | round | sector |
|---|---|---|---|---|
| 347 | Intel | 2024-11-26 | Government investment | Semiconductors |
| 433 | Intel (Secure Enclave) | 2024-09-16 | Government investment | Semiconductors |

**Different events for the same legal entity** — Intel's commercial CHIPS award (Nov 26, $7.86B) vs Intel's separate DoD-trusted-foundry Secure Enclave award (Sep 16, $3B). Both legitimately distinct.

Per the multi-row convention documented in 3Q24, "Same `company` name (verbatim)" is required for grouping. Two options:
- **Option A (preferred):** rename idx=433 `Intel (Secure Enclave)` → `Intel`, distinguish via `round`/`robotnik_notes` only. Same shape as the Polar Semiconductor multi-row case.
- **Option B:** assign distinct entity_ids (e.g., `INTC` for commercial, `intel-secure-enclave` for the DoD program). Breaks the "all Intel CHIPS history rolls up to one ticker" pattern.

Suggested: Option A.

### 3b. Near-collisions (different capitalization/format in entity_id)

**2 cases.** Silent join-breakers.

#### `robot-era` vs `robotera` — likely two different companies

| idx | entity_id | company | date | round |
|---|---|---|---|---|
| 371 | `robot-era` | Robot Era | 2024-10-15 | Pre-Series A |
| 86 | `robot-era` | Robot Era | 2025-07-08 | Series A |
| 186 | `robotera` | Robotera | 2025-11-25 | Series A |

Robot Era and Robotera are two different Chinese humanoid companies — Robot Era is the Tsinghua spinout (机器时代); Robotera is a separate startup (also called 星动纪元, RobotEra Co.). Verify by reading the [robotnik_notes](data/funding/rounds.json) for idx=186 — if it describes a different team/product, leave both as-is. If it's the same company, normalize to `robot-era`.

**Recommended:** verify the idx=186 source URL and notes against the idx=86/371 rows before mutating.

#### `deep-robotics` vs `deeprobotics` — same company, format split

| idx | entity_id | company | date | round |
|---|---|---|---|---|
| 478 | `deep-robotics` | Deep Robotics | 2024-08-07 | Series B (extension) |
| 202 | `deeprobotics` | DeepRobotics | 2025-12-08 | Series C |

Same Chinese quadruped/humanoid company written two ways. Suggested canonical: `deep-robotics` (kebab-case matches the prevailing convention) and `Deep Robotics` (with space) for `company`. Mutation: rename idx=202 `DeepRobotics` → `Deep Robotics`, `deeprobotics` → `deep-robotics`.

---

## Section 4 — `subsector_uncertain` flags

**Important caveat:** The canonical schema does NOT persist `subsector_uncertain` as a field on `rounds.json` rows. The flag was a research-time annotation in agent JSON outputs that survived only in the per-quarter [backfill summary docs](data/funding/) and the temp candidate files at `/tmp/{1,2,3,4}q24_research/all_candidates.json`.

**55 rows from the 4 backfilled quarters (1Q24-4Q24) had `subsector_uncertain: true`** at agent time. The original 1Q25-2Q26 dataset has no equivalent flag history.

### Distribution by quarter

- 1Q24: 11 rows
- 2Q24: 24 rows
- 3Q24: 17 rows
- 4Q24: 3 rows

### Top 30 by subsector concentration (where the enum is failing most)

| idx | Company | Sector | Assigned subsector |
|---|---|---|---|
| 316 | Lumen Orbit | Space | Space Components |
| 318 | U-Space | Space | Space Components |
| 402 | Star Catcher Industries | Space | In-Orbit Services |
| 405 | AstroForge | Space | In-Orbit Services |
| 406 | Starpath Robotics | Space | In-Orbit Services |
| 412 | Ursa Major Technologies | Space | Space Components |
| 414 | Reflect Orbital | Space | In-Orbit Services |
| 423 | Sentient | Token | Decentralized AI / DePIN |
| 424 | Sahara AI | Token | Decentralized AI / DePIN |
| 447 | Botrista Technology | Robotics | Industrial Robots |
| 451 | Sojo Industries | Robotics | Industrial Robots |
| 455 | Applied Carbon | Robotics | Autonomous Systems & Drones |
| 458 | Intramotev | Robotics | Autonomous Systems & Drones |
| 473 | Leap Automation | Robotics | Industrial Robots |
| 486 | Varda Space Industries | Space | In-Orbit Services |
| 491 | Sift | Space | Space Components |
| 493 | Zeno Power | Space | Space Components |
| 501 | Aligned Layer | Token | Decentralized AI / DePIN |
| 504 | SendingNetwork | Token | Decentralized AI / DePIN |
| 512 | Skyports Infrastructure | Robotics | Autonomous Systems & Drones |
| 523 | Ripcord | Robotics | Industrial Robots |
| 530 | Kinetic | Robotics | Autonomous Systems & Drones |
| 531 | Greeneye Technology | Robotics | Autonomous Systems & Drones |
| 534 | Planted Solar | Robotics | Industrial Robots |
| 548 | Shinkei Systems | Robotics | Industrial Robots |
| 549 | Relocalize | Robotics | Industrial Robots |
| 554 | Carbon Robotics | Robotics | Industrial Robots |
| 641 | Hippo Harvest | Robotics | Autonomous Systems & Drones |
| 661 | Forvision | Robotics | Autonomous Systems & Drones |
| 668 | ACWA Robotics | Robotics | Autonomous Systems & Drones |
| 669 | Neatleaf | Robotics | Autonomous Systems & Drones |

### Subsectors with most uncertain flags

| Subsector | Uncertain rows | Total rows | % uncertain |
|---|---|---|---|
| Autonomous Systems & Drones | 9 | 117 | 8% |
| Industrial Robots | 8 | 43 | 19% |
| Space Components | 5 | 19 | 26% |
| In-Orbit Services | 5 | 30 | 17% |
| Decentralized AI / DePIN | 4 | 13 | 31% |
| Humanoid & Service Robots | 3 | 48 | 6% |
| Surgical & Medical | 3 | 26 | 12% |
| Silicon & Substrates | 3 | 11 | 27% |
| Battery Materials | 2 | 22 | 9% |
| Fabless Design | 2 | 55 | 4% |

**Interpretation:** `Autonomous Systems & Drones` and `Industrial Robots` are over-stretched buckets — many ag-robotics, lab-automation, food-robotics, and construction-robotics deals are flagged uncertain. If you want to tighten the taxonomy, candidate new subsectors:
- `Agricultural Robotics` (currently absorbed into `Autonomous Systems & Drones`)
- `Lab & Bio-Automation` (currently absorbed into `Industrial Robots` or `Software & Simulation`)
- `Food & Beverage Automation` (currently absorbed into `Industrial Robots`)
- `Construction Robotics` (currently absorbed into `Industrial Robots`)
- `Space Manufacturing` (currently absorbed into `In-Orbit Services`)

---

## Section 5 — Companies in 3+ rows

14 companies have 3+ rows. Each shows a sensible round progression — no Phoenix-Tailings-style duplicates.

### Cerebras Systems (4 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 426 | 2024-09-30 | IPO (filed) | null | 3Q24 |
| 427 | 2024-09-30 | Series E | $85M | 3Q24 |
| 143 | 2025-09-30 | Series G | $1100M | 3Q25 |
| 240 | 2026-02-04 | Series H | $1000.0M | 1Q26 |

**Notes:** IPO (filed) + Series E (Series F-1 bridge) on same date is the documented multi-row convention; followed by Series G (3Q25) and Series H (1Q26). All distinct events. ✅

### Stoke Space (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 4 | 2025-01-15 | Series C | $260M | 1Q25 |
| 147 | 2025-10-08 | Series D | $510.0M | 4Q25 |
| 243 | 2026-02-10 | Series D (extension) | $350.0M | 1Q26 |

**Notes:** Series progression looks sensible. ✅

### K2 Space (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 579 | 2024-02-13 | Series A | $50M | 1Q24 |
| 16 | 2025-02-13 | Series B | $110M | 1Q25 |
| 204 | 2025-12-11 | Series C | $250.0M | 4Q25 |

**Notes:** Series progression looks sensible. ✅

### Northwood Space (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 581 | 2024-02-19 | Seed | $6.3M | 1Q24 |
| 43 | 2025-04-22 | Series A | $30M | 2Q25 |
| 234 | 2026-01-27 | Series B | $100M | 1Q26 |

**Notes:** Series progression looks sensible. ✅

### Quantum Systems (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 464 | 2024-09-24 | Series B (extension) | $43.6M | 3Q24 |
| 51 | 2025-05-06 | Series C | $176M | 2Q25 |
| 187 | 2025-11-27 | Series C (extension) | $208.0M | 4Q25 |

**Notes:** Series B → Series B (extension) → Series C → Series C (extension). Standard progression with 2 extensions. ✅

### RobCo (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 632 | 2024-02-29 | Series B | $42.5M | 1Q24 |
| 52 | 2025-05-10 | Series B | $52M | 2Q25 |
| 235 | 2026-01-28 | Series C | $100.0M | 1Q26 |

**Notes:** Series progression looks sensible. ✅

### Dexory (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 363 | 2024-10-01 | Series B | $80M | 4Q24 |
| 59 | 2025-05-15 | Series C | $165M | 2Q25 |
| 152 | 2025-10-14 | Series C | $165.0M | 4Q25 |

**Notes:** Series B (4Q24) → Series C (2Q25) → Series C (4Q25). Two Series C rows 5 months apart — likely a tranched close, not a duplicate. Same amount ($165M) on both. **Potential duplicate** — verify against source URLs.

### Cyclic Materials (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 416 | 2024-09-25 | Series B | $53.0M | 3Q24 |
| 69 | 2025-06-11 | Undisclosed | $25M | 2Q25 |
| 230 | 2026-01-23 | Series C | $75M | 1Q26 |

**Notes:** Series progression looks sensible. ✅

### Skild AI (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 440 | 2024-07-09 | Series A | $300M | 3Q24 |
| 72 | 2025-06-12 | Series B | $135M | 2Q25 |
| 220 | 2026-01-14 | Series C | $1400.0M | 1Q26 |

**Notes:** Series progression looks sensible. ✅

### Hadrian (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 635 | 2024-02-21 | Series B | $117M | 1Q24 |
| 100 | 2025-07-17 | Series C | $260M | 3Q25 |
| 231 | 2026-01-25 | Undisclosed | null | 1Q26 |

**Notes:** Series B (Feb 2024) → Series C (Jul 2025) → Undisclosed (Jan 2026). Standard progression. ✅

### ICEYE (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 484 | 2024-04-17 | Strategic | $93M | 2Q24 |
| 323 | 2024-12-12 | Series D (extension) | $65M | 4Q24 |
| 200 | 2025-12-05 | Series E | $163M | 4Q25 |

**Notes:** Series progression looks sensible. ✅

### PLD Space (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 584 | 2024-01-26 | Government investment | $43.8M | 1Q24 |
| 487 | 2024-04-23 | Other | $85M | 2Q24 |
| 271 | 2026-03-04 | Series C | $209.0M | 1Q26 |

**Notes:** Government investment (Jan 2024 PERTE) → Other (Apr 2024 mixed equity+grant) → Series C (Mar 2026). Three distinct mechanics. ✅

### Rebellions (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 607 | 2024-01-25 | Series B | $124M | 1Q24 |
| 434 | 2024-07-23 | Series B (extension) | $15M | 3Q24 |
| 300 | 2026-03-26 | Government investment | $166.0M | 1Q26 |

**Notes:** Series B (Jan 2024) → Series B (extension) (Jul 2024) → Government investment (Mar 2026). Reasonable. ✅

### Physical Intelligence (3 rows)

| idx | date | round | $ | quarter |
|---|---|---|---|---|
| 631 | 2024-03-04 | Seed | $70M | 1Q24 |
| 357 | 2024-11-04 | Series A | $400M | 4Q24 |
| 305 | 2026-03-27 | Series C | $1000.0M | 1Q26 |

**Notes:** Series progression looks sensible. ✅

### Potential duplicate flagged

**Dexory** has two Series C rows at $165M each (idx=59 dated 2025-05-15 and idx=152 dated 2025-10-14). If these are the same round announced/re-announced, this matches the Phoenix Tailings pattern. Check both source URLs:
- idx=59: 2025-05-15, source = `https://techcrunch.com`
- idx=152: 2025-10-14, source = `https://sifted.eu/articles/ai-robotics-startup-dexory-raises-165m`

---

## Section 6 — Schema consistency

| Check | Result |
|---|---|
| Sector enum | ✅ all in {Robotics, Semiconductors, Space, Materials, Token} |
| deal_type enum | ✅ all in {venture, government, strategic_corporate, debt, token} |
| Date format (ISO YYYY-MM-DD) | ✅ all parse |
| Quarter consistent with date | ✅ 0 mismatches |
| Source URL present | ✅ all 676 rows |
| robotnik_notes present | ✅ all 676 rows |
| entity_id present | ✅ all 676 rows |
| Distinct subsectors | 27 (matches enum) |
| Distinct round values | 30 |

### ⚠️ 15 rows missing `date_display` and `month_year`

All 15 are in the original 1Q25-2Q26 dataset (i.e., were present before the backfill started). The schema technically allowed these fields to be optional in early data (4Q24 backfill noted "16 rows" missing in initial assessment — consistent with this finding minus one).

| idx | company | date | quarter |
|---|---|---|---|
| 0 | KoBold Metals | 2025-01-01 | 1Q25 |
| 8 | ElectraLith | 2025-01-16 | 1Q25 |
| 38 | Fairmat | 2025-04-02 | 2Q25 |
| 44 | Albedo | 2025-04-23 | 2Q25 |
| 50 | Alta Resource Technologies | 2025-05-05 | 2Q25 |
| 71 | Aethero | 2025-06-11 | 2Q25 |
| 76 | Turion Space | 2025-06-18 | 2Q25 |
| 113 | Vulcan Elements | 2025-08-11 | 3Q25 |
| 123 | Cambridge GaN Devices | 2025-09-01 | 3Q25 |
| 144 | Commcrete | 2025-09-30 | 3Q25 |
| 162 | constellr | 2025-11-01 | 4Q25 |
| 200 | ICEYE | 2025-12-05 | 4Q25 |
| 207 | SatVu | 2025-12-15 | 4Q25 |
| 230 | Cyclic Materials | 2026-01-23 | 1Q26 |
| 307 | Starfish Space | 2026-03-31 | 1Q26 |

Suggested fix: derive `date_display` (e.g. `15-Jan-25`) and `month_year` (e.g. `Jan-25`) from each row's existing `date` field. Mechanical, no judgment calls.

### Round enum review

| Round | Count | Notes |
|---|---|---|
| Series A | 131 |  |
| Series B | 108 |  |
| Seed | 97 |  |
| Series C | 73 |  |
| Series D | 36 |  |
| Other | 32 |  |
| Strategic | 27 | pre-approved by user during 4Q24 review |
| Government investment | 26 |  |
| Undisclosed | 23 |  |
| Series A (extension) | 16 |  |
| Series E | 15 |  |
| Series B (extension) | 13 |  |
| Pre-Seed | 9 |  |
| Series C (extension) | 9 |  |
| IPO | 8 |  |
| Pre-Series A | 8 |  |
| Series F | 7 |  |
| Series G | 6 |  |
| Grant | 6 |  |
| Debt Financing | 6 |  |
| Government | 3 |  |
| Series D (extension) | 3 |  |
| IPO (filed) | 3 |  |
| Seed (extension) | 3 | added in 2Q24 (SendingNetwork) |
| Bridge | 2 |  |
| Series H | 2 |  |
| Series B Extension | 1 |  |
| Series E+ | 1 |  |
| M&A | 1 |  |
| Series E (extension) | 1 | added in 4Q24 (Skydio) |

No unexpected round values.

---

## Section 7 — Geographic / location anomalies

### ⚠️ UK / United Kingdom split (29 rows)

**18 rows use `UK`, 11 rows use `United Kingdom`.** All other countries appear to use a single canonical form (USA, China, Germany, France, etc.).

**Pattern:** the original 1Q25-2Q26 data tended to use `UK`. The backfill batches drew from agent outputs that used `United Kingdom`. Recommended: normalize to one form. Suggested canonical: `United Kingdom` (matches other multi-word country names like `South Korea`, `United Arab Emirates`).

- `UK`: 18 rows (mostly original 1Q25-2Q26 data)
- `United Kingdom`: 11 rows (mostly 1Q24-4Q24 backfill)

### ⚠️ Empty/null locations (2 rows)

| idx | company | date | sector |
|---|---|---|---|
| 289 | Rivr | 2026-03-19 | Robotics |
| 294 | SatEnlight | 2026-03-24 | Space |

Both are recent 1Q26 entries (Rivr, SatEnlight). Manual fill needed.

### ✅ No other format anomalies

- 0 rows with mismatched parens
- 0 rows using `United States` or `US` instead of `USA`
- 0 rows with embedded line breaks or stray whitespace

### Country distribution (top 25)

| Country | Rows |
|---|---|
| USA | 373 |
| China | 56 |
| Germany | 36 |
| France | 25 |
| Israel | 19 |
| UK | 18 |
| Canada | 17 |
| South Korea | 15 |
| Switzerland | 13 |
| United Kingdom | 11 |
| Japan | 9 |
| Spain | 9 |
| Singapore | 7 |
| Norway | 6 |
| Netherlands | 6 |
| Belgium | 6 |
| Italy | 6 |
| India | 6 |
| Australia | 5 |
| Finland | 4 |
| Global | 4 |
| Denmark | 3 |
| Sweden | 3 |
| Poland | 3 |
| Croatia | 2 |

---

## Section 8 — Headline aggregate sanity

### 8a. deal_type × sector matrix

| deal_type | Robotics | Semis | Space | Materials | Token | Total |
|---|---|---|---|---|---|---|
| `venture` | 312 / $57.89B | 131 / $20.56B | 105 / $13.15B | 50 / $7.62B | — | **598 / $99.23B** |
| `government` | — | 20 / $29.53B | 6 / $205M | 9 / $5.05B | — | **35 / $34.78B** |
| `strategic_corporate` | 10 / $1.69B | 6 / $1.22B | 5 / $373M | 3 / $100M | — | **24 / $3.37B** |
| `debt` | 1 / $37M | 1 / $750M | 3 / $409M | 1 / $120M | — | **6 / $1.32B** |
| `token` | — | — | — | — | 13 / $316M | **13 / $316M** |
| **Total** | **323 / $59.62B** | **158 / $52.06B** | **119 / $14.14B** | **63 / $12.89B** | **13 / $316M** | **676 / $139.02B** |

**Observations:**
- `government` is concentrated in Semiconductors ($29.5B / 20 rows) — the CHIPS Act effect. 4Q24 alone is $23B of that.
- `token` is uniformly Token-sector (13/13). Clean.
- `strategic_corporate` is small ($3.4B / 24 rows) — mostly Robotics (Cruise, Motional, etc.).
- `debt` is the smallest bucket (6 rows / $1.3B) — expected for a private-markets dataset.

### 8b. Venture-only by quarter

| Quarter | Deals | Aggregate $ |
|---|---|---|
| 1Q24 | 81 | $4.67B |
| 2Q24 | 81 | $5.18B |
| 3Q24 | 66 | $5.41B |
| 4Q24 | 70 | $5.15B |
| 1Q25 | 36 | $6.81B |
| 2Q25 | 46 | $9.27B |
| 3Q25 | 61 | $10.33B |
| 4Q25 | 68 | $7.75B |
| 1Q26 | 85 | $44.03B |
| 2Q26 | 4 | $629M |

**Observations:**

- **1Q25 venture-deal count is anomalously low (36 deals).** Compare to:
  - 4Q24: 70 deals
  - 2Q25: 46 deals

  This is the original dataset's 1Q25 — possibly undercounted at original ingestion. Worth a separate review pass to backfill missing 1Q25 deals if you want a smooth time-series.

- **1Q26 venture aggregate ($44.0B) spikes vs neighboring quarters.** Driven by very large rounds (Waymo $16B, Skild AI Series C $1.4B, Physical Intelligence $1B, multiple $500M+ deals). Likely real, but worth verifying against original-dataset provenance.

- **2Q26 has only 4 deals ($629M)** — partial quarter (today is 2026-05-03; backfill cut-off was earlier).

- **Smooth elsewhere:** 1Q24-4Q24 venture aggregates are tight ($4.7B-$5.4B). 3Q25 + 4Q25 in the $7.7B-$10.3B band. Consistent with a maturing private-markets dataset.

---

## Recommended fix priorities

### Tier 1 — easy, mechanical, no judgment calls
1. Backfill `date_display` + `month_year` for the 15 missing rows (Section 6) — derive from `date`.
2. Normalize `UK` → `United Kingdom` (or vice versa) across all 29 affected rows (Section 7).
3. Fill the 2 empty location values (Rivr, SatEnlight) (Section 7).
4. Rename `Neura Robotics` → `NEURA Robotics` (idx=270) for capitalization consistency (Section 3a).
5. Normalize `DeepRobotics` → `Deep Robotics` and `deeprobotics` → `deep-robotics` (Section 3b).

### Tier 2 — judgment calls
1. Decide Intel multi-row convention: rename `Intel (Secure Enclave)` → `Intel` (Option A) vs assign distinct entity_id (Option B). Section 3a.
2. Verify `Robotera` (idx=186) is a different company from `Robot Era` (idx=86, 371) before mutating. Section 3b.
3. Verify Dexory Series C duplicate (idx=59 + idx=152) — same round announced twice or two distinct tranches? Section 5.

### Tier 3 — taxonomy decisions (deferred)
1. Decide whether to add 5 candidate new subsectors (Agricultural Robotics, Lab Automation, Food Automation, Construction Robotics, Space Manufacturing) to address the 55 `subsector_uncertain` rows. Section 4.
2. Re-review the 1Q25 undercounting — possible separate "1Q25 supplemental backfill" task to bring deal count up to 4Q24/2Q25 levels. Section 8b.

---

**End of integrity sweep.** No mutations applied. Awaiting follow-up triage prompt.