#!/usr/bin/env python3
"""
Teaching figure: how a column times a row makes a grid — the outer
product u v^T, using toy mode 1 (sigma = 2.0,
u = (+0.5, -0.2, +0.9, +0.1), v = (+0.3, +0.4, -0.6, +0.8)).

Left grid: u v^T — every entry of the column times every entry of the
row; one cell (n3, n4) is spotlighted with dashed guides from its two
parents. Right grid: the same grid scaled by sigma — the mode's layer,
matching make_mode_block_eq9.py. No addition happens anywhere in this
figure; adding starts only when a block of the layer is summed.

Output: outer-product.png in an output/ folder beside this script
(created if it does not exist).
Run:    python make_outer_product.py
Needs:  matplotlib
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "outer-product.png"

BG = "#1E1E1E"
INK = "#D4D4D4"
DIM = "#8A8A8A"
FAINT = "#5A5A5A"
GOLD = "#E8A33D"
TEAL = "#4EC9B0"
PURPLE = "#C586C0"
CELL_BG = "#252526"
GOLD_BG = "#33270F"
TEAL_BG = "#12312B"
PURPLE_BG = "#2E1A2E"

SIGMA = 2.0
U = [0.5, -0.2, 0.9, 0.1]
V = [0.3, 0.4, -0.6, 0.8]
SPOT = (2, 3)  # (row, col) of the spotlight cell: n3 x n4


def fmt(v):
    return f"{v:+.2f}".replace("-", "\u2212")


def draw_grid(ax, gx, gy, cs, values, block_outline=False):
    for i in range(4):
        for j in range(4):
            in_block = i in (0, 1) and j in (2, 3)
            ax.add_patch(Rectangle(
                (gx + j * cs, gy - (i + 1) * cs), cs, cs,
                facecolor=GOLD_BG if (block_outline and in_block) else CELL_BG,
                edgecolor="#3C3C3C", linewidth=0.8, zorder=1))
            ax.text(gx + (j + 0.5) * cs, gy - (i + 0.5) * cs, fmt(values[i][j]),
                    ha="center", va="center", fontsize=12, zorder=3,
                    color=INK, fontweight="bold")
    if block_outline:
        ax.add_patch(Rectangle((gx + 2 * cs, gy - 2 * cs), 2 * cs, 2 * cs,
                               facecolor="none", edgecolor=GOLD,
                               linewidth=2.2, zorder=4))


def main():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8, 8.66, "Column \u00d7 row = grid \u2014 the outer product "
            r"$u_1 v_1^{T}$ (toy mode 1)",
            ha="center", va="center", fontsize=20, color=INK)

    cs = 0.80
    gy = 6.80  # grid top

    # ---------- left: u, v and their product grid ----------
    gx = 3.55
    ax.text(gx + 2 * cs, gy + 1.24, r"$u_1 v_1^{T}$ — every $u$ times every $v$",
            ha="center", va="center", fontsize=14.5, color=INK)

    # v row (targets) above the grid
    for j in range(4):
        spot = j == SPOT[1]
        ax.add_patch(Rectangle((gx + j * cs, gy + 0.16), cs, cs,
                               facecolor=PURPLE_BG, edgecolor=PURPLE,
                               linewidth=2.6 if spot else 1.0, zorder=2))
        ax.text(gx + (j + 0.5) * cs, gy + 0.16 + cs / 2, fmt(V[j]),
                ha="center", va="center", fontsize=12, color=INK, zorder=3,
                fontweight="bold")
    ax.text(gx + 4 * cs + 0.22, gy + 0.53,
            "$v_1$ \u2014 the row (targets)",
            fontsize=12.5, color=PURPLE, va="center")

    # u column (sources) left of the grid
    for i in range(4):
        spot = i == SPOT[0]
        ax.add_patch(Rectangle((gx - 0.92, gy - (i + 1) * cs), cs, cs,
                               facecolor=TEAL_BG, edgecolor=TEAL,
                               linewidth=2.6 if spot else 1.0, zorder=2))
        ax.text(gx - 0.92 + cs / 2, gy - (i + 0.5) * cs, fmt(U[i]),
                ha="center", va="center", fontsize=12, color=INK, zorder=3,
                fontweight="bold")
    ax.text(gx - 0.55, gy - 4 * cs - 0.32, "$u_1$ \u2014 the column (sources)",
            ha="center", va="center", fontsize=12.5, color=TEAL)
    ax.text(gx - 0.55, gy + 0.53, "\u00d7", ha="center", va="center",
            fontsize=20, color=INK)

    # dashed guides from the spotlight parents to the spotlight cell
    si, sj = SPOT
    cell_cx = gx + (sj + 0.5) * cs
    cell_cy = gy - (si + 0.5) * cs
    ax.plot([gx - 0.18, cell_cx], [cell_cy, cell_cy], color=DIM, lw=1.4,
            linestyle=(0, (4, 3)), zorder=2)
    ax.plot([cell_cx, cell_cx], [gy + 0.16, cell_cy], color=DIM, lw=1.4,
            linestyle=(0, (4, 3)), zorder=2)

    raw = [[U[i] * V[j] for j in range(4)] for i in range(4)]
    draw_grid(ax, gx, gy, cs, raw)
    # spotlight cell outline
    ax.add_patch(Rectangle((gx + sj * cs, gy - (si + 1) * cs), cs, cs,
                           facecolor="none", edgecolor=INK, linewidth=2.6,
                           zorder=5))

    # ---------- arrow: times sigma ----------
    ax.annotate("", xy=(9.05, gy - 2 * cs), xytext=(7.05, gy - 2 * cs),
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=2.6,
                                mutation_scale=26))
    ax.text(8.05, gy - 2 * cs + 0.42, r"$\times\ \sigma_1 = 2.0$",
            ha="center", va="center", fontsize=15, color=GOLD)

    # ---------- right: the layer ----------
    gx2 = 9.45
    ax.text(gx2 + 2 * cs, gy + 1.24,
            r"the layer $\sigma_1 u_1 v_1^{T}$ — every cell doubled",
            ha="center", va="center", fontsize=14.5, color=INK)
    lay = [[SIGMA * raw[i][j] for j in range(4)] for i in range(4)]
    draw_grid(ax, gx2, gy, cs, lay, block_outline=True)
    ax.text(gx2 + 2 * cs, gy - 4 * cs - 0.34,
            "gold outline: the $A \\times B$ block that\n"
            "equation (9) goes on to sum",
            ha="center", va="top", fontsize=11.5, color=DIM, linespacing=1.5)

    # ---------- bottom: the spotlight worked out + the rule ----------
    ax.text(1.15, 2.52,
            "the spotlight cell, $n_3 \\rightarrow n_4$:  take $u_3 = +0.90$ "
            "from the column and $v_4 = +0.80$ from the row \u2014\n"
            "multiply:  $+0.90 \\times +0.80 = +0.72$  (then $\\times\\ \\sigma_1$ "
            "in the layer: $+1.44$)",
            fontsize=13.5, color=INK, va="top", linespacing=1.6)
    ax.text(1.15, 1.42,
            "Every cell is born the same way: its row's $u$ \u00d7 its column's "
            "$v$. 4 + 4 numbers make 4 \u00d7 4 = 16 cells.\n"
            "No adding happens here \u2014 addition only starts when a block of "
            "the layer is summed.",
            fontsize=13.5, color=DIM, va="top", linespacing=1.6)

    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
