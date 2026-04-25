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

    Layout (top to bottom):
      Title -- subtitle -- four bands (Space/Robotics/Semis/Materials)
      with header strips, body boxes, and inter-band annotations in
      the gaps. Cross-layer arrows route in the left/right gutters.
      Legend at the bottom.

    Bands are ordered top-down so the stack reads visually from
    deployment (Space, top) to upstream origin (Materials, bottom).
    Conceptual demand flows upward.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Title + subtitle. Extra spacing between the two so they breathe.
    fig.text(0.5, 0.972, "The Frontier Technology Stack",
             ha="center", va="top",
             fontproperties=title_font(size=18 * fontscale),
             color=PALETTE.ink)
    fig.text(0.5, 0.927,
             "Dependency flows across four sectors. Disruption in any layer propagates through the rest.",
             ha="center", va="top",
             fontproperties=subtitle_font(size=10 * fontscale),
             color=PALETTE.axis)

    # Reserve a legend strip at the bottom (was a caption panel).
    x_left, x_right = 0.10, 0.90
    top_y = 0.86               # extra top margin so subtitle never clips into bands
    legend_h = 0.07
    bottom_y = 0.04 + legend_h

    header_h = 0.030
    flow_h   = 0.058
    n_bands  = len(BANDS)
    band_h   = (top_y - bottom_y - n_bands * header_h - (n_bands - 1) * flow_h) / n_bands

    bands_geom = []  # (band_box_top, band_box_bottom, header_top)
    y_cursor = top_y
    for i, (key, header, color, columns) in enumerate(BANDS):
        header_top    = y_cursor
        header_bottom = header_top - header_h
        band_top      = header_bottom
        band_bottom   = band_top - band_h
        bands_geom.append((band_top, band_bottom, header_top))

        # Header strip — solid sector colour with DARK NAVY text for
        # contrast (white was hard to read on green / salmon).
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

        # Band body — soft tint background
        body_rect = FancyBboxPatch(
            (x_left, band_bottom), x_right - x_left, band_top - band_bottom,
            boxstyle="round,pad=0.001,rounding_size=0.007",
            linewidth=0, facecolor=_tint(color, 0.10), zorder=1,
            transform=ax.transAxes,
        )
        ax.add_patch(body_rect)

        # Columns. Internal padding bumped from 0.008 → 0.014 so text
        # doesn't squash against the column-box border.
        n = len(columns)
        side_pad = 0.012
        gap = 0.012
        total = (x_right - x_left) - 2 * side_pad
        col_w = (total - gap * (n - 1)) / n
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
                (x, band_bottom + 0.012), col_w, (band_top - band_bottom) - 0.024,
                **box_kw,
            )
            ax.add_patch(col_box)
            # Column title — sits with comfortable headroom from the box top.
            ax.text(x + col_w / 2, band_top - 0.020, col_title,
                    ha="center", va="top",
                    fontsize=8.5 * fontscale, fontweight="bold",
                    color=PALETTE.ink, family="Space Grotesk",
                    transform=ax.transAxes, zorder=3)
            # Entity lines, taller line-height for breathing room.
            line_h = 0.020 * fontscale
            entity_start = band_top - 0.054
            for ei, ent in enumerate(entities):
                ax.text(x + col_w / 2,
                        entity_start - ei * line_h, ent,
                        ha="center", va="top",
                        fontsize=7.5 * fontscale, color=PALETTE.axis,
                        family="Mulish",
                        transform=ax.transAxes, zorder=3)
            # Private indicator: small italic "private" tag below the
            # entity list. Mulish doesn't ship the ● BLACK CIRCLE glyph
            # so we keep it text-only.
            if private:
                priv_y = entity_start - len(entities) * line_h - 0.005
                ax.text(x + col_w / 2, priv_y, "private",
                        ha="center", va="top",
                        fontsize=6.8 * fontscale, color=PALETTE.axis,
                        family="Mulish", style="italic",
                        transform=ax.transAxes, zorder=3)

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

    # Right gutter: yellow demand-flow arrows, going UP. Three arrows
    # at slightly different x positions so they don't fully overlap.
    # Thickened from 1.4 → 2.0 so they're clearly visible at small
    # output sizes; arrowheads scaled up to match.
    right_base = 0.935
    for src, dst, lbl, kind, offset in FLOWS:
        if kind != "right-up":
            continue
        src_top = bands_geom[src][0]
        dst_bot = bands_geom[dst][1]
        gx = right_base + offset
        arrow(gx, src_top, gx, dst_bot,
              PALETTE.composite, 2.2, rad=-0.18)

    # Left gutter: dark-navy feedback arrow, going DOWN. Made
    # noticeably thicker so it doesn't disappear in print.
    left_x = 0.065
    for src, dst, lbl, kind, _offset in FLOWS:
        if kind != "left-down":
            continue
        src_bot = bands_geom[src][1]
        dst_top = bands_geom[dst][0]
        arrow(left_x, src_bot, left_x, dst_top,
              DARK_NAVY, 1.8, rad=-0.18)

    # Legend strip at the bottom — arrow icons matching the chart.
    legend_top = bottom_y - 0.012
    legend_bot = 0.04
    legend_rect = FancyBboxPatch(
        (x_left, legend_bot), x_right - x_left, legend_top - legend_bot,
        boxstyle="round,pad=0.002,rounding_size=0.006",
        linewidth=0.6, edgecolor=PALETTE.grid, facecolor="#FAFBFC",
        zorder=1, transform=ax.transAxes,
    )
    ax.add_patch(legend_rect)

    legend_entries = [
        (PALETTE.composite, "Materials → Robotics",      "NdFeB magnets for servo motors"),
        (PALETTE.composite, "Materials → Space",         "NdFeB magnets for reaction wheels"),
        (PALETTE.composite, "Semiconductors → Space",    "On-board processors, direct-to-device"),
        (DARK_NAVY,         "Robotics → Semiconductors", "Fab automation (feedback)"),
    ]
    rows_per_col = 2
    panel_inner_h = legend_top - legend_bot
    col_w = (x_right - x_left - 0.03) / 2
    row_h = panel_inner_h / rows_per_col
    for i, (col, title, desc) in enumerate(legend_entries):
        c = i // rows_per_col
        r = i % rows_per_col
        cx = x_left + 0.015 + c * (col_w + 0.015)
        cy = legend_top - 0.014 - r * row_h
        # Arrow icon — coloured marker mirroring the chart arrow
        ax.text(cx, cy, "→",
                ha="left", va="center",
                fontsize=12 * fontscale, fontweight="bold",
                color=col, family="Space Grotesk",
                transform=ax.transAxes, zorder=3)
        # Title in dark ink (was previously coloured, which read faint)
        ax.text(cx + 0.018, cy, title,
                ha="left", va="center",
                fontsize=8.5 * fontscale, fontweight="bold",
                color=DARK_NAVY, family="Space Grotesk",
                transform=ax.transAxes, zorder=3)
        ax.text(cx + 0.018, cy - 0.020 * fontscale, desc,
                ha="left", va="center",
                fontsize=7.8 * fontscale, color=PALETTE.axis,
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
    # Title + subtitle (drawn as fig.text to match Figures 1-3)
    fig.text(0.5, 0.965, "The Public-Private Divergence in Robotics",
             ha="center", va="top",
             fontproperties=title_font(size=14 * fontscale),
             color=PALETTE.ink)
    fig.text(0.5, 0.920,
             "Private capital deployment vs public sub-index performance, April 2025 – March 2026",
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

    # Right-axis limit leaves headroom so the 1Q26 bar label fits
    # above the bar with the callout text clearly clear of the bar
    # top.
    ax2.set_ylim(0, max(max(bar_y) * 1.55, 5))
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

    # The two callouts must not overlap each other. Place the public
    # sub-index callout to the LEFT of the Q1 bar (above the line's
    # rising right-side path) and the Q1 bar callout DIRECTLY above
    # the Q1 bar. Both use thin grey leaders — never the line styling
    # (which would read as a trend, not a callout).
    from datetime import timedelta
    q1 = bars[-1]
    # Multiplier vs the immediately preceding quarter (4Q25), per spec.
    prior_q = bars[-2][1] if len(bars) > 1 else q1[1]
    multiplier = q1[1] / prior_q if prior_q > 0 else 0

    # Public sub-index callout — anchored over the line at ~mid-Jan,
    # well left of the Q1 bar so the two callouts share no horizontal
    # space.
    if robotics:
        end_d, end_v = robotics[-1]
        # Lookup the value at the callout anchor date so the leader
        # touches the actual line, not floating space.
        anchor_d = date(2026, 1, 15)
        anchor_v = end_v
        for d, v in robotics:
            if d <= anchor_d:
                anchor_v = v
            else:
                break
        # Label sits well above the line at the upper-left of the chart
        line_max = max(v for _, v in robotics)
        callout_y = line_max + (line_max - 100) * 0.06
        ax1.annotate(f"Public sub-index +{line_return_pct:.0f}% 12m",
                     xy=(anchor_d, anchor_v),
                     xytext=(date(2025, 8, 15), callout_y),
                     ha="left", va="bottom",
                     fontsize=10 * fontscale, fontweight="bold",
                     color=PALETTE.ink,
                     arrowprops=dict(arrowstyle="-", color="#9CA3AF", lw=0.5,
                                     shrinkA=2, shrinkB=4),
                     zorder=10)

    # Q1 2026 bar callout — directly above the bar with a vertical
    # leader. Stays in its own air column so it can never collide
    # with the sub-index callout.
    # Avoid repeating "$31.5b" — that figure is already on the bar
    # label. Callout adds the magnitude commentary only.
    callout_q1_y = q1[1] + max(bar_y) * 0.22
    ax2.annotate(f"{multiplier:.0f}× prior quarter",
                 xy=(q1[0], q1[1]),
                 xytext=(q1[0], callout_q1_y),
                 ha="center", va="bottom",
                 fontsize=10 * fontscale, fontweight="bold",
                 color=PALETTE.ink,
                 arrowprops=dict(arrowstyle="-", color="#9CA3AF", lw=0.5,
                                 shrinkA=2, shrinkB=4),
                 zorder=10)

    # Baseline label on the rebase=100 dashed reference line — sits at
    # the LEFT of the chart on the line itself, well clear of the
    # right-axis ticks.
    ax1.text(date(2025, 5, 5), 100, "rebase = 100",
             ha="left", va="bottom",
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
    # Print embed: 2500x1600 → at 300dpi that's 8.33 x 5.33 inches.
    fig = _draw_dependency_chain((8.33, 5.33), fontscale=1.0)
    out = OUT_PRINT / "dependency_chain.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart A print  → {out}")

    # LinkedIn 1200x630 (landscape)
    fig = _draw_dependency_chain((8, 4.2), fontscale=0.85)
    out = OUT_SOCIAL / "dependency_chain_linkedin.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    plt.close(fig)
    print(f"Chart A li     → {out}")

    # Square 1080x1080 — recompose with taller vertical (boxes stacked tight).
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
