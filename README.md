# python-scripts

Personal Python utilities for local development, in three families:

1. **A spelling/grammar bridge** that lets the Obsidian "LanguageTool
   Integration" plugin proofread with a local LLM served by LM Studio
   (the server machine is nicknamed *Barda*).
2. **Journal-style maths slides** for the *eigen-decomposition* project —
   an analysis pipeline for directed functional connectivity in
   *Drosophila* central-complex circuits, built from Hemibrain 1.2 data
   exported through FlyBrainLab. The slides define and defend the two
   scores the pipeline computes: the **resonator score** $S$ over
   reciprocal neuron pairs, and the **pathway weight** $P$ behind the
   gold group-to-group edges of the combined graph. Four small
   **teaching figures** accompany the pathway slide, unpacking its
   equations (8)–(9) step by step on a 4-neuron toy example.
   A further three-slide set works equations (8)–(10) end to end on
   the reference run's real numbers.
3. **Experiment-design slides** for the anesthetic programme run with
   Bruno van Swinderen's lab — one slide overviewing the four-leg
   experiment, and a companion slide stating what would count as the
   cognitive link.

Plus one general utility: a read-only checker to run before moving a
JetBrains project folder.

Branch convention: `main` is the owner's; contributions from the Muse
agent land on the **`muse`** branch first and are merged by hand.

## Contents

| Script | What it does | Needs |
|---|---|---|
| `lt_bridge.py` | LanguageTool-API ⇄ LM Studio bridge server for Obsidian proofreading | Python 3, standard library only |
| `make_resonator_slides.py` | The three resonator-score slides (definition of $S$; the $E$ factor; the $G$ factor) | matplotlib |
| `s_index_image1.py` | Alternative draft rendering of resonator slide 1, with a worked example | matplotlib |
| `make_pathway_slide.py` | Slide defining the pathway weight $P$ (the gold edges) | matplotlib |
| `make_pathway_slide_gloss-revision.py` | Variant of the pathway slide with an expanded gloss under equation (9) | matplotlib |
| `make_nested_loop_eq8.py` | Teaching figure: equation (8) in two stages — group pairs first, then A/B as dummy variables | matplotlib |
| `make_two_directions.py` | Teaching figure: $R_{AB}$ and $R_{BA}$ are separate rectangles of the same $W$ | matplotlib |
| `make_mode_block_eq9.py` | Teaching figure: equation (9) on a toy — mode layers, the $\omega$ weights, the blend $M$ | matplotlib |
| `make_outer_product.py` | Teaching figure: how a column × a row builds one mode's layer (the outer product) | matplotlib |
| `make_eq8_9_slides.py` | Three slides working equations (8)–(10) on the reference run's real numbers (G01 → G09) | numpy, matplotlib + run data |
| `make_experiment_overview.py` | Overview slide for the Bruno anesthetic experiment (hypothesis, circuit, four legs) | matplotlib |
| `make_what_counts.py` | Companion slide: what would count as the cognitive link (the three criteria) | matplotlib |
| `check_project_move.py` | Read-only pre-move checker for JetBrains project folders | Python 3, standard library only |

Every figure script writes its PNG into an **`output/` folder beside
the script itself** (the folder is created automatically if it does not
exist) — no machine-specific paths — so they run unchanged on any
machine. The one exception: the two Bruno experiment slides write into
an **`out_qbi/`** folder instead, to keep their files apart from the
eigen-decomposition figures.

## Setup

```bash
conda create -n python-scripts python=3.11 pip
conda activate python-scripts
pip install matplotlib
```

(One hard-won detail: on conda-forge, the `python` package does **not**
bundle `pip` — name `pip` explicitly when creating the environment, as
above, or `pip` will not exist inside it. `lt_bridge.py` needs nothing
beyond the standard library.)

---

## The mathematics on the slides

### 1. From z-scores to a signed weight $w$

Each directed connection $a \to b$ in a FlyBrainLab export carries two
z-scores: $\mathrm{pre\_z}$, the connection's prominence in the sender's
output profile, and $\mathrm{post\_z}$, its prominence in the receiver's
input profile (both bounded to $[0.1, 1.0]$ by the export). Phase 02 of
the pipeline fuses the pair into one signed weight:

$$w_{ab} \;=\; s \cdot \tanh\!\Big(\alpha \cdot \log \frac{\mathrm{post\_z}}{\mathrm{pre\_z} + \varepsilon}\Big), \qquad s = \frac{|\mathrm{pre\_z}| + |\mathrm{post\_z}|}{2}, \qquad \alpha = 1,\;\; \varepsilon = 0.1$$

The sign of $w$ is a **dominance** sign, not excitation/inhibition:
negative $w$ means pre-dominance (the connection weighs more in the
sender's output profile), positive $w$ means post-dominance. One synapse,
two viewpoints — not two strengths. The weights fill the **directed
functional connectivity matrix** $W$ (Phase 03; rows = source,
columns = target). In the reference run below, $W$ is $62 \times 62$
with $\sum w^2 = 40.15$ over 590 directed pairs.

### 2. Modes and groups

The singular value decomposition $W = U \Sigma V^{T}$ (Phase 04) splits
$W$ into modes — shared wiring patterns across the neuron set. The
reference run retains $k = 9$ modes (the median of three heuristics:
elbow 11, spectral gap 1, 90%-variance 9; cumulative explained variance
0.910). Neurons are partitioned into 12 **groups** by home mode (the mode
of maximal RMS participation, with polarity splits), using the
family-aware grouping in the reference configuration (`87ef7c02`).

### 3. The resonator score $S = G \times E$ (slides 1–3)

A candidate resonator is a **reciprocal pair** — a 2-cycle $a \rightleftarrows b$.
Only reciprocal pairs are scored (127 of the 590 directed pairs in the
reference run); for a non-reciprocal pair $S$ is **undefined, not zero**,
because the missing leg has no z-scores. The score multiplies two
geometric means:

$$G_{ab} = \sqrt{|w_{ab}|\,|w_{ba}|} \qquad\text{(loop strength)}$$

$$E_{ab} = \sqrt{\mathrm{post\_z}(a{\to}b) \cdot \mathrm{post\_z}(b{\to}a)} \qquad\text{(mutual receiver-side prominence)}$$

$$S_{ab} = G_{ab} \times E_{ab}$$

- $G$ is the *intensity* of the 2-cycle in the sense of Onnela et al.
  (2005): the geometric mean of the two legs' weights. Its square,
  $\Lambda_{ab} = G_{ab}^{2} = |w_{ab} w_{ba}|$, is the pair's loop gain.
  The geometric mean is load-bearing: it fails the pair when either leg
  fails (legs 0.9 and 0 give $G = 0$, where an arithmetic mean would
  claim 0.45), and it taxes imbalance between the legs.
- $E$ asks whether each side of the loop is prominent *to its receiver*:
  a loop both of whose legs loom large in the target's input profile.
  $E \in [0.1, 1]$ by the export's bounding.
- **Proposition (slide 1).** $S$ is symmetric in $a \leftrightarrow b$;
  $S = 0$ iff a leg has zero weight (annihilation is carried by $G$
  alone, since $E \geq 0.1$); $S$ is strictly increasing in each leg,
  other quantities held fixed; and $0 \leq S < 1$.

**Worked example (slide 1 draft).** FB5U ↔ hDeltaH7:
$w = -0.360 / +0.415$ gives $G = \sqrt{0.360 \times 0.415} = 0.387$;
$\mathrm{post\_z} = 0.70 / 0.97$ gives $E = \sqrt{0.70 \times 0.97} = 0.824$;
hence $S = 0.387 \times 0.824 = 0.319$ — the top-scoring pair of the
reference run. Seven of the top 12 pairs by $S$ join a glutamatergic
FB5 neuron to a cholinergic hDelta neuron ($p = 0.0002$ against chance).

**Controls and predecessors (slide 2).** Two alternatives were computed
and rejected on evidence:

- $E_{\mathrm{pre}} = \sqrt{\mathrm{pre\_z}(a{\to}b)\,\mathrm{pre\_z}(b{\to}a)}$
  (sender-side prominence). Its top 12 contains only 1 Glu–ACh pair
  ($p = 0.85$): the discriminating signal lives specifically in
  $\mathrm{post\_z}$, which is why $E = E_{\mathrm{post}}$ is the headline.
- $E_{I}$, the predecessor, measured dependence on the pair's share of
  each neuron's **in-set** input budget $I_a = \sum_u |w_{ua}|$
  (Bascompte-style dependence), giving the closed form
  $S_I = |w_{ab}|\,|w_{ba}| \,/\, \sqrt{I_a I_b}$. It was superseded
  because $I$ depends on which neurons happen to be in the exported
  set — a pair score should be intrinsic to the pair.

**What $S$ does not claim.** $S$ nominates *structural candidacy* for
resonance; it is not evidence of resonance. A biological resonator also
needs an excitatory–inhibitory sign structure (read from transmitters,
not from the sign of $w$) and dynamical timescales that $W$ does not
contain. Recordings, and fitted dynamical models, decide.

### 4. The pathway weight $P$ — the gold edges (pathway slide)

The gold dashed edges of the combined graph are an aggregate layer over
the groups of §2. For distinct groups $A$, $B$:

$$R_{AB} = \sum_{(a,b)\,\in\,A \times B} w_{ab} \qquad\text{(raw block sum)}$$

$$M_{AB} = \sum_{m=1}^{9} \omega_m \sum_{(a,b)\,\in\,A \times B} \sigma_m\, u_{am} v_{bm}, \qquad \omega_m = \frac{\sigma_m^2}{\sum_{j=1}^{9} \sigma_j^2} \qquad\text{(mode block sum)}$$

$$P_{AB} = 0.7\, R_{AB} + 0.3\, M_{AB}$$

$R$ adds the pair weights themselves over the whole block, signs
included. $M$ reads the same block through the nine retained modes: each
mode's rank-1 layer $\sigma_m u_m v_m^{T}$ is block-summed and weighted
by $\omega_m$, the mode's share of the retained variance
($\sum_m \omega_m = 1$). The blend constant 0.3 belongs to this layer
alone — it is not the $\alpha$ of the $w$ formula.

**Drawing rule.** Edge $A \to B$ is drawn (gold, dashed) exactly when

$$|P_{AB}| \;\geq\; 0.10 \times \max_{C \neq D} |P_{CD}|,$$

keeping at most the five largest $|P|$ per source group. In the
reference run, 11 of the 132 ordered group pairs are drawn — 10
negative, 1 positive.

**Worked example.** G01 → G09: $R = -15.18$ over 42 wired pairs,
$M = -6.01$, so $P = 0.7(-15.18) + 0.3(-6.01) = -12.43$ — the largest
$|P|$ of any pair, which sets the cutoff at $1.24$. The one positive
edge is G11 → G06, $P = +1.44$ (from $R = +2.01$, $M = +0.10$). In this
run the five-per-source cap never binds (the busiest source, G10, has 3
edges); the cutoff does all the filtering.

**Reading the gold layer honestly.** A block sum is signed, so opposed
pair traffic *cancels* inside a block: a heavily wired pair of groups
can draw no gold edge — **no gold edge does not mean no interaction**.
Pairs *inside* one group never receive a gold edge at all, so the
resonator loops of §3 (mostly inside G06) are invisible to this layer.
The sign of $P$ is the block's net pre-dominance (negative) or
post-dominance (positive) — again, not excitation or inhibition.

---

## Script reference

### `lt_bridge.py` — LanguageTool ⇄ LM Studio bridge

Speaks the LanguageTool HTTP API on the front (the Obsidian plugin POSTs
to `/v2/check`) and LM Studio's OpenAI-compatible chat-completions API
on the back, translating the model's proofreading back into
LanguageTool-shaped matches. Standard library only.

```bash
# minimal: point it at your LM Studio server and run
LMSTUDIO_URL=http://192.168.1.20:1234/v1 python3 lt_bridge.py
```

Then in Obsidian: *Settings → LanguageTool Integration → Endpoint →
Custom URL* → `http://localhost:8081`.

All configuration is by environment variable:

| Variable | Default | Meaning |
|---|---|---|
| `LT_BRIDGE_HOST` | `127.0.0.1` | Bind address |
| `LT_BRIDGE_PORT` | `8081` | Listen port |
| `LMSTUDIO_URL` | `http://localhost:1234/v1` | LM Studio base URL |
| `LMSTUDIO_MODEL` | first model at `/v1/models` | Model id to use |
| `LMSTUDIO_API_KEY` | `lm-studio` | Sent as the API key (LM Studio ignores it) |
| `MAX_CHARS` | `6000` | Max characters per model request; longer notes are split into paragraph chunks |
| `REQUEST_TIMEOUT` | `180` | Seconds to wait for the model, per chunk |

Example with several variables set:

```bash
LMSTUDIO_URL=http://bigbarda:1234/v1 \
LMSTUDIO_MODEL=qwen2.5-7b-instruct \
LT_BRIDGE_PORT=8081 \
MAX_CHARS=6000 \
python3 lt_bridge.py
```

### `make_resonator_slides.py` — the resonator slide set

```bash
python3 make_resonator_slides.py          # slide 1 only (the definition of S)
python3 make_resonator_slides.py 1        # slide 1: Definition 1, Proposition 1
python3 make_resonator_slides.py 2        # slide 2: the E factor (E_post, E_pre control, E_I)
python3 make_resonator_slides.py 3        # slide 3: the G factor (Onnela intensity, loop gain)
python3 make_resonator_slides.py all      # all three slides
```

Outputs, written to the `output/` folder: `resonator-slide1-definition.png`,
`resonator-slide2-E.png`, `resonator-slide3-G.png`. Any other argument
builds nothing. The one positional argument is the script's only option.

### `s_index_image1.py` — slide 1, alternative draft

```bash
python3 s_index_image1.py                 # no options
```

Writes `s_index_image1.png` to the `output/` folder. A two-column alternative
rendering of slide 1 (Figure 1 plus the worked FB5U ↔ hDeltaH7 example
of §3). It is a draft variant kept for comparison; the canonical slide 1
is the one built by `make_resonator_slides.py`.

### `make_pathway_slide.py` — the gold-edge slide

```bash
python3 make_pathway_slide.py             # no options
```

Writes `pathway-slide.png` to the `output/` folder: Definition 2 and
equations (8)–(10) of §4, the drawing rule, and the worked
G01 → G09 example.

### `make_pathway_slide_gloss-revision.py` — the gold-edge slide, expanded gloss

```bash
python3 make_pathway_slide_gloss-revision.py   # no options
```

A variant of `make_pathway_slide.py` with one change: the gloss under
equation (9) is expanded to spell out the recipe — take the $A$
entries of $U$'s column $m$ and the $B$ entries of $V^{T}$'s row $m$,
multiply every $A$ entry by every $B$ entry (the grid
$\sigma_m u_m v_m^{T}$), add them all, then weight by $\omega_m$.
It writes the same `pathway-slide.png` filename to the `output/`
folder, so it overwrites the main slide's output (and vice versa);
it is kept as a separate script until the expanded gloss is adopted.

### `make_nested_loop_eq8.py` — teaching figure: equation (8) in two stages

```bash
python3 make_nested_loop_eq8.py           # no options
```

Writes `nested-loop-eq8.png` to the `output/` folder. Equation (8)
in two stages on a toy $4 \times 4$ $W$ (neurons $n_1$–$n_4$ in two
groups, $G1 = \{n_1, n_2\}$ and $G2 = \{n_3, n_4\}$). Stage 1: the
groups make two ordered pairs, and each pair fills the roles of
eq. (8) — $A$ and $B$ are dummy variables, not groups. Stage 2:
each pair's block is summed cell by cell in loop order —
$R_{G1 \rightarrow G2} = R_{AB} = +0.06$ and
$R_{G2 \rightarrow G1} = R_{AB} = +0.50$. The toy weights are
invented for clean arithmetic, not pipeline data. (This figure
absorbs the point of `make_two_directions.py`, which stays in the
repo.)

### `make_two_directions.py` — teaching figure: $R_{AB}$ and $R_{BA}$ are different sums

```bash
python3 make_two_directions.py            # no options
```

Writes `two-directions.png` to the `output/` folder. The same toy
$W$ with both off-diagonal blocks outlined: $R_{AB} = +0.06$ (rows
$A$, columns $B$) and $R_{BA} = +0.50$ (rows $B$, columns $A$).
Every cell carries a direction (read row → column), mirror cells
across the diagonal are different synapses, and the double sum
inside one block never produces the other direction — the pipeline
evaluates all 132 ordered group pairs separately.

### `make_mode_block_eq9.py` — teaching figure: the mode block sum and the $\omega$ weights

```bash
python3 make_mode_block_eq9.py            # no options
```

Writes `mode-block-eq9.png` to the `output/` folder. Equation (9) on
the same toy neurons with $k = 2$ invented modes ($\sigma = 2, 1$):
each mode's layer is block-summed ($+0.12$ and $+0.77$), the weights
$\omega_m$ are read off the $\Sigma$ diagonal — $\omega_m =
\sigma_m^2 / \sum_j \sigma_j^2$, here $0.80$ and $0.20$ — and
$M_{AB} = 0.80 \times 0.12 + 0.20 \times 0.77 = +0.25$. The toy modes
are invented for clean arithmetic; they are not the SVD of the toy
$W$.

### `make_outer_product.py` — teaching figure: column × row = grid

```bash
python3 make_outer_product.py             # no options
```

Writes `outer-product.png` to the `output/` folder. How one mode's
layer is built: every entry of the column $u_1$ times every entry of
the row $v_1^{T}$ — a multiplication table with no addition
anywhere. One cell is spotlighted ($n_3 \to n_4$: $+0.90 \times
+0.80 = +0.72$, then $\times\ \sigma_1 = 2.0$ in the layer,
$+1.44$); addition only starts when a block of the layer is summed,
as in equation (9).

### `make_eq8_9_slides.py` — equations (8)–(10) on the real run

```bash
python3 make_eq8_9_slides.py              # slide 1 only (the raw block sum R)
python3 make_eq8_9_slides.py 2            # slide 2: the mode block sum M
python3 make_eq8_9_slides.py 3            # slide 3: the blend P, end to end
python3 make_eq8_9_slides.py all          # all three slides
python3 make_eq8_9_slides.py all --data-dir /path/to/run-folder
```

Writes `eq8-9-slide1.png`, `eq8-9-slide2.png` and `eq8-9-slide3.png`
to the `output/` folder. Where the teaching figures above use an
invented toy, these slides work the pathway example of §4 on the
reference run's real numbers: slide 1 opens up the G01 → G09 block of
$W$ and adds its 42 cells ($R = -15.18$); slide 2 reads the same block
through the nine retained modes — mode 1 contributes $-6.00$ of
$M = -6.01$, modes 2–9 together $-0.01$; slide 3 substitutes into
$P = 0.7R + 0.3M = -12.43$. The block sums are spelled with the single
summation $\sum_{(a,b)\,\in\,A \times B}$, matching §4 — the same sum,
written over the set of ordered pairs.

Needs numpy and matplotlib, plus the run's two data files
(`z_matrix.42d6ad4c.npz` and `eigen.42d6ad4c.json`), located by
`--data-dir` if given, else the `EIGEN_RUN_DIR` environment variable,
else beside the script (or in the current folder), else in a
`data/processed/hDelta_ABH_FB_15pre_001_merged_data_v1/` folder
beside the script. On loading, the script verifies that
G01 → G09 is the largest $|P|$ of the 132 ordered group pairs.

### `make_experiment_overview.py` — the Bruno experiment on one slide

```bash
python3 make_experiment_overview.py       # no options
```

Writes `bruno-experiment-overview.png` to the `out_qbi/` folder. The
experiment tests whether anesthetics silence cognition by
preferentially suppressing excitatory (cholinergic) transmission to
the fan-shaped body. The slide carries the hypothesis — including the
catch that both branches of the ExR7 fork are cholinergic synapses
from the same axon, so any dissociation must emerge downstream — the
circuit (EPG → ExR7, forking to FB4Y and the FB5 ⇄ hDelta loop on one
side and to LAL013 and exploratory turning on the other), and the
four legs: baseline, deactivation, graded anesthetic atlas, and the
combined test.

### `make_what_counts.py` — what would count as the cognitive link

```bash
python3 make_what_counts.py               # no options
```

Writes `bruno-what-counts.png` to the `out_qbi/` folder: the three
pre-agreed criteria for calling the anesthetic's effect cognitive —
a shared EC50 between its physiological and behavioural effects,
phenocopy (genetic silencing of FB5 reproducing the anesthetic's
fingerprint with no drug present), and occlusion read as the
two-route dissociation — each with a worked illustration and the
failure mode that would rule it out.

### `check_project_move.py` — before moving a project folder

```bash
python3 check_project_move.py /path/to/project [/path/to/new/location]
```

Read-only, standard library only: it never moves, edits or deletes
anything. Run it before relocating a PyCharm / GoLand project root.
It reports absolute references to the old location inside the project
(scripts, configs, `.idea` run configurations), an in-project
`.venv` (recreate it after the move — its internals hold absolute
paths), git worktrees, submodules or a `.git` file pointing
elsewhere, absolute symlinks, and `go.mod` `replace` directives
pointing at absolute paths. Exit code 0 = nothing that would break
the move, 1 = at least one blocking item, 2 = usage error.

---

## References

- Onnela, J.-P., Saramäki, J., Kertész, J. & Kaski, K. (2005).
  Intensity and coherence of motifs in weighted complex networks.
  *Physical Review E* 71, 065103. doi:10.1103/PhysRevE.71.065103
- Bascompte, J., Jordano, P. & Olesen, J. M. (2006). Asymmetric
  coevolutionary networks facilitate biodiversity maintenance.
  *Science* 312, 431–433. doi:10.1126/science.1123412
- Scheffer, L. K. et al. (2020). A connectome and analysis of the adult
  *Drosophila* central brain. *eLife* 9, e57443.
  doi:10.7554/eLife.57443
- Wilson, H. R. & Cowan, J. D. (1972). Excitatory and inhibitory
  interactions in localized populations of model neurons.
  *Biophysical Journal* 12, 1–24. doi:10.1016/S0006-3495(72)86068-5
