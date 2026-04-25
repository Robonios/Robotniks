"""
Robotnik Report — Extra Figures
================================
Two additional charts for the 1Q26 report + social distribution:

  A. The Frontier Stack Dependency Chain
     Four-band diagram (Materials -> Semis -> Robotics -> Space)
     with labelled dependency flows between bands.

  B. The Public-Private Divergence in Robotics
     Dual-axis 12-month view: Robotics sub-index (yellow line)
     vs quarterly private funding (green bars).

Each chart is saved in three sizes:
  data/exports/report_charts/<name>.png      — 300 DPI print
  data/exports/social/<name>_linkedin.png    — 1200x630
  data/exports/social/<name>_square.png      — 1080x1080

Usage:
    python scripts/generate_extra_report_figures.py
"""

from pathlib import Path
import json
from collections import defaultdict
from datetime import datetime, date

from report_chart_style import (
    apply_style, save_report_chart,
    PALETTE, DPI,
    title_font, subtitle_font,
    composite_kw, secondary_kw, base_ref_kw,
)
apply_style()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT       = Path(__file__).resolve().parent.parent
INDEX_SUBS = ROOT / "data" / "index" / "sub_indices.json"
ROUNDS     = ROOT / "data" / "funding" / "rounds.json"

OUT_PRINT  = ROOT / "data" / "exports" / "report_charts"
OUT_SOCIAL = ROOT / "data" / "exports" / "social"
for p in (OUT_PRINT, OUT_SOCIAL):
    p.mkdir(parents=True, exist_ok=True)


# ═════════════════════════════════════════════════════════════════════
# CHART A — Dependency chain diagram
# ═════════════════════════════════════════════════════════════════════
#
# Layout: four horizontal bands with titled column boxes inside. Between
# each pair of adjacent bands we draw a set of labelled curved arrows
# that represent the structural dependencies called out in the task
# spec. A separate thin arrow runs upward from Robotics to
# Semiconductors to show the feedback loop (fab automation).

DARK_NAVY = "#1A1A2E"

# Each band: (key, header, color, columns)
# columns: list of (column title, [entity lines], optional kwargs)
# The optional 4th element is a dict with style flags — currently only
# {"dashed": True, "private": True} is supported and applies to the
# Humanoid column to mark its private constituents.
#
# Bands ordered TOP TO BOTTOM. The stack reads from Space (deployment
# endpoint, top) down to Materials & Inputs (upstream origin, bottom).
# Conceptual flow is from bottom up — every arrow on the right gutter
# points upward.
BANDS = [
    ("space", "SPACE", PALETTE.subindices["space"], [
        ("Prime Contractors",     ["Lockheed Martin", "Northrop Grumman"], {}),
        ("Launch",                ["Rocket Lab", "Arianespace"], {}),
        ("Satellite Services",    ["AST SpaceMobile", "Planet Labs", "Satellogic"], {}),
        ("Components & Materials", ["Hexcel", "Toray", "Moog"], {}),
    ]),
    ("robotics", "ROBOTICS", PALETTE.subindices["robotics"], [
        ("Motion Control",   ["Fanuc", "Yaskawa", "Nidec"], {}),
        ("Industrial Auto",  ["Siemens", "ABB", "Keyence"], {}),
        ("Humanoid",         ["Figure", "1X", "Agility"], {"dashed": True, "private": True}),
        ("Surgical",         ["Intuitive Surgical"], {}),
    ]),
    ("semiconductor", "SEMICONDUCTORS", PALETTE.subindices["semiconductor"], [
        ("Fabless Design",   ["NVIDIA", "Broadcom", "AMD"], {}),
        ("Foundry",          ["TSMC", "Intel"], {}),
        ("Equipment",        ["ASML", "Applied Materials", "Lam Research"], {}),
        ("Memory",           ["Micron", "SK Hynix", "Samsung"], {}),
    ]),
    ("materials", "MATERIALS & INPUTS", PALETTE.subindices["materials"], [
        ("Rare Earths",      ["Northern Rare Earth", "MP Materials", "Lynas"], {}),
        ("Silicon Wafers",   ["Shin-Etsu", "SUMCO"], {}),
        ("Industrial Gases", ["Linde", "Air Liquide"], {}),
        ("ABF Substrates",   ["Unimicron", "Ibiden"], {}),
    ]),
]

# Inter-band annotations. Placed in the gap ABOVE the receiving layer,
# describing what the lower layer sends upward.
# (gap_below_band_index, label_text)
INTER_BAND_ANNOTATIONS = [
    (1, "CMP polishing · 300mm wafers · Ultra-pure neon · CoWoS packaging"),
    # gap above Semiconductors — Materials supplies these
    (0, "Edge AI chips, power management, motor control MCUs"),
    # gap above Robotics — Semiconductors supplies these (also Space, see arrow)
]
# Index meanings (top-down):
#   0 = Space, 1 = Robotics, 2 = Semiconductors, 3 = Materials.
# Annotation index is the band INDEX whose gap-above is being labelled.
# So (1, …) labels the gap above ROBOTICS (between Robotics and Semis).
# And (0, …) labels the gap above SPACE? No — Space is on top, no gap
# above. We want the gap ABOVE Robotics? Actually re-read.
#
# The semantic is "what flows up". "Edge AI" flows from Semis up to
# Robotics, so it's labelled in the gap between Semis and Robotics.
# That's the gap ABOVE Semis (band 2) which is the same gap as the
# one BELOW Robotics (band 1). I'll use the convention "index of the
# RECEIVING band" = put the label in the gap above the receiver.
#
# Therefore:
#   - "Edge AI chips…": between Semis (sender, below) and Robotics
#     (receiver, above). Label sits in the gap with index = receiver
#     index = 1 (Robotics).
#   - "CMP polishing…": between Materials (sender, bottom) and Semis
#     (receiver, above Materials). Label sits in the gap with index =
#     receiver index = 2 (Semis).
INTER_BAND_ANNOTATIONS = [
    (1, "Edge AI chips, power management, motor control MCUs"),
    (2, "CMP polishing · 300mm wafers · Ultra-pure neon · CoWoS packaging"),
]

# Cross-layer arrows. All flow upward (sender below → receiver above)
# except the feedback loop (Robotics → Semis, which is downward in the
# inverted stack).
# (sender_band_idx, receiver_band_idx, label, kind, x_offset)
# Right gutter: yellow upward demand. Left gutter: dark-navy downward feedback.
FLOWS = [
    # Materials (3) → Robotics (1): yellow, right gutter, up
    (3, 1, "NdFeB magnets for servo motors",      "right-up", 0.000),
    # Materials (3) → Space (0): yellow, right gutter (further out), up
    (3, 0, "NdFeB magnets for reaction wheels",   "right-up", 0.030),
    # Semiconductors (2) → Space (0): yellow, right gutter (innermost), up
    (2, 0, "On-board processors, direct-to-device", "right-up", -0.030),
    # Robotics (1) → Semiconductors (2): dark navy, left gutter, DOWN
    # (Robotics now sits above Semis in the inverted stack)
    (1, 2, "Fab automation (feedback)", "left-down", 0.0),
]


def _draw_dependency_chain(figsize, fontscale=1.0, is_square=False):
    """Render the dependency chain at a given figure size.

    Geometry decisions in this rebuild:
      - Bands are ordered top-down: SPACE / ROBOTICS / SEMIS / MATERIALS.
      - Every column box has the SAME height across the entire chart
        (visual rhythm). The height is sized for the worst-case
        content: title + private indicator + 3 entity lines + padding.
      - Boxes with fewer entities centre their content vertically
        within the box, instead of clustering at the top.
      - Right gutter carries FOUR clearly-separated arrows
        (Materials→Robotics, Materials→Space, Semis→Space, and the
        Robotics→Semiconductors feedback in dark navy at the
        outermost offset).
      - No left-side arrow.
      - Legend at the bottom is a clean 2×2 grid; description text
        indents under the title text, not under the arrow icon.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    # Force the axes to fill the entire figure — default subplot
    # margins were eating ~23% of the canvas, which compressed every
    # box vertically and made text overflow at the bottom.
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Title + subtitle in AXES coords (since the axes now fills the
    # whole figure, axes coords == figure coords). Keeping them on
    # the same coordinate system as the bands means the subtitle
    # can't drift into a band header on resize / tight-bbox crop.
    ax.text(0.5, 0.97, "The Frontier Technology Stack",
            ha="center", va="top",
            fontproperties=title_font(size=18 * fontscale),
            color=PALETTE.ink, transform=ax.transAxes, zorder=10)
    ax.text(0.5, 0.93,
            "Dependency flows across four sectors. Disruption in any layer propagates through the rest.",
            ha="center", va="top",
            fontproperties=subtitle_font(size=10 * fontscale),
            color=PALETTE.axis, transform=ax.transAxes, zorder=10)

    # Inner band area (x). Right edge pulled in to x=0.84 to leave a
    # ~16% gutter for the FOUR cleanly-separated arrows.
    x_left, x_right = 0.08, 0.84
    # Top of stack — sits below the subtitle with a small clearance.
    top_y    = 0.885
    # Legend area at the bottom.
    legend_top    = 0.165
    legend_bottom = 0.025
    bottom_y = legend_top + 0.010

    header_h = 0.024
    flow_h   = 0.038
    n_bands  = len(BANDS)
    band_h   = (top_y - bottom_y - n_bands * header_h - (n_bands - 1) * flow_h) / n_bands

    # Pre-compute the global content layout used by every column box.
    # Every box has the SAME height; content vertically centres within
    # that height. Worst-case content: title + indicator + 3 entities
    # (Humanoid). Tighter line-heights so the layout actually fits the
    # band height, which the previous draft did not.
    MAX_ENTITY_ROWS  = max(len(c[1]) for b in BANDS for c in b[3])
    BOX_INNER_PAD    = 0.008
    TITLE_LINE_H     = 0.018 * fontscale
    INDICATOR_LINE_H = 0.014 * fontscale
    ENTITY_LINE_H    = 0.014 * fontscale
    BOX_INNER_H      = (BOX_INNER_PAD * 2
                        + TITLE_LINE_H
                        + INDICATOR_LINE_H
                        + MAX_ENTITY_ROWS * ENTITY_LINE_H)
    BOX_OUTER_PAD    = 0.006

    bands_geom = []  # (band_box_top, band_box_bottom, header_top)
    y_cursor = top_y
    for i, (key, header, color, columns) in enumerate(BANDS):
        header_top    = y_cursor
        header_bottom = header_top - header_h
        band_top      = header_bottom
        band_bottom   = band_top - band_h
        bands_geom.append((band_top, band_bottom, header_top))

        # Header strip — solid sector colour with dark-navy text.
        header_rect = FancyBboxPatch(
            (x_left, header_bottom), x_right - x_left, header_h,
            boxstyle="round,pad=0.001,rounding_size=0.007",
            linewidth=0, facecolor=color, zorder=2,
            transform=ax.transAxes,
        )
        ax.add_patch(header_rect)
        ax.text(x_left + 0.015, header_bottom + header_h / 2, header,
                ha="left", va="center",
                fontsize=10.5 * fontscale, fontweight="bold",
                color=DARK_NAVY, family="Space Grotesk",
                transform=ax.transAxes, zorder=3)

        # Band body — soft sector tint background.
        body_rect = FancyBboxPatch(
            (x_left, band_bottom), x_right - x_left, band_top - band_bottom,
            boxstyle="round,pad=0.001,rounding_size=0.007",
            linewidth=0, facecolor=_tint(color, 0.10), zorder=1,
            transform=ax.transAxes,
        )
        ax.add_patch(body_rect)

        # Columns — uniform width and uniform box height across the whole chart.
        n = len(columns)
        side_pad = 0.012
        gap = 0.012
        total = (x_right - x_left) - 2 * side_pad
        col_w = (total - gap * (n - 1)) / n

        # Box outer placement inside the band — centred vertically.
        box_top    = band_top - BOX_OUTER_PAD
        box_bottom = box_top - BOX_INNER_H
        # Anchor to band top with the small outer pad — band heights
        # are already sized so this comfortably fits.

        for ci, col_def in enumerate(columns):
            col_title, entities, *rest = col_def
            kwargs = rest[0] if rest else {}
            dashed = kwargs.get("dashed", False)
            private = kwargs.get("private", False)

            x = x_left + side_pad + ci * (col_w + gap)
            box_kw = dict(
                boxstyle="round,pad=0.001,rounding_size=0.006",
                linewidth=1.0, edgecolor=color, facecolor="white", zorder=2,
                transform=ax.transAxes,
            )
            if dashed:
                box_kw["linestyle"] = (0, (3, 2))
            col_box = FancyBboxPatch(
                (x, box_bottom), col_w, BOX_INNER_H, **box_kw,
            )
            ax.add_patch(col_box)

            # Inside-box layout. Title is always at the top. Below it,
            # the entity block (and the private indicator if any) is
            # vertically CENTRED in the remaining space, so a 1-entity
            # box doesn't look top-heavy next to a 3-entity box.
            title_y = box_top - BOX_INNER_PAD
            ax.text(x + col_w / 2, title_y, col_title,
                    ha="center", va="top",
                    fontsize=8.5 * fontscale, fontweight="bold",
                    color=PALETTE.ink, family="Space Grotesk",
                    transform=ax.transAxes, zorder=3)

            # Reserved height below the title for entities + indicator.
            below_title_top    = title_y - TITLE_LINE_H
            below_title_bottom = box_bottom + BOX_INNER_PAD
            block_total_h      = below_title_top - below_title_bottom

            # Actual content height for THIS box.
            actual_lines = len(entities) + (1 if private else 0)
            line_height = ENTITY_LINE_H
            content_h = actual_lines * line_height
            # Centre that content vertically inside the reserved block.
            content_top = below_title_top - (block_total_h - content_h) / 2

            row_y = content_top
            if private:
                ax.text(x + col_w / 2, row_y, "• private",
                        ha="center", va="top",
                        fontsize=7.0 * fontscale, color=PALETTE.axis,
                        family="Mulish", style="italic",
                        transform=ax.transAxes, zorder=3)
                row_y -= line_height
            for ent in entities:
                ax.text(x + col_w / 2, row_y, ent,
                        ha="center", va="top",
                        fontsize=7.5 * fontscale, color=PALETTE.axis,
                        family="Mulish",
                        transform=ax.transAxes, zorder=3)
                row_y -= line_height

        y_cursor = band_bottom - flow_h

    # Inter-band annotations — italic grey, centred in the gap above
    # the receiver band. Describes what the lower (sender) band sends
    # upward.
    for receiver_idx, label in INTER_BAND_ANNOTATIONS:
        receiver_band_bottom = bands_geom[receiver_idx][1]
        # The gap below this receiver, between this band and the next
        # band below. The lower band's HEADER top is at receiver_band_bottom
        # - flow_h. Place label in the middle of that flow_h gap.
        if receiver_idx + 1 < len(bands_geom):
            lower_header_top = bands_geom[receiver_idx + 1][2]
            mid_y = (receiver_band_bottom + lower_header_top) / 2
            ax.text(0.5, mid_y, label,
                    ha="center", va="center", style="italic",
                    fontsize=8.2 * fontscale, color=PALETTE.axis,
                    family="Mulish",
                    transform=ax.transAxes, zorder=5)

    # Cross-layer arrows. Helper supports both gutters and arbitrary
    # endpoints with curve.
    def arrow(x0, y0, x1, y1, color, lw, rad=0, zorder=4, dashed=False):
        kw = dict(
            arrowstyle="-|>", mutation_scale=14 * fontscale,
            color=color, linewidth=lw,
            transform=ax.transAxes, zorder=zorder,
        )
        if rad:
            kw["connectionstyle"] = f"arc3,rad={rad}"
        if dashed:
            kw["linestyle"] = (0, (3, 2))
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), **kw))

    # Right gutter: four CLEARLY DISTINCT arrows. Per spec, the
    # innermost arrow (closest to figure edge) is A; D is outermost.
    #
    #   x = 0.965 → Arrow A: Materials → Robotics (yellow, up)
    #   x = 0.935 → Arrow B: Materials → Space     (yellow, up)
    #   x = 0.905 → Arrow C: Semis → Space         (yellow, up)
    #   x = 0.875 → Arrow D: Robotics → Semis      (DARK NAVY, down)
    arrow_specs = [
        # (src band idx, dst band idx, x, color, rad)
        (3, 1, 0.965, PALETTE.composite, -0.18),  # Arrow A
        (3, 0, 0.935, PALETTE.composite, -0.18),  # Arrow B
        (2, 0, 0.905, PALETTE.composite, -0.18),  # Arrow C
        (1, 2, 0.875, DARK_NAVY,         -0.18),  # Arrow D (feedback, DOWN)
    ]
    for src, dst, gx, col, rad in arrow_specs:
        if src > dst:
            # Going UP: from sender body top up to receiver body bottom.
            y_start = bands_geom[src][0]
            y_end   = bands_geom[dst][1]
        else:
            # Going DOWN (feedback): from sender body bottom down to
            # receiver body top.
            y_start = bands_geom[src][1]
            y_end   = bands_geom[dst][0]
        arrow(gx, y_start, gx, y_end, col, 2.2, rad=rad)

    # Legend at the bottom — clean 2×2 grid, generous spacing.
    # Two columns separated by a clear horizontal gap; each cell
    # carries a coloured arrow icon, a bold dark-ink title on the
    # first line, and an italic grey description on the second line
    # indented under the title text (NOT under the arrow icon).
    #
    # Layout target:
    #   [→ yellow]  Materials → Robotics             [→ yellow]  Semiconductors → Space
    #               NdFeB magnets for servo motors               On-board processors, direct-to-device
    #
    #   [→ yellow]  Materials → Space                [→ navy]    Robotics → Semiconductors (feedback)
    #               NdFeB magnets for reaction wheels            Fab automation
    legend_panel_top = legend_top
    legend_panel_bot = legend_bottom
    legend_rect = FancyBboxPatch(
        (x_left, legend_panel_bot), x_right - x_left,
        legend_panel_top - legend_panel_bot,
        boxstyle="round,pad=0.002,rounding_size=0.006",
        linewidth=0.6, edgecolor=PALETTE.grid, facecolor="#FAFBFC",
        zorder=1, transform=ax.transAxes,
    )
    ax.add_patch(legend_rect)

    # 2×2 grid arranged in reading order (left-to-right, top-to-bottom).
    legend_grid = [
        # Top row
        [(PALETTE.composite, "Materials → Robotics",     "NdFeB magnets for servo motors"),
         (PALETTE.composite, "Semiconductors → Space",   "On-board processors, direct-to-device")],
        # Bottom row
        [(PALETTE.composite, "Materials → Space",        "NdFeB magnets for reaction wheels"),
         (DARK_NAVY,         "Robotics → Semiconductors","Fab automation (feedback)")],
    ]

    # Inner geometry: padding inside the panel + 40px column gap.
    inner_pad_x = 0.020
    inner_pad_y = 0.022
    col_gap     = 0.030  # ~40px at print scale
    n_cols = 2
    avail_w = (x_right - x_left) - 2 * inner_pad_x - col_gap * (n_cols - 1)
    cell_w  = avail_w / n_cols
    avail_h = (legend_panel_top - legend_panel_bot) - 2 * inner_pad_y
    row_h   = avail_h / 2
    arrow_w = 0.022           # space reserved for the icon

    for r, row in enumerate(legend_grid):
        for c, (col, title, desc) in enumerate(row):
            cell_x = x_left + inner_pad_x + c * (cell_w + col_gap)
            cell_top = legend_panel_top - inner_pad_y - r * row_h
            # Title row: arrow icon + bold dark-ink title
            arrow_y = cell_top - 0.018 * fontscale
            ax.text(cell_x, arrow_y, "→",
                    ha="left", va="center",
                    fontsize=12 * fontscale, fontweight="bold",
                    color=col, family="Space Grotesk",
                    transform=ax.transAxes, zorder=3)
            ax.text(cell_x + arrow_w, arrow_y, title,
                    ha="left", va="center",
                    fontsize=8.8 * fontscale, fontweight="bold",
                    color=DARK_NAVY, family="Space Grotesk",
                    transform=ax.transAxes, zorder=3)
            # Description row: italic grey, indented under the title
            # text (so all descriptions left-align cleanly).
            desc_y = arrow_y - 0.024 * fontscale
            ax.text(cell_x + arrow_w, desc_y, desc,
                    ha="left", va="center",
                    fontsize=8.0 * fontscale, color=PALETTE.axis,
                    family="Mulish", style="italic",
                    transform=ax.transAxes, zorder=3)

    return fig


def _tint(hex_color, alpha):
    """Mix a hex color with white at the given alpha (0=white, 1=color)."""
    # The matplotlib patch supports rgba directly — simpler than colour math.
    return (*_hex_to_rgb(hex_color), alpha)


def _hex_to_rgb(hx):
    hx = hx.lstrip("#")
    return tuple(int(hx[i:i+2], 16) / 255.0 for i in (0, 2, 4))


# ═════════════════════════════════════════════════════════════════════
# CHART B — Public-Private Divergence
# ═════════════════════════════════════════════════════════════════════

def _load_robotics_series():
    """Robotics sub-index, 2025-03-31 to 2026-03-31, rebased to 100."""
    data = json.load(open(INDEX_SUBS))
    series = data["robotics"]["series"]
    start = date(2025, 3, 31)
    end   = date(2026, 3, 31)
    pts = []
    for p in series:
        d = datetime.strptime(p["date"], "%Y-%m-%d").date()
        if start <= d <= end:
            pts.append((d, p["value"]))
    if not pts:
        return pts
    base = pts[0][1]
    return [(d, v / base * 100) for d, v in pts]


def _load_quarterly_funding():
    """Quarterly Robotics private funding totals, 2Q25 to 1Q26 inclusive."""
    rounds = json.load(open(ROUNDS))["rounds"]
    qtr = defaultdict(float)
    for item in rounds:
        if item.get("sector") != "Robotics":
            continue
        amt = item.get("amount_m") or 0
        if not amt:
            continue
        d = item.get("date", "")
        if not d:
            continue
        yr = int(d[:4])
        mo = int(d[5:7])
        q  = (mo - 1) // 3 + 1
        qtr[(yr, q)] += amt / 1000.0  # $bn
    wanted = [(2025, 2), (2025, 3), (2025, 4), (2026, 1)]
    labels  = ["2Q25", "3Q25", "4Q25", "1Q26"]
    # Anchor each bar at the mid-point of its quarter for plotting.
    mids = {
        (2025, 2): date(2025, 5, 15),
        (2025, 3): date(2025, 8, 15),
        (2025, 4): date(2025, 11, 15),
        (2026, 1): date(2026, 2, 15),
    }
    return [(mids[k], qtr.get(k, 0.0), labels[i]) for i, k in enumerate(wanted)]


def _draw_divergence(figsize, fontscale=1.0):
    robotics = _load_robotics_series()
    bars     = _load_quarterly_funding()

    fig, ax1 = plt.subplots(figsize=figsize)
    # Title + subtitle. Reframed under Option A: the public sub-index
    # rose materially in the same window as the private-capital surge,
    # so the chart is a "both rising" story with the magnitude
    # contrast (9× quarterly capital deployment) doing the lifting.
    fig.text(0.5, 0.965, "Capital floods into public and private robotics",
             ha="center", va="top",
             fontproperties=title_font(size=14 * fontscale),
             color=PALETTE.ink)
    fig.text(0.5, 0.920,
             "Public sub-index returns vs private funding deployment, April 2025 – March 2026",
             ha="center", va="top",
             fontproperties=subtitle_font(size=10 * fontscale),
             color=PALETTE.axis)

    # Base-100 reference line on the left axis
    ax1.axhline(100, **base_ref_kw())

    # Robotics sub-index line (left axis, yellow)
    xs = [d for d, _ in robotics]
    ys = [v for _, v in robotics]
    ax1.plot(xs, ys, **composite_kw(label="Robotics sub-index (rebased 100)"))

    # Quarterly funding bars (right axis, green)
    ax2 = ax1.twinx()
    bar_x   = [m for m, _, _ in bars]
    bar_y   = [a for _, a, _ in bars]
    # ~ 45 days wide = 1/8 of 12-month x-axis
    bar_w_days = 45
    ax2.bar(bar_x, bar_y, width=bar_w_days, align="center",
            color=PALETTE.subindices["robotics"], alpha=0.55, zorder=1,
            edgecolor=PALETTE.subindices["robotics"], linewidth=0.6,
            label="Quarterly private robotics funding ($b)")

    # Quarter boundary vertical rules (subtle)
    for qd in (date(2025, 6, 30), date(2025, 9, 30), date(2025, 12, 31)):
        ax1.axvline(qd, color=PALETTE.grid, linewidth=0.6, zorder=0)

    # Axis labels + ticks
    ax1.set_ylabel("Sub-index value (rebased to 100)", fontsize=10 * fontscale)
    ax2.set_ylabel("Private funding ($b)", fontsize=10 * fontscale,
                   color=PALETTE.axis)
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax1.set_xlim(date(2025, 3, 31), date(2026, 3, 31))

    # Right-axis limit gives enough headroom for the "9× prior
    # quarter" callout to sit above the LEFT-axis line peak in clear
    # whitespace. Explicit yticks at clean 10-step values so the top
    # tick label reads as a plain integer — the previous draft's
    # default formatter combined with the spine cap rendered the
    # topmost tick as "- 40" (the dash being the tick mark).
    ax2.set_ylim(0, max(max(bar_y) * 1.85, 5))
    ax2.set_yticks([0, 10, 20, 30, 40])
    # Tick direction inward so tick marks don't read as a leading
    # dash on the labels.
    ax2.tick_params(axis="y", direction="in", length=3)
    # Hide right-axis gridlines (only left axis carries them)
    ax2.grid(False)

    # Bar labels — consistent convention: "QyYY  $X.Xb" just above
    # each bar's top edge, including the Q1 2026 bar (the magnitude
    # callout below adds the "9× prior quarter" context separately).
    for (m, a, lbl) in bars:
        ax2.text(m, a + max(bar_y) * 0.03,
                 f"{lbl}  ${a:.1f}b",
                 ha="center", va="bottom",
                 fontsize=8.5 * fontscale, color=PALETTE.axis,
                 family="Mulish")

    # Compute the 12-month return from the rebased line so the
    # annotation matches the data — the spec's +5.3% figure was
    # carried over from a stale state. Use the actual value.
    if robotics:
        line_return_pct = (robotics[-1][1] / robotics[0][1] - 1) * 100
    else:
        line_return_pct = 0.0

    # Two callouts in non-overlapping air columns:
    #   - Public sub-index callout: anchors its leader at the line's
    #     final point (March 2026), label sits above the line on the
    #     left side of the chart.
    #   - "9× prior quarter" callout: sits well ABOVE the line's peak
    #     (line peaks ~187 around late Feb), in clear whitespace, with
    #     a leader to the Q1 bar top. Does not overlap the line.
    from datetime import timedelta
    q1 = bars[-1]
    prior_q = bars[-2][1] if len(bars) > 1 else q1[1]
    multiplier = q1[1] / prior_q if prior_q > 0 else 0

    # Public sub-index callout — label placed ABOVE the line's PEAK
    # at the right edge of the chart, with a short, mostly-vertical
    # leader down to the line's actual endpoint (March 2026).
    if robotics:
        end_d, end_v = robotics[-1]
        line_max_top = max(v for _, v in robotics)
        ax1.annotate(f"Public sub-index +{line_return_pct:.0f}% 12m",
                     xy=(end_d, end_v),
                     xytext=(end_d, line_max_top + 30),
                     ha="right", va="bottom",
                     fontsize=10 * fontscale, fontweight="bold",
                     color=PALETTE.ink,
                     arrowprops=dict(arrowstyle="-", color="#9CA3AF", lw=0.5,
                                     shrinkA=2, shrinkB=4),
                     zorder=10)

    # Set both axis ylims explicitly so the geometry is predictable:
    #   ax1 (line, left axis): 85 → line_max + 40, leaving clear
    #                          whitespace above the line peak.
    #   ax2 (bars, right axis): 0 → max_bar * 2.5, pulling the bars
    #                           into the lower 40% of the chart so
    #                           the upper-right air column is free
    #                           for the 9× callout.
    if robotics:
        line_max = max(v for _, v in robotics)
        ax1.set_ylim(85, line_max + 40)
    bar_max_visible = max(bar_y) * 2.5
    ax2.set_ylim(0, bar_max_visible)

    # "9× prior quarter" callout sits in the upper-right air column.
    # Coordinates on ax2 (bars). At ax2 y = bar_max_visible * 0.92
    # the callout is in the top 8% of the chart, well above the line
    # peak which lives in the upper-third in ax1's range.
    callout_q1_y = bar_max_visible * 0.92
    ax2.annotate(f"{multiplier:.0f}× prior quarter",
                 xy=(q1[0], q1[1]),
                 xytext=(q1[0], callout_q1_y),
                 ha="center", va="top",
                 fontsize=10 * fontscale, fontweight="bold",
                 color=PALETTE.ink,
                 arrowprops=dict(arrowstyle="-", color="#9CA3AF", lw=0.5,
                                 shrinkA=2, shrinkB=4),
                 zorder=10)

    # Baseline label — right side, just above the dashed line. The
    # Q1 bar would otherwise sit on top of it; with bar ylim now
    # 0→79ish the bar top is well below 100 visually so the label
    # at left-axis y=102 is clear.
    ax1.text(date(2026, 3, 28), 102, "rebase = 100",
             ha="right", va="bottom",
             fontsize=8 * fontscale, color="#9CA3AF",
             style="italic", family="Mulish",
             zorder=3)

    # Legend — combine handles from both axes
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9 * fontscale,
               framealpha=0.92)

    # Tint the right-axis label green to match the bars
    ax2.tick_params(axis="y", colors=PALETTE.axis)

    fig.tight_layout(rect=[0, 0, 1, 0.89])
    return fig


# ═════════════════════════════════════════════════════════════════════
# Output — three sizes per chart
# ═════════════════════════════════════════════════════════════════════

def _save_png(fig, path, pixel_size=None):
    """Save PNG at 300 DPI (default) or a fixed pixel size."""
    if pixel_size:
        # Convert desired pixel size -> figure size inches at 150 DPI
        w_px, h_px = pixel_size
        fig.set_size_inches(w_px / 150, h_px / 150)
        fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    else:
        fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=PALETTE.paper)
    return path


def main():
    # ─── Chart A ───────────────────────────────────────────────────
    # Print embed bumped to 8.33 x 7.5 in (~2500x2250 at 300dpi). The
    # earlier 5.33-tall figure compressed every box vertically; with
    # 7.5 in tall every band has clear headroom for title + 3 entity
    # rows + indicator slot.
    fig = _draw_dependency_chain((8.33, 7.5), fontscale=1.0)
    out = OUT_PRINT / "dependency_chain.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart A print  → {out}")

    # LinkedIn 1200x630 — wide-landscape constraint forces tighter
    # boxes. Drop fontscale to 0.78 so the entity rows still fit the
    # band height at this aspect.
    fig = _draw_dependency_chain((8, 4.2), fontscale=0.78)
    out = OUT_SOCIAL / "dependency_chain_linkedin.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart A li     → {out}")

    # Square 1080x1080 — taller aspect, cleanest of the three.
    fig = _draw_dependency_chain((7.2, 7.2), fontscale=0.9, is_square=True)
    out = OUT_SOCIAL / "dependency_chain_square.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart A square → {out}")

    # ─── Chart B ───────────────────────────────────────────────────
    fig = _draw_divergence((8.33, 4.67), fontscale=1.0)
    out = OUT_PRINT / "public_private_divergence.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart B print  → {out}")

    fig = _draw_divergence((8, 4.2), fontscale=0.85)
    out = OUT_SOCIAL / "divergence_linkedin.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart B li     → {out}")

    fig = _draw_divergence((7.2, 7.2), fontscale=0.95)
    out = OUT_SOCIAL / "divergence_square.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart B square → {out}")


if __name__ == "__main__":
    main()
