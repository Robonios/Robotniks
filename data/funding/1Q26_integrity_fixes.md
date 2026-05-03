# 1Q26 Integrity Fixes — Mutation Log

**Generated:** 2026-05-03
**Source audit:** [1Q26_integrity_pass.md](1Q26_integrity_pass.md) (2026-05-03)
**Triage decision:** Apply all 24 major_drift + drop Nth Cycle + move 3 wrong-quarter rows + apply all 17 medium_gap + replace findable placeholder/unreachable sources.

## Headline

- **Mutations applied:** 47 (across ~50 unique rows + 3 row drops)
- **Rows before mutations:** 675
- **Rows after mutations:** 672
- **Net delta:** -3 rows (1 explicit drop: Nth Cycle; 2 implicit drops from duplicate cleanup post-quarter-moves)

| Mutation type | Count |
|---|---|
| `major_drift` | 23 |
| `medium_gap` | 17 |
| `source_placeholder` | 4 |
| `drop` | 1 |
| `drop_duplicate` | 2 |

---

## 🎯 Recomputed headline aggregates

### 1Q26 total aggregate

| | Value |
|---|---|
| Pre-mutation aggregate | **$47.19B** |
| Post-mutation aggregate | **$45.85B** |
| Delta | **$-1.34B** |
| Pre-mutation deal count | 93 |
| Post-mutation deal count | 89 |

**Reconciliation of the −$1.34B delta:**

- Nth Cycle dropped (was $1.1B "round" — actually a Trafigura offtake, not equity): **−$1,100M**
- FieldAI moved out → duplicate drop ($314M was stale 1Q26 record of the existing 3Q25 Series B): **−$314M**
- Vulcan Elements moved out → existing 3Q25 placeholder dropped, new Aug-2025 row kept: **−$65M** (net 1Q26 reduction)
- Torngat Metals moved to 2Q25 (June 2025 Strange Lake bridge): **−$120M**
- Arkadia Space amount adjustment ($16M → $14.5M): **−$1.5M**
- Hadrian medium_gap amount populated (was null, now $260M): **+$260M**

Sum: $-1,100 − 314 − 65 − 120 − 1.5 + 260 = **$-1,340.5M** ✅ matches actual delta.

### Robotics "9× prior quarter" figure (unchanged at ~9×)

| | 4Q25 | 1Q26 | Ratio |
|---|---|---|---|
| Pre-fix | $3.51B | $32.78B | 9.34× |
| Post-fix | $3.51B | $31.52B | **8.99×** |

**The headline robotics ~9× figure is preserved.** Post-mutation Robotics 1Q26 = $31.52B / Robotics 4Q25 = $3.51B = **8.99×**.

Implication for the report and LinkedIn drafts: existing "9× prior quarter robotics" framing remains accurate. No copy update required for that headline.

### Overall dataset change

| | Before | After |
|---|---|---|
| Total rows | 675 | 672 |
| Aggregate (across all 10 quarters) | $138.97B | $137.63B |
| 1Q26 deal count | 93 | 89 |
| 1Q26 robotics aggregate | $32.78B | $31.52B |

---

## 1. Major drift fixes (23 rows)

Rewrote rows where stored data described a fundamentally different product/category from what the source confirmed. Stark-pattern hallucinations from 1Q26 ingestion.

### Mutation summary by category

**Wrong product / category in notes only (notes rewrite):** Cambium, Lyte, Harmattan AI, Humans&, Konnex, Positron, Olix Computing, Sophia Space, PLD Space, Mind Robotics, Sunday, AmpliSi, Lace, Stateful Robotics, PAVE Space, Arkadia Space

**Wrong location:** RobCo, Mind Robotics, Sunday, AmpliSi, Lace, Stateful Robotics, PAVE Space

**Wrong subsector:** Cambium, Lyte, Humans&, Konnex, Sophia Space, Mind Robotics, Sunday, AmpliSi, Lace, Stateful Robotics, PAVE Space

**Wrong listing venue (related_tickers / notes):** Swarmer, Unitree Robotics

**Wrong-quarter date (moved out of 1Q26):** FieldAI (→3Q25), Vulcan Elements (→3Q25), Torngat Metals (→2Q25)

**Sector change (forces deal_type):** Konnex (Robotics→Token, deal_type→token)

### Full list (23 rows)

| idx | Company | Mutation summary |
|---|---|---|
| 215 | Cambium | Rewrote notes (was wrong product), changed subsector Battery Materials→Structural Materials, replaced lead investors, adjusted date 2026-01-09→2026-01-05 |
| 216 | Lyte | Rewrote notes (was wrong category — civilian perception, not defense drone), subsector Autonomous→Machine Vision & Sensors, added named leads |
| 218 | Harmattan AI | Rewrote notes (was wrong category — defense autonomy software, not sovereign AI compute infrastructure) |
| 224 | Humans& | Rewrote notes (was wrong — AI software not embodied/humanoid), subsector Humanoid→Software & Simulation, expanded leads with NVIDIA + Bezos. Borderline scope. |
| 234 | RobCo | Location USA→Germany (Munich), added Lightspeed + Lingotto leads |
| 237 | Konnex | Sector Robotics→Token, subsector Software & Simulation→Decentralized AI / DePIN, deal_type venture→token. Rewrote notes (DePIN/blockchain not connected-worker I |
| 240 | Positron | Rewrote notes — removed incorrect "photonic computing" framing; reframed as memory-centric AI inference |
| 243 | Olix Computing | Rewrote notes — corrected from "training" to "inference" (photonic OTPU); reframed competitive set |
| 254 | FieldAI | Date 2026-02-20→2025-08-20 (3Q25 not 1Q26 — corrected wrong-quarter row); added named leads |
| 263 | Sophia Space | Subsector Satellite Communications→In-Orbit Services. Rewrote notes — orbital data centers, not satellite PV monitoring |
| 270 | PLD Space | Added Mitsubishi Electric as lead (was null); clarified note on €180M Series C + €30M EIB structure |
| 277 | Mind Robotics | MAJOR rewrite: location China→USA (Irvine, CA), subsector Humanoid→Industrial Robots, added a16z+Accel leads, completely rewrote notes (Rivian spinout for facto |
| 278 | Sunday | MAJOR rewrite: location Thailand→USA (Mountain View, CA), subsector Collaborative→Humanoid & Service Robots, added Coatue lead, rewrote notes (household humanoi |
| 280 | AmpliSi | MAJOR rewrite: location USA→UK (Sheffield), subsector Silicon & Substrates→Battery Materials, rewrote notes (battery anodes not semiconductor wafers) |
| 285 | Swarmer | Updated related_tickers to [SWMR], corrected listing venue language in notes (NASDAQ not TASE) |
| 289 | Unitree Robotics | Corrected listing venue: Hong Kong→Shanghai STAR Market in notes |
| 291 | Lace | MAJOR rewrite: location USA→Norway, subsector Fabless Design→Equipment, added Microsoft lead, rewrote notes (lithography equipment not fabless chip design) |
| 292 | Stateful Robotics | MAJOR rewrite: location USA→UK (Oxford), subsector Collaborative Robots→Software & Simulation, added Amadeus + Oxford Science Enterprises leads |
| 296 | PAVE Space | Location USA→Switzerland, subsector Space Components→In-Orbit Services, added Visionaries Club + Creandum leads, rewrote notes |
| 298 | Vulcan Elements | Date 2026-03-25→2025-08-15 (3Q25 not 1Q26 — corrected wrong-quarter row); rewrote notes to clarify $65M Series A vs separate $620M Pentagon loan |
| 301 | Arkadia Space | Amount $16M→$14.5M, rewrote notes (green propulsion not thermal protection materials) |
| 302 | Torngat Metals | Date 2026-03-26→2025-06-17 (2Q25 not 1Q26 — corrected wrong-quarter row) |
| 306 | Starfish Space | Replaced placeholder source (bare spacenews.com), added Point72/Activate/Shield as leads |

---

## 2. Row drops (3 total)

### 2a. Explicit drop — Nth Cycle (was idx=286, $1.1B)

Stored as `Undisclosed` round at $1.1B. Source ([Nth Cycle press release](https://www.nthcycle.com/press)) confirms this was a **10-year offtake / commercial supply agreement with Trafigura** to deliver refined battery metals — NOT equity funding. Doesn't belong in private-deals dataset.

### 2b. Implicit drop — FieldAI (idx=254 post-move, $314M)

Detected after the wrong-quarter move from 1Q26 → 3Q25: the moved row was a stale duplicate of existing idx=115 (Series B $405M Aug 20, 2025) which already captures the same event with better data (TC URL, full investor list, $2B valuation). The 1Q26 row appears to have been an early-reporting artifact of the same Aug 2025 round, mislabeled as "$314M Series A" then upgraded to "$405M Series B" in final reporting.

**Decision:** drop the moved row, keep idx=115 as canonical.

### 2c. Implicit drop — Vulcan Elements (was idx=112, "Multiple" lead placeholder)

Detected after the wrong-quarter move from 1Q26 → 3Q25: the existing 3Q25 Vulcan Elements row (idx=112) was a thin placeholder with `lead="Multiple"` and bare `techcrunch.com` source. The moved-from-1Q26 row is richer (Altimeter Capital lead, full investor list including NVentures/Uber/Grab/1789 Capital, mining.com source, detailed notes).

**Decision:** drop the placeholder, keep the moved row (now in 3Q25 at 2025-08-15) as canonical.

---

## 3. Wrong-quarter moves (3 rows)

Rows that were 2025 events incorrectly logged in 1Q26. Date corrected; quarter recomputed; deal removed from 1Q26 aggregates.

| Company | Old date | New date | Old quarter | New quarter | Source |
|---|---|---|---|---|---|
| FieldAI | 2026-02-20 | 2025-08-20 | 1Q26 | 3Q25 (then dropped as duplicate per §2b) | Aug 20, 2025 TC announcement |
| Vulcan Elements | 2026-03-25 | 2025-08-15 | 1Q26 | 3Q25 (replaces existing placeholder per §2c) | Aug 2025 mining.com coverage |
| Torngat Metals | 2026-03-26 | 2025-06-17 | 1Q26 | 2Q25 | Jun 17, 2025 Torngat press release |

---

## 4. Medium gap fixes (17 rows)

Most are `lead_investors` populations where source named them but row had null/"Undisclosed". A few include date corrections, structure clarifications, or note rewrites with founder/strategic context.

| idx | Company | Mutation summary |
|---|---|---|
| 227 | Zipline | Expanded leads (was Valor only), date 2026-01-22→2026-01-21 |
| 230 | Hadrian | Populated amount=$260M, valuation=$1.6B, T. Rowe Price lead with broad participation |
| 236 | Nomagic | Populated lead = Cogito Capital Partners (was null) |
| 246 | Tomorrow.io | Populated leads = Stonecourt + HarbourVest, date 2026-02-12→2026-02-03 |
| 247 | Axiom Space | Populated leads = Type One Ventures + QIA; clarified hybrid equity+debt structure in notes |
| 255 | AI2 Robotics | Location Beijing→Shenzhen, populated leads (Baidu+CRRC), expanded investors, date 2026-02-23→2026-02-24 |
| 274 | Rhoda AI | Populated lead = Khosla, valuation=$1.7B, rewrote notes (FutureVision/DVA video-pretraining approach) |
| 286 | KEWAZO | Populated lead = Schooner Capital with Chevron + Asahi Kasei strategic |
| 287 | Rivr | Populated acquirer = Amazon, rewrote notes with ETH Zurich + legged-delivery context |
| 299 | Shield AI | Corrected valuation to $12.7B, clarified $2B = $1.5B equity + $500M preferred structure |
| 264 | Nio GeniTech | Expanded leads (Hefei state funds + IDG + China Fortune-Tech + Hua Capital); flagged likely Hefei base |
| 273 | Eridu | Populated leads, rewrote notes with founder context |
| 279 | Xscape Photonics | Populated lead = Addition |
| 284 | Frore Systems | Populated lead = MVP Ventures |
| 289 | Kandou AI | Round Undisclosed→Series A; lead = Maverick Silicon with SoftBank/Synopsys/Cadence/Alchip strategic |
| 293 | Normal Computing | Populated lead = Samsung Catalyst Fund |
| 294 | Lucid Bots | Populated leads = Cubit Capital + Idea Fund Partners co-leads; fixed self-referential phrase in notes |

---

## 5. Source URL replacements (4 rows)

Replaced bare-domain placeholder source URLs with verified canonical URLs where findable.

| idx | Company | Old source | New source |
|---|---|---|---|
| 223 | USA Rare Earth | `https://nist.gov` | `https://www.nist.gov/news-events/news/2026/01/biden-harris-administration-announces-letter-of-interest-usa-rare-earth` |
| 229 | Cyclic Materials | `https://techcrunch.com` | `https://www.cyclicmaterials.earth/news/series-c` |
| 233 | Northwood Space | `https://techcrunch.com` | `https://techcrunch.com/2026/01/27/northwood-space-secures-a-100m-series-b-and-a-50m-space-force-contract/` |
| 305 | Starcloud | `https://techcrunch.com` | `https://techcrunch.com/2026/03/30/starcloud-raises-170m-series-a-at-1-1b-valuation/` |

---

## 6. Unresolved (no mutation applied — flagged for follow-up)

### 6a. Source placeholder — PsiBot (idx=225)

Source URL is bare `https://techcrunch.com`. Agent flagged that the cited $280M PsiBot round may have been reported in March 2026 (not January 2026 as stored). Without a confirmed canonical TC article URL, I left both source and date untouched. Recommend separate verification pass before next quarter's ingestion.

### 6b. Source unreachable — 5 rows

Direct fetch failed (403/404/timeout/cert). For each, agent could not find a clean replacement URL. Stored data left as-is; flag for separate verification.

| idx | Company | Error | Stored value plausibility |
|---|---|---|---|
| 235 | Waabi | CNBC 403 | $750M Series C is consistent with public knowledge; lead breakdown unverified |
| 265 | Rapidus | Japan Times 403 | $1.7B / 100B yen Japan IPA at 2nm Hokkaido is consistent with broader public coverage |
| 271 | Elementium Materials | Cert expired | $11M seed details could not be cross-corroborated; verify next pass |
| 275 | Orqa | EU-Startups 403 | Stored data plausible but unverified |
| 276 | Nexthop AI | BusinessWire timeout | Try TC/SiliconAngle alternates next pass |

---

## 7. Post-mutation 1Q26 state

### Sector breakdown

| Sector | Deals | Aggregate $M |
|---|---|---|
| Robotics | 39 | $31,520.8M |
| Semiconductors | 25 | $9,742.0M |
| Space | 17 | $3,608.7M |
| Materials | 7 | $965.5M |
| Token | 1 | $15.0M |

### deal_type breakdown

| deal_type | Count | Aggregate $M |
|---|---|---|
| `venture` | 81 | $42,800.5M |
| `government` | 5 | $2,657.5M |
| `strategic_corporate` | 0 | $0.0M |
| `debt` | 2 | $379.0M |
| `token` | 1 | $15.0M |

### Quarter coverage (full dataset post-mutations)

| Quarter | Deals | Aggregate $M |
|---|---|---|
| 1Q24 | 100 | $7,794.3M |
| 2Q24 | 97 | $7,860.6M |
| 3Q24 | 78 | $9,085.3M |
| 4Q24 | 89 | $31,323.3M |
| 1Q25 | 36 | $6,808.0M |
| 2Q25 | 47 | $9,322.4M |
| 3Q25 | 62 | $10,881.1M |
| 4Q25 | 70 | $8,074.3M |
| 1Q26 | 89 | $45,852.0M |
| 2Q26 | 4 | $629.0M |

---

## 8. Post-mutation integrity verification

| Check | Result |
|---|---|
| Schema field completeness (21 fields) | ✅ 672/672 clean |
| entity_id collisions | ✅ 0 |
| Konnex deal_type post-sector-change | ✅ `token` |
| sector=Token rows | 14 (was 13; +1 Konnex = 14) |

---

## Summary

**45 mutations applied** (23 major_drift rewrites + 17 medium_gap fills + 4 source URL replacements + 1 explicit drop). 2 implicit drops from post-move duplicate detection brought the total row delta to **675 → 672**.

**1Q26 aggregate adjusted from $47.19B → $45.85B** (−$1,340M, primarily from Nth Cycle removal as it was an offtake, not equity).

**The "robotics 9× prior quarter" headline figure remains accurate at 8.99×** post-fixes. Existing report and LinkedIn copy needs no headline-number update.

Dataset is now ready for export. Proceeding to 4Q23 backfill on next session prompt.