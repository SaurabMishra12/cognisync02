# CogniSync → TMLR: experiment suite and rewritten manuscript

Everything needed to turn the rejected CIKM submission into a TMLR paper whose
claims match its evidence. Six notebooks, a rewritten manuscript, and the tooling
that connects them.

```
tmlr/
├── notebooks/          run these in Colab or Kaggle, in order
│   ├── NB1_full_corpus_beir.ipynb      full-corpus BEIR, matched rerank budgets
│   ├── NB2_alpha_headroom.ipynb        oracle bound + why learning misses it
│   ├── NB3_adaptive_security.ipynb     attack × defense matrix, matched FPR
│   ├── NB4_downstream_llm.ipynb        behavioural ASR on a real local model
│   ├── NB5_cost_accounting.ipynb       cost/quality frontier on real corpora
│   └── NB6_tables_figures.ipynb        emits every table, figure, and macro
├── paper/
│   ├── cognisync_tmlr.tex              the rewritten manuscript
│   ├── cognisync_tmlr.bib
│   └── lint_paper.py                   pre-submission structural check
├── docs/
│   ├── GPU_BUDGET.md                   what to run where, and what it costs
│   └── REVIEWER_RESPONSE.md            every CIKM criticism → where it is answered
└── builders/                           the scripts that generate the notebooks
    ├── build_nb*.py
    ├── nbutil.py
    └── smoketest.py                    71 offline checks on the notebook logic
```

---

## The short version of what changed

The CIKM reviews were right, and the paper cannot be saved by adding experiments
to the existing narrative. Three of its load-bearing claims do not survive
contact with a fair protocol:

| CIKM claim | Problem |
|---|---|
| +2.80 pp MRR@5 over Dense | The proposed system had a cross-encoder; the baselines did not. |
| MRR@5 = 0.887 | Measured by reranking dataset-provided candidate pools, not by retrieving from a corpus. |
| Adaptive-injection ASR 99.3% → 0.12% | The "adaptive" attack was the query text plus a fixed template, so 99.3% is a property of the construction, not a measurement. |

Two further problems are visible in the repository rather than the paper. The
full-corpus script (`calc_full_corpus_significance.py`) that produced the
0.9216 vs 0.9197 result uses a **fixed α = 0.6 and no cross-encoder**, so it
never evaluated the proposed system; and `latency_results.txt` records a 3,325 ms
median where the paper reports 275.6 ms.

**The reframe.** TMLR does not ask for novelty or state-of-the-art results. It
asks two questions: are the claims supported by convincing evidence, and would
some subset of its audience be interested. That makes the honest version of this
work *stronger* than the version that was rejected, because its most interesting
findings are the ones the reviewers extracted themselves. The paper becomes a
measurement study with three results, two of them corrective:

1. **Per-query fusion weighting does not pay, and here is the bound on how much
   it ever could.** An oracle establishes the headroom; a flatness analysis shows
   the target is largely unidentifiable. That is a bounded negative result, which
   is publishable and useful.
2. **Lightweight retrieval-layer filters do not survive an adaptive attacker.**
   Six attackers × six defenses at matched false-positive budgets. The
   three-feature filter collapses; a fine-tuned classifier holds.
3. **Payload entry overstates real risk**, by a factor this paper measures. No
   prior work in this area reports the conversion factor from payload entry to
   downstream compliance.

Full mapping in [`docs/REVIEWER_RESPONSE.md`](docs/REVIEWER_RESPONSE.md).

---

## Running the experiments

Read [`docs/GPU_BUDGET.md`](docs/GPU_BUDGET.md) first — it has the exact
hardware, runtime, and tier choices. The summary:

**Everything fits on a free Colab T4.** Peak VRAM across all six notebooks is
about 7 GB (NB4 with a 3B model), well inside a T4's 15 GB. Host RAM is the
binding constraint, not the GPU. The only thing needing Kaggle is the optional
full MS MARCO tier in NB1, which wants ~22 GB of RAM.

```
NB1  ~55 min   ← run first, its cached embeddings speed up NB2/NB3/NB5
NB2  ~15 min
NB3  ~60 min
NB4  ~55 min   ← reads NB3's attack documents
NB5  ~20 min
NB6  <1 min, CPU only
────────────
     ~3.5 h total on one free T4
```

Notebooks are independent — each regenerates what it needs if an upstream one
has not run — but running in order avoids recomputing embeddings and lets NB4
replay NB3's exact adaptive attack documents, which is what ties the retrieval
and behavioural numbers to the same corpus.

Artifacts land in `cognisync_tmlr/results/` (Kaggle: `/kaggle/working/…`; Colab:
Drive if mounted). **Mount Drive on Colab** — free sessions disconnect, and the
embedding cache is what makes a re-run cheap.

## Producing the paper

```bash
# after NB6 has run, copy its output next to the manuscript
cp cognisync_tmlr/paper/*.tex cognisync_tmlr/paper/*.pdf tmlr/paper/

cd tmlr/paper
python3 lint_paper.py cognisync_tmlr.tex      # structural check, no LaTeX needed
latexmk -pdf cognisync_tmlr.tex
```

Get `tmlr.sty` from <https://github.com/JmlrOrg/tmlr-style-file>.

**No number in the manuscript is typed by hand.** Inline figures are LaTeX macros
defined in `results_macros.tex`, which NB6 generates from the artifacts; tables
are `\input` files NB6 writes. Before the notebooks run, every macro renders as a
red `[placeholder]`, so an unfilled slot cannot be mistaken for a measurement.
NB6 also writes `claims.json` and audits the `.tex` against it, which is the
mechanism that would have caught the CIKM version's tables disagreeing with each
other.

## Verifying the notebook logic without a GPU

```bash
python3 builders/smoketest.py
```

71 checks over the pure-Python logic — fusion, nDCG, the bootstrap, every attack
constructor, QA scoring, reranking. It found four real bugs while this suite was
being written, all now fixed and covered by regression tests:

- `paired_bootstrap` returned **p = 0** for two systems with identical per-query
  scores (zero-variance differences broke the percentile test). Given that the
  paper's ablation claims two systems are *statistically indistinguishable*, this
  one mattered.
- Attack template selection used Python's `hash()` on strings, which is
  randomised per process — the generated attack corpus differed on every run.
- One core directive contained the word `output`, which is on the very keyword
  list the imperative-free attacker exists to evade.
- Two generated LaTeX tables had a column-count mismatch and an unescaped `%`;
  both would have failed compilation. NB6 now validates every table it writes.

## Regenerating the notebooks

The `.ipynb` files are generated, so edit the builders and rebuild:

```bash
for b in build_nb1 build_nb2 build_nb3 build_nb4 build_nb5_nb6; do
  python3 builders/$b.py
done
python3 builders/smoketest.py
```
