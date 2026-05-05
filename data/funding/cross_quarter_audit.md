# Cross-Quarter Consistency Audit (read-only)

**Date:** 2026-05-05
**Dataset version:** v1.0 (1,080 rows, 14 quarters)
**Scope:** Round-letter regressions, sequential close labeling, lead-investor switches, entity_id collisions
**Mutations:** None — this is a read-only audit. All findings are advisory.

## Summary

| Check | Findings | Actionable | Informational |
|-------|---------:|-----------:|--------------:|
| Round-letter regressions | 4 | 1 | 3 |
| Sequential close inconsistencies | 17 | 4 | 13 |
| Lead investor switches (no overlap, same letter) | 25 | 0 | 25 |
| Entity_id collisions | 2 | 2 | 0 |
| **Total** | **48** | **7** | **41** |

The dataset is in good shape overall. **Seven actionable items** worth resolving in a future cleanup pass. The remaining 41 findings are normal narrative drift across multi-close rounds.

---

## 1. Round-letter regressions (4)

### 🚨 ACTIONABLE: ispace `9348 JP` — IPO (2Q23) → Series D (1Q26)

| Date | Round | Quarter |
|------|-------|---------|
| 2023-04-12 | IPO | 2Q23 |
| 2026-02-12 | Series D | 1Q26 |

ispace went public on TSE Growth Market in April 2023 (ticker 9348). A "Series D" round 33 months later for a publicly-listed company is structurally inconsistent — public companies don't raise Series-letter rounds. The 1Q26 row is likely either:
- A public secondary / PIPE (should be excluded per the Aurora rule)
- A mislabeled round (could be Strategic / Other)
- A pre-IPO Series D that closed late and got back-dated incorrectly

**Recommended action:** Investigate the 1Q26 ispace row. Either drop (if it's a public secondary) or reclassify to Strategic / Debt Financing.

### Informational (3)

These are not real regressions — they're sequential closes within the same round letter where the second close should have been labeled "(extension)" but wasn't. Listed under §2 below as labeling inconsistencies, not regressions. The flagged "regressions" are an artifact of the ranking heuristic.

| Entity | Pattern |
|--------|---------|
| Shield AI `shield-ai` | Series F (extension) 4Q23 → Series F 1Q25 — should be "Series F (extension)" or note as separate close |
| Agtonomy `agtonomy` | Series A (extension) 4Q24 → Series A 1Q25 — should be "Series A (extension)" |
| Cerebras Systems `cerebras-systems` | IPO (filed) 3Q24 + Series E 3Q24 same day — multi-row convention for concurrent IPO+Series E close (user-approved precedent) ✓ |

---

## 2. Sequential close inconsistencies (17)

Entities with multiple rows under the same Series letter where labeling is inconsistent (some closes marked "(extension)", others not).

### 🚨 ACTIONABLE (4)

#### Boston Metal `boston-metal` — Series C
Three close events but inconsistent labeling:
| Date | Round | Quarter | Notes excerpt |
|------|-------|---------|---------------|
| 2023-01-27 | Series C | 1Q23 | "MIT spinout commercializing molten oxide electrolysis (MOE) for green steel" |
| 2023-09-06 | Series C | 3Q23 | "Final close of Series C ($120M earlier + $140M Sept)" |
| 2024-01-30 | Series C (extension) | 1Q24 | "Series C2 extension brings total Series C to $282M" |

The Sept 2023 row should be **"Series C (extension)"** (it's explicitly the final close of the same Series C). Currently labeled bare "Series C" creates two same-letter rows with different leads (ArcelorMittal vs Aramco Ventures-led).

#### Zhiyuan Robotics (AgiBot) `zhiyuan-robotics-agibot` — Series A
| Date | Round | Quarter | Notes excerpt |
|------|-------|---------|---------------|
| 2023-08-15 | Series A | 3Q23 | "Initial Series A close..." |
| 2023-12-14 | Series A | 4Q23 | "First institutional round for the Peng Zhihui (ex-Huawei Genius Youth) humanoid..." |

Two Series A entries 4 months apart, neither labeled extension. The 4Q23 row's notes ("First institutional round") suggest it might actually be the *real* Series A and the 3Q23 row is an earlier seed-style close. Verify and either: (a) label 4Q23 as "Series A (extension)" or (b) reclassify 3Q23 as "Pre-Series A".

#### Shield AI `shield-ai` — Series F
4 same-letter rows:
| Date | Round | Quarter | Amount |
|------|-------|---------|-------:|
| 2023-09-14 | Series F | 3Q23 | $150M |
| 2023-10-31 | Series F | 4Q23 | $200M |
| 2023-12-29 | Series F (extension) | 4Q23 | $300M |
| 2025-03-06 | Series F | 1Q25 | $240M |

The 1Q25 row — 14 months after the F extension — should likely be "Series F (extension)" or possibly its own letter. Verify.

#### Agtonomy `agtonomy` — Series A
| Date | Round | Quarter | Amount |
|------|-------|---------|-------:|
| 2023-12-19 | Series A | 4Q23 | $22.5M |
| 2024-10-16 | Series A (extension) | 4Q24 | $10M |
| 2025-03-20 | Series A | 1Q25 | $38M |

The 1Q25 row should be **"Series A (extension)"** — three Series A closes total, only middle one labeled.

### Informational (13)

These are normal narrative drift — the second close mentions extension/tranche/total while the first doesn't (because at first-close time, no extension existed yet). No action needed.

| Entity | Round | Closes |
|--------|-------|-------:|
| RobCo | Series B | 2 (Feb 2024 + May 2025 — possibly should be "Series B (extension)" for the 2Q25 row, marginal) |
| XTEND | Series B + ext | 2 |
| Ursa Major | Series D + ext | 2 |
| Pixxel | Series B + ext | 2 |
| GITAI | Series B (extension) × 3 | 3 sequential extensions, each labeled |
| Carbon Robotics | Series C + ext | 2 |
| Astranis | Series D × 2 | 2 (separate $200M and $200M+ rounds at different cap tables — both legitimately Series D-1 and D-2 per Astranis convention) |
| Wingtra | Series B + ext | 2 |
| Ascend Elements | Series D + ext | 2 |
| EnergyX | Series B + ext | 2 |
| FERNRIDE | Series A + ext | 2 |
| Verity | Series B + ext | 2 |
| Q-CTRL | Series B (extension) × 2 | 2 sequential extensions |

---

## 3. Lead investor switches (25)

Same entity_id, same round letter, no investor name overlap between consecutive closes. **All 25 are normal extension-syndicate dynamics.** Listed for transparency only — no action recommended.

Common patterns:
- **Original lead anchors round, new strategic anchors extension** (Lightmatter Fidelity → GV; Carbon Robotics Sozo → NVentures; Ascend Elements Decarbonization Partners → Just Climate)
- **Geography expansion via new regional lead** (Boston Metal ArcelorMittal → Aramco Ventures → Marunouchi; Wingtra DiamondStream → RKKVC)
- **"Multiple" / "Undisclosed" lead** in extension closes (Quantum Systems, Pixxel, Cambridge GaN Devices, Turion Space, Infravision, Xscape Photonics)
- **Long gap with new market/strategy** (KEWAZO Fifth Wall 2023 → Schooner 2026; Augmentus Sierra 2023 → Woori 2025; Skydio Linse 2023 → KDDI/Axon 2024)
- **Extension led by Korean / Saudi / Singapore strategic capital** (Rebellions KT → Aramco Wa'ed; XTEND Chartered → Aliya/Protego; Infravision multiple → GIC)

Full list available in `/tmp/cross_quarter_findings.json`.

---

## 4. Entity_id collisions (2)

### 🚨 ACTIONABLE: `ecorobotix` — name variants

| entity_id | Companies (same entity, different spelling) |
|-----------|---------------------------------------------|
| `ecorobotix` | "Ecorobotix" + "ecoRobotix" |

Same Swiss agricultural robotics company. Normalize company name to single canonical spelling (recommend "ecoRobotix" per their own branding).

### 🚨 ACTIONABLE: `9348 JP` — iSpace / ispace name variants

| entity_id | Companies |
|-----------|-----------|
| `9348 JP` | "iSpace" + "ispace" |

Same Japanese lunar lander company (TSE: 9348). Normalize to "ispace" (per company's official spelling). Also see §1 — there's a Series D label issue at this entity_id that needs investigation.

### Already flagged in [audit_followups.md](audit_followups.md)

- `saronic` vs `saronic-technologies` — different entity_ids for the same company. Three rows total (1 + 2 + 1 = 4). Already in queue.

---

## Summary table — actionable items

| # | Item | File reference | Action |
|---|------|----------------|--------|
| 1 | ispace 2026-02-12 "Series D" — likely public-co PIPE | rounds.json idx for `9348 JP` 1Q26 row | Investigate → drop or reclassify |
| 2 | Boston Metal Sep 2023 row — should be "Series C (extension)" not bare "Series C" | rounds.json `boston-metal` 3Q23 | Relabel round |
| 3 | Zhiyuan Robotics — Series A vs Pre-Series A | rounds.json `zhiyuan-robotics-agibot` 3Q23 | Investigate → relabel one |
| 4 | Shield AI 1Q25 row — likely should be "Series F (extension)" | rounds.json `shield-ai` 1Q25 | Verify and relabel |
| 5 | Agtonomy 1Q25 row — should be "Series A (extension)" | rounds.json `agtonomy` 1Q25 | Relabel round |
| 6 | `ecorobotix` company name variants | rounds.json `ecorobotix` rows | Normalize company name |
| 7 | `9348 JP` company name variants (iSpace / ispace) | rounds.json `9348 JP` rows | Normalize company name |

These can be batched into a single Tier-1 mechanical mutation pass when the user is ready. Estimated mutation count: 7-8 rows. None are blocking for v1.0.

---

## Methodology

```python
# Round letter ranking used for regression detection
ROUND_RANK = {
    'Pre-Seed': 0, 'Seed': 1, 'Seed (extension)': 1.5,
    'Pre-Series A': 1.8, 'Series A': 2, 'Series A (extension)': 2.5,
    'Pre-Series B': 2.8, 'Series B': 3, 'Series B (extension)': 3.5, 'Series B Extension': 3.5,
    'Pre-Series C': 3.8, 'Series C': 4, 'Series C (extension)': 4.5,
    'Series D': 5, 'Series D (extension)': 5.5,
    'Series E': 6, 'Series E (extension)': 6.5, 'Series E+': 6.5,
    'Series F': 7, 'Series F (extension)': 7.5,
    'Series G': 8, 'Series G (extension)': 8.5,
    'Series H': 9,
    'IPO': 10, 'IPO (filed)': 9.9,
    # Bridge, Debt Financing, Strategic, Government investment, Grant, M&A, Other, Undisclosed → not ranked
}

# Regression: rankable[i].rank < rankable[i-1].rank for same entity_id, sorted by date
# Sequential inconsistency: same Series letter across rows where some have "(extension)" in round name and notes mention it, but adjacent rows don't
# Lead switch: same entity_id + same round letter base + zero investor name overlap between adjacent rows
# Collision: entity_id maps to >1 distinct company name
```

Raw findings exported to `/tmp/cross_quarter_findings.json` (gitignored).
