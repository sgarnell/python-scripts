#!/usr/bin/env python3
"""
Teaching figure: how the double sum in equation (8) adds up a block.

    R_AB = sum_{a in A} sum_{b in B} w_ab

Shown on a toy 4x4 matrix W (not real data). Groups: A = source rows {1, 2},
B = target columns {3, 4}. The nested loop visits the 2x2 A x B rectangle
row by row and adds its four cells; every cell outside the rectangle is
never visited.

Output: nested-loop-eq8.png in an output/ folder beside this script
(created if it does not exist).
Run:    python make_nested_loop_eq8.py
Needs:  matplotlib
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "nested-loop-eq8.png"

BG = "#1E1E1E"
INK = "#D4D4D4"
DIM = "#8A8A8A"
FAINT = "#5A5A5A"
GOLD = "#E8A33D"
TEAL = "#4EC9B0"    # group A
PURPLE = "#C586C0"  # group B
CELL_BG = "#252526"
BLOCK_BG = "#33270F"

W = [
    [+0.21, -0.45, -0.30, +0.40],
    [-0.08, +0.33, +0.12, -0.16],
    [+0.52, -0.19, +0.27, -0.38],
    [-0.24, +0.41, -0.11, +0.18],
]
A_ROWS = [0, 1]   # neurons 1, 2
B_COLS = [2, 3]   # neurons 3, 4


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
    ax.text(
        8, 8.72,
        r"$R_{AB}\;=\;\sum_{a\,\in\,A}\;\sum_{b\,\in\,B}\;w_{ab}$"
        "   \u2014   the nested loop, on a toy matrix",
        ha="center", va="center", fontsize=20, color=INK,
    )

    # ---------- left: the 4x4 grid ----------
    gx, gy, cs = 1.55, 7.30, 1.02  # grid left x, top y, cell size

    # column labels: target neuron names
    for j in range(4):
        in_b = j in B_COLS
        ax.text(gx + (j + 0.5) * cs, gy + 0.30, rf"$n_{{{j + 1}}}$",
                ha="center", va="center", fontsize=14.5,
                color=PURPLE if in_b else FAINT,
                fontweight="bold" if in_b else "normal")
    # row labels: source neuron names
    for i in range(4):
        in_a = i in A_ROWS
        ax.text(gx - 0.38, gy - (i + 0.5) * cs, rf"$n_{{{i + 1}}}$",
                ha="center", va="center", fontsize=14.5,
                color=TEAL if in_a else FAINT,
                fontweight="bold" if in_a else "normal")

    # cells
    for i in range(4):
        for j in range(4):
            in_block = i in A_ROWS and j in B_COLS
            ax.add_patch(Rectangle(
                (gx + j * cs, gy - (i + 1) * cs), cs, cs,
                facecolor=BLOCK_BG if in_block else CELL_BG,
                edgecolor="#3C3C3C", linewidth=0.8, zorder=1))
            ax.text(gx + (j + 0.5) * cs, gy - (i + 0.5) * cs, fmt(W[i][j]),
                    ha="center", va="center", fontsize=14.5, zorder=3,
                    color=INK if in_block else FAINT,
                    fontweight="bold" if in_block else "normal")

    # gold outline around the A x B rectangle
    ax.add_patch(Rectangle(
        (gx + B_COLS[0] * cs, gy - (A_ROWS[-1] + 1) * cs),
        len(B_COLS) * cs, len(A_ROWS) * cs,
        facecolor="none", edgecolor=GOLD, linewidth=3.0, zorder=4))

    # group A bracket (left of rows 1-2) and group B bracket (above cols 3-4)
    ax.annotate("", xy=(gx - 0.80, gy - 0.06),
                xytext=(gx - 0.80, gy - 2 * cs + 0.06),
                arrowprops=dict(arrowstyle="-", color=TEAL, lw=2.5))
    ax.text(gx - 1.06, gy - cs, "A", ha="center", va="center",
            fontsize=19, color=TEAL, fontweight="bold")
    ax.annotate("", xy=(gx + B_COLS[0] * cs + 0.06, gy + 0.56),
                xytext=(gx + 4 * cs - 0.06, gy + 0.56),
                arrowprops=dict(arrowstyle="-", color=PURPLE, lw=2.5))
    ax.text(gx + 3 * cs, gy + 0.80, "B \u2014 target columns", ha="center",
            va="center", fontsize=11.5, color=PURPLE)

    ax.text(gx - 0.40, gy - 4 * cs - 0.34,
            "toy matrix $W$ \u2014 the neurons are $n_1$ to $n_4$\n"
            "$n_1, n_2$ form group A \u00b7 $n_3, n_4$ form group B\n"
            "each neuron sits in exactly one group;\n"
            "only the gold rectangle is summed;\n"
            "grey cells are never visited",
            ha="left", va="top", fontsize=11.5, color=DIM, linespacing=1.5)

    # ---------- right top: the loops as code ----------
    rx = 7.05
    ax.text(rx, 8.02, "the two $\\Sigma$'s are two loops:", fontsize=15,
            color=INK, va="center")
    code = (
        "total = 0\n"
        "for a in A:      \u2190 outer \u03a3 \u2014 a = source neuron: n1, then n2\n"
        "    for b in B:  \u2190 inner \u03a3 \u2014 b = target neuron: n3, then n4\n"
        "        total = total + w[a][b]"
    )
    ax.text(rx + 0.15, 7.70, code, fontsize=12.5, color="#9CDCFE",
            va="top", family="monospace", linespacing=1.55)

    # ---------- right middle: the block, enlarged, in visit order ----------
    bx, by, bs = 7.35, 5.98, 1.28  # block left x, top y, cell size
    ax.text(bx + bs, by + 0.32, "the block, visited in loop order",
            ha="center", va="center", fontsize=14.5, color=INK)
    order = [(0, 2), (0, 3), (1, 2), (1, 3)]  # (row, col) in visit order
    centres = {}
    for n, (i, j) in enumerate(order, start=1):
        li, lj = i - A_ROWS[0], j - B_COLS[0]
        x0, y0 = bx + lj * bs, by - (li + 1) * bs
        centres[n] = (x0 + bs / 2, y0 + bs / 2)
        ax.add_patch(Rectangle((x0, y0), bs, bs, facecolor=BLOCK_BG,
                               edgecolor=GOLD, linewidth=1.6, zorder=1))
        ax.text(x0 + bs / 2, y0 + bs / 2 + 0.14, fmt(W[i][j]),
                ha="center", va="center", fontsize=17, color=INK,
                fontweight="bold", zorder=3)
        ax.text(x0 + bs / 2, y0 + bs / 2 - 0.34,
                rf"$n_{{{i + 1}}} \rightarrow n_{{{j + 1}}}$",
                ha="center", va="center", fontsize=11.5, color=DIM, zorder=3)
        # visit-order badge
        ax.add_patch(plt.Circle((x0 + 0.21, y0 + bs - 0.21), 0.155,
                                facecolor=GOLD, edgecolor="none", zorder=4))
        ax.text(x0 + 0.21, y0 + bs - 0.21, str(n), ha="center", va="center",
                fontsize=11, color="#1E1E1E", fontweight="bold", zorder=5)
    # wrap arrow: end of row a=1 down to row a=2, on the right side
    (x2, y2), (x3, y3) = centres[2], centres[3]
    ax.add_patch(FancyArrowPatch(
        (bx + 2 * bs + 0.30, y2), (bx + 2 * bs + 0.30, y3),
        arrowstyle="-|>", mutation_scale=17, color=GOLD, lw=2,
        connectionstyle="arc3,rad=-0.45", zorder=2))
    ax.text(bx + 2 * bs + 0.66, (y2 + y3) / 2,
            "next row:\nthe inner loop\nstarts over",
            ha="left", va="center", fontsize=10.5, color=DIM, linespacing=1.45)

    # ---------- right bottom: the running total ----------
    ax.text(rx, 3.06, "the running total:", fontsize=15, color=INK,
            va="center")
    lines = ["start at 0"]
    run = 0.0
    for n, v in enumerate([-0.30, +0.40, +0.12, -0.16], start=1):
        run += v
        lines.append(f"step {n}:  add {fmt(v)}   \u2192   total {fmt(run)}")
    ax.text(rx + 0.15, 2.76, "\n".join(lines), fontsize=13,
            color="#9CDCFE", va="top", family="monospace", linespacing=1.6)
    ax.text(13.55, 1.00, r"$R_{AB}\;=\;+\,0.06$", fontsize=23, color=GOLD,
            ha="center", va="center", fontweight="bold")

    # ---------- footer ----------
    ax.text(8, 0.36,
            "Equation (9) runs this same loop over each mode's layer grid "
            "instead of over $W$.",
            ha="center", va="center", fontsize=12.5, color=DIM)

    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
