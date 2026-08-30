# CogniSync → TMLR experiment suite

Code for the reframed paper. Written for a single Kaggle/Colab T4; every script
checkpoints and resumes, and embeddings cache to disk so the seven-dataset sweep encodes
each corpus once.

Read `docs/EXPERIMENT_PLAN.md` first. It has the code audit these experiments are answering
and the run order.

## Install

```bash
pip install -r requirements.txt
export COGNISYNC_ROOT=/kaggle/working/cognisync_out
export COGNISYNC_CACHE=/kaggle/working/cognisync_cache   # survives within a session
```

`bm25s` matters. `rank_bm25` scores every document in pure Python on every query, which is
why the CIKM evaluation never ran full-corpus; on the 382k-document Touché corpus it is
minutes per query against milliseconds for `bm25s`.

## What each script produces

Every run writes three things into `$COGNISYNC_ROOT`:

- `results/<name>.csv` — the aggregate table
- `results/<name>__per_query.csv` — raw per-query values, so every significance claim in
  the paper can be recomputed without re-running retrieval
- `logs/<name>.json` — the fully resolved config plus package versions, GPU, and git commit

Reviewer 2 listed six underspecified details in the CIKM PDF. The log file is designed so
that list cannot happen again.

## Scripts

### Track A — retrieval under a protocol that does not flatter it

| Script | Replaces | Runtime (T4) |
|---|---|---|
| `exp_a/a1_beir_full_corpus.py` | Table 1. Full-corpus zero-shot BEIR, full factorial over first stage × reranker | 4–6 h for `--all` |
| `exp_a/a2_contamination.py` | Table 4. Train-vs-dev contrast, reranker provenance, mixture membership | ~2 h |
| `exp_a/a3_alpha_decomposition.py` | Table 5. Separates the Random Forest from the undisclosed override, adds oracle-α and best-fixed-α | ~2 h |
| `exp_a/a4_ce_budget.py` | New. Sweeps the rerank depth the CIKM code hardcoded at 10 | ~2 h |

```bash
python -m exp_a.a1_beir_full_corpus --all --rerankers none ms-marco
python -m exp_a.a2_contamination --contrast all
python -m exp_a.a3_alpha_decomposition --datasets scifact nfcorpus fiqa --with-reranker
python -m exp_a.a4_ce_budget --depths 5 10 20 50 100 200
```

### Track B — security, with an adversary who knows the filter

| Script | Replaces | Runtime |
|---|---|---|
| `exp_b/b1_b2_attack_ladder.py` | Table 7. Oracle vs held-out centroid × six levels of adversary knowledge | ~3 h |
| `exp_b/b3_downstream_compliance.py` | New. Payload entry vs actual model compliance, plus tool spoofing | ~4 h |
| `exp_b/b4_detector_comparison.py` | The bare 86.36% number. Adds baselines, cost, and a transfer matrix | ~2 h |
| `exp_b/b5_defense_cost_curve.py` | Table 9. Threshold sweep at realistic poisoning base rates | ~2 h |

```bash
python -m exp_b.b1_b2_attack_ladder --dataset scifact --centroid-sources oracle holdout
python -m exp_b.b3_downstream_compliance --models gemma2-2b qwen2.5-3b
python -m exp_b.b3_downstream_compliance --tool-spoofing --models qwen2.5-3b
python -m exp_b.b4_detector_comparison
python -m exp_b.b5_defense_cost_curve --dataset scifact
```

`exp_b/attacks.py` holds the six-level ladder; `exp_b/defenses.py` holds the filter and its
baselines. The one change that matters most is `centroid_source`: `"oracle"` reproduces the
CIKM configuration (centroid fit on the query's own clean pool), `"holdout"` is deployable.

### Track C — episodic memory, implemented

| Script | Replaces | Runtime |
|---|---|---|
| `exp_c/episodic_graph.py` | Section 4.2's design sketch. A working graph plus four baselines | — |
| `exp_c/c1_longmemeval.py` | Table 10. Real evaluation on LongMemEval | ~6 h with generation |
| `exp_c/c2_graph_ablation.py` | New. Edge ablation plus a timestamp-shuffling control | ~2 h |

```bash
python -m exp_c.c1_longmemeval --variant s --n-instances 100
python -m exp_c.c1_longmemeval --variant s --n-instances 100 --with-qa --qa-model qwen2.5-3b
python -m exp_c.c2_graph_ablation --n-instances 100
```

### Track D — cost

```bash
python -m exp_d.d1_latency_profile --sizes 10000 100000 --device cuda
python -m exp_d.d1_latency_profile --sizes 10000 --device cpu    # the local-first number
```

## Running on Kaggle (12-Hour Session Plan)

Upload [`cognisync_tmlr_master.ipynb`](file:///home/saurab/Documents/cognySync/cognisync02/cognisync-tmlr/cognisync_tmlr_master.ipynb) (or [`notebooks/kaggle_runner.ipynb`](file:///home/saurab/Documents/cognySync/cognisync02/cognisync-tmlr/notebooks/kaggle_runner.ipynb)) directly into Kaggle.
- **Accelerator:** GPU T4 x1
- **Internet:** ON
- **Persistence:** Filesystem / Variables ON

The runner is partitioned into **three 12-hour session blocks** (and a 10-minute smoke test):

0. **Block 0 (10–15 min):** Quick Smoke Test (verifies all 4 tracks on small subsets)
1. **Block 1 (8–10 h):** `A1` (BEIR sweep & embedding cache) + `A2` (Contamination) + `A3` (Alpha decomposition) + `A4` (CE budget)
2. **Block 2 (8–10 h):** `B1/B2` (Attack ladder) + `B4` (Detector comparison) + `B3` (LLM compliance) + `B5` (Defense cost curve)
3. **Block 3 (8–9 h):** `C1` (LongMemEval episodic graph) + `C2` (Graph ablation & timestamp control) + `D1` (Latency profile)

Stop after Block 1 and look at the numbers (`a2_contamination_gap.csv`, `a3_alpha_diagnostics.csv`, `a3_alpha_decomposition.csv`). If the contamination gap and the fallback firing rate come out as expected, the paper's core retrieval thesis is established. If A3's oracle-α row shows real headroom over best-fixed-α, that is a different and more constructive paper and worth rethinking before spending Blocks 2–3.

## Things that will bite you

- **Touché and TREC-COVID are the expensive cells.** Start `a1` with the small datasets to
  confirm the pipeline, then add `--all`.
- **`beir`'s download mirror is flaky on Kaggle.** `common/data.py` falls back to the
  `BeIR/*` Hugging Face mirrors automatically; the fallback is slower but reliable.
- **`gemma-2-2b-it` needs a Hugging Face token** and license acceptance. `qwen2.5-3b`
  does not, so start there if you want to test the harness.
- **4-bit Qwen-7B needs `bitsandbytes` and `accelerate`.** Both are commented out in
  `requirements.txt`; uncomment if you want that condition.
- **Do not reuse the CIKM numbers.** Several of them measure a system the paper does not
  describe. The audit section of the plan lists which ones.
