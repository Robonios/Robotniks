#!/usr/bin/env python3
"""
Populate value_chain on every active entity in entity_registry.json.

Per the locked 8-tier taxonomy (upstream → downstream):

  1. Upstream Materials              raw / refined inputs feeding fabs
                                      and manufacturers
  2. IP & Design                     fabless chip designers, EDA
                                      software, IP licensors
  3. Capital Equipment               machines used by fabs and
                                      manufacturers
  4. Fabrication & Manufacturing     physical production of chips,
                                      wafers, finished silicon at scale
  5. Components & Subsystems         finished building blocks
                                      (sensors, actuators, power,
                                      analog, motors, batteries)
  6. System Integration              whole systems — robots, rockets,
                                      satellites, vehicles
  7. Deployment & Operation          operators of deployed hardware —
                                      satellite operators, neoclouds,
                                      fleet operators, launch services
  8. Software & Services             pure-play software / simulation /
                                      middleware that sits alongside
                                      the physical stack

Tagging rules (from brief):
  R1  Parent entities get centre-of-gravity tag (no dual-tagging).
  R2  Fab-dominant IDMs → Fabrication & Manufacturing.
      Intel, Micron, Samsung-semi, SK Hynix.
  R3  Component-selling IDMs → Components & Subsystems.
      Texas Instruments, STMicroelectronics, Infineon, NXP, ON, MCHP,
      Renesas — they sell finished analog / power / MCU components.
  R4  EDA → IP & Design. Generic industrial sim (Ansys, Bentley) →
      Software & Services.
  R5  Integrators ship end-systems; operators run them. SpaceX the
      launch-vehicle builder = System Integration. Starlink as a
      service = Deployment & Operation. Use centre-of-gravity when
      rolled into one entity.

Authoritative home is entity_registry.json. calculate_metrics.py
propagates value_chain into public_markets.json alongside subsector.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "registries" / "entity_registry.json"

ALLOWED_TIERS = {
    "Upstream Materials",
    "IP & Design",
    "Capital Equipment",
    "Fabrication & Manufacturing",
    "Components & Subsystems",
    "System Integration",
    "Deployment & Operation",
    "Software & Services",
}

# ────────────────────────────────────────────────────────────────────
# Default tier by (sector, subsector). Per-ticker overrides below.
# ────────────────────────────────────────────────────────────────────
DEFAULT_BY_SUBSECTOR = {
    # ───── Semiconductors ─────
    ("Semiconductors", "EDA & IP"):               "IP & Design",
    ("Semiconductors", "Equipment"):              "Capital Equipment",
    ("Semiconductors", "Fabless Design"):         "IP & Design",
    ("Semiconductors", "Foundry"):                "Fabrication & Manufacturing",
    ("Semiconductors", "Frontier Compute"):       "IP & Design",
    # IDM default: component-seller (Rule 3). The fab-dominant IDMs
    # (INTC, MU, Samsung-semi, SK Hynix, WOLF) override to
    # "Fabrication & Manufacturing" below.
    ("Semiconductors", "IDM"):                    "Components & Subsystems",
    ("Semiconductors", "OSAT / Packaging & Test"):"Fabrication & Manufacturing",
    ("Semiconductors", "Power & Analog"):         "Components & Subsystems",

    # ───── Robotics ─────
    ("Robotics", "Autonomous Systems & Drones"):  "System Integration",
    ("Robotics", "Collaborative Robots"):         "System Integration",
    ("Robotics", "Frontier Compute"):             "IP & Design",
    ("Robotics", "Humanoid & Service Robots"):    "System Integration",
    ("Robotics", "Industrial Robots"):            "System Integration",
    ("Robotics", "Machine Vision & Sensors"):     "Components & Subsystems",
    ("Robotics", "Motion Control & Actuators"):   "Components & Subsystems",
    # Software & simulation platforms → Software & Services (Rule 4 tail).
    ("Robotics", "Software & Simulation"):        "Software & Services",
    ("Robotics", "Surgical & Medical"):           "System Integration",
    ("Robotics", "Surgical & Medical Robots"):    "System Integration",
    ("Robotics", "Test & Measurement"):           "Capital Equipment",
    ("Robotics", "Warehouse & Logistics"):        "System Integration",
    ("Robotics", "Warehouse & Logistics Automation"): "System Integration",

    # ───── Materials ─────
    ("Materials", "Battery Materials"):           "Upstream Materials",
    ("Materials", "Frontier Compute"):            "Upstream Materials",
    ("Materials", "Industrial & Specialty Gases"):"Upstream Materials",
    ("Materials", "Packaging & Substrates"):      "Upstream Materials",
    ("Materials", "Process Chemicals"):           "Upstream Materials",
    ("Materials", "Rare Earths & Critical Minerals"): "Upstream Materials",
    ("Materials", "Silicon & Substrates"):        "Upstream Materials",
    ("Materials", "Structural Materials"):        "Upstream Materials",

    # ───── Space ─────
    ("Space", "Earth Observation"):               "Deployment & Operation",
    ("Space", "Frontier Compute"):                "Components & Subsystems",
    ("Space", "Ground Systems & Antennas"):       "Components & Subsystems",
    # In-Orbit Services companies typically BUILD the spacecraft they
    # operate. Centre of gravity is the spacecraft itself (ispace lunar
    # lander, Intuitive Machines, Voyager Tech etc.) → System Integration.
    # Pure-service operators are overridden per-ticker below.
    ("Space", "In-Orbit Services"):               "System Integration",
    ("Space", "Launch"):                          "System Integration",
    ("Space", "Satellite Comms"):                 "Deployment & Operation",
    ("Space", "Satellite Communications"):        "Deployment & Operation",
    ("Space", "Space Components"):                "Components & Subsystems",

    # ───── Token ─────
    # Crypto tokens / protocols / networks tied to frontier-tech themes.
    # Not rendered on the Frontier Assets page but every registry entity
    # gets tagged for completeness. Default is Software & Services
    # (protocols / on-chain software). Per-ticker overrides below handle
    # tokens that are explicitly infrastructure operators (IoT networks,
    # RTK grids, sensor networks).
    ("Token", ""):                                "Software & Services",
}


# Tokens that operate physical-world infrastructure on-chain — treat as
# Deployment & Operation rather than pure software (Rule 5).
TOKEN_OPERATORS = {
    "IOTX",    # IoTeX — IoT device network
    "GEOD",    # Geodnet — RTK precision positioning network
    "SLC",     # Silencio — noise sensor network
    "NATIX",   # NATIX — dashcam-driven road intelligence network
    "ONO",     # Onocoy — RTK network
    "ROVR",    # ROVR Network — GPS / precision positioning
    "EDGE",    # Edge — distributed edge compute
}


# ────────────────────────────────────────────────────────────────────
# Per-ticker overrides. Each comes with a one-line rationale.
# Edge cases are reported at the end of the run.
# ────────────────────────────────────────────────────────────────────
OVERRIDES = {
    # ── Rule 2: fab-dominant IDMs → Fabrication & Manufacturing ──
    "INTC":      ("Fabrication & Manufacturing", "R2 fab-dominant IDM; foundry is the moat"),
    "MU":        ("Fabrication & Manufacturing", "R2 fab-dominant IDM (memory fab)"),
    "WOLF":      ("Fabrication & Manufacturing", "R2 SiC fab-dominant vertical"),
    # Samsung, SK Hynix if/when in registry — add here.

    # ── Rule 5: integrators vs operators ──
    # Mobileye: ships EyeQ SoCs + full ADAS stacks into automakers'
    # cars. Revenue centre is chips-as-components → Components & Subsystems.
    "MBLY":      ("Components & Subsystems", "R5 sells EyeQ SoCs into OEM systems"),
    # Virgin Galactic: builds vehicles but centre of gravity is
    # operating the tourism flights → Deployment & Operation.
    "SPCE":      ("Deployment & Operation", "R5 centre-of-gravity is running flights"),
    # Serve Robotics: builds + operates its own delivery fleet →
    # operator by centre of gravity.
    "SERV":      ("Deployment & Operation", "R5 runs its own delivery fleet"),

    # ── Rule 3 edge calls: component-heavy IDM-like businesses with
    #    non-IDM subsector tags ──
    # 600111 (China Northern Rare Earth) was put into a Robotics
    # subsector by registry convention. Business is rare-earth mining.
    # Value-chain position is upstream materials.
    "600111":    ("Upstream Materials", "Business is rare-earth mining regardless of registry sector tag"),

    # ── Industrial / commercial software platforms in Robotics sector ──
    # Siemens AG rolls up factory automation + industrial software
    # into a single listing. Centre of gravity per the worked examples
    # is Software & Services.
    "SIE GR":    ("Software & Services", "Worked-example locked: Siemens AG"),
    "EMR":       ("Software & Services", "R4 industrial control + software platforms"),
    "ROK":       ("Software & Services", "R4 industrial automation software platform"),
}


def main():
    with open(REGISTRY) as f:
        reg = json.load(f)

    applied = 0
    skipped_excluded = 0
    unknown = []
    edge_cases = []

    for ticker, entry in reg.items():
        if not isinstance(entry, dict):
            continue
        if entry.get("status") == "excluded":
            skipped_excluded += 1
            continue

        sector = entry.get("sector") or ""
        key_sector = {
            "Materials & Inputs": "Materials",
            "Semiconductor": "Semiconductors",
        }.get(sector, sector)
        subsector = entry.get("subsector") or ""

        override = OVERRIDES.get(ticker)
        if override:
            tier, reason = override
            edge_cases.append((ticker, sector, subsector, tier, reason))
        elif key_sector == "Token" and ticker in TOKEN_OPERATORS:
            tier = "Deployment & Operation"
            edge_cases.append((ticker, sector, subsector, tier,
                               "Token operates physical-world infrastructure"))
        else:
            tier = DEFAULT_BY_SUBSECTOR.get((key_sector, subsector))
            if not tier and key_sector == "Token":
                # Catch-all for tokens without a subsector.
                tier = "Software & Services"
            if not tier:
                unknown.append((ticker, sector, subsector, entry.get("name")))
                continue

        assert tier in ALLOWED_TIERS, f"Illegal tier {tier!r} for {ticker}"
        entry["value_chain"] = tier
        applied += 1

    with open(REGISTRY, "w") as f:
        json.dump(reg, f, indent=2)

    # ────────── Validation report ──────────
    print(f"Set value_chain on {applied} entities (skipped {skipped_excluded} excluded).")

    # Completeness + distribution by tier
    from collections import Counter
    tiers = Counter(v.get("value_chain") for k, v in reg.items()
                    if isinstance(v, dict) and v.get("status") != "excluded" and v.get("value_chain"))
    total = sum(tiers.values())
    print("\nDistribution by tier:")
    for t in ["Upstream Materials", "IP & Design", "Capital Equipment",
             "Fabrication & Manufacturing", "Components & Subsystems",
             "System Integration", "Deployment & Operation", "Software & Services"]:
        count = tiers.get(t, 0)
        pct = (count / total * 100) if total else 0
        flag = "  ← ZERO"            if count == 0 else \
               f"  ← {pct:.0f}% CONCENTRATED" if pct > 50 else ""
        print(f"  {t:34s} {count:>4d}  ({pct:.1f}%){flag}")

    # Orthogonality — any entity where subsector reads identical to
    # value_chain after the update?
    ortho_issues = []
    for k, v in reg.items():
        if not isinstance(v, dict):
            continue
        if v.get("status") == "excluded":
            continue
        sub = (v.get("subsector") or "").strip()
        vc = (v.get("value_chain") or "").strip()
        if sub and vc and sub.lower() == vc.lower():
            ortho_issues.append((k, sub, vc))
    print(f"\nOrthogonality check: {len(ortho_issues)} entities with identical subsector/value_chain")
    for k, sub, vc in ortho_issues[:10]:
        print(f"  {k}  sub={sub!r}  vc={vc!r}")

    # Edge cases (Rules 2/3/5 applied)
    print(f"\nEdge-case overrides applied ({len(edge_cases)}):")
    for ticker, sector, subsector, tier, reason in edge_cases:
        print(f"  {ticker:10s} sector={sector:15s} sub={subsector:30s} → {tier:30s}  [{reason}]")

    # Anything still missing
    if unknown:
        print(f"\nUNKNOWN — no tier assigned ({len(unknown)}):")
        for t, s, sub, n in unknown:
            print(f"  {t}  sector={s}  subsector={sub}  name={n}")


if __name__ == "__main__":
    main()
