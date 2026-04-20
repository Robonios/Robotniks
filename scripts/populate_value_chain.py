#!/usr/bin/env python3
"""
Populate value_chain_tier on every visible public-markets entity in
data/markets/enrichment_data.json.

Per the glossary:
  "Value-Chain Tier: The entity's position in the supply chain, from
   upstream materials to downstream system deployers."

This is distinct from `subsector` (which describes what the company
MAKES within its sector). The tier describes WHERE in the supply
chain it sits. A Japanese precision-bearing manufacturer and a
humanoid-robot integrator may both sit in the Robotics sector and
have distinct subsectors, but the bearing-maker is mid-chain
Components & Subsystems and the humanoid builder is downstream
System Integration.

Taxonomy (upstream → downstream):

  1. Upstream Materials        rare earths, gases, chemicals, wafers,
                               substrates, structural materials
  2. Capital Equipment         manufacturing equipment for fabs,
                               robotics factories, satellite assembly,
                               test & measurement hardware
  3. IP & EDA                  chip IP licensing, EDA software,
                               pre-silicon enablers
  4. Fabless Design            chip design without owning a fab
  5. Manufacturing             silicon fabrication — foundries + IDMs
  6. Packaging & Test          OSAT, post-fab packaging
  7. Components & Subsystems   sensors, actuators, motion parts,
                               power / analog chips that feed into
                               larger integrated systems, satellite
                               components, ground-station hardware
  8. System Integration        complete systems: industrial robots,
                               humanoid robots, launch vehicles,
                               satellites, drones, warehouse automation
                               platforms, surgical robots
  9. Deployment & Operation    end-service providers: satellite
                               comms operators, earth observation
                               service providers, industrial
                               software / simulation platforms

The mapping is driven by (sector, subsector) with per-ticker overrides
for cases where the default doesn't fit. Idempotent — writes the
value every run so the taxonomy stays consistent across future
subsector refinements.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_MARKETS = ROOT / "data" / "markets" / "robotnik_public_markets.json"
ENRICHMENT = ROOT / "data" / "markets" / "enrichment_data.json"


# Default (sector, subsector) → tier. Exceptions handled below in OVERRIDES.
DEFAULT_BY_SUBSECTOR = {
    # ───── Semiconductors ─────
    ("Semiconductors", "EDA & IP"):               "IP & EDA",
    ("Semiconductors", "Equipment"):              "Capital Equipment",
    ("Semiconductors", "Fabless Design"):         "Fabless Design",
    ("Semiconductors", "Foundry"):                "Manufacturing",
    ("Semiconductors", "Frontier Compute"):       "Fabless Design",
    ("Semiconductors", "IDM"):                    "Manufacturing",
    ("Semiconductors", "OSAT / Packaging & Test"):"Packaging & Test",
    ("Semiconductors", "Power & Analog"):         "Components & Subsystems",

    # ───── Robotics ─────
    ("Robotics", "Autonomous Systems & Drones"):  "System Integration",
    ("Robotics", "Collaborative Robots"):         "System Integration",
    ("Robotics", "Frontier Compute"):             "Fabless Design",
    ("Robotics", "Humanoid & Service Robots"):    "System Integration",
    ("Robotics", "Industrial Robots"):            "System Integration",
    ("Robotics", "Machine Vision & Sensors"):     "Components & Subsystems",
    ("Robotics", "Motion Control & Actuators"):   "Components & Subsystems",
    ("Robotics", "Software & Simulation"):        "Deployment & Operation",
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
    ("Space", "In-Orbit Services"):               "System Integration",
    ("Space", "Launch"):                          "System Integration",
    ("Space", "Satellite Comms"):                 "Deployment & Operation",
    ("Space", "Satellite Communications"):        "Deployment & Operation",
    ("Space", "Space Components"):                "Components & Subsystems",
}


# Per-ticker overrides where (sector, subsector) would classify wrong.
# Most of the universe is handled by the default; these are the exceptions.
OVERRIDES = {
    # Some "Power & Analog" ICs are actually fabless chip designers
    # (not just components — they design and outsource fabrication).
    # Still mid-chain components; leaving the default.
    #
    # System integrators tagged as sensor/vision pure-plays:
    "MBLY": "System Integration",          # Mobileye ships full ADAS stacks
    "HSAI": "Components & Subsystems",     # LiDAR supplier into AV integrators
    # Intuitive Surgical is clearly a system integrator even if we
    # categorised the subsector as "Surgical & Medical" — default already
    # handles this correctly.
}


def main():
    with open(PUBLIC_MARKETS) as f:
        pm = json.load(f)
    try:
        with open(ENRICHMENT) as f:
            enr = json.load(f)
    except FileNotFoundError:
        enr = {}

    VISIBLE_SECTORS = {
        "Semiconductors", "Semiconductor", "Robotics", "Space",
        "Materials", "Materials & Inputs",
    }

    applied = 0
    unknown = []
    for ticker, e in pm.get("entities", {}).items():
        sector = e.get("sector")
        if sector not in VISIBLE_SECTORS:
            continue
        subsector = e.get("subsector")
        # Normalise Materials & Inputs → Materials, Semiconductor → Semiconductors.
        key_sector = {
            "Materials & Inputs": "Materials",
            "Semiconductor": "Semiconductors",
        }.get(sector, sector)

        tier = OVERRIDES.get(ticker) or DEFAULT_BY_SUBSECTOR.get((key_sector, subsector))
        if not tier:
            unknown.append((ticker, sector, subsector, e.get("name")))
            continue

        entry = enr.get(ticker) or {}
        entry["value_chain_tier"] = tier
        enr[ticker] = entry
        applied += 1

    with open(ENRICHMENT, "w") as f:
        json.dump(enr, f, indent=2)

    print(f"Set value_chain_tier on {applied} entities.")
    if unknown:
        print(f"\n{len(unknown)} entities with no tier mapping:")
        for t, s, sub, n in unknown:
            print(f"  {t:15s} sector={s!r:20s} subsector={sub!r:35s} name={n}")
    else:
        print("All visible entities classified.")


if __name__ == "__main__":
    main()
