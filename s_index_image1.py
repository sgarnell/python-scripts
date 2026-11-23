#!/usr/bin/env python3
"""S-index slide image 1 (draft): S = E x G, the definition.

Journal typography (numbered definitions, Proposition
box) on Saul's dark slide ground (VS Code Dark+ palette, as in the
AI-class slides and make_explainer_images.py). Numbers verified against
resonator-pairs.87ef7c02.post.csv (62-neuron hDelta run, config 87ef7c02):
  FB5U <-> hDeltaH7: w = -0.360 / +0.415, post_z = 0.70 / 0.97,
  G = sqrt(0.360*0.415) = 0.387, E_post = sqrt(0.70*0.97) = 0.824,
  S_post = 0.387*0.824 = 0.319.
Domain counts: 127 reciprocal pairs of 590 directed pairs; 3 of the 127
have a zero |w| leg (G = 0).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, "s_index_image1.png")

INK = "#E6E6E6"
DIM = "#9DA3AB"
BLUE = "#569CD6"
TEAL = "#4EC9B0"
YELLOW = "#DCDCAA"
GOLD = "#E8A33D"
PURPLE = "#C586C0"
RED = "#D64541"
GROUND = "#1E1E1E"
PANEL = "#14181D"

fig = plt.figure(figsize=(16, 9), dpi=150)
fig.patch.set_facecolor(GROUND)

# ---- title block -------------------------------------------------------
fig.text(0.5, 0.955, "The resonator score  $S$ — Definition",
         color=INK, fontsize=27, weight="bold", ha="center", va="center")
fig.text(0.5, 0.905,
         "$S_{\\mathrm{post}}$, the final version  ·  62-neuron hDelta run (config 87ef7c02)  ·  "
         "image 1 of 3: the definition  ·  image 2: $E$  ·  image 3: $G$",
         color=DIM, fontsize=13, ha="center", va="center")
fig.text(0.5, 0.868, "Every symbol defined, in dependency order",
         color=DIM, fontsize=12, style="italic", ha="center", va="center")

# ---- left: 2-cycle diagram -------------------------------------------
ax = fig.add_axes([0.03, 0.52, 0.36, 0.30])
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.set_facecolor(PANEL)
for (x, y, lab) in [(2.2, 3.0, "$a$"), (7.8, 3.0, "$b$")]:
    ax.add_patch(Circle((x, y), 1.05, fc="#26313D", ec=BLUE, lw=2.2, zorder=3))
    ax.text(x, y, lab, color=INK, fontsize=26, ha="center", va="center", zorder=4)
top = FancyArrowPatch((3.2, 3.9), (6.8, 3.9), connectionstyle="arc3,rad=0.45",
                      arrowstyle="-|>", mutation_scale=22, lw=2.4, color=TEAL, zorder=2)
bot = FancyArrowPatch((6.8, 2.1), (3.2, 2.1), connectionstyle="arc3,rad=0.45",
                      arrowstyle="-|>", mutation_scale=22, lw=2.4, color=GOLD, zorder=2)
ax.add_patch(top); ax.add_patch(bot)
ax.text(5.0, 5.35, "$w_{ab}$", color=TEAL, fontsize=20, ha="center", va="center")
ax.text(5.0, 0.65, "$w_{ba}$", color=GOLD, fontsize=20, ha="center", va="center")
ax.text(5.0, 4.55, "$\\mathrm{post\\_z}(a\\!\\to\\! b)$", color=DIM, fontsize=11, ha="center")
ax.text(5.0, 1.45, "$\\mathrm{post\\_z}(b\\!\\to\\! a)$", color=DIM, fontsize=11, ha="center")
fig.text(0.21, 0.505, "Figure 1. A reciprocal pair (2-cycle). Each leg carries one $w$ and one $\\mathrm{post\\_z}$.",
         color=DIM, fontsize=11.5, ha="center", va="center")

# ---- left: worked example ---------------------------------------------
fig.text(0.03, 0.46, "Check it — the top pair, FB5U $\\leftrightarrow$ hDeltaH7",
         color=YELLOW, fontsize=14.5, weight="bold", ha="left", va="center")
ex = [
    "$w = -0.360,\\ +0.415$  $\\;\\Rightarrow\\;$  $G = \\sqrt{0.360 \\cdot 0.415} = 0.387$",
    "$\\mathrm{post\\_z} = 0.70,\\ 0.97$  $\\;\\Rightarrow\\;$  $E_{\\mathrm{post}} = \\sqrt{0.70 \\cdot 0.97} = 0.824$",
    "$S_{\\mathrm{post}} = 0.387 \\times 0.824 = 0.319$",
]
for i, line in enumerate(ex):
    fig.text(0.045, 0.405 - i * 0.045, line, color=INK, fontsize=14.5, ha="left", va="center")
fig.text(0.045, 0.255,
         "All three numbers are read straight off the pair table\n"
         "(resonator-pairs.87ef7c02.post.csv, rank 1 of 127).",
         color=DIM, fontsize=11.5, ha="left", va="center", linespacing=1.5)
fig.text(0.045, 0.155,
         "Sign of $w$ is pre/post-dominance,\nnot excitation / inhibition.",
         color=PURPLE, fontsize=11.5, ha="left", va="center", linespacing=1.5)

# ---- right: definition stack ------------------------------------------
x0 = 0.43
fig.text(x0, 0.815, "Definition 1.", color=TEAL, fontsize=15, weight="bold", ha="left", va="center")
defs = [
    (r"(1)  $\;w_{ab} = s \cdot \tanh\left(\alpha \cdot \log\frac{\mathrm{post\_z}}{\mathrm{pre\_z}+\varepsilon}\right)$",
     "the unified weight of $a \\to b$ (Phase 02); $s=(|\\mathrm{pre\\_z}|+|\\mathrm{post\\_z}|)/2$, $\\alpha=1$, $\\varepsilon=0.1$; $|w|<1$ by the $\\tanh$."),
    (r"(2)  $\;G_{ab} = \sqrt{|w_{ab}| \cdot |w_{ba}|}$",
     "loop strength — the geometric mean of the two $|w|$ legs."),
    (r"(3)  $\;E_{ab} = \sqrt{\mathrm{post\_z}(a\!\to\! b) \cdot \mathrm{post\_z}(b\!\to\! a)}$",
     "mutual receiver prominence — the geometric mean of the two $\\mathrm{post\\_z}$ legs; pair-local."),
    (r"(4)  $\;S_{ab} = G_{ab} \times E_{ab}$",
     "the resonator score. This is $S_{\\mathrm{post}}$: the final version."),
]
y = 0.755
for eq, gloss in defs:
    fig.text(x0, y, eq, color=INK, fontsize=16.5, ha="left", va="center")
    fig.text(x0 + 0.015, y - 0.042, gloss, color=DIM, fontsize=12, ha="left", va="center")
    y -= 0.115
# anchor equation, large
fig.text(x0, 0.315, r"$\mathbf{S_{ab} = G_{ab} \times E_{ab}}$",
         color=YELLOW, fontsize=30, weight="bold", ha="left", va="center")
fig.text(x0, 0.265, "One score per reciprocal pair, from the same two numbers every time.",
         color=DIM, fontsize=12, ha="left", va="center")

# ---- proposition box ----------------------------------------------------
box = FancyBboxPatch((0.43, 0.035), 0.54, 0.185, boxstyle="round,pad=0.008,rounding_size=0.012",
                     fc=PANEL, ec=TEAL, lw=1.4, transform=fig.transFigure, zorder=1)
fig.patches.append(box)
fig.text(0.445, 0.195, "Proposition 1.  What $S$ promises, the definition delivers.",
         color=TEAL, fontsize=13.5, weight="bold", ha="left", va="center")
props = [
    "Symmetric:  $S_{ab} = S_{ba}$.",
    "Zero iff a leg is zero:  $S_{ab}=0 \\Leftrightarrow |w_{ab}|=0$ or $|w_{ba}|=0$ — a missing or zero leg is not a loop.",
    "Monotone:  $S$ grows with each $|w|$ leg and each $\\mathrm{post\\_z}$ leg.",
    "Range:  $0 \\leq S_{ab} < 1$  ($|w|<1$; $\\mathrm{post\\_z} \\leq 1$ in the export).",
]
for i, line in enumerate(props):
    fig.text(0.445, 0.16 - i * 0.032, line, color=INK, fontsize=12, ha="left", va="center")

# ---- footnotes ------------------------------------------------------------
fig.text(0.03, 0.095,
         "Domain: reciprocal pairs only — 127 of 590 directed pairs in this run.\n"
         "A non-reciprocal pair scores $S = 0$ by construction: there is no return leg.",
         color=DIM, fontsize=11.5, ha="left", va="center", linespacing=1.5)
fig.text(0.03, 0.042,
         "Pedigree: $G$ is the Onnela et al. (2005) intensity of a weighted 2-cycle.\n"
         "$E_{\\mathrm{post}}$ replaces the legacy $E_I$ (input shares $|w|/I$, set-dependent) — image 2.",
         color=DIM, fontsize=10.5, ha="left", va="center", linespacing=1.5)

plt.savefig(OUT, facecolor=GROUND)
print("wrote", OUT)
