# Audit follow-ups

Open items surfaced during integrity sweeps that are not blocking but should be re-verified during the next full sweep.

Last updated: 2026-05-03

## Source URL re-verification needed

Five 1Q26 rows had source URLs that returned non-200 responses (404/403/429/TLS) at the time of the 1Q26 integrity pass. Verify and replace with canonical alternates if the originals remain unreachable. Treat as a single batch task during the next sweep.

| Idx | Company | Date | Current source |
|----:|---------|------|----------------|
| 234 | Waabi | 2026-01-28 | `cnbc.com/2026/01/28/autonomous-startup-waabi-raises-750-million...` |
| 263 | Rapidus | 2026-02-27 | `japantimes.co.jp/business/2026/02/27/companies/rapidus-new-investmen...` |
| 269 | Elementium Materials | 2026-03-06 | `elementium.com/news/seed` |
| 273 | Orqa | 2026-03-10 | `eu-startups.com/2026/03/orqa-series-a/` |
| 274 | Nexthop AI | 2026-03-10 | `businesswire.com/news/home/20260310574112/en/Nexthop-AI-Accelerates-...` |

Acceptance: each row has a 200-OK source URL whose content corroborates the round (date ± 7 days, amount ± 5%, lead investor exact match).

## Other deferred items

- **PsiBot (idx=224) — RESOLVED 2026-05-03.** Canonical source confirmed as Gasgoo (`autonews.gasgoo.com/.../2-billion-yuan-why-did-state-backed-capital...`). Date corrected from 2026-01-20 to 2026-03-10. Round restructured as Angel + Pre-A combined ($280M from RMB 2B), state-backed syndicate. FX captured.
- **D-Orbit 2024-01-11 row** (Series C €100M / $110M). SpaceNews coverage during 4Q23 backfill suggests the first close of D-Orbit's two-part Series C may actually have been **January 2023**, not January 2024. Once 1Q23 is in scope, verify and potentially move this row. Reference: `spacenews.com/d-orbit-raises-150-million-euros-in-two-part-series-c-round/` describes "100 million euros announced in January 2023... additional 50 million euros announced Nov 9, 2023."
- **Saronic / Saronic Technologies entity_id split.** Existing rows have both `saronic` (idx for 2025-02-19 row) and `saronic-technologies` (idx for 2024-07-19 and the new 2023-10-09 row). These are the same company. Consolidate to one entity_id during the next sweep.
- **1Q25 deal-count gap.** 1Q25 has 36 deals vs neighbors at 46-70. Worth a supplemental backfill pass to confirm whether this reflects market reality or coverage gap.
- **25 minor_discrepancy 1Q26 rows.** Left as-is per user triage on 2026-05-03. Not blocking; revisit only if specific rows surface in downstream queries.
