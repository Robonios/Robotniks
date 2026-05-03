# 1Q26 Integrity Pass — Source Verification Across All 93 Rows

**Generated:** 2026-05-03
**Methodology:** WebFetch each row's `source` URL and compare extracted facts (company, date, round, amount, lead investor, location, product description) against stored data. Same approach as the 10-row spot-check, scaled to all 93 rows in 1Q26.
**Mode:** Read-only audit. No mutations applied.

## TL;DR

| Severity | Count | % |
|---|---|---|
| `major_drift` | 24 | 26% |
| `medium_gap` | 17 | 18% |
| `minor_discrepancy` | 25 | 27% |
| `source_placeholder` | 5 | 5% |
| `source_unreachable` | 5 | 5% |
| `clean` | 17 | 18% |

**66 of 93 rows (71%) have actionable mismatches** spanning major drifts, medium gaps, and minor discrepancies. Only 17 rows (18%) cleanly match source data.

**This quarter is significantly under-curated relative to the 1Q24-4Q24 backfill** (which had ~10% drift on spot-check). Strong recommendation: do not ship the export to VCs without addressing the 24 `major_drift` items at minimum.

---

## 🚨 MAJOR DRIFT (24 rows) — wrong product / category / amount / fundamentals

These rows describe materially different things from what the source confirms. Likely Stark-pattern hallucinations during 1Q26 ingestion. Fix before VCs see the export.

### idx=215 — Cambium

**Issue:** Stored notes describe 'lithium-ion battery cathode materials using recycled feedstock' but source describes Cambium as an AI/chemical-informatics platform designing advanced monomers/polymers for aerospace, defense, energy, marine. Lead investor stored as 'Decarbonization Partners (BlackRock + Temasek)' but actual lead is 8VC with Lockheed Martin Ventures. Date Jan 9 vs source Jan 5.

**Stored:** `lithium-ion battery cathode materials, Decarbonization Partners`
**Source says:** AI/chemical-informatics company designing monomers/polymers for high-performance materials; led by 8VC with Lockheed Martin Ventures, MVP Ventures, and others
**Suggested fix:** Rewrite notes to reflect AI-driven advanced materials thesis; replace lead investor; correct date to 2026-01-05.

### idx=216 — Lyte

**Issue:** Row characterizes Lyte as 'Defence drone and autonomous systems company' suggesting classified DoD programs. Source describes Lyte as a perception/visual-brain company for robots and physical AI, founded by ex-Apple Face ID engineers. Investors are Fidelity, Atreides Management, Exor Ventures, Avigdor Willenz — civilian/commercial, not classified defense.

**Stored:** `Defence drone and autonomous systems company (stealth ops); $107M; lead null`
**Source says:** Integrated perception/depth-sensing platform (LyteVision) for AMRs, robotic arms, robotaxis, humanoids; investors Fidelity, Atreides, Exor, Key1, VentureTech Alliance, Willenz
**Suggested fix:** Rewrite notes; reclassify subsector from Autonomous Systems & Drones to Machine Vision & Sensors; add named investors; consider date Jan 5/6 vs Jan 9.

### idx=218 — Harmattan AI

**Issue:** Row describes Harmattan as 'French AI compute company building sovereign AI infrastructure', competing with Nscale/CoreWeave/hyperscalers. Source confirms Harmattan is a defense-tech company building autonomy and mission-system software for defense aircraft/drones — not AI compute infrastructure. Subsector and competitive set are wrong.

**Stored:** `Sovereign AI infrastructure compute; competes with Nscale/CoreWeave`
**Source says:** Defense technology company developing autonomy/mission software for defense aircraft and drones
**Suggested fix:** Rewrite notes to reflect defense-tech autonomy positioning; competitive set should be Anduril/Helsing/Quantum Systems, not Nscale.

### idx=224 — Humans&

**Issue:** Row classifies in 'Humanoid & Service Robots' subsector and describes as 'Stealth AI company founded by former Google DeepMind researchers focused on embodied AI and physical intelligence.' Source describes Humans& as an AI software company building human-collaboration tools ('AI version of an instant messaging app'), founded by ex-Anthropic, xAI, Google researchers. Not embodied AI/humanoid. Investors include Nvidia, Bezos, GV, Emerson Collective beyond SV Angel/Harik.

**Stored:** `Subsector: Humanoid & Service Robots; ex-DeepMind embodied AI; lead SV Angel + Georges Harik`
**Source says:** Human-centric AI software for collaboration; founders ex-Anthropic, xAI, Google; backers Nvidia, Bezos, SV Angel, GV, Emerson Collective
**Suggested fix:** Reclassify subsector to Software & Simulation (or remove from physical-AI universe entirely if out-of-scope); rewrite notes; expand lead investors list.

### idx=234 — RobCo

**Issue:** Row says location 'USA' but RobCo is founded in Munich, Germany (with US expansion). Lead investor stored as null; source identifies Lightspeed Venture Partners + Lingotto Innovation as co-leads.

**Stored:** `Location: USA; lead_investors: null`
**Source says:** Founded Munich, Germany (now also SF/Austin); co-led by Lightspeed and Lingotto Innovation
**Suggested fix:** Change location to Germany (Munich); populate lead_investors with Lightspeed + Lingotto.

### idx=237 — Konnex

**Issue:** Row describes Konnex as 'Connected worker platform integrating IoT with frontline manufacturing operations' competing with Tulip/PTC/Augmentir. Source describes Konnex as a blockchain/DePIN-based platform for orchestrating autonomous robots — KNX tokens, on-chain physical economy. Wrong product category.

**Stored:** `Connected worker IoT platform; competes with Tulip/PTC/Augmentir`
**Source says:** Blockchain/DePIN platform decentralizing autonomous robotic labor; smart contracts; KNX tokens
**Suggested fix:** Rewrite notes to reflect blockchain/robot-orchestration positioning; competitive set is closer to Auki Labs/Geodnet than Tulip.

### idx=240 — Positron

**Issue:** Row says Positron 'designs AI inference chips using photonic computing architecture.' Source describes Positron as developing memory-centric chips for AI inference (Atlas chip). No mention of photonic architecture — competes more with NVIDIA than with photonic startups.

**Stored:** `Photonic computing architecture`
**Source says:** AI inference chips with focus on memory; Atlas chip matches H100 at <1/3 power; no photonics mention
**Suggested fix:** Remove 'photonic' from notes; reframe as memory-bound or alternative-architecture AI inference.

### idx=243 — Olix Computing

**Issue:** Row says 'UK-based AI chip company designing custom silicon for large-scale AI training' and competes with Cerebras/Graphcore on training. Source describes Olix as photonic AI inference chips (OTPU), explicitly inference-focused, ships 2027. Wrong workload category (training vs inference).

**Stored:** `Custom silicon for AI training`
**Source says:** Photonic OTPU AI inference chips; first products ship 2027
**Suggested fix:** Change focus from training to inference; reframe competitive set with Lightmatter, Lightelligence, etc.

### idx=254 — FieldAI

**Issue:** Source URL is bare fieldai.com homepage (pre-flagged). $314M Series A actually closed in August 2025 (announced Aug 20, 2025), not February 2026. Row date is materially wrong (~6 months). Lead 'Multiple' is technically OK — co-led by Bezos Expeditions, Prysm, Temasek.

**Stored:** `2026-02-20`
**Source says:** Aug 20, 2025; co-leads Bezos Expeditions, Prysm, Temasek
**Suggested fix:** Move row to 3Q25 (August 2025); update source URL to canonical PR; expand lead investors.

### idx=263 — Sophia Space

**Issue:** Row describes Sophia Space as 'satellite-based photovoltaic energy monitoring systems for solar farm optimisation.' Source describes Sophia Space as a developer of modular cooling and TILES processors for ORBITAL (space-based) data centers — i.e., orbital data center infrastructure, not solar monitoring. Sector should be In-Orbit Services or Frontier Compute, not Satellite Communications.

**Stored:** `Satellite PV energy monitoring`
**Source says:** Modular cooling + TILES servers for space-based data centers (orbital DC)
**Suggested fix:** Rewrite notes; reclassify subsector to In-Orbit Services or Frontier Compute.

### idx=270 — PLD Space

**Issue:** Row says €209M with no lead. Source confirms €180M Series C (with €30M EIB later, total ~€210M) led by Mitsubishi Electric Corporation as strategic customer/investor. Row's note attributes Mitsubishi-led deal to Tulip (idx 222) but PLD Space's actual lead is Mitsubishi Electric — same investor twice in 1Q26.

**Stored:** `€209M Series C, lead null`
**Source says:** €180M Series C led by Mitsubishi Electric (plus EIB €30M later for total ~€210M)
**Suggested fix:** Adjust amount_m to ~180 (or split EIB tranche separately); set lead_investors to Mitsubishi Electric.

### idx=277 — Mind Robotics

**Issue:** Row classifies Mind Robotics as 'Chinese humanoid robot company' located in China with null lead. Source: Mind Robotics is a Rivian spinout based in the USA, founded by Rivian CEO RJ Scaringe; $500M Series A co-led by Andreessen Horowitz and Accel; focuses on industrial factory robots (NOT humanoids). All four core fields wrong: location, lead, sector, product type.

**Stored:** `China; humanoid; null lead`
**Source says:** USA (Rivian spinout); industrial factory robots; co-led Andreessen Horowitz + Accel; $2B valuation
**Suggested fix:** Major rewrite: change location to USA, subsector to Industrial Robots, populate lead investors, rewrite notes entirely.

### idx=278 — Sunday

**Issue:** Row says Thailand (Bangkok), Collaborative Robots subsector, agriculture/outdoor. Source: Sunday is based in Mountain View, California, builds household humanoid robots (dishwashing, laundry — Memo robot), Series B led by Coatue at $1.15B valuation. All key fields wrong.

**Stored:** `Thailand (Bangkok); Collaborative Robots; agriculture; null lead`
**Source says:** Mountain View CA; humanoid household robotics (Memo); Coatue lead
**Suggested fix:** Major rewrite: location, subsector (Humanoid & Service Robots), notes; populate lead Coatue.

### idx=280 — AmpliSi

**Issue:** Row says USA, Materials/Silicon & Substrates, $2.5M pre-seed competing with Shin-Etsu/SUMCO. Source: AmpliSi is a UK (Sheffield) university spinout developing porous silicon ANODES for lithium-ion batteries (not silicon substrates for semiconductors); £2M (~$2.5M) pre-seed led by Northern Gritstone + Clean Growth Fund. Wrong location, wrong product (battery anodes, not wafer substrates), wrong competitive set.

**Stored:** `USA; silicon substrates for semiconductors`
**Source says:** UK (Sheffield); porous silicon anodes for lithium-ion batteries; £2M pre-seed
**Suggested fix:** Major rewrite: location to UK, subsector to Battery Materials, lead investors, full notes.

### idx=285 — Swarmer

**Issue:** Row says 'IPO'd on public market' with location Israel and links to en.globes.co.il (TASE-implied). Source: Swarmer IPO'd on NASDAQ (ticker SWMR), priced at $5/share with 3M shares for ~$15M raise, surged 450% on debut March 17, 2026. The company is software-first (drone swarm software), founded with Ukrainian wartime deployment experience — not an Israeli TASE-listed company. Listing venue and possibly origin wrong.

**Stored:** `Israel; TASE-implied URL; null lead`
**Source says:** NASDAQ listing (SWMR); $5/share IPO; ~$15M; software-first drone swarm company
**Suggested fix:** Change exchange/location framing to NASDAQ-listed; verify HQ (Ukraine vs Israel); update source URL to NASDAQ filing.

### idx=286 — Nth Cycle

**Issue:** Row presents the $1.1B as a funding round at undisclosed stage. Source: $1.1B is a 10-year OFFTAKE AGREEMENT with Trafigura to supply refined battery metals — not equity funding. This is a commercial supply contract, not capital raised by Nth Cycle.

**Stored:** `$1.1B undisclosed funding round`
**Source says:** 10-year $1.1B offtake/supply agreement with Trafigura (not equity)
**Suggested fix:** Reclassify entry: either remove from funding rounds dataset entirely, or change round type to 'Offtake/Commercial Agreement' and amount to $1.1B contract value (not capital raised).

### idx=289 — Unitree Robotics

**Issue:** Row says 'filing for Hong Kong IPO.' Source: Unitree filed for STAR Market (Shanghai Stock Exchange) IPO on March 20, 2026 — NOT Hong Kong. Targeting CNY 4.2B (~$608M). Wrong listing venue.

**Stored:** `Hong Kong IPO`
**Source says:** STAR Market (Shanghai) IPO filing
**Suggested fix:** Change listing venue to Shanghai STAR Market; correct robotnik_notes.

### idx=291 — Lace

**Issue:** Row says USA fabless semiconductor with limited info. Source: Lace is Norway-based, makes chip-MAKING EQUIPMENT (helium ion beam lithography), $40M round backed by Microsoft. Not fabless design — semicap equipment. Wrong location AND wrong subsector.

**Stored:** `USA; Fabless Design; limited info`
**Source says:** Norway; Equipment (helium beam lithography); Microsoft-backed
**Suggested fix:** Change location to Norway; subsector to Equipment; rewrite notes.

### idx=292 — Stateful Robotics

**Issue:** Row says USA, Collaborative Robots, $4.8M pre-seed, lead null. Source: Stateful Robotics is an Oxford UK university spinout, lead Amadeus Capital Partners + Oxford Science Enterprises, focused on long-horizon decision-making/persistent memory for physical AI (closer to Software & Simulation than Collaborative Robots).

**Stored:** `USA; Collaborative Robots; lead null`
**Source says:** UK (Oxford spinout); Software/AI for physical robots; Amadeus Capital + Oxford Science Enterprises
**Suggested fix:** Change location to UK; subsector to Software & Simulation; populate lead_investors.

### idx=296 — PAVE Space

**Issue:** Row says USA, generic 'space components,' lead null. Source: PAVE Space is Switzerland-based, builds in-space propulsion / orbital transfer vehicles (OTVs / kickstages), $40M seed co-led by Visionaries Club and Creandum. Location, product, lead all need correction.

**Stored:** `USA; generic Space Components; lead null`
**Source says:** Switzerland; in-space propulsion / orbital transfer; co-led Visionaries Club + Creandum
**Suggested fix:** Change location; refine subsector to In-Orbit Services or refine notes; populate lead investors.

### idx=298 — Vulcan Elements

**Issue:** Source says $65M Series A was announced in August 2025 (not March 25, 2026 as stored). Date materially wrong by ~7 months. Also: Pentagon's $620M loan to Vulcan was announced November 2025. Lead Altimeter Capital + One Investment Management.

**Stored:** `2026-03-25`
**Source says:** Aug 2025 ($65M Series A); Pentagon $620M loan Nov 2025
**Suggested fix:** Move row to 3Q25; check whether the row is actually trying to log a different (later) Vulcan event.

### idx=301 — Arkadia Space

**Issue:** Row describes Arkadia as 'satellite thermal protection and materials technology' company. Source: Arkadia Space is developing GREEN PROPULSION (hypergolic bipropellant based on high-concentration hydrogen peroxide), not thermal protection. €14.5M total (€2.5M grant + €6M EIC equity + €6M private), not €16M.

**Stored:** `Thermal protection materials; €16M`
**Source says:** Green propulsion (H2O2-based); €14.5M total
**Suggested fix:** Rewrite notes to reflect green propulsion; adjust amount to 14.5; subsector probably Launch or In-Orbit Services rather than Space Components.

### idx=302 — Torngat Metals

**Issue:** Source dates the C$165M (~$120M USD) bridge financing announcement to June 17, 2025 — not March 26, 2026 as stored. Date is wrong by ~9 months. Otherwise EDC + CIB co-financing and Strange Lake project details are correct.

**Stored:** `2026-03-26`
**Source says:** June 17, 2025
**Suggested fix:** Move row to 2Q25 (June 2025); or replace with a later 2026 Torngat-specific event if one exists (Ottawa $175M commitment was reported in March 2026).

### idx=306 — Starfish Space

**Issue:** Source URL is bare spacenews.com homepage (pre-flagged placeholder). Real raise was over $100M Series B led by Point72 Ventures with Activate Capital and Shield Capital co-leading; announcement date is around April 2026 (per Via Satellite & SpaceNews coverage), not March 31. Row stores lead as 'Multiple' and amount $110M.

**Stored:** `Lead 'Multiple'; date 2026-03-31; source bare domain`
**Source says:** Lead Point72 Ventures with Activate + Shield co-leads; announced ~April 2026
**Suggested fix:** Replace source URL; populate lead_investors with Point72 Ventures; verify whether this is March-end or April announcement.

---

## ⚠️ MEDIUM GAP (17 rows) — fixable data gaps where source has the missing info

Most are `lead_investors=Undisclosed`/null where the source explicitly names them (WIRobotics-pattern). A few are wrong-location or claim-without-source-evidence cases.

### idx=227 — Zipline

**Issue:** Row says lead is 'Valor Equity Partners' alone; source identifies Fidelity, Baillie Gifford, Valor Equity Partners, and Tiger Global as co-leads. Date Jan 22 vs source Jan 21 (1 day off).
**Stored:** `Lead: Valor Equity Partners`
**Source says:** Co-led by Fidelity Management & Research, Baillie Gifford, Valor Equity Partners, Tiger Global
**Suggested fix:** Expand lead investors list; align date to 2026-01-21.

### idx=230 — Hadrian

**Issue:** Row stores amount as null and lead as null; source confirms ~$260M raise at $1.6B valuation led by T. Rowe Price (with Altimeter, D1, StepStone, 1789 Capital, Founders Fund, Lux, a16z, Construct).
**Stored:** `amount_m: null; lead_investors: null`
**Source says:** $260M at $1.6B valuation, led by T. Rowe Price with broad participation
**Suggested fix:** Populate amount_m=260 and lead_investors='T. Rowe Price'; expand notes with Mesa, AZ Factory 3 milestone.

### idx=236 — Nomagic

**Issue:** Row lead_investors=null; source identifies Cogito Capital Partners as lead.
**Stored:** `lead_investors: null`
**Source says:** Led by Cogito Capital Partners
**Suggested fix:** Populate lead_investors with Cogito Capital Partners.

### idx=246 — Tomorrow.io

**Issue:** Row lead_investors=null and stored date 2026-02-12; source confirms lead is Stonecourt Capital and HarbourVest, with date Feb 3, 2026 (9 days off).
**Stored:** `lead_investors: null; date: 2026-02-12`
**Source says:** Lead: Stonecourt Capital and HarbourVest; date Feb 3, 2026
**Suggested fix:** Populate lead_investors with Stonecourt + HarbourVest; correct date to 2026-02-03.

### idx=247 — Axiom Space

**Issue:** Row tags as 'Debt Financing' with null lead. Source describes the $350M as a hybrid equity+debt mix co-led by Type One Ventures and Qatar Investment Authority (QIA), with 1789 Capital, 4iG, LuminArx Capital Management, and Kam Ghaffarian also participating.
**Stored:** `Round: Debt Financing; lead: null`
**Source says:** Hybrid equity+debt mix, co-led Type One Ventures and QIA
**Suggested fix:** Change round to 'Hybrid (Equity + Debt)' or split into two entries; add lead investors.

### idx=255 — AI2 Robotics

**Issue:** Row says location 'China (Beijing)' and lead null; source says Shenzhen and lists named investors Baidu, CRRC, Yusys Technologies, Sentury Tire, Guotai Haitong Securities. Date Feb 23 vs Feb 24 (1 day off).
**Stored:** `Location: China (Beijing); lead_investors: null`
**Source says:** Shenzhen; investors Baidu, CRRC, Yusys, Sentury, Guotai Haitong
**Suggested fix:** Change location to Shenzhen; add investors; align date.

### idx=264 — Nio GeniTech

**Issue:** Row lead 'IDG Capital, Nio Capital'; source identifies a broader investor group: Hefei State-owned Investment, Hefei Haiheng, IDG, China Fortune-Tech Capital, Hua Capital. Hefei (Anhui) involvement suggests location may be Hefei rather than Shanghai as stored.
**Stored:** `Lead: IDG Capital, Nio Capital; location Shanghai`
**Source says:** Lead: Hefei State-owned Investment + Hefei Haiheng + IDG + China Fortune-Tech + Hua Capital; likely Hefei base
**Suggested fix:** Expand lead_investors; verify HQ location (likely Hefei).

### idx=273 — Eridu

**Issue:** Row says 'limited details, lead investor undisclosed.' Source confirms Eridu is an AI networking chip company (high-radix networking for AI), founded by Drew Perkins and Omar Hassen (ex-Broadcom/Marvell). Round led by Socratic Partners, John Doerr, Matter Venture Partners with Hudson River Trading, Capricorn, MediaTek, Bosch Ventures, TDK, Eclipse, VentureTech Alliance (TSMC).
**Stored:** `Description vague; lead null`
**Source says:** AI networking chip startup; lead Socratic Partners + John Doerr + Matter Venture Partners
**Suggested fix:** Rewrite notes; populate lead_investors; note founders' Broadcom/Marvell pedigree.

### idx=274 — Rhoda AI

**Issue:** Row lead null and notes call it 'AI-powered robotics software company (stealth mode).' Source: Rhoda exited stealth on March 10 with $450M Series A led by Khosla Ventures, with Temasek, Mayfield, Capricorn, Premji Invest, John Doerr; valuation $1.7B; uses video-pretrained DVA models for robotic intelligence.
**Stored:** `Stealth; lead null`
**Source says:** Exited stealth; lead Khosla Ventures (with Temasek, Mayfield, etc.); $1.7B valuation
**Suggested fix:** Update lead_investors; rewrite notes to reflect FutureVision/DVA models, video-pretraining approach.

### idx=279 — Xscape Photonics

**Issue:** Row lead null; source identifies Addition (new investor) as lead with continued participation by IAG Capital Partners and NVIDIA. Date March 11 confirmed.
**Stored:** `lead_investors: null`
**Source says:** Led by Addition; continued IAG Capital Partners, NVIDIA
**Suggested fix:** Populate lead_investors with Addition.

### idx=284 — Frore Systems

**Issue:** Row lead null; source says lead is MVP Ventures with participation from Fidelity, Mayfield, Addition, Qualcomm Ventures, Alumni Ventures.
**Stored:** `lead_investors: null`
**Source says:** Lead: MVP Ventures
**Suggested fix:** Populate lead_investors with MVP Ventures.

### idx=287 — KEWAZO

**Issue:** Row lead null; source identifies Schooner Capital as lead with Chevron Technology Ventures, Asahi Kasei, and others co-investing.
**Stored:** `lead_investors: null`
**Source says:** Lead: Schooner Capital with Chevron Technology Ventures, Asahi Kasei et al.
**Suggested fix:** Populate lead_investors.

### idx=288 — Rivr

**Issue:** Row says acquirer 'undisclosed.' Source: Amazon acquired Rivr (March 19, 2026) — acquirer is now public. Rivr is a stair-climbing legged delivery robot startup spun out of ETH Zurich's Robotic Systems Lab.
**Stored:** `Acquirer undisclosed`
**Source says:** Acquirer: Amazon
**Suggested fix:** Populate lead_investors / acquirer with Amazon; rewrite notes to mention legged-delivery robots and ETH Zurich heritage.

### idx=290 — Kandou AI

**Issue:** Row lead null; source identifies Maverick Silicon as lead with strategic participation from SoftBank, Synopsys, Cadence Design Systems, and Alchip Technologies. Round is Series A (oversubscribed), valuation ~$400M per Bloomberg. Description should clarify this is high-speed connectivity (not just generic interconnect IP).
**Stored:** `lead null; round 'Undisclosed'`
**Source says:** Series A; lead Maverick Silicon; SoftBank/Synopsys/Cadence/Alchip strategic
**Suggested fix:** Populate lead_investors; change round to 'Series A'.

### idx=294 — Normal Computing

**Issue:** Row lead null; source says Samsung Catalyst Fund led with Galvanize, Brevan Howard, ArcTern, Celesta, Drive Capital, First Spark Ventures, Micron Ventures.
**Stored:** `lead_investors: null`
**Source says:** Lead: Samsung Catalyst Fund
**Suggested fix:** Populate lead_investors with Samsung Catalyst.

### idx=295 — Lucid Bots

**Issue:** Row lead null; source says co-led Cubit Capital + Idea Fund Partners. Notes contain self-referential phrasing 'Competes with Lucid Bots in drone-based cleaning' (typo/error).
**Stored:** `lead_investors: null`
**Source says:** Co-led: Cubit Capital + Idea Fund Partners
**Suggested fix:** Populate lead_investors; fix self-referential phrase in notes.

### idx=300 — Shield AI

**Issue:** Row says $2B Series G at $18B+ valuation with Advent + JPMorgan as lead. Source confirms $1.5B equity + $500M preferred equity (~$2B package), led by Advent International with JPMorgan Strategic Investment Group co-leading; Blackstone separately weighing additional $750M. Valuation reportedly $12.7B (per article URL slug), not $18B as row asserts.
**Stored:** `$2B; ~$18B+ valuation`
**Source says:** $1.5B equity + $500M preferred; ~$12.7B valuation
**Suggested fix:** Correct valuation and/or split into equity vs preferred.

---

## ℹ️ MINOR DISCREPANCY (25 rows) — small framing/granularity differences

These are framing nuances (e.g. "Series A" vs source's "Series A-3"), 1-7 day date offsets, slight rounding, or notes emphasis differences that don't change product description. Low priority — could be left as-is or batch-fixed.

| idx | company | issue (one-line) |
|---|---|---|
| 214 | Moonshot AI | Source dates announcement Dec 31, 2025; row stores 2026-01-01 (1 day off, likely timezone). Lead investor noted in row as IDG Capital but article does not speci |
| 219 | Skild AI | Row credits SoftBank as sole lead; source says SoftBank with participation from Nvidia, Macquarie, 1789 Capital. Row says largest robotics software raise — defe |
| 221 | Mytra | Source dates Jan 15 not Jan 14 (1 day off). Round details otherwise match. |
| 222 | Tulip Interfaces | Source says Jan 13 announcement (row Jan 14, 1 day off). Lead Mitsubishi Electric and amount confirmed. Notes contain typo 'Tulip competes with Tulip competes w |
| 226 | SpinQ Technology | Specific revenue/operations claims (40 countries, 65% superconducting revenue, 80% YoY growth) are confirmed by parallel reporting (36kr/quantum sources). Lead  |
| 231 | StepFun | Stored amount $718M; source says $717M (rounding ok). Row says lead Shanghai SDIC; source mentions Tencent increased stake along with state-backed Shanghai SDIC |
| 239 | Cerebras Systems | Source dates Feb 3, 2026; row says Feb 4 (1 day off). Otherwise lead Tiger Global and $1B Series H confirmed. |
| 241 | Bedrock Robotics | Row's industry framing: 'AI-powered industrial robotics company building autonomous systems for heavy manufacturing.' Source describes Bedrock as autonomous con |
| 248 | Galaxea AI | Row lists only Jinding Capital as lead; source identifies Jinding Capital, BAIC Group Industrial Investment, and Hone Capital as new investors with Cathay Capit |
| 249 | iSpace | Round announced Feb 9-10, 2026 (row says Feb 12, 2-3 days off). Lead Cowin + Jingming + Spring Partners + Chengdu Industry Group + Qianlima — row only lists Cow |
| 251 | ChipAgents | Source describes round as 'Series A1' rather than 'Series A'. $50M round, $74M total. Otherwise lead Matter Venture Partners confirmed. |
| 252 | World Labs | Row's lead investor list excludes Andreessen Horowitz which appears in source as participant. Otherwise matches. |
| 253 | Taalas | Lead is Quiet Capital + Fidelity + Pierre Lamond per source; row lists only Quiet Capital. 73x H200 claim is verified as company-asserted in Reuters/SiliconAngl |
| 256 | Axelera AI | Row lead Innovation Industries; source confirms Innovation Industries lead with BlackRock and SiteGround Capital as new participants. |
| 258 | SambaNova | Row lead 'Vista Equity Partners, Cambium Capital'; source includes Intel Capital as third lead investor. |
| 259 | Spirit AI | Row lead 'Chaos Investment, YF Capital'; source adds HongShan Capital Group and Chongqing Industrial Investment Mother Fund as participants. $290M reported as n |
| 260 | Wayve | Row mentions co-leads but source highlights additional automaker investors Mercedes-Benz, Nissan, Stellantis, plus existing investors Microsoft, Nvidia, Uber. R |
| 262 | Revel | Row describes Revel as 'AI-driven autonomous systems test and evaluation platform'; source frames as 'unified software platform for hardware visualization, tele |
| 266 | Sierra Space | Source dates announcement March 5, 2026 (row March 3, 2 days off). Lead LuminArx Capital confirmed; existing investors General Atlantic, Coatue, Moore Strategic |
| 268 | Vast | Source dates announcement March 9, 2026 (row March 3, 6 days off). |
| 282 | DOE CMEI Program | Source confirms $500M Notice of Funding Opportunity (NOFO) for critical minerals processing/recycling/battery manufacturing. Row says 'grant programme' which is |
| 293 | SatEnlight | Row already notes the Via Satellite source dates announcement to Feb 2026 vs row's March 24, 2026. €995K seed (~$1.2M) confirmed; lead investor not specified by |
| 299 | Rebellions | Row lead 'South Korean government'; source specifies South Korea's National Growth Fund — first direct equity investment in domestic AI accelerator. Date March  |
| 303 | Performance Drone Works | Source dates announcement March 25, 2026 (row says March 26, 1 day off). Lead Ondas confirmed; co-investors Hood River, Cedar Pine, Hanwha Asset Management, Boo |
| 304 | Physical Intelligence | Row implies round closed at $1B Series C; source describes the round as in talks/reportedly raising $1B at >$11B valuation, Founders Fund and Lightspeed in disc |

---

## 🔗 SOURCE_PLACEHOLDER (5 rows) — bare-domain URLs, no row-specific content

Source URLs are bare homepages (e.g. `https://techcrunch.com`, `https://nist.gov`). Cannot have row-specific information. Need replacement source URLs.

| idx | company | issue | suggested fix |
|---|---|---|---|
| 223 | USA Rare Earth | Source URL is bare 'https://nist.gov' homepage, not a specific article. Pre-flagged as placeholder. Underlying announcement (USAR LOI for $277M direct + $1.3B loan + $1.5B PIPE) is real and dates to Jan 26, 2026 (not Jan 15 as stored). | Replace source with NIST press release URL; correct date to 2026-01-26; clarify that $277M is direct funding portion of $1.6B LOI (with concurrent $1.5B PIPE). |
| 225 | PsiBot | Source URL is bare techcrunch.com homepage. Pre-flagged as placeholder. Search results suggest the cited $280M PsiBot round is reported in March 2026 not January 20 — date appears wrong as well. Company is dexterous-hands-focused per public reporting. | Find canonical PsiBot Series A press release; verify date (likely March 2026 not January); refine product description (dexterous hands/embodied AI not just 'humanoids for manufacturing'). |
| 229 | Cyclic Materials | Source URL is bare techcrunch.com homepage. Pre-flagged. Real announcement is Jan 23, 2026, $75M Series C led by T. Rowe Price (not 'Multiple') with Canada Growth Fund participation. | Replace source with cyclicmaterials.earth/businesswire URL; replace lead with T. Rowe Price. |
| 233 | Northwood Space | Source URL is bare techcrunch.com homepage. Pre-flagged. Real article exists at techcrunch.com/2026/01/27/northwood-space-secures-a-100m-series-b-and-a-50m-space-force-contract/. Stored data otherwise correct ($100M Series B, Washington Harbour + a16z, $49.8M Space Force contract). | Replace source with canonical TechCrunch article URL. |
| 305 | Starcloud | Source is bare techcrunch.com homepage. Pre-flagged. Real announcement: $170M Series A at $1.1B valuation, March 30, 2026, led by Benchmark and EQT Ventures. Row data otherwise matches. | Replace source URL with canonical TC link. |

---

## 🚫 SOURCE_UNREACHABLE (5 rows) — fetch failed (404/403/TLS/timeout)

URLs that returned errors. Some are likely real articles behind paywalls/regional blocks; others may be dead.

| idx | company | error | suggested fix |
|---|---|---|---|
| 235 | Waabi | CNBC URL returned 403. Search-corroborated: $750M Series C, but precise lead breakdown not confirmed by direct fetch. | Try alternate source (Bloomberg/TechCrunch) to verify lead investors. |
| 265 | Rapidus | Japan Times URL returned 403. Stored data ($1.7B / 100B yen Japan IPA, 2nm in Hokkaido) is consistent with general public knowledge of Rapidus. | Verify with METI or alternate Japanese-language source. |
| 271 | Elementium Materials | Direct fetch failed (cert expired). No corroborating coverage surfaced via search. Cannot verify $11M seed details. | Find alternate source (PR Newswire, BusinessWire, or VC site); validate company exists and amount. |
| 275 | Orqa | EU-Startups URL returned 403. Stored data plausible but unverified by direct fetch. | Try alternate EU defense-tech source. |
| 276 | Nexthop AI | BusinessWire URL returned 60s timeout. | Try secondary source (TC, SiliconAngle). |

---

## ✅ CLEAN (17 rows) — source matches stored data

| idx | company |
|---|---|
| 217 | NEU Battery Materials |
| 220 | Etched.ai |
| 228 | Neurophos |
| 232 | Ricursive Intelligence |
| 238 | Waymo |
| 242 | Stoke Space |
| 244 | Apptronik |
| 245 | Aalyria |
| 250 | Stark |
| 257 | MatX |
| 261 | OQ Technology |
| 267 | Ayar Labs |
| 269 | NEURA Robotics |
| 272 | Nscale |
| 281 | Elephantech |
| 283 | RoboForce |
| 297 | Xona Space Systems |

---

## Patterns observed

### Hallucinated product/category descriptions (6 rows)

Notes describe a fundamentally different company from what the source covers — Stark-pattern. Likely from filling notes via search-result snippets without reading the underlying article.

- **Mind Robotics** (idx=277) — stored as Chinese humanoid; actually Rivian-USA spinout for industrial factory robots
- **Sunday** (idx=278) — stored as Thailand agricultural cobot; actually Mountain View household humanoid (dishwasher robot)
- **Cambium** (idx=215) — stored as battery cathode materials; actually AI-driven advanced materials/composites
- **Lyte** (idx=216) — stored as classified DoD defense drone; actually civilian perception/vision platform from ex-Apple Face ID team
- **Harmattan AI** (idx=218) — stored as sovereign AI compute infrastructure; actually defense autonomy/mission software
- **Humans&** (idx=224) — stored as embodied/humanoid; actually AI software for human collaboration ("AI version of IM app")

### Wrong dates — 2025 events logged as 1Q26 (3 rows)

Likely a systematic ingestion bug — these are 2025 events that should belong in 3Q25 or 4Q25.

- **FieldAI** (idx=254) — closed Aug 2025, not Feb 2026. Belongs in 3Q25.
- **Vulcan Elements** (idx=298) — Series A announced Aug 2025, not March 2026.
- **Torngat Metals** (idx=302) — financing was June 2025, not March 2026.

### Wrong locations (6 rows)

Country attribution errors — UK companies logged as USA, etc.:
- AmpliSi & Stateful Robotics — UK Oxford/Sheffield spinouts logged as USA
- Mind Robotics, Sunday, Lace, PAVE Space, RobCo, etc.

### `lead_investors=null` when source names them (17 rows)

Most of the medium_gap bucket. WIRobotics-pattern. Source explicitly names lead but row says "Undisclosed"/null. Examples include Tomorrow.io, Hadrian, Frore, Normal Computing, Eridu, Rhoda, RobCo, Nomagic, Kandou, Lucid Bots, KEWAZO.

### Wrong listing venues (2 rows)

- **Unitree Robotics** — listed on Shanghai STAR Market, not Hong Kong as stored
- **Swarmer** — listed on NASDAQ, not TASE as stored

### Source quality

- 5 sources are bare-domain stubs (homepage URLs without specific articles)
- 5 sources are unreachable (paywalls, regional blocks, dead links)
- spacenews.com heavily rate-limited (429); cross-verified via web search
- techcrunch.com is the most-used domain (18 rows) but several entries point to its homepage rather than specific articles

---

## Recommendations

### Tier 1 — must-fix before VC export
1. Address all 24 `major_drift` items. Several involve Stark-pattern wrong-product descriptions that will visibly fail VC due-diligence.
2. Verify and correct the 3 wrong-date rows (FieldAI, Vulcan Elements, Torngat Metals) — they're currently in the wrong quarter, which corrupts time-series analysis.
3. Recheck Unitree listing venue (Shanghai STAR vs Hong Kong) — affects related_tickers and any cross-reference to public-market data.

### Tier 2 — high-value ROI
1. Backfill `lead_investors` for the 17 medium_gap rows where source names them. Mostly WowTale/SpaceNews/SiliconANGLE coverage that's easy to extract.
2. Fix the 5 source_placeholder URLs. Each one needs an alternate source.

### Tier 3 — defer
1. The 25 minor_discrepancy items can be batch-cleaned later or left as-is.
2. The 5 source_unreachable items: try once more with different fetch strategies, accept the 1-2 that remain dead.

### Process implication

1Q26 has the highest drift rate observed across any quarter (26% major drift, 71% any actionable issue). The 1Q24-4Q24 backfill batches I ran went through agent-driven verification with multiple sources per deal. The 1Q26 data appears to have been ingested differently — likely with thinner verification or LLM-generated notes from search snippets. Worth investigating the original ingestion process if you want to apply consistent quality bar going forward.

---

**End of integrity pass.** Read-only. Awaiting triage before mutating.