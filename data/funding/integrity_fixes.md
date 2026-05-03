# Robotnik Funding Dataset — Integrity Fixes Mutation Log

**Generated:** 2026-05-03
**Source audit:** [integrity_sweep.md](integrity_sweep.md) (2026-05-03)
**Triage decision:** Apply Tier 1 (mechanical) + Tier 2 (with decisions); defer Tier 3.

## Headline

- **Mutations applied:** 39 (across 38 rows + 1 row dropped)
- **Rows before:** 676
- **Rows after:** 675

| Mutation type | Count | Tier |
|---|---|---|
| `backfill_date_fields` | 15 | Tier 1 |
| `normalize_uk` | 18 | Tier 1 |
| `fill_location` | 2 | Tier 1 |
| `rename_company` (NEURA + Intel) | 2 | Tier 1 + 2 |
| `rename_company_and_entity_id` (Deep Robotics) | 1 | Tier 1 |
| `drop_duplicate` (Dexory) | 1 | Tier 2 (post-evidence) |

---

## 1. Backfilled `date_display` + `month_year` (15 rows)

All 15 rows were in the original 1Q25-2Q26 dataset (pre-backfill). Both fields derived mechanically from `date`:
- `date_display`: `D-Mon-YY` (e.g., `15-Jan-25`)
- `month_year`: `Mon-YY` (e.g., `Jan-25`)

Field order in each affected row was reset to canonical (date_display after `date`, month_year after `source`) for diff-readability.

| idx (pre-drop) | company | date | added date_display | added month_year |
|---|---|---|---|---|
| 0 | KoBold Metals | 2025-01-01 | `1-Jan-25` | `Jan-25` |
| 8 | ElectraLith | 2025-01-16 | `16-Jan-25` | `Jan-25` |
| 38 | Fairmat | 2025-04-02 | `2-Apr-25` | `Apr-25` |
| 44 | Albedo | 2025-04-23 | `23-Apr-25` | `Apr-25` |
| 50 | Alta Resource Technologies | 2025-05-05 | `5-May-25` | `May-25` |
| 71 | Aethero | 2025-06-11 | `11-Jun-25` | `Jun-25` |
| 76 | Turion Space | 2025-06-18 | `18-Jun-25` | `Jun-25` |
| 113 | Vulcan Elements | 2025-08-11 | `11-Aug-25` | `Aug-25` |
| 123 | Cambridge GaN Devices | 2025-09-01 | `1-Sep-25` | `Sep-25` |
| 144 | Commcrete | 2025-09-30 | `30-Sep-25` | `Sep-25` |
| 162 | constellr | 2025-11-01 | `1-Nov-25` | `Nov-25` |
| 200 | ICEYE | 2025-12-05 | `5-Dec-25` | `Dec-25` |
| 207 | SatVu | 2025-12-15 | `15-Dec-25` | `Dec-25` |
| 230 | Cyclic Materials | 2026-01-23 | `23-Jan-26` | `Jan-26` |
| 307 | Starfish Space | 2026-03-31 | `31-Mar-26` | `Mar-26` |

## 2. Normalized UK → United Kingdom (18 rows)

Per triage decision: `United Kingdom` chosen as canonical (matches multi-word convention used for `South Korea`, `United Arab Emirates`, etc.).

All 18 affected rows were original 1Q25-2Q26 dataset rows. The 11 UK-region rows from the 1Q24-4Q24 backfill already used `United Kingdom`.

| idx (pre-drop) | company | date | old | new |
|---|---|---|---|---|
| 9 | BOW | 2025-01-27 | `UK (Sheffield)` | `United Kingdom (Sheffield)` |
| 17 | Cambridge GaN Devices | 2025-02-18 | `UK (Cambridge)` | `United Kingdom (Cambridge)` |
| 25 | Tokamak Energy | 2025-03-01 | `UK (Oxford)` | `United Kingdom (Oxford)` |
| 36 | CMR Surgical | 2025-04-02 | `UK (Cambridge)` | `United Kingdom (Cambridge)` |
| 54 | Space Forge | 2025-05-14 | `UK (Cardiff)` | `United Kingdom (Cardiff)` |
| 59 | Dexory | 2025-05-15 | `UK (London)` | `United Kingdom (London)` |
| 78 | Infravision | 2025-06-20 | `UK` | `United Kingdom` |
| 118 | Paragraf | 2025-08-25 | `UK (Cambridgeshire)` | `United Kingdom (Cambridgeshire)` |
| 123 | Cambridge GaN Devices | 2025-09-01 | `UK (Cambridge)` | `United Kingdom (Cambridge)` |
| 124 | Surgerii Robotics | 2025-09-05 | `UK` | `United Kingdom` |
| 130 | CuspAI | 2025-09-10 | `UK (Cambridge)` | `United Kingdom (Cambridge)` |
| 152 | Dexory | 2025-10-14 | `UK (London)` | `United Kingdom (London)` |
| 156 | CMR Surgical | 2025-10-20 | `UK (Cambridge)` | `United Kingdom (Cambridge)` |
| 207 | SatVu | 2025-12-15 | `UK` | `United Kingdom` |
| 244 | Olix Computing | 2026-02-11 | `UK (London)` | `United Kingdom (London)` |
| 261 | Wayve | 2026-02-24 | `UK (London)` | `United Kingdom (London)` |
| 273 | Nscale | 2026-03-09 | `UK (London)` | `United Kingdom (London)` |
| 313 | ALL.SPACE | 2024-10-03 | `UK (Reading)` | `United Kingdom (Reading)` |

## 3. Filled empty locations (2 rows)

Both source URLs (`therobotreport.com/rivr-acquired/` and `satenlight.com/news/seed`) returned 404 at fetch time. Resolved via web search against authoritative secondary sources.

### Rivr (idx=289, date=2026-03-19)

- **Old:** `None`
- **New:** `Switzerland (Zurich)`
- **Source:** Web search confirmed Swiss spinoff from ETH Zurich; Amazon acquisition March 2026

### SatEnlight (idx=294, date=2026-03-24)

- **Old:** `None`
- **New:** `Italy (Milan)`
- **Source:** Via Satellite + Gizmodo + SpaceNews; University of Milan spinoff

**⚠️ NOTE: existing robotnik_notes describes SatEnlight as "Satellite-based solar energy monitoring" but Via Satellite confirms the company actually does inter-satellite optical communication (laser-based data multiplexing). Notes content may need separate fix — out of scope for this pass.**

## 4. Renamed companies (3 rows)

Three separate rename operations, all preserving `entity_id` (which was already canonical):

### `Neura Robotics` → `NEURA Robotics` (idx=270, date=2026-03-04)

**Reason:** Capitalization consistency with existing entity_id=neura-robotics rows; NEURA matches company brand.

### `Intel (Secure Enclave)` → `Intel` (idx=433, date=2024-09-16)

**Reason:** Multi-row convention: same legal entity, distinct rounds. Both rows now share company="Intel" + entity_id="INTC". Distinguishing detail (Secure Enclave) preserved in robotnik_notes.

### `DeepRobotics` → `Deep Robotics` (idx=202, date=2025-12-08)

- **Old company:** `DeepRobotics`, old entity_id: `deeprobotics`
- **New company:** `Deep Robotics`, new entity_id: `deep-robotics`
- **Reason:** Format consistency with existing 3Q24 row (entity_id=deep-robotics, company="Deep Robotics"). Same Chinese quadruped/humanoid company.

### Verification: Intel rows post-rename

Both Intel rows now share `company="Intel"` + `entity_id="INTC"`, conforming to the multi-row convention from 3Q24:

| idx | company | date | round | Notes |
|---|---|---|---|---|
| 346 | Intel | 2024-11-26 | Government investment | Commercial CHIPS Act award ($7.86B) |
| 432 | Intel | 2024-09-16 | Government investment | DoD-trusted-foundry Secure Enclave award ($3B) |

Distinguishing detail (Secure Enclave) preserved in `robotnik_notes` of the Sep 16 row.

## 5. Dropped Dexory duplicate (1 row)

Per Tier 2 triage: investigated source URLs before mutating.

### Evidence gathered

**idx=59** (May 15, 2025) — was placeholder/stub:
- `lead_investors`: `"Multiple"` (placeholder)
- `source`: `"https://techcrunch.com"` (URL stub, no specific article)
- `robotnik_notes`: thin one-liner ("Autonomous warehouse scanning robots creating digital twins of logistics facilities")
- `other_investors`: empty

**idx=152** (Oct 14, 2025) — was the real announcement:
- `lead_investors`: `"Eurazeo (Growth)"`
- `source`: `"https://sifted.eu/articles/ai-robotics-startup-dexory-raises-165m"`
- `robotnik_notes`: rich, with comp/competitor context
- `other_investors`: full named syndicate including $65M debt component

### Sifted article (Oct 14, 2025) confirms

> **Announcement Date:** October 14, 2025
> **Round Structure:** "$100m in equity, led by Eurazeo with participation from LTS Growth and Endeavor Catalyst, alongside existing investors Atomico, Lakestar, Elaia, Latitude Ventures. Bootstrap Europe provided $65m in debt funding."
> **Single announcement, not multiple tranches.** No language suggesting May 2025 partial close.

### Decision: drop the May 15, 2025 row

Same canonical pattern as the Phoenix Tailings duplicate resolved in 4Q24 revision 2: keep the row with named lead, full investor list, real press URL, and rich notes; drop the placeholder row.

| | Dropped (idx=59) | Kept (idx=152) |
|---|---|---|
| date | 2025-05-15 | 2025-10-14 |
| round | Series C | Series C |
| amount_m | 165 | 165.0 |
| lead_investors | "Multiple" | Eurazeo (Growth) |
| source | https://techcrunch.com | https://sifted.eu/articles/ai-robotics-startup-dexory-raises-165m |
| quarter | 2Q25 | 4Q25 |

---

## Post-mutation verification

All Section 6 schema checks re-run against the 675-row dataset:

| Check | Result |
|---|---|
| Schema field completeness | ✅ all 675 rows have all 21 fields |
| Sector enum | ✅ clean |
| deal_type enum | ✅ clean |
| Date format | ✅ all parse |
| Quarter consistent with date | ✅ 0 mismatches |
| Empty locations | ✅ 0 |
| `UK ` or `UK` location prefix | ✅ 0 |
| Entity_id exact collisions | ✅ 0 (was 2) |
| Entity_id near-collisions | 1 remaining (`robot-era` vs `robotera` — kept distinct per Tier 2 decision: different companies) |

## Updated quarter coverage (post-Dexory drop)

| Quarter | Deals | Δ from pre-fix |
|---|---|---|
| 1Q24 | 100 |  |
| 2Q24 | 97 |  |
| 3Q24 | 78 |  |
| 4Q24 | 89 |  |
| 1Q25 | 36 |  |
| 2Q25 | 46 (-1) | Dexory dup removed |
| 3Q25 | 62 |  |
| 4Q25 | 70 |  |
| 1Q26 | 93 |  |
| 2Q26 | 4 |  |

---

## Deferred (Tier 3, per triage decision)

1. **55 `subsector_uncertain` rows** — taxonomy expansion (Agricultural Robotics, Lab & Bio-Automation, Food Automation, Construction Robotics, Space Manufacturing) deferred. Rows remain flagged in agent commentary at `/tmp/{1,2,3,4}q24_research/all_candidates.json`.
2. **1Q25 deal-count gap** (36 venture vs neighboring 46-70) — noted for future supplemental backfill task.

## Other items flagged but not mutated

### SatEnlight robotnik_notes content error

Existing notes describe SatEnlight as "satellite-based solar energy monitoring", but Via Satellite + SpaceNews + Gizmodo confirm the company actually does **inter-satellite optical communication** (laser-based data multiplexing for higher LEO data rates). The note content appears to be a hallucination from the original 1Q26 ingestion.

Out of scope for this fix pass (only location was approved). Flagged here for follow-up — likely the SatEnlight 1Q26 row should have its `robotnik_notes` rewritten in a separate cleanup pass.

---

**End of mutation log.** Dataset is now at 675 rows, schema fully consistent, ready for export.