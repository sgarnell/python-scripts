#!/usr/bin/env python3
"""Pathway (gold edge) slide for Sharon: how the gold lines are calculated.

Companion to make_resonator_slides.py -- same journal structure (numbered
Definition, numbered equations continuing the set, Remark box) typeset in
Computer Modern math (matplotlib mathtext, fontset 'cm') with Liberation
Serif text on Saul's dark slide ground (#1E1E1E, VS Code Dark+ accents).
The pathway weight P is gold #E8A33D; w keeps its light blue #9CDCFE.

The maths, exactly as implemented in functional_motifs.py (04D pathway):
  R_AB  = block sum of the raw weights w over all directed pairs A -> B
  M_AB  = sum over retained modes m of omega_m * (block sum of the mode's
          rank-1 layer sigma_m u_m v_m^T), with omega_m = sigma_m^2 /
          sum_j sigma_j^2 renormalised over the retained modes (sum = 1)
  P_AB  = 0.7 * R_AB + 0.3 * M_AB        (rule 'hybrid', alpha = 0.3)
  drawn iff A != B, |P_AB| >= 0.10 * max |P_CD|, top 5 outgoing per group.

Numbers (62-neuron hDelta run, config 87ef7c02, k = 9), verified against
the pipeline's stored pathway values:
  G01 -> G09: R = -15.18 (42 wired pairs), M = -6.01,
              P = 0.7*(-15.18) + 0.3*(-6.01) = -12.43 (largest |P|)
  G11 -> G06: R = +2.01 (12 wired pairs), M = +0.10, P = +1.44
              (the only positive of the 11 drawn edges)
  12 groups -> 132 ordered pairs A != B; 11 edges pass the cutoff 1.24.
  Top-5 cap never binds in this run (busiest source, G10, has 3 edges).

Usage: python3 make_pathway_slide.py
Output: pathway-slide.png in an output/ folder beside this script
(created if it does not exist).
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BG = "#1E1E1E"
PANEL = "#26262B"
INK = "#EDEDED"
GREY = "#A9A9A9"
BLUE = "#569CD6"
LBLUE = "#9CDCFE"  # w
GOLD = "#E8A33D"   # P, the pathway weight

plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Liberation Serif", "DejaVu Serif"]

FIG_W, FIG_H, DPI = 13.333, 7.5, 200
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "pathway-slide.png")


def new_slide():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.09",
        linewidth=0.9, edgecolor="#3F3F46", facecolor=PANEL, zorder=1))


def main():
    fig, ax = new_slide()

    # ---- title, with a sample gold dashed arrow -------------------------
    ax.text(0.55, 7.06, "The pathway weight — the gold edges",
            fontsize=19, color=INK, fontweight="bold", va="center")
    ax.add_patch(FancyArrowPatch(
        (10.05, 7.06), (12.72, 7.06), arrowstyle="-|>", mutation_scale=26,
        linewidth=3.2, linestyle=(0, (7, 4)), color=GOLD, zorder=3))
    ax.plot([0.55, 12.78], [6.74, 6.74], color="#3F3F46", lw=1.0)

    # ---- Definition 2 ----------------------------------------------------
    ax.text(0.55, 6.44, "Definition 2.", fontsize=14.5, color=BLUE,
            fontweight="bold", va="center")
    ax.text(2.42, 6.44,
            "The groups $G_1, \\dots, G_{12}$ partition the 62 neurons. For "
            "distinct groups $A$, $B$, two sums run over the",
            fontsize=12.3, color=INK, va="center")
    ax.text(0.55, 6.13,
            "same directed pairs $a \\in A$, $b \\in B$:",
            fontsize=12.3, color=INK, va="center")

    # (8) raw block sum
    ax.text(2.05, 5.58,
            r"$R_{AB} \;=\; \sum_{a \in A}\; \sum_{b \in B} w_{ab}$",
            fontsize=17.5, color=INK, va="center")
    ax.text(12.28, 5.58, "(8)", fontsize=13, color=GREY, va="center")
    ax.text(2.05, 5.22,
            "the raw block sum — the pair weights themselves, added with "
            "their signs.",
            fontsize=11.5, color=GREY, va="center")

    # (9) mode block sum
    ax.text(2.05, 4.76,
            r"$M_{AB} \;=\; \sum_{m=1}^{9} \omega_m \sum_{a \in A}\;"
            r"\sum_{b \in B} \sigma_m\, u_{am} v_{bm}$",
            fontsize=17, color=INK, va="center")
    ax.text(8.62, 4.76,
            r"$\omega_m = \sigma_m^2 \,/\, \sum_{j=1}^{9} \sigma_j^2$",
            fontsize=14.5, color=INK, va="center")
    ax.text(12.28, 4.76, "(9)", fontsize=13, color=GREY, va="center")
    ax.text(2.05, 4.27,
            "the mode block sum — for mode $m$, take the $A$ entries of "
            "$U$'s column $m$ and the $B$ entries of $V^{T}$'s row "
            "$m$;",
            fontsize=11.5, color=GREY, va="center")
    ax.text(2.05, 3.98,
            "multiply every $A$ entry by every $B$ entry (the grid "
            "$\\sigma_m u_m v_m^{T}$), add them all, then weight by "
            "$\\omega_m$ ($\\sum_m \\omega_m = 1$).",
            fontsize=11.5, color=GREY, va="center")

    # (10) the blend
    ax.text(2.05, 3.52,
            r"$\mathbf{P}_{AB} \;=\; 0.7\, R_{AB} \;+\; 0.3\, M_{AB}$",
            fontsize=20, color=GOLD, va="center")
    ax.text(12.28, 3.52, "(10)", fontsize=13, color=GREY, va="center")
    ax.text(2.05, 3.16,
            "the pathway weight. The 0.3 belongs to this layer alone — it "
            "is not the $\\alpha$ of the $w$ formula (Phase 02).",
            fontsize=11.5, color=GREY, va="center")

    # ---- drawing rule -----------------------------------------------------
    ax.text(0.55, 2.78, "Drawing rule.", fontsize=14.5, color=BLUE,
            fontweight="bold", va="center")
    ax.text(2.62, 2.78,
            "Gold, dashed, $A \\to B$ exactly when",
            fontsize=12.3, color=INK, va="center")
    ax.text(6.05, 2.78,
            r"$|P_{AB}| \;\geq\; 0.10 \times \max_{C \neq D} |P_{CD}|$",
            fontsize=13.5, color=INK, va="center")
    ax.text(0.55, 2.44,
            "keeping at most the five largest $|P|$ per source group. Of "
            "the 132 ordered group pairs, 11 are drawn — 10 negative, 1 "
            "positive.",
            fontsize=12.3, color=INK, va="center")

    # ---- check it ----------------------------------------------------------
    box(ax, 0.55, 1.24, 12.23, 1.00)
    ax.text(0.80, 2.04, "Check it.", fontsize=12.5, color=INK,
            fontweight="bold", va="center", zorder=3)
    ax.text(2.28, 2.04,
            "$G01 \\to G09$:  $R = -15.18$ over 42 wired pairs, $M = "
            "-6.01$, so $P = 0.7(-15.18) + 0.3(-6.01) = -12.43$ — the "
            "largest $|P|$ of any pair,",
            fontsize=11.8, color=INK, va="center", zorder=3)
    ax.text(0.80, 1.71,
            "hence the cutoff $0.10 \\times 12.43 = 1.24$. The one positive "
            "edge, $G11 \\to G06$: $P = +1.44$, from $R = +2.01$ (12 pairs) "
            "and $M = +0.10$. The five-per-source cap never",
            fontsize=11.8, color=INK, va="center", zorder=3)
    ax.text(0.80, 1.40,
            "binds in this run — the busiest source, G10, has 3 edges — "
            "so the cutoff does all of the filtering.",
            fontsize=11.8, color=INK, va="center", zorder=3)

    # ---- remark -------------------------------------------------------------
    ax.text(0.55, 1.06, "Remark.", fontsize=12.5, color=BLUE,
            fontweight="bold", va="center")
    ax.text(2.02, 1.06,
            "A block sum is signed, so opposed pair traffic cancels inside "
            "a block: a heavily wired pair of groups can draw no gold edge "
            "— no gold edge does",
            fontsize=11.5, color=GREY, va="center")
    ax.text(0.55, 0.76,
            "not mean no interaction. Pairs inside one group never receive "
            "a gold edge, so the resonator loops of Definition 1 — mostly "
            "inside G06 — are invisible to",
            fontsize=11.5, color=GREY, va="center")
    ax.text(0.55, 0.46,
            "this layer. The sign of $P$ is the block's net pre-dominance "
            "(negative) or post-dominance (positive) — not excitation or "
            "inhibition.",
            fontsize=11.5, color=GREY, va="center")

    ax.text(0.55, 0.14,
            "62-neuron hDelta run, configuration 87ef7c02; family-aware "
            "grouping; k = 9 modes. Code: pathway rule \u201chybrid\u201d, "
            "edge threshold 0.10, top 5 per source.",
            fontsize=9.5, color=GREY, va="center")

    fig.savefig(OUT, dpi=DPI, facecolor=BG)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
