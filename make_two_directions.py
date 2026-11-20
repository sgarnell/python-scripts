#!/usr/bin/env python3
"""
Teaching figure (companion to make_nested_loop_eq8.py): one square matrix,
two directions.

    R_AB = sum_{a in A} sum_{b in B} w_ab      (top-right rectangle)
    R_BA = sum_{b in B} sum_{a in A} w_ba      (bottom-left rectangle)

Same toy 4x4 W as the nested-loop figure. Rows (Y axis) are sources,
columns (X axis) are targets; each cell is one directed connection
row -> column. The double sum nests inside ONE direction; the reverse
direction is the same formula run again with the groups swapped.

Output: two-directions.png in an output/ folder beside this script
(created if it does not exist).
Run:    python make_two_directions.py
Needs:  matplotlib
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "two-directions.png"

BG = "#1E1E1E"
INK = "#D4D4D4"
DIM = "#8A8A8A"
FAINT = "#5A5A5A"
GOLD = "#E8A33D"
BLUE = "#569CD6"
TEAL = "#4EC9B0"    # group A
PURPLE = "#C586C0"  # group B
CELL_BG = "#252526"
GOLD_BG = "#33270F"
BLUE_BG = "#14273D"

W = [
    [+0.21, -0.45, -0.30, +0.40],
    [-0.08, +0.33, +0.12, -0.16],
    [+0.52, -0.19, +0.27, -0.38],
    [-0.24, +0.41, -0.11, +0.18],
]
A_ROWS = [0, 1]
B_COLS = [2, 3]
B_ROWS = [2, 3]
A_COLS = [0, 1]


def fmt(v):
    return f"{v:+.2f}".replace("-", "\u2212")


def main():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # ---------- title ----------
    ax.text(8, 8.70, "One square, two directions \u2014 "
            r"$R_{AB}$ and $R_{BA}$",
            ha="center", va="center", fontsize=20, color=INK)

    # ---------- left: the grid with both off-diagonal blocks ----------
    gx, gy, cs = 2.15, 7.05, 1.06

    # axis titles
    ax.text(gx + 2 * cs, gy + 0.86, "TARGET \u2014 who receives (columns)",
            ha="center", va="center", fontsize=13.5, color=INK,
            fontweight="bold")
    ax.text(0.62, gy - 2 * cs, "SOURCE \u2014 who sends (rows)",
            ha="center", va="center", fontsize=13.5, color=INK,
            fontweight="bold", rotation=90)

    # column labels (neuron names, targets)
    for j in range(4):
        in_b = j in B_COLS
        ax.text(gx + (j + 0.5) * cs, gy + 0.30, rf"$n_{{{j + 1}}}$",
                ha="center", va="center", fontsize=14.5,
                color=PURPLE if in_b else FAINT,
                fontweight="bold" if in_b else "normal")
    # row labels (neuron names, sources)
    for i in range(4):
        in_a = i in A_ROWS
        ax.text(gx - 0.40, gy - (i + 0.5) * cs, rf"$n_{{{i + 1}}}$",
                ha="center", va="center", fontsize=14.5,
                color=TEAL if in_a else FAINT,
                fontweight="bold" if in_a else "normal")

    # cells
    for i in range(4):
        for j in range(4):
            if i in A_ROWS and j in B_COLS:
                face = GOLD_BG
            elif i in B_ROWS and j in A_COLS:
                face = BLUE_BG
            else:
                face = CELL_BG
            lit = face != CELL_BG
            ax.add_patch(Rectangle(
                (gx + j * cs, gy - (i + 1) * cs), cs, cs,
                facecolor=face, edgecolor="#3C3C3C", linewidth=0.8, zorder=1))
            ax.text(gx + (j + 0.5) * cs, gy - (i + 0.5) * cs, fmt(W[i][j]),
                    ha="center", va="center", fontsize=14.5, zorder=3,
                    color=INK if lit else FAINT,
                    fontweight="bold" if lit else "normal")

    # dashed mirror connector: n1->n3 cell and its mirror n3->n1
    ax.plot([gx + 2.5 * cs, gx + 0.5 * cs], [gy - 0.5 * cs, gy - 2.5 * cs],
            color=DIM, lw=1.4, linestyle=(0, (4, 3)), zorder=2)

    # block outlines
    ax.add_patch(Rectangle(
        (gx + B_COLS[0] * cs, gy - (A_ROWS[-1] + 1) * cs),
        2 * cs, 2 * cs, facecolor="none", edgecolor=GOLD, linewidth=3.0,
        zorder=4))
    ax.add_patch(Rectangle(
        (gx + A_COLS[0] * cs, gy - (B_ROWS[-1] + 1) * cs),
        2 * cs, 2 * cs, facecolor="none", edgecolor=BLUE, linewidth=3.0,
        zorder=4))

    # group brackets
    ax.annotate("", xy=(gx - 0.82, gy - 0.06),
                xytext=(gx - 0.82, gy - 2 * cs + 0.06),
                arrowprops=dict(arrowstyle="-", color=TEAL, lw=2.5))
    ax.text(gx - 1.08, gy - cs, "A", ha="center", va="center",
            fontsize=19, color=TEAL, fontweight="bold")
    ax.annotate("", xy=(gx + B_COLS[0] * cs + 0.06, gy + 0.58),
                xytext=(gx + 4 * cs - 0.06, gy + 0.58),
                arrowprops=dict(arrowstyle="-", color=PURPLE, lw=2.5))
    ax.text(gx + 4 * cs + 0.22, gy + 0.58, "B", ha="left", va="center",
            fontsize=16, color=PURPLE, fontweight="bold")

    ax.text(gx + 2 * cs, gy - 4 * cs - 0.36,
            "every neuron appears on both axes \u2014\n"
            "once as a source (its row), once as a target (its column);\n"
            "the dashed line joins two mirror cells:\n"
            "different synapses, opposite directions.",
            ha="center", va="top", fontsize=11.5, color=DIM, linespacing=1.5)

    # ---------- right: the two formulas ----------
    rx = 7.45
    ax.text(rx, 7.72, r"$R_{AB}\;=\;\sum_{a\,\in\,A}\;\sum_{b\,\in\,B}\;w_{ab}$",
            fontsize=19, color=GOLD, va="center")
    ax.text(rx, 7.14, "rows A \u00d7 columns B \u2014 the top-right rectangle",
            fontsize=12.5, color=DIM, va="center")
    ax.text(rx, 6.62,
            "\u22120.30 + 0.40 + 0.12 \u2212 0.16   =   +0.06",
            fontsize=14.5, color=INK, va="center", family="monospace")

    ax.text(rx, 5.62, r"$R_{BA}\;=\;\sum_{b\,\in\,B}\;\sum_{a\,\in\,A}\;w_{ba}$",
            fontsize=19, color=BLUE, va="center")
    ax.text(rx, 4.92, "rows B \u00d7 columns A \u2014 the bottom-left rectangle. "
            "Same formula,\ngroups swapped \u2014 note $w_{ba}$: the subscripts swap too",
            fontsize=12.5, color=DIM, va="center", linespacing=1.45)
    ax.text(rx, 4.06,
            "+0.52 \u2212 0.19 \u2212 0.24 + 0.41   =   +0.50",
            fontsize=14.5, color=INK, va="center", family="monospace")

    ax.text(rx, 3.30,
            "mirror cells:  $n_1 \\rightarrow n_3$  = \u22120.30,   "
            "but  $n_3 \\rightarrow n_1$  = +0.52",
            fontsize=13.5, color=INK, va="center")

    # ---------- key point box ----------
    ax.add_patch(Rectangle((rx - 0.25, 0.78), 8.35, 2.02,
                           facecolor="#252526", edgecolor=GOLD,
                           linewidth=1.2, zorder=1))
    ax.text(rx + 0.05, 2.52,
            "The double \u03a3 nests inside ONE direction \u2014 it walks the\n"
            "(a, b) pairs of a single block. The reverse direction is not\n"
            "hidden in the nesting: it is the same formula called again\n"
            "with the groups swapped. The pathway code calls it for all\n"
            "132 ordered pairs of groups.",
            fontsize=12.5, color=INK, va="top", linespacing=1.55, zorder=2)

    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
