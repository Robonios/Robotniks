"""
Robotnik Report — Index Charts (Figures 1, 2, 3)
================================================
Regenerates the three index charts that appear in every quarterly
report. Always consumes the live data files in data/index/ and
data/prices/benchmarks.json — the script itself never transforms
the data, it only visualises what's there.

Figures produced:
  Fig 1  chart_q1_benchmark_comparison.png
         Composite vs SPY / QQQ / SOXX / ROBO, Q1 2026, rebased 100
  Fig 2  chart_since_inception.png
         Composite 12-month view, 31 Mar 2025 → 31 Mar 2026 (base 1000)
  Fig 3  chart_q1_subindex_comparison.png
         Composite + 4 sub-indices, Q1 2026, rebased 100

Outputs go to both:
  data/exports/report_charts/       — 300 DPI, for the PDF
  data/exports/report_charts_web/   — 150 DPI, for the HTML web copy

Uses scripts/report_chart_style.py (the locked visual template).

Usage:
    python scripts/generate_index_charts.py
"""

from pathlib import Path
import json
from datetime import datetime

import matplotlib.dates as mdates

# Must import + apply style BEFORE any pyplot Figure is created.
from report_chart_style import (
    apply_style, save_report_chart,
    PALETTE, SIZE, DPI,
    composite_kw, secondary_kw, base_ref_kw,
    title_font, subtitle_font,
    annotate_event,
)
apply_style()

import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────

ROOT       = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "data" / "index" / "robotnik_index.json"
SUBS_PATH  = ROOT / "data" / "index" / "sub_indices.json"
BENCH_PATH = ROOT / "data" / "prices" / "benchmarks.json"

OUT_PRINT  = ROOT / "data" / "exports" / "report_charts"
OUT_WEB    = ROOT / "data" / "exports" / "report_charts_web"
for p in (OUT_PRINT, OUT_WEB):
    p.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────
# Data loaders — return ordered (date-object, value) tuples
# ─────────────────────────────────────────────────────────────────────

def _as_dt(d):
    return datetime.strptime(d, "%Y-%m-%d").date()


def load_composite():
    data = json.load(open(INDEX_PATH))
    return [(_as_dt(p["date"]), p["value"]) for p in data["series"]]


def load_sub(key):
    data = json.load(open(SUBS_PATH))
    series = data[key]["series"]
    return [(_as_dt(p["date"]), p["value"]) for p in series]


def load_benchmark(ticker):
    data = json.load(open(BENCH_PATH))
    series = data["benchmarks"][ticker]["series"]
    return [(_as_dt(p["date"]), p["close"]) for p in series]


def slice_between(series, start, end):
    """Inclusive date window."""
    return [(d, v) for d, v in series if start <= d <= end]


def value_on_or_before(series, target):
    """Last (date, value) on or before target. For rebasing."""
    for d, v in reversed(series):
        if d <= target:
            return d, v
    return None, None


def rebase_to(series, base_date, base=100.0):
    """Rebase every value to ``base`` at ``base_date`` (on-or-before)."""
    _, base_val = value_on_or_before(series, base_date)
    if not base_val:
        return series
    return [(d, base * v / base_val) for d, v in series]


# ─────────────────────────────────────────────────────────────────────
# Figure 1 — Composite vs benchmarks, Q1 2026
# ─────────────────────────────────────────────────────────────────────

def fig1_benchmark_comparison():
    start = _as_dt("2025-12-31")
    end   = _as_dt("2026-03-31")

    comp = slice_between(load_composite(), start, end)
    comp = rebase_to(comp, start)

    bench = {}
    labels = {
        "SPY":  "S&P 500",
        "QQQ":  "NASDAQ",
        "SOXX": "SOX",
        "ROBO": "ROBO Global",
    }
    for t in ("SPY", "QQQ", "SOXX", "ROBO"):
        b = slice_between(load_benchmark(t), start, end)
        bench[t] = rebase_to(b, start)

    fig, ax = plt.subplots(figsize=SIZE)

    # Base-100 reference
    ax.axhline(100, **base_ref_kw())

    # Benchmarks first so the Composite hero line sits on top.
    for t in ("SPY", "QQQ", "SOXX", "ROBO"):
        xs = [d for d, _ in bench[t]]
        ys = [v for _, v in bench[t]]
        ax.plot(xs, ys, **secondary_kw(PALETTE.benchmarks[t], label=labels[t]))

    # Composite
    cxs = [d for d, _ in comp]
    cys = [v for _, v in comp]
    ax.plot(cxs, cys, **composite_kw(label="Robotnik Composite"))

    ax.set_title("Robotnik Composite vs Major Benchmarks — Q1 2026",
                 fontproperties=title_font())
    fig.text(0.5, 0.905, "All series rebased to 100 on 31 December 2025",
             ha="center", va="top", fontproperties=subtitle_font(),
             color=PALETTE.axis)

    # X-axis: month ticks
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlim(start, end)

    ax.set_ylabel("Index (31 Dec 2025 = 100)")
    ax.legend(loc="upper left", ncol=1)

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    return fig, _q1_closes("fig1", comp, bench)


def _q1_closes(tag, comp, bench):
    last_comp = comp[-1] if comp else None
    lasts = {"Robotnik Composite": last_comp[1] if last_comp else None}
    for t, series in bench.items():
        lasts[t] = series[-1][1] if series else None
    return lasts


# ─────────────────────────────────────────────────────────────────────
# Figure 2 — Composite 12-month view
# ─────────────────────────────────────────────────────────────────────

def fig2_since_inception():
    start = _as_dt("2025-03-31")
    end   = _as_dt("2026-03-31")

    comp_all = load_composite()
    comp = slice_between(comp_all, start, end)

    fig, ax = plt.subplots(figsize=SIZE)

    ax.axhline(1000, **base_ref_kw())

    xs = [d for d, _ in comp]
    ys = [v for _, v in comp]
    ax.plot(xs, ys, **composite_kw(label="Robotnik Composite"))

    # Event annotations. y-offsets staggered to avoid overlap.
    series_map = {d: v for d, v in comp}
    def val_on_or_before(target):
        target_d = _as_dt(target)
        ds = sorted([d for d in series_map if d <= target_d], reverse=True)
        return ds[0], series_map[ds[0]]

    # (date, label, yoff, xoff_days) — the two Q1 events are 7 weeks
    # apart so their annotation pills collide at this figure width if
    # both are pinned to the same x. Stagger: push the rare-earth pill
    # further down and the tariff pill further right so their boxes
    # don't overlap the text.
    from datetime import timedelta as _td
    events = [
        ("2025-07-31", "Q2 earnings beats",       +140, 0),
        ("2025-10-24", "Q3 earnings surprise",    +160, 0),
        ("2026-02-04", "China rare-earth ban",    -260, -18),
        ("2026-03-26", "Tariff ruling −4.6% day", -150, +8),
    ]
    for date_str, label, yoff, xoff_days in events:
        x, y = val_on_or_before(date_str)
        xoff = _td(days=xoff_days) if xoff_days else 0
        annotate_event(ax, x, y, label, yoff, xoff=xoff)

    ax.set_title("Robotnik Composite Index — Twelve Month Review",
                 fontproperties=title_font())
    fig.text(0.5, 0.905,
             "Base 1,000 on 31 March 2025 to close 1,848.95 on 31 March 2026 (+84.9%)",
             ha="center", va="top", fontproperties=subtitle_font(),
             color=PALETTE.axis)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_xlim(start, end)

    ax.set_ylabel("Index level")
    ax.legend(loc="upper left")

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    return fig


# ─────────────────────────────────────────────────────────────────────
# Figure 3 — Sub-indices + Composite, Q1 2026
# ─────────────────────────────────────────────────────────────────────

def fig3_subindex_comparison():
    start = _as_dt("2025-12-31")
    end   = _as_dt("2026-03-31")

    comp = rebase_to(slice_between(load_composite(), start, end), start)
    subs = {
        k: rebase_to(slice_between(load_sub(k), start, end), start)
        for k in ("semiconductor", "robotics", "space", "materials")
    }

    labels = {
        "semiconductor": "Semiconductors",
        "robotics":      "Robotics",
        "space":         "Space",
        "materials":     "Materials & Inputs",
    }

    fig, ax = plt.subplots(figsize=SIZE)
    ax.axhline(100, **base_ref_kw())

    # Plot sub-indices first so the Composite hero sits on top.
    for key in ("semiconductor", "robotics", "space", "materials"):
        s = subs[key]
        xs = [d for d, _ in s]
        ys = [v for _, v in s]
        ax.plot(xs, ys, **secondary_kw(PALETTE.subindices[key], label=labels[key]))

    cxs = [d for d, _ in comp]
    cys = [v for _, v in comp]
    ax.plot(cxs, cys, **composite_kw(label="Robotnik Composite"))

    ax.set_title("Robotnik Sub-Indices — Q1 2026 Performance",
                 fontproperties=title_font())
    fig.text(0.5, 0.905, "All series rebased to 100 on 31 December 2025",
             ha="center", va="top", fontproperties=subtitle_font(),
             color=PALETTE.axis)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlim(start, end)

    ax.set_ylabel("Index (31 Dec 2025 = 100)")
    ax.legend(loc="upper left", ncol=1)

    fig.tight_layout(rect=[0, 0, 1, 0.90])

    closes = {"Robotnik Composite": comp[-1][1]}
    for k in subs:
        closes[labels[k]] = subs[k][-1][1]
    return fig, closes


# ─────────────────────────────────────────────────────────────────────
# Save at two sizes
# ─────────────────────────────────────────────────────────────────────

def _save_both(fig, filename):
    """Write a high-DPI copy for the PDF and a 150-DPI copy for the web."""
    p1 = OUT_PRINT / filename
    p2 = OUT_WEB / filename
    save_report_chart(fig, p1)
    fig.savefig(p2, dpi=150, bbox_inches="tight", facecolor=PALETTE.paper)
    return p1, p2


def main():
    # Figure 1
    fig, f1_closes = fig1_benchmark_comparison()
    p1, p2 = _save_both(fig, "chart_q1_benchmark_comparison.png")
    plt.close(fig)
    print(f"Fig 1 → {p1}  (+ web copy)")
    print(f"  31 Mar 2026 closes (index base 100):")
    for k, v in f1_closes.items():
        if v is not None:
            print(f"    {k:<22} {v:>6.2f}")

    # Figure 2
    fig = fig2_since_inception()
    p1, p2 = _save_both(fig, "chart_since_inception.png")
    plt.close(fig)
    print(f"Fig 2 → {p1}  (+ web copy)")

    # Figure 3
    fig, f3_closes = fig3_subindex_comparison()
    p1, p2 = _save_both(fig, "chart_q1_subindex_comparison.png")
    plt.close(fig)
    print(f"Fig 3 → {p1}  (+ web copy)")
    print(f"  31 Mar 2026 closes (index base 100):")
    for k, v in f3_closes.items():
        if v is not None:
            print(f"    {k:<22} {v:>6.2f}")


if __name__ == "__main__":
    main()
