#!/usr/bin/env python3
"""
Teaching figure: equation (8) in two stages -- pair the groups, then
fill the roles.

    R_AB = sum over (a, b) in A x B of w_ab

A and B in eq. (8) are dummy variables: placeholders for whichever
group is sending and whichever is receiving. Stage 1 (left): the groups,
and one role-binding box per ordered pair -- those pairs are all
the AB pairs there are. Stage 2 (right): take the first pair and bind the roles,
A := the sending group, B := the receiving group; the block is then
A's neurons (rows) x B's neurons (columns), and the pair loop sums it.
The second pair runs the same code with the roles filled the other way.

Shown on a toy 4x4 matrix W (not real data): groups G1 = {n1, n2} and
G2 = {n3, n4}; pair 1 (G1 -> G2) gives R = +0.06, pair 2 (G2 -> G1)
gives R = +0.50. (This absorbs the point of make_two_directions.py,
which stays in the repo.)

Output: nested-loop-eq8.png in an output/ folder beside this script
(created if it does not exist).
Run:    python make_nested_loop_eq8.py
Needs:  matplotlib
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "nested-loop-eq8.png"

BG = "#1E1E1E"
PANEL = "#141A22"
INK = "#D4D4D4"
DIM = "#8A8A8A"
FAINT = "#5A5A5A"
GOLD = "#E8A33D"
BLUE = "#569CD6"     # pair 2
LIGHT = "#9CDCFE"
TEAL = "#4EC9B0"     # group G1
PURPLE = "#C586C0"   # group G2
CELL_BG = "#252526"
BLOCK_BG = "#33270F"
BLOCK_BG_BA = "#1B2733"

W = [
    [+0.21, -0.45, -0.30, +0.40],
    [-0.08, +0.33, +0.12, -0.16],
    [+0.52, -0.19, +0.27, -0.38],
    [-0.24, +0.41, -0.11, +0.18],
]
G1_IDX = [0, 1]   # neurons n1, n2
G2_IDX = [2, 3]   # neurons n3, n4


def fmt(v):
    return f"{v:+.2f}".replace("-", "\u2212")


def block_sum(rows, cols):
    return sum(W[i][j] for i in rows for j in cols)


def group_tile(ax, x, y, w, h, name, members, colour):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07",
        facecolor=PANEL, edgecolor=colour, lw=1.6, zorder=1))
    ax.text(x + 0.20, y + h - 0.28, name, fontsize=15, color=colour,
            fontweight="bold", va="center", zorder=3)
    pw, ph, gap = 0.72, 0.44, 0.14
    start = x + (w - (len(members) * pw + (len(members) - 1) * gap)) / 2
    for k, m in enumerate(members):
        px = start + k * (pw + gap)
        ax.add_patch(FancyBboxPatch(
            (px, y + 0.15), pw, ph, boxstyle="round,pad=0,rounding_size=0.05",
            facecolor="#DDE3EC", edgecolor="none", zorder=2))
        ax.text(px + pw / 2, y + 0.15 + ph / 2, m, fontsize=12.5,
                color="#141A22", fontweight="bold", ha="center",
                va="center", zorder=3)


def main():
    r_pair1 = block_sum(G1_IDX, G2_IDX)   # +0.06
    r_pair2 = block_sum(G2_IDX, G1_IDX)   # +0.50

    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # ---------- title ----------
    ax.text(
        8, 8.70,
        r"$R_{AB}\;=\;\sum_{(a,\,b)\,\in\,A\,\times\,B}\;w_{ab}$"
        "   \u2014   A and B are dummy variables, filled pair by pair",
        ha="center", va="center", fontsize=18.5, color=INK,
    )

    # ================= LEFT: stage 1 -- pair the groups =================
    ax.text(0.55, 8.10, "1 \u2014 the groups, and every ordered pair",
            fontsize=14.5, color=INK, va="center", fontweight="bold")

    group_tile(ax, 0.55, 6.50, 2.62, 1.20, "G1", ["n1", "n2"], TEAL)
    group_tile(ax, 3.32, 6.50, 2.62, 1.20, "G2", ["n3", "n4"], PURPLE)

    ax.text(0.55, 6.16, "two groups, two ordered pairs:",
            fontsize=12.5, color=DIM, va="center")

    # one binding box per pair: gold for pair 1, blue for pair 2
    def binding_box(top, edge, lead, a_name, a_col, b_name, b_col):
        ax.add_patch(FancyBboxPatch(
            (0.55, top - 1.12), 5.38, 1.12,
            boxstyle="round,pad=0,rounding_size=0.07",
            facecolor=PANEL, edgecolor=edge, lw=1.6, zorder=1))
        ax.text(0.80, top - 0.26, lead, fontsize=11.5, color=DIM,
                va="center", zorder=3)
        ax.text(0.80, top - 0.60, f"A = {a_name}", fontsize=14,
                color=a_col, fontweight="bold", va="center", zorder=3)
        ax.text(1.95, top - 0.60, "\u2014 the sending group",
                fontsize=12.5, color=INK, va="center", zorder=3)
        ax.text(0.80, top - 0.90, f"B = {b_name}", fontsize=14,
                color=b_col, fontweight="bold", va="center", zorder=3)
        ax.text(1.95, top - 0.90, "\u2014 the receiving group",
                fontsize=12.5, color=INK, va="center", zorder=3)

    binding_box(5.90, GOLD, "take pair 1 \u2014 fill the roles:",
                "G1", TEAL, "G2", PURPLE)
    binding_box(4.56, BLUE,
                "take pair 2 \u2014 fill the roles the other way:",
                "G2", PURPLE, "G1", TEAL)

    ax.text(0.55, 3.18,
            "A and B are not groups \u2014 they are the two roles in\n"
            "eq. (8). Each pair fills them with its own groups,\n"
            "and gets its own block and its own sum.\n"
            "real run: 12 groups \u2192 132 ordered pairs",
            ha="left", va="top", fontsize=11, color=DIM, linespacing=1.5)

    # ================= RIGHT: stage 2 -- fill the roles, take the block ==
    ax.text(6.80, 8.10, "2 \u2014 with the roles filled, take the block",
            fontsize=14.5, color=INK, va="center", fontweight="bold")

    gx, gy, cs = 7.55, 7.00, 0.94  # grid left x, top y, cell size
    # column labels: target neuron names, coloured by their group
    for j in range(4):
        ax.text(gx + (j + 0.5) * cs, gy + 0.30, rf"$n_{{{j + 1}}}$",
                ha="center", va="center", fontsize=13.5,
                color=TEAL if j in G1_IDX else PURPLE, fontweight="bold")
    # row labels: source neuron names, coloured by their group
    for i in range(4):
        ax.text(gx - 0.36, gy - (i + 0.5) * cs, rf"$n_{{{i + 1}}}$",
                ha="center", va="center", fontsize=13.5,
                color=TEAL if i in G1_IDX else PURPLE, fontweight="bold")

    for i in range(4):
        for j in range(4):
            cross = (i in G1_IDX) != (j in G1_IDX)
            ba = i in G2_IDX and j in G1_IDX
            ax.add_patch(Rectangle(
                (gx + j * cs, gy - (i + 1) * cs), cs, cs,
                facecolor=(BLOCK_BG_BA if ba else BLOCK_BG) if cross
                else CELL_BG,
                edgecolor="#3C3C3C", linewidth=0.8, zorder=1))
            ax.text(gx + (j + 0.5) * cs, gy - (i + 0.5) * cs, fmt(W[i][j]),
                    ha="center", va="center", fontsize=13.5, zorder=3,
                    color=INK if cross else FAINT,
                    fontweight="bold" if (i in G1_IDX and j in G2_IDX)
                    else "normal")

    # outlines: gold around pair 1's block (A rows x B cols),
    # thin blue around pair 2's block (the mirror rectangle)
    ax.add_patch(Rectangle(
        (gx + G2_IDX[0] * cs, gy - (G1_IDX[-1] + 1) * cs),
        len(G2_IDX) * cs, len(G1_IDX) * cs,
        facecolor="none", edgecolor=GOLD, linewidth=3.0, zorder=4))
    ax.add_patch(Rectangle(
        (gx + G1_IDX[0] * cs, gy - (G2_IDX[-1] + 1) * cs),
        len(G1_IDX) * cs, len(G2_IDX) * cs,
        facecolor="none", edgecolor=BLUE, linewidth=1.6, zorder=4))

    # brackets: rows on the left, columns on top; role + group together
    for rows, colour in ((G1_IDX, TEAL), (G2_IDX, PURPLE)):
        ax.annotate("", xy=(gx - 0.68, gy - rows[0] * cs - 0.05),
                    xytext=(gx - 0.68, gy - (rows[-1] + 1) * cs + 0.05),
                    arrowprops=dict(arrowstyle="-", color=colour, lw=2.5))
    ax.text(gx - 1.14, gy - cs, "A = G1", ha="center", va="center",
            fontsize=11.5, color=TEAL, fontweight="bold")
    ax.text(gx - 1.14, gy - 3 * cs, "G2", ha="center", va="center",
            fontsize=11.5, color=PURPLE, fontweight="bold")
    for cols, colour in ((G1_IDX, TEAL), (G2_IDX, PURPLE)):
        ax.annotate("", xy=(gx + cols[0] * cs + 0.05, gy + 0.58),
                    xytext=(gx + (cols[-1] + 1) * cs - 0.05, gy + 0.58),
                    arrowprops=dict(arrowstyle="-", color=colour, lw=2.5))
    ax.text(gx + cs, gy + 0.84, "G1", ha="center", va="center",
            fontsize=11.5, color=TEAL, fontweight="bold")
    ax.text(gx + 3 * cs, gy + 0.84, "B = G2", ha="center", va="center",
            fontsize=11.5, color=PURPLE, fontweight="bold")

    # ---------- each pair's block enlarged, in visit order ----------
    bx, bs = 12.05, 1.04
    ax.text(bx + bs, 7.94, "each pair's block, in loop order",
            ha="center", va="center", fontsize=12.5, color=INK)

    def enlarged_block(top, rows, cols, edge, bgc, badge, result, rcolour,
                       run_line):
        for n, (i, j) in enumerate(
                [(i, j) for i in rows for j in cols], start=1):
            li, lj = i - rows[0], j - cols[0]
            x0, y0 = bx + lj * bs, top - (li + 1) * bs
            ax.add_patch(Rectangle((x0, y0), bs, bs, facecolor=bgc,
                                   edgecolor=edge, linewidth=1.6, zorder=1))
            ax.text(x0 + bs / 2, y0 + bs / 2 + 0.12, fmt(W[i][j]),
                    ha="center", va="center", fontsize=15, color=INK,
                    fontweight="bold", zorder=3)
            ax.text(x0 + bs / 2, y0 + bs / 2 - 0.30,
                    rf"$n_{{{i + 1}}} \rightarrow n_{{{j + 1}}}$",
                    ha="center", va="center", fontsize=10.5, color=DIM,
                    zorder=3)
            ax.add_patch(plt.Circle((x0 + 0.19, y0 + bs - 0.19), 0.135,
                                    facecolor=badge, edgecolor="none",
                                    zorder=4))
            ax.text(x0 + 0.19, y0 + bs - 0.19, str(n), ha="center",
                    va="center", fontsize=10, color="#1E1E1E",
                    fontweight="bold", zorder=5)
        ax.text(bx + bs, top - 2 * bs - 0.40, result, ha="center",
                va="center", fontsize=16.5, color=rcolour,
                fontweight="bold")
        ax.text(bx + bs, top - 2 * bs - 0.78, run_line, ha="center",
                va="center", fontsize=10.5, color=DIM)

    enlarged_block(7.00, G1_IDX, G2_IDX, GOLD, BLOCK_BG, GOLD,
                   r"$R_{G1 \rightarrow G2}\;=\;R_{AB}\;=\;+\,0.06$", GOLD,
                   "0 \u2192 \u22120.30 \u2192 +0.10 \u2192 +0.22 \u2192 +0.06")
    enlarged_block(3.76, G2_IDX, G1_IDX, BLUE, BLOCK_BG_BA, BLUE,
                   r"$R_{G2 \rightarrow G1}\;=\;R_{AB}\;=\;+\,0.50$", LIGHT,
                   "0 \u2192 +0.52 \u2192 +0.33 \u2192 +0.09 \u2192 +0.50")

    # ---------- under the matrix: one formula, two bindings ----------
    ax.text(gx, 2.94,
            "the formula is one; the bindings are two \u2014\n"
            "each pair fills A and B with its own groups.",
            ha="left", va="top", fontsize=11.5, color=DIM, linespacing=1.55)

    # ---------- footer ----------
    ax.text(8, 0.36,
            "Equation (9) runs the same pairing over each mode's "
            "layer grid instead of over $W$.",
            ha="center", va="center", fontsize=12.5, color=DIM)

    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
