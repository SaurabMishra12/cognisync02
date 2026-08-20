# GPU budget: what to run, where, and what it costs

**Bottom line: every experiment in this paper runs on a free Colab T4.** Peak
VRAM across the whole suite is about 7 GB against a T4's 15 GB, and the total
is roughly 3.5 hours. Kaggle's 2×T4 buys you longer sessions and more host RAM,
not more speed — nothing here is sharded across GPUs.

The constraint that actually bites is **host RAM**, not VRAM. Colab free gives
you ~12.7 GB; Kaggle gives ~29 GB. That single difference decides which tier of
NB1 you can run.

---

## Per-notebook budget

Measured for the default configuration on a T4 (16 GB card, ~15 GB usable).

| Notebook | Wall clock | Peak VRAM | Peak host RAM | Disk | Needs GPU? |
|---|---|---|---|---|---|
| NB1 `standard` tier, 1 encoder | ~55 min | 2.5 GB | ~5 GB | 1.2 GB | yes |
| NB1 `standard`, 4 encoders | ~3.2 h | 2.5 GB | ~5 GB | 4 GB | yes |
| NB1 `extended` tier | ~2.5 h | 3.5 GB | ~9 GB | 3 GB | yes |
| NB1 `msmarco` tier | ~2.5 h | 8 GB | **~22 GB** | 15 GB | Kaggle only |
| NB2 | ~15 min | 2 GB | ~4 GB | — | yes (reuses NB1 cache) |
| NB3 | ~60 min | 5 GB | ~6 GB | 2 GB | yes |
| NB4, 1 model (1.5B) | ~20 min | 3.2 GB | ~4 GB | 3 GB | yes |
| NB4, 2 models (1.5B + 3B) | ~55 min | 6.4 GB | ~4 GB | 9 GB | yes |
| NB5 | ~20 min | 3 GB | ~5 GB | — | yes |
| NB6 | <1 min | — | <1 GB | — | **no** |

### Where the time goes

- **Encoding corpora.** MiniLM-L6 does ~3,000 passages/s on a T4. The `standard`
  BEIR tier is 272K documents ≈ 90 s. Cached to disk after the first run, so a
  re-run after a disconnect skips it entirely.
- **Cross-encoder reranking.** ~1,500 pairs/s at batch 256. This dominates NB1:
  the grid is deduplicated so each (query, document) pair is scored once across
  all systems and budgets, which cuts what would be a 4× cost down to ~1.2×.
- **BM25.** `bm25s`, not `rank_bm25`. This is not a micro-optimisation — the
  original code's `rank_bm25` scores every document in pure Python on every
  query, which at 500K documents × 2,000 queries is several hours. `bm25s` does
  it in seconds.
- **Generation in NB4.** ~25–40 tok/s per stream on a T4; batch 8 and 64 new
  tokens gives roughly 2 s per batch.

---

## Free Colab T4

The realistic plan on the free tier, given that sessions are capped around 12 h
and get reclaimed when idle:

| Session | Run | Time |
|---|---|---|
| 1 | NB1 `standard`, `ENCODERS=["minilm"]` | ~55 min |
| 2 | NB2 + NB5 (both reuse NB1's cache) | ~35 min |
| 3 | NB3 | ~60 min |
| 4 | NB4 with `MODELS=["Qwen/Qwen2.5-1.5B-Instruct"]` | ~20 min |
| 5 | NB6 (no GPU needed — use a CPU runtime) | ~1 min |

**Mount Drive first, in every session.** The notebooks write to
`/content/drive/MyDrive/cognisync_tmlr/` when Drive is present, which is what
makes the embedding cache survive a disconnect. Without it a dropped session
costs you the whole run.

```python
from google.colab import drive
drive.mount('/content/drive')
```

If you get a K80 or a P4 instead of a T4, everything still runs; expect roughly
2× the wall clock, and drop `GEN_BATCH` to 4 in NB4.

## Kaggle 2×T4

Kaggle gives 12 h uninterrupted sessions and 30 h/week of GPU quota — enough for
the entire suite plus the extras Colab cannot hold. Use it for:

- **NB1 `msmarco` tier.** The full 8.84M-passage MS MARCO corpus needs ~22 GB of
  host RAM for the fp16 embedding matrix plus the BM25 index. This is the one
  thing Colab free cannot do, and it is worth doing: MS MARCO was the CIKM
  paper's headline dataset, so evaluating it at true full-corpus scale directly
  answers the reviewers' question about the 100K-passage experiment.
- **NB1 with all 4 encoders**, for the generality grid (~2.3 h).
- **NB4 with a 3B model**, or two models back to back.

The second T4 is not used by any notebook. If you want the multi-model NB4 table
faster, run two Kaggle sessions with different `MODELS` lists rather than trying
to shard one.

Set the accelerator to **GPU T4 ×2** anyway — Kaggle allocates more host RAM to
that configuration than to the single-GPU one, and host RAM is what you need.

Artifacts go to `/kaggle/working/cognisync_tmlr/`. Commit the notebook version at
the end so the outputs persist; `/kaggle/working` is wiped when the session ends
otherwise.

---

## Tier selection

Pick the smallest tier that supports the claim you want to make.

| Tier | Corpora | Docs | What it supports |
|---|---|---|---|
| `smoke` | nfcorpus, scifact | 9K | Verifying the pipeline runs. Not a result. |
| `standard` | + arguana, scidocs, fiqa, trec-covid | 272K | **The paper's main table.** Six BEIR corpora at full corpus scale is a defensible retrieval claim. |
| `extended` | + quora, touche2020 | 1.18M | Strengthens the generality claim; adds ~1.5 h. |
| `msmarco` | MS MARCO dev-small, full corpus | 8.84M | Directly replaces the CIKM full-corpus experiment. Worth the Kaggle session. |

`standard` is enough to submit. `standard` + `msmarco` is what forecloses the
reviewer objection that made the CIKM version's retrieval claim unusable.

---

## If you hit a limit

**CUDA OOM.** Lower `batch_size` in `DenseIndex` (256 → 128) and `GEN_BATCH` in
NB4 (8 → 4). VRAM is not the constraint at defaults, so an OOM usually means the
runtime gave you a smaller card than a T4 — check `torch.cuda.get_device_name(0)`.

**Host RAM OOM.** Almost always NB1 on `extended` or `msmarco` under Colab free.
Drop to `standard`, or move to Kaggle. Reducing `FIRST_STAGE_DEPTH` from 1000 to
200 also helps and costs little, since nothing here reranks deeper than 100.

**No space left on device.** The embedding cache is the bulk of it. Delete
`cognisync_tmlr/cache/emb_*.npy` for corpora you have already scored — the
results are in `results/`, and only re-runs need the cache.

**Session disconnects mid-run.** Re-run the same notebook. Every corpus checks
its cache before encoding, so you resume rather than restart. This is why Drive
mounting matters on Colab.

**A dataset fails to load.** BEIR mirrors occasionally move. NB1's per-dataset
loop catches exceptions and continues, so one broken corpus does not lose the
run — check the printed `!!` lines and re-run just that dataset afterwards.

---

## Cutting the budget further

If GPU time is genuinely scarce, the suite degrades gracefully in this order,
and this is roughly the order of how much each costs you in reviewer confidence:

1. **NB4 to one model.** Halves NB4. The compliance-gap result still stands; you
   lose the cross-model generality claim.
2. **NB1 to one encoder.** Cuts NB1 from 3.2 h to 55 min. You lose the "does not
   depend on the backbone" claim, which is worth keeping if you can afford it.
3. **NB3's `A5_N` from 60 to 30 queries.** Halves the adaptive-attack section.
   Widens the confidence interval on the most important number in the paper —
   do this last.
4. **Skip `extended` and `msmarco`.** Free, but MS MARCO at full scale is
   specifically what the metareview asked for.

Do not cut: the matched rerank budgets in NB1, the matched FPR calibration in
NB3, or the A5 attacker. Those three are the methodological content of the paper,
and without any one of them it reverts to the version that was rejected.
