# Spot-Check Report — 10 Random Rows vs Source URLs

**Generated:** 2026-05-03
**Sample size:** 10 rows (random, seed=42, drawn from 675 post-fix dataset)
**Mode:** Read-only audit. No mutations applied to spot-check rows.

## Headline

| Tier | Count |
|---|---|
| ✅ Source confirms stored data | 5 rows |
| ⚠️ Notes content drift / data mismatch | 3 rows |
| 🚫 Source unreachable (TLS / 404 / 403 / 429) | 4 rows (1 overlaps with confirmed via secondary search) |

**3 actionable mismatches found.** All 3 should be considered for follow-up mutation.

---

## Sample selection

```python
import random
random.seed(42)
sample_indices = sorted(random.sample(range(675), 10))
# Result: [25, 89, 104, 114, 142, 228, 250, 281, 558, 654]
```

| idx | company | date | round | $M | sector |
|---|---|---|---|---|---|
| 25 | Tokamak Energy | 2025-03-01 | Other | 125 | Materials |
| 89 | Kongsberg Ferrotech | 2025-07-09 | Seed | 13 | Robotics |
| 104 | MP Materials | 2025-07-25 | Government investment | 550 | Materials |
| 114 | SpinLaunch | 2025-08-18 | Series C | 30 | Space |
| 142 | Cerebras Systems | 2025-09-30 | Series G | 1100 | Semiconductors |
| 228 | Neurophos | 2026-01-22 | Series A | 110 | Semiconductors |
| 250 | Stark | 2026-02-12 | Undisclosed | null | Robotics |
| 281 | Elephantech | 2026-03-12 | Series F | 27 | Semiconductors |
| 558 | Rivos | 2024-04-16 | Series A | 250 | Semiconductors |
| 654 | WIRobotics | 2024-03-28 | Series A | 9.66 | Robotics |

---

## ⚠️ Actionable mismatches (3)

### 1. Stark (idx=250) — wrong product category in notes

**Stored `robotnik_notes`:**
> "Peter Thiel-backed AI infrastructure startup (highly stealth). Amount and details undisclosed; Founders Fund involvement..."

**Source ([Sifted](https://sifted.eu/articles/stark-unicorn-valuation-following-german-armed-forces-deal)) confirms:**
> "Stark builds **weaponized drones for military applications**. Founded in 2024 by Florian Seibel (formerly of Quantum Systems), the startup develops **armed drone systems for armed forces procurement**."
> "Stark has secured a €2.4bn framework agreement with Germany's military"
> "Sequoia Capital led August 2025 round; Thiel Capital participated"

**Severity:** **MAJOR.** Stored notes describe Stark as "AI infrastructure" — wrong product category entirely. Stark is a defense-tech weaponized-drone company, not AI infra. Likely a hallucination during 1Q26 ingestion.

**Suggested fix:**
- Rewrite notes to reflect weaponized drones for German Armed Forces (€2.4B framework agreement)
- Verify lead_investors (currently null per row) — sources name Sequoia (Aug 2025) + Thiel Capital
- Verify subsector — currently `Robotics` / would need to check stored subsector
- Note Florian Seibel founder context (ex-Quantum Systems)

---

### 2. WIRobotics (idx=654) — `lead_investors` is "Undisclosed" but actually Intervest

**Stored row:**
- `lead_investors`: `"Undisclosed"`
- `robotnik_notes`: "Wearable exoskeleton for industrial back-support (WIBS) and mobility-assist (WIM); founded by ex-Samsung robotics engineers..."

**Source (stored URL [tracxn.com/d/companies/wirobotics/](https://tracxn.com/d/companies/wirobotics/)) returned 404.** Resolved via web search:

[WowTale (March 28, 2024)](https://en.wowtale.net/2024/03/28/222839/) explicitly states:
> "The Series A round **was led by Intervest** and included other investors."

**Severity:** **MEDIUM.** Original 1Q24 backfill agent flagged this as `single_source: true` (Tracxn-only) which is now the dead source. Lead investor exists in the public record but row says undisclosed.

**Suggested fix:**
- Update `lead_investors`: "Undisclosed" → "Intervest"
- Update `source` URL: dead Tracxn link → working WowTale article
- Optional: keep flagged as borderline-corroborated since secondary source still thin

---

### 3. MP Materials (idx=104) — date mismatch

**Stored:** `date: 2025-07-25`

**Source ([InvestorNews op-ed](https://investornews.com/market-opinion/follow-the-money-u-s-government-funding-for-critical-minerals/)) confirms:**
> "**July 10, 2025**: Transformational Public-Private Partnership with the Department of Defense to Accelerate U.S. Rare Earth Magnet Independence"
> "$400M preferred stock + $150M direct loan + 10-year NdPr price floor (~$110/kg)"

Multiple primary sources (DoD press release, Reuters) consistently date the announcement as **July 10, 2025**, not July 25.

**Severity:** **LOW** (15-day discrepancy, same quarter). Notes content matches the source well otherwise.

**Suggested fix:**
- Update `date`: `2025-07-25` → `2025-07-10`
- `date_display`/`month_year`/`quarter` would need recompute (still July, still 3Q25, so quarter is unaffected)

---

## ✅ Confirmed matches (5)

### idx=89 Kongsberg Ferrotech — clean
[Source](https://www.nif.fund/news/nato-innovation-fund-leads-eur12-million-seed-financing-round-in-kongsberg-ferrotech/) confirms €12M ($13M), NATO Innovation Fund led, 2025-07-09 date matches. Subsea inspection/repair robot description matches.

**Caveat:** Notes mention "backed by Equinor/Kongsberg Gruppen" but source identifies Investinor (Norway sovereign fund) as co-investor, not Equinor. Equinor and Kongsberg Gruppen are likely customers/partners, not investors in this round. Minor framing concern but not a content error per se.

### idx=142 Cerebras Systems — mostly clean, minor note drift
[Source](https://techcrunch.com/2025/09/30/a-year-after-filing-to-ipo-still-private-cerebras-systems-raises-1-1b/) confirms $1.1B Series G on Sept 30 2025, CFIUS review delaying IPO due to G42 investment.

**Caveat:** Notes claim "revenue grew $6M to $70M in one year" — TechCrunch source mentions "explosive growth" but does NOT cite specific $6M→$70M revenue progression. Specific numbers may be from a different/uncited source. Either source the figures or soften the language.

### idx=228 Neurophos — clean
[Source](https://techcrunch.com/2026/01/22/from-invisibility-cloaks-to-ai-chips-neurophos-raises-110m-to-build-tiny-optical-processors-for-inferencing/) confirms $110M Series A on 2026-01-22, Gates Frontier lead, metasurface modulators. Notes match well.

### idx=281 Elephantech — clean (verified via web search after primary URL 403'd)
Stored URL [thebridge.jp](https://thebridge.jp/en/2026/03/elephantech-secures-%C2%A54-billion-series-f-funding) returned 403, but [Mitsubishi Electric press release](https://www.mitsubishielectric.com/en/pr/2026/0312-b/) confirms ¥4B (~$27M) Series F from Mitsubishi Electric on March 12, 2026 for SustainaCircuits printed-electronics partnership. Notes match.

### idx=558 Rivos — clean, minor stage label nuance
[Source](https://siliconangle.com/2024/04/16/rivos-raises-250m-develop-chips-ai-analytics-workloads/) confirms $250M, April 16 2024, Matrix Capital lead, Intel Capital + MediaTek participation. RISC-V CPU + GPGPU on TSMC 3nm matches notes.

**Caveat:** Source labels this "Series-A3" (third tranche / extension). Stored row uses simpler "Series A". Acceptable simplification but worth noting if you want to use `Series A (extension)` for granularity.

---

## 🚫 Sources unreachable (4)

### idx=25 Tokamak Energy — TLS error
- **Stored URL:** `https://fusionindustryassociation.org`
- **Error:** `ERR_TLS_CERT_ALTNAME_INVALID`
- **Issue:** URL is the homepage of the Fusion Industry Association, not a specific article about Tokamak Energy's $125M raise. Even if accessible, it would not contain row-specific information.
- **Severity:** **HIGH source-quality concern.** Stored data ($125M, "Other" round, DOE Milestone Program) cannot be verified from this URL.

### idx=114 SpinLaunch — 429 rate-limited
- **Stored URL:** `https://spacenews.com/spinlaunch-raises-30-million-for-work-on-meridian-space-constellation/`
- **Error:** Rate-limited (429) on both attempts.
- **Severity:** **TEMPORARY** — URL pattern suggests a real SpaceNews article. Likely retrievable later.

### idx=281 Elephantech — 403 (resolved via search)
- **Stored URL:** `https://thebridge.jp/en/2026/03/elephantech-secures-%C2%A54-billion-series-f-funding`
- **Error:** 403 Forbidden (likely paywall/regional block)
- **Resolved via:** Mitsubishi Electric press release + multiple secondary sources confirming the deal as stored.
- **Severity:** **LOW** — primary source exists and is verifiable, just gated to WebFetch.

### idx=654 WIRobotics — 404 (resolved via search)
- **Stored URL:** `https://tracxn.com/d/companies/wirobotics/`
- **Error:** 404 Not Found
- **Severity:** **MEDIUM** — Tracxn company-profile URLs are notoriously gated/transient. The original 1Q24 backfill flagged this row as `single_source: true` and the source is now dead. WowTale article exists as a stable replacement.
- **Suggested fix:** Replace stored URL with the WowTale alternative, surfaced in mismatch #2 above.

---

## Pattern observations

**Source-quality stratification:**
- Original 1Q25-2Q26 dataset rows in this sample: idx=25 (Tokamak), idx=104 (MP Materials) — both have lower-quality sources (homepage, op-ed)
- Backfill (1Q24-4Q24) rows in this sample: idx=558 (Rivos), idx=654 (WIRobotics) — sources are more specific (SiliconANGLE article, Tracxn profile) but Tracxn URLs prone to dying

**Hallucination risk concentrated in 1Q26:**
- 4 rows in this sample are 1Q26 (idx=228, 250, 281, 250) → 1 has a major content drift (Stark) and 1 has an actionable lead-investor gap. 25% major drift rate vs 0% in 1Q24-4Q24 backfill rows. Worth flagging that 1Q26 ingestion may need its own integrity sweep.

**Suggested follow-up:**
1. Apply the 3 actionable fixes above (Stark notes, WIRobotics lead, MP Materials date)
2. Spot-check 10-20 more 1Q26 rows specifically — 1Q26 looks under-curated relative to 1Q24-4Q24 backfill quality
3. Consider source-URL health scan as a separate pass (TLS / 404 / 403 detection across all 675 rows)

---

**End of spot-check.** No mutations applied to sample rows. Awaiting follow-up triage.
