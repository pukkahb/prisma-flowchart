"""
=============================================================================
PRISMA 2020 Flow Diagram
=============================================================================
USAGE:
    python prisma_flowdiagram.py

OUTPUT:
    prisma_flowdiagram.png  (in OUTPUT_DIR)

EDIT:
    • COUNTS dict  — update all numeric values
    • REASONS list — update full-text exclusion reasons
    • STYLE dict   — swap any colour
=============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT_DIR = "~/"
DPI        = 300

STYLE = {
    # header banner
    "header_fill":   "#FFBF00",   # gold/amber
    "header_text":   "black",

    # section tab pills (left margin)
    "tab_fill":      "#2A7B9B",   # teal-blue  ← edit to recolour tabs
    "tab_text":      "black",

    # main flow boxes
    "box_fill":      "#D6EAF8",   # light blue
    "box_edge":      "#2A7B9B",   # teal border
    "box_text":      "#1A1A2E",   # near-black text

    # exclusion boxes (right column)
    "excl_fill":     "#D6EAF8",
    "excl_edge":     "#2A7B9B",
    "excl_text":     "#1A1A2E",

    # arrows
    "arrow":         "#1A1A2E",
    "bg":            "white",
    "font":          "Times New Roman",
}

# ─────────────────────────────────────────────────────────────────────────────
# DRAWING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def box(ax, cx, cy, w, h, text,
        fill=None, edge=None, text_color=None,
        fontsize=9, bold=False, radius=0.018, linew=1.6,
        valign="center"):
    """
    Rounded-rectangle box with multi-line centred text.
    cx, cy = centre; w, h = full width / height (in axes units).
    """
    fill       = fill       or STYLE["box_fill"]
    edge       = edge       or STYLE["box_edge"]
    text_color = text_color or STYLE["box_text"]

    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fill, edgecolor=edge,
        linewidth=linew, zorder=3,
    )
    ax.add_patch(patch)
    ax.text(cx, cy, text,
            ha="center", va=valign,
            fontsize=fontsize,
            color=text_color,
            fontweight="bold" if bold else "normal",
            fontfamily=STYLE["font"],
            multialignment="center",
            linespacing=1.35,
            zorder=4)


def arrow_down(ax, cx, y_top, y_bot, lw=2.0):
    """Vertical downward arrow (centre-aligned)."""
    ax.annotate(
        "", xy=(cx, y_bot), xytext=(cx, y_top),
        arrowprops=dict(
            arrowstyle="-|>",
            color=STYLE["arrow"],
            lw=lw,
            mutation_scale=16,
        ), zorder=5,
    )


def arrow_right(ax, x_left, y, x_right, lw=2.0):
    """
    Horizontal arrow pointing RIGHT using FancyArrow.
    This gives exact geometric control — head always points right.
    x_right should be the left edge of the destination box.
    """
    import matplotlib.patches as mp
    dx        = x_right - x_left
    head_len  = 0.022          # arrowhead length in axes units
    head_w    = 0.018          # arrowhead width in axes units
    ax.add_patch(mp.FancyArrow(
        x_left, y, dx - head_len * 0.3, 0,
        width=lw * 0.003,
        head_width=head_w,
        head_length=head_len,
        length_includes_head=True,
        color=STYLE["arrow"],
        zorder=5,
    ))


def section_tab(ax, cy, label, x=0.055, w=0.072, h=0.10, radius=0.025):
    """
    Teal rounded-pill tab on the left margin, text rotated 90°.
    """
    patch = FancyBboxPatch(
        (x - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=STYLE["tab_fill"],
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(patch)
    ax.text(x, cy, label,
            ha="center", va="center",
            fontsize=12, fontweight="bold",
            color=STYLE["tab_text"],
            fontfamily=STYLE["font"],
            rotation=90, zorder=4)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN DIAGRAM
# ─────────────────────────────────────────────────────────────────────────────
def draw_prisma(save=True):

    # ── EDIT THESE VALUES ────────────────────────────────────────────────────
    COUNTS = {
        "database_results":   251,   # total records identified
        "duplicates_removed":  74,   # duplicates removed
        "records_screened":   177,   # = database_results - duplicates_removed
        "records_excluded":   111,   # excluded at title/abstract
        "full_text_assessed":  66,   # full-text retrieved
        "full_text_excluded":  17,   # full-text excluded
        "studies_included":    49,   # final included
    }

    # Two databases in identification box
    DB_LINES = [
        "PubMed  (n = 104)",
        "Scopus  (n = 147)",
    ]

    # Removals before screening (right box in Identification row)
    REMOVALS = [
        f"Duplicate records removed  (n = {COUNTS['duplicates_removed']})",
        #"Records marked ineligible by automation tools  (n = 0)",
        #"Records removed for other reasons  (n = 0)",
    ]

    # Full-text exclusion reasons (right box in Eligibility row)
    REASONS = [
        "No access (n = 14)",
        "Wrong study design  (n = 2)",
        "Wrong publication type  (n = 1)",
    ]
    # ── END EDITABLE SECTION ─────────────────────────────────────────────────

    # ── canvas ──
    fig, ax = plt.subplots(figsize=(12, 15))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor(STYLE["bg"])

    # ── layout geometry ──
    # X positions
    X_TAB   = 0.055   # section tab centre
    X_LEFT  = 0.340   # main-flow box centre
    X_RIGHT = 0.790   # exclusion box centre

    # box sizes
    BW = 0.38    # main flow box width  ← shrunk to create gap for arrow
    BH = 0.085   # main flow box height
    EW = 0.36    # exclusion box width
    EH = 0.085   # exclusion box height  (will be stretched for reasons)
    # Gap between boxes: X_RIGHT - EW/2 - (X_LEFT + BW/2) = 0.790-0.180-0.340-0.190 = 0.080

    # Y centres for each row (1 = top)
    Y_HEADER = 0.955
    Y_ID     = 0.845   # Identification row
    Y_SCR    = 0.655   # Screening row
    Y_FT     = 0.475   # Full-text (Eligibility) row
    Y_INC    = 0.270   # Included row

    HB = 0.040   # header banner half-height

    # ── HEADER BANNER ────────────────────────────────────────────────────────
    header = FancyBboxPatch(
        (0.08, Y_HEADER - HB), 0.84, HB * 2,
        boxstyle="round,pad=0,rounding_size=0.020",
        facecolor=STYLE["header_fill"], edgecolor="none", zorder=3,
    )
    ax.add_patch(header)
    ax.text(0.50, Y_HEADER,
            "Identification of studies via databases",
            ha="center", va="center",
            fontsize=12, fontweight="bold",
            color=STYLE["header_text"],
            fontfamily=STYLE["font"], zorder=4)

    # ── SECTION TABS ─────────────────────────────────────────────────────────
    section_tab(ax, Y_ID,  "Identification", h=0.105)
    section_tab(ax, Y_SCR, "Screening",       h=0.095)
    section_tab(ax, Y_FT,  "Eligibility",     h=0.095)
    section_tab(ax, Y_INC, "Included",        h=0.075)

    # ── ROW 1: IDENTIFICATION ─────────────────────────────────────────────────
    # Left box — databases
    db_text = (
        f"Records identified from databases*\n"
        f"(n = {COUNTS['database_results']})\n"
        + "\n".join(f"   • {l}" for l in DB_LINES)
    )
    box(ax, X_LEFT, Y_ID, BW, BH + 0.03, db_text, fontsize=9)

    # Right box — removals before screening
    rem_text = (
        "Records removed before screening:\n"
        + "\n".join(f"  • {r}" for r in REMOVALS)
    )
    box(ax, X_RIGHT, Y_ID, EW, BH + 0.03, rem_text, fontsize=8.5)

    # Arrow: left box → right box (horizontal, pointing right)
    arrow_right(ax, X_LEFT + BW / 2, Y_ID, X_RIGHT - EW / 2)

    # Arrow: left box downward to screening row
    arrow_down(ax, X_LEFT, Y_ID - (BH + 0.03) / 2, Y_SCR + BH / 2)

    # ── ROW 2: SCREENING ────────────────────────────────────────────────────
    scr_text = (
        f"Records screened\n(n = {COUNTS['records_screened']})"
    )
    box(ax, X_LEFT, Y_SCR, BW, BH, scr_text, fontsize=9)

    excl_scr_text = (
        f"Records excluded based on title / abstract\n"
        f"(n = {COUNTS['records_excluded']})"
    )
    box(ax, X_RIGHT, Y_SCR, EW, BH, excl_scr_text, fontsize=8.5)

    arrow_right(ax, X_LEFT + BW / 2, Y_SCR, X_RIGHT - EW / 2)
    arrow_down(ax, X_LEFT, Y_SCR - BH / 2, Y_FT + BH / 2)

    # ── ROW 3: ELIGIBILITY ───────────────────────────────────────────────────
    ft_text = (
        f"Full-text articles assessed for eligibility\n"
        f"(n = {COUNTS['full_text_assessed']})"
    )
    box(ax, X_LEFT, Y_FT, BW, BH, ft_text, fontsize=9)

    # Exclusion box with reasons listed inside
    reasons_text = (
        f"Records excluded  (n = {COUNTS['full_text_excluded']}):\n"
        + "\n".join(f"  • {r}" for r in REASONS)
    )
    # taller box to fit all reasons
    excl_h = BH + 0.014 * len(REASONS)
    box(ax, X_RIGHT, Y_FT, EW, excl_h, reasons_text, fontsize=8.0)

    arrow_right(ax, X_LEFT + BW / 2, Y_FT, X_RIGHT - EW / 2)
    arrow_down(ax, X_LEFT, Y_FT - BH / 2, Y_INC + BH / 2)

    # ── ROW 4: INCLUDED ──────────────────────────────────────────────────────
    inc_text = (
        f"Studies included in systematic review\n"
        f"(n = {COUNTS['studies_included']})"
    )
    box(ax, X_LEFT, Y_INC, BW, BH, inc_text,
        fontsize=12, bold=True)

    # ── FOOTNOTE ─────────────────────────────────────────────────────────────
    ax.text(0.10, 0.025,
            "* PRISMA 2020 — Preferred Reporting Items for Systematic Reviews and Meta-Analyses.\n"
            "  Databases searched: PubMed and Scopus.",
            ha="left", va="bottom", fontsize=7.5,
            color="#555555", style="italic",
            fontfamily=STYLE["font"])

    plt.tight_layout(pad=0.5)
    if save:
        plt.savefig(
            OUTPUT_DIR + "prisma_flowdiagram.png",
            dpi=DPI, bbox_inches="tight",
            facecolor=STYLE["bg"],
        )
        print("Saved prisma_flowdiagram.png")
    plt.close()


if __name__ == "__main__":
    draw_prisma()
