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

# Each band: (key, header, color, columns)
# columns: list of (column title, [entity lines])
BANDS = [
    ("materials", "MATERIALS & INPUTS", PALETTE.subindices["materials"], [
        ("Rare Earths",       ["Northern Rare Earth", "MP Materials", "Lynas"]),
        ("Silicon Wafers",    ["Shin-Etsu", "SUMCO"]),
        ("Industrial Gases",  ["Linde", "Air Liquide"]),
        ("ABF Substrates",    ["Unimicron", "Ibiden"]),
    ]),
    ("semiconductor", "SEMICONDUCTORS", PALETTE.subindices["semiconductor"], [
        ("Fabless Design",    ["NVIDIA", "Broadcom", "AMD"]),
        ("Foundry",           ["TSMC", "Intel"]),
        ("Equipment",         ["ASML", "Applied Materials", "Lam Research"]),
        ("Memory",            ["Micron", "SK Hynix", "Samsung"]),
    ]),
    ("robotics", "ROBOTICS", PALETTE.subindices["robotics"], [
        ("Motion Control",    ["Fanuc", "Yaskawa", "Nidec"]),
        ("Industrial Auto",   ["Siemens", "ABB", "Keyence"]),
        ("Humanoid (Private)", ["Figure", "1X", "Agility"]),
        ("Surgical",          ["Intuitive Surgical"]),
    ]),
    ("space", "SPACE", PALETTE.subindices["space"], [
        ("Prime Contractors", ["Lockheed Martin", "Northrop Grumman"]),
        ("Launch",            ["Rocket Lab", "Arianespace"]),
        ("Satellite Services", ["AST SpaceMobile", "Planet Labs", "Satellogic"]),
    ]),
]

# Flow labels grouped by (from-band, to-band) to keep the diagram
# readable. Spec lists 9 specific flows; groups 1-3 collapse the four
# Materials→Semi flows into a single interface label block, which
# stays true to the data but avoids a thicket of crossing arrows.
FLOWS = [
    # (from band index, to band index, [labels], direction, gutter_offset)
    # Adjacent-band flows get a single compact label string joined with
    # " · " so the arrow doesn't drag a vertically-stacked label column
    # into the narrow inter-band gap. Skip / feedback flows stay
    # unlabelled on the diagram and carry their description in the
    # caption panel below.
    (0, 1, ["CMP polishing · 300mm wafers · Ultra-pure neon · CoWoS packaging"],
     "down", 0.0),
    (1, 2, ["Edge AI chips, power management"], "down", 0.0),
    (0, 2, ["NdFeB magnets for servo motors"],    "down-skip", 0.00),
    (0, 3, ["NdFeB magnets for reaction wheels"], "down-skip", 0.025),
    (1, 3, ["On-board processors, direct-to-device"], "down-skip", -0.025),
    (2, 1, ["Fab automation (feedback)"],         "up", 0.0),
]


def _draw_dependency_chain(figsize, fontscale=1.0, is_square=False):
    """Render the dependency chain at a given figure size.

    Layout in figure-axes coordinates:
      - Top strip (y > 0.92) — title + subtitle.
      - 4 sector bands each comprise a header strip above a box row.
      - Between adjacent bands is a flow band with the primary
        (adjacent) dependency arrow + labels.
      - Skip-flow and feedback arrows are drawn in the left/right
        gutters as unlabelled visual indicators. Their textual
        descriptions live in a small caption panel under the stack
        — keeps the diagram clean at small sizes.
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    fig.text(0.5, 0.968, "The Frontier Technology Stack",
             ha="center", va="top",
             fontproperties=title_font(size=18 * fontscale),
             color=PALETTE.ink)
    fig.text(0.5, 0.933,
             "Dependency flows across four sectors. Disruption in any layer propagates through the rest.",
             ha="center", va="top",
             fontproperties=subtitle_font(size=10 * fontscale),
             color=PALETTE.axis)

    # Leave an 8%-tall caption panel at the bottom for the skip /
    # feedback descriptions. Everything above bottom_y is the stack.
    x_left, x_right = 0.09, 0.91
    top_y = 0.895
    caption_h = 0.12
    bottom_y = 0.03 + caption_h

    header_h = 0.028            # per-band header strip
    flow_h   = 0.055            # between-band gap carrying labels
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

        # Header strip — solid sector colour with white text
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
                color="white", family="Space Grotesk",
                transform=ax.transAxes, zorder=3)

        # Band body — soft tint background
        body_rect = FancyBboxPatch(
            (x_left, band_bottom), x_right - x_left, band_top - band_bottom,
            boxstyle="round,pad=0.001,rounding_size=0.007",
            linewidth=0, facecolor=_tint(color, 0.10), zorder=1,
            transform=ax.transAxes,
        )
        ax.add_patch(body_rect)

        # Columns
        n = len(columns)
        total = (x_right - x_left) - 0.02          # 0.01 side padding each side
        gap   = 0.012
        col_w = (total - gap * (n - 1)) / n
        for ci, (col_title, entities) in enumerate(columns):
            x = x_left + 0.01 + ci * (col_w + gap)
            col_box = FancyBboxPatch(
                (x, band_bottom + 0.008), col_w, (band_top - band_bottom) - 0.016,
                boxstyle="round,pad=0.001,rounding_size=0.006",
                linewidth=0.9, edgecolor=color, facecolor="white", zorder=2,
                transform=ax.transAxes,
            )
            ax.add_patch(col_box)
            # Column title
            ax.text(x + col_w / 2, band_top - 0.014, col_title,
                    ha="center", va="top",
                    fontsize=8.5 * fontscale, fontweight="bold",
                    color=PALETTE.ink, family="Space Grotesk",
                    transform=ax.transAxes, zorder=3)
            # Entities — start with enough gap below the title baseline.
            line_h = 0.019 * fontscale
            for ei, ent in enumerate(entities):
                ax.text(x + col_w / 2,
                        band_top - 0.048 - ei * line_h,
                        ent,
                        ha="center", va="top",
                        fontsize=7.5 * fontscale, color=PALETTE.axis,
                        family="Mulish",
                        transform=ax.transAxes, zorder=3)

        y_cursor = band_bottom - flow_h

    # Draw flows.
    def arrow(x0, y0, x1, y1, color, lw, style="-|>", rad=0, zorder=4, dashed=False):
        kw = dict(
            arrowstyle=style, mutation_scale=14 * fontscale,
            color=color, linewidth=lw,
            transform=ax.transAxes, zorder=zorder,
        )
        if rad:
            kw["connectionstyle"] = f"arc3,rad={rad}"
        if dashed:
            kw["linestyle"] = (0, (3, 2))
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), **kw))

    # Adjacent flows (down arrows in each inter-band gap). One joined
    # label per flow — centred above the arrow so it doesn't run off
    # the right edge.
    for src, dst, labels, kind, _offset in FLOWS:
        if kind != "down":
            continue
        src_bottom = bands_geom[src][1]
        dst_header_top = bands_geom[dst][2]
        ax_x = 0.50
        arrow(ax_x, src_bottom - 0.002, ax_x, dst_header_top + 0.002,
              PALETTE.composite, 1.8)
        gap_top = src_bottom
        gap_bot = dst_header_top
        lines_y_center = (gap_top + gap_bot) / 2
        for li, lbl in enumerate(labels):
            y = lines_y_center + (li - (len(labels) - 1) / 2) * (0.014 * fontscale)
            ax.text(ax_x, y, lbl,
                    ha="center", va="center", style="italic",
                    fontsize=8 * fontscale, color=PALETTE.axis,
                    family="Mulish",
                    bbox=dict(boxstyle="round,pad=0.25",
                              facecolor="white", edgecolor="none"),
                    transform=ax.transAxes, zorder=5)

    # Skip flows — drawn as unlabelled thin arrows in the right gutter.
    # Labels go in the caption panel below the diagram.
    right_gutter_base = 0.945
    for src, dst, labels, kind, offset in FLOWS:
        if kind != "down-skip":
            continue
        src_bottom = bands_geom[src][1]
        dst_header_top = bands_geom[dst][2]
        gutter_x = right_gutter_base + offset
        arrow(gutter_x, src_bottom, gutter_x, dst_header_top,
              PALETTE.composite, 1.1, rad=-0.22)

    # Feedback flow — unlabelled dashed arrow in the left gutter;
    # described in the caption panel.
    left_gutter = 0.055
    for src, dst, labels, kind, _offset in FLOWS:
        if kind != "up":
            continue
        src_top    = bands_geom[src][2]
        dst_bottom = bands_geom[dst][1]
        arrow(left_gutter, src_top, left_gutter, dst_bottom,
              PALETTE.axis, 0.9, rad=0.25, dashed=True)

    # Caption panel — explains the skip flows + feedback loop using
    # coloured markers that match the arrows. Two columns to keep the
    # block compact.
    panel_top = bottom_y - 0.012
    panel_h   = caption_h - 0.015
    panel_x0, panel_x1 = x_left, x_right
    panel_rect = FancyBboxPatch(
        (panel_x0, panel_top - panel_h), panel_x1 - panel_x0, panel_h,
        boxstyle="round,pad=0.002,rounding_size=0.006",
        linewidth=0.8, edgecolor=PALETTE.grid, facecolor="#FAFBFC",
        zorder=1, transform=ax.transAxes,
    )
    ax.add_patch(panel_rect)

    # Caption entries: (colour, label, description)
    caption_entries = [
        (PALETTE.composite, "Materials → Robotics",
         "NdFeB magnets for servo motors"),
        (PALETTE.composite, "Materials → Space",
         "NdFeB magnets for reaction wheels"),
        (PALETTE.composite, "Semiconductors → Space",
         "On-board processors, direct-to-device"),
        (PALETTE.axis,      "Robotics → Semiconductors (feedback)",
         "Fab automation"),
    ]
    # Two-column layout inside the panel
    rows_per_col = 2
    col_w = (panel_x1 - panel_x0 - 0.03) / 2
    row_h = panel_h / rows_per_col
    for i, (col, title, desc) in enumerate(caption_entries):
        c = i // rows_per_col
        r = i % rows_per_col
        cx = panel_x0 + 0.015 + c * (col_w + 0.015)
        cy = panel_top - 0.015 - r * row_h
        # Small coloured swatch (circle)
        ax.scatter([cx], [cy], s=40 * fontscale, color=col,
                   zorder=3, transform=ax.transAxes)
        ax.text(cx + 0.012, cy, title,
                ha="left", va="center",
                fontsize=8.5 * fontscale, fontweight="bold",
                color=PALETTE.ink, family="Space Grotesk",
                transform=ax.transAxes, zorder=3)
        ax.text(cx + 0.012, cy - 0.024 * fontscale, desc,
                ha="left", va="center",
                fontsize=8 * fontscale, color=PALETTE.axis,
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
            label="Quarterly private robotics funding ($bn)")

    # Quarter boundary vertical rules (subtle)
    for qd in (date(2025, 6, 30), date(2025, 9, 30), date(2025, 12, 31)):
        ax1.axvline(qd, color=PALETTE.grid, linewidth=0.6, zorder=0)

    # Axis labels + ticks
    ax1.set_ylabel("Sub-index value (rebased to 100)", fontsize=10 * fontscale)
    ax2.set_ylabel("Private funding ($ billions)", fontsize=10 * fontscale,
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

    # Annotate the 3 smaller bars with quarter + $ amount (the 1Q26
    # bar gets its own bold callout below, so we skip it here to
    # avoid the redundant "1Q26 $31.5bn" stacking on top).
    for (m, a, lbl) in bars[:-1]:
        ax2.text(m, a + max(bar_y) * 0.03,
                 f"{lbl}  ${a:.1f}bn",
                 ha="center", va="bottom",
                 fontsize=8.5 * fontscale, color=PALETTE.axis,
                 family="Mulish")

    # 1Q26 bold callout — sits clearly above the bar with enough
    # headroom so the semi-transparent bar green doesn't bleed
    # through the lettering.
    q1 = bars[-1]
    ax2.text(q1[0], q1[1] + max(bar_y) * 0.15,
             f"Q1 2026\n${q1[1]:.1f}bn private capital",
             ha="center", va="bottom",
             fontsize=10 * fontscale, fontweight="bold",
             color=PALETTE.ink, zorder=10)

    # Robotics end-of-year annotation — pulled well to the LEFT of the
    # Q1 bar so the yellow line label doesn't collide with the bar's
    # bold callout. Single line, anchored at the line's end point via
    # the small indicator dot.
    if robotics:
        end_d, end_v = robotics[-1]
        from datetime import timedelta
        ax1.annotate("Public Robotics: +5.3% over 12 months",
                     xy=(end_d - timedelta(days=10), end_v),
                     xytext=(end_d - timedelta(days=120), end_v + 18),
                     ha="center", va="bottom",
                     fontsize=9.5 * fontscale, fontweight="bold",
                     color=PALETTE.ink,
                     arrowprops=dict(arrowstyle="-", color=PALETTE.axis, lw=0.8,
                                     shrinkA=2, shrinkB=4))

    # Divergence callout — one italic line placed at mid-right so it
    # labels the visible gap between bar height and line level.
    fig.text(0.60, 0.34,
             "The divergence: private conviction ahead of public pricing",
             ha="center", va="center",
             fontsize=9 * fontscale, fontweight="bold",
             color=PALETTE.axis, style="italic",
             family="Mulish")

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
