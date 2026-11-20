#!/usr/bin/env python3
"""
Teaching figure: equation (9), the mode block sum, on the toy example.

    M_AB = sum_m omega_m * (block sum of mode m's layer sigma_m u_m v_m^T)
    omega_m = sigma_m^2 / sum_j sigma_j^2

Same toy neurons as the nested-loop figure (n1, n2 = group A; n3, n4 =
group B), with k = 2 invented toy modes chosen for clean arithmetic
(they are NOT the SVD of the toy W). Shows: one mode's kit (a column of
U, the sigma cell of Sigma, a row of V^T) multiplying out into a layer;
the A x B block of each layer; omega read off the Sigma diagonal,
squared and shared out; the weighted blend landing on M_AB.

Output: mode-block-eq9.png beside this script.
Run:    python make_mode_block_eq9.py
Needs:  matplotlib
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent / "mode-block-eq9.png"

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

# toy modes: (sigma, u column, v row)
MODES = [
    (2.0, [0.5, -0.2, 0.9, 0.1], [0.3, 0.4, -0.6, 0.8]),
    (1.0, [0.4, 0.3, -0.5, 0.6], [0.7, -0.1, 0.2, 0.9]),
]
A_ROWS = [0, 1]
B_COLS = [2, 3]


def fmt(v):
    return f"{v:+.2f}".replace("-", "\u2212")


def fmt3(v):
    return f"{v:+.3f}".replace("-", "\u2212")


def layer(sigma, u, v):
    return [[sigma * u[i] * v[j] for j in range(4)] for i in range(4)]


def mode_panel(ax, gy, m, sigma, u, v, omega, block, contrib):
    """Draw one mode's kit + layer at grid-top gy."""
    cs = 0.50
    gx = 3.10  # layer grid left
    # heading
    ax.text(0.50, gy + 0.34, f"Mode {m}", fontsize=15.5, color=INK,
            fontweight="bold", va="center")
    ax.text(0.50, gy - 0.14, rf"$\sigma_{{{m}}} = {sigma:.1f}$",
            fontsize=14, color=GOLD, va="center")
    # v row (targets) above the grid
    for j in range(4):
        ax.add_patch(Rectangle((gx + j * cs, gy + 0.08), cs, cs,
                               facecolor=PURPLE_BG, edgecolor=PURPLE,
                               linewidth=0.9, zorder=1))
        ax.text(gx + (j + 0.5) * cs, gy + 0.08 + cs / 2, fmt(v[j]),
                ha="center", va="center", fontsize=9.5, color=INK, zorder=2)
    ax.text(gx + 4 * cs + 0.18, gy + 0.33,
            rf"$v_{{{m}}}$ — row of $V^T$ (targets)",
            fontsize=11, color=PURPLE, va="center")
    # u column (sources) left of the grid
    for i in range(4):
        ax.add_patch(Rectangle((gx - 0.62, gy - (i + 1) * cs), cs, cs,
                               facecolor=TEAL_BG, edgecolor=TEAL,
                               linewidth=0.9, zorder=1))
        ax.text(gx - 0.62 + cs / 2, gy - (i + 0.5) * cs, fmt(u[i]),
                ha="center", va="center", fontsize=9.5, color=INK, zorder=2)
    ax.text(gx - 0.37, gy - 2.0 - 0.32, rf"$u_{{{m}}}$ — column of $U$ (sources)",
            fontsize=11, color=TEAL, va="center", ha="center")
    # layer grid
    lay = layer(sigma, u, v)
    for i in range(4):
        for j in range(4):
            in_block = i in A_ROWS and j in B_COLS
            ax.add_patch(Rectangle(
                (gx + j * cs, gy - (i + 1) * cs), cs, cs,
                facecolor=GOLD_BG if in_block else CELL_BG,
                edgecolor="#3C3C3C", linewidth=0.7, zorder=1))
            ax.text(gx + (j + 0.5) * cs, gy - (i + 0.5) * cs, fmt(lay[i][j]),
                    ha="center", va="center", fontsize=8.5, zorder=2,
                    color=INK if in_block else FAINT,
                    fontweight="bold" if in_block else "normal")
    ax.add_patch(Rectangle(
        (gx + B_COLS[0] * cs, gy - (A_ROWS[-1] + 1) * cs), 2 * cs, 2 * cs,
        facecolor="none", edgecolor=GOLD, linewidth=2.4, zorder=3))
    # annotations right of the grid
    terms = " + ".join(fmt(lay[i][j]).replace("+", " ") if False else fmt(lay[i][j])
                       for i in A_ROWS for j in B_COLS)
    ax.text(5.55, gy - 0.28,
            rf"layer $= \sigma_{{{m}}}\, u_{{{m}}} v_{{{m}}}^{{T}}$",
            fontsize=12.5, color=INK, va="center")
    ax.text(5.55, gy - 0.86,
            f"gold block sums to {fmt(block)}",
            fontsize=12.5, color=INK, va="center")
    ax.text(5.55, gy - 1.44,
            rf"$\omega_{{{m}}} = {omega:.2f}$  →  contributes {fmt3(contrib)}",
            fontsize=12.5, color=GOLD, va="center")


def main():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8, 8.68,
            r"$M_{AB}\;=\;\sum_{m}\omega_m \cdot "
            r"\left(\mathrm{block~sum~of~} \sigma_m u_m v_m^{T}\right)$"
            "   \u2014   equation (9) on the toy",
            ha="center", va="center", fontsize=18.5, color=INK)

    # mode panels (block sums: mode 1 -> +0.12, mode 2 -> +0.77)
    mode_panel(ax, 7.42, 1, *MODES[0], omega=0.80, block=+0.12, contrib=+0.096)
    mode_panel(ax, 4.28, 2, *MODES[1], omega=0.20, block=+0.77, contrib=+0.154)

    # ---------- right: where omega comes from ----------
    rx = 10.05
    ax.text(rx, 8.06, "where $\\omega$ comes from \u2014 the $\\Sigma$ diagonal",
            fontsize=13.5, color=INK, va="center", fontweight="bold")
    # mini Sigma (toy, 2x2 diagonal)
    sx, sy, sc = rx + 0.15, 7.62, 0.52
    sig = [2.0, 1.0]
    for i in range(2):
        for j in range(2):
            diag = i == j
            ax.add_patch(Rectangle((sx + j * sc, sy - (i + 1) * sc), sc, sc,
                                   facecolor=GOLD_BG if diag else CELL_BG,
                                   edgecolor=GOLD if diag else "#3C3C3C",
                                   linewidth=1.2 if diag else 0.7, zorder=1))
            ax.text(sx + (j + 0.5) * sc, sy - (i + 0.5) * sc,
                    f"{sig[i]:.1f}" if diag else "0",
                    ha="center", va="center", fontsize=12, zorder=2,
                    color=INK if diag else FAINT,
                    fontweight="bold" if diag else "normal")
    ax.text(sx + 2 * sc + 0.22, sy - sc, "$\\Sigma$ (toy) \u2014 the diagonal\n"
            "holds the mode strengths",
            fontsize=11.5, color=DIM, va="center", linespacing=1.45)
    ax.text(rx + 0.15, 6.28,
            "square them:  $\\sigma_1^2 = 4$   $\\sigma_2^2 = 1$\n"
            "retained total:  $4 + 1 = 5$\n"
            "share them out:  $\\omega_1 = 4/5 = 0.80$    "
            "$\\omega_2 = 1/5 = 0.20$",
            fontsize=12.5, color=INK, va="top", linespacing=1.65)
    ax.text(rx + 0.15, 4.86,
            "$\\omega$ is not a separate measurement \u2014 it is\n"
            "the $\\Sigma$ diagonal, squared and shared out.\n"
            "$\\sigma_m^2$ is the mode's energy (its eigenvalue\n"
            "share of $W$); $\\omega_m$ is that share within\n"
            "the retained modes.",
            fontsize=12, color=DIM, va="top", linespacing=1.55)

    # ---------- right bottom: the blend ----------
    ax.add_patch(Rectangle((rx - 0.28, 0.86), 5.95, 2.30,
                           facecolor="#252526", edgecolor=GOLD,
                           linewidth=1.2, zorder=1))
    ax.text(rx + 0.02, 2.88, "the blend:",
            fontsize=13.5, color=INK, va="center", fontweight="bold")
    ax.text(rx + 0.02, 2.34,
            "$M_{AB} = 0.80 \\times (+0.12) \\; + \\; 0.20 \\times (+0.77)$",
            fontsize=13.5, color=INK, va="center")
    ax.text(rx + 0.64, 1.80,
            "$= \\; +0.096 \\; + \\; +0.154$",
            fontsize=13.5, color=INK, va="center")
    ax.text(rx + 2.62, 1.22, r"$M_{AB}\;=\;+\,0.25$", fontsize=19,
            color=GOLD, va="center", fontweight="bold")

    # ---------- footer ----------
    ax.text(8, 0.36,
            "Toy modes invented for clean arithmetic (not the SVD of the toy "
            "$W$); the toy keeps $k = 2$ modes, your run keeps 9 \u2014 same recipe. "
            "In your run $\\sigma_1 = 3.85$, so $\\omega_1 = 14.85 / 36.55 \\approx 0.41$.",
            ha="center", va="center", fontsize=11.5, color=DIM)

    fig.savefig(OUT, facecolor=BG)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
