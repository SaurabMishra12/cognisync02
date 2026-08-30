"""A4: how much reranking budget does it take to erase first-stage differences?

Reviewer 2 asked how many candidates the cross-encoder sees. The CIKM code answers
`top_n = min(10, ...)`, hardcoded and never reported. That number decides the whole
ablation: at depth 10 the reranker can only reorder ten documents, so first-stage recall
into the top ten is everything, and at depth 200 the first stage barely matters.

This sweeps the budget and plots quality against latency for each first stage. Two
outcomes are interesting and one is not:

* If first-stage differences shrink as depth grows, the fusion mechanism is a
  recall-under-budget device, which is a defensible and testable claim the paper could
  make honestly.
* If they never appear at any depth, the mechanism does nothing, which is a cleaner
  negative result than anything in the CIKM draft.
* If they only appear at depth 10, that is worth knowing before anyone deploys this.

Usage
-----
    python -m exp_a.a4_ce_budget --datasets scifact fiqa nfcorpus --depths 5 10 20 50 100 200
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import RetrievalConfig, set_all_seeds
from common.data import load_beir
from common.io_utils import Checkpoint, write_result
from common.metrics import evaluate_run
from common.retrieval import AlphaPredictor, BM25Index, DenseIndex, HybridRetriever, Reranker, minmax, oracle_alpha_for_query, query_features


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datasets", nargs="+", default=["scifact", "nfcorpus", "fiqa"])
    ap.add_argument("--depths", nargs="+", type=int, default=[5, 10, 20, 50, 100, 200])
    ap.add_argument("--first-stages", nargs="+", default=["dense", "rrf", "learned+fallback"])
    ap.add_argument("--reranker", default="ms-marco")
    ap.add_argument("--query-limit", type=int, default=None)
    args = ap.parse_args()

    set_all_seeds()
    max_depth = max(args.depths)
    cfg = RetrievalConfig(first_stage_depth=max(100, max_depth), reranker_key=args.reranker)
    checkpoint = Checkpoint("a4_ce_budget")

    rows = []
    for dataset in args.datasets:
        print(f"\n{'=' * 78}\n{dataset}\n{'=' * 78}")
        corpus, queries, qrels = load_beir(dataset)
        doc_ids = list(corpus)
        doc_texts = [corpus[d] for d in doc_ids]

        qids = sorted(queries)
        rng = np.random.default_rng(42)
        rng.shuffle(qids)
        n_tune = min(cfg.alpha_tuning_queries, max(1, len(qids) // 5))
        tuning_qids, eval_qids = qids[:n_tune], qids[n_tune:]
        if args.query_limit:
            eval_qids = eval_qids[: args.query_limit]

        dense = DenseIndex(cfg.encoder_key, batch_size=cfg.batch_size).build(doc_ids, doc_texts, cache_tag=dataset)
        lexical = BM25Index().build(doc_ids, doc_texts)
        retriever = HybridRetriever(cfg, dense, lexical)

        if any("learned" in s for s in args.first_stages):
            feats, alphas = [], []
            for qid in tqdm(tuning_qids, desc="alpha tuning", leave=False):
                d_sc, _ = retriever._dense_candidates(queries[qid], cfg.first_stage_depth)
                l_sc = retriever._lexical_candidates(queries[qid], cfg.first_stage_depth)
                union = sorted(set(d_sc) | set(l_sc))
                if len(union) < 2:
                    continue
                dv = minmax(np.array([d_sc.get(d, -1e9) for d in union], dtype=float))
                lv = minmax(np.array([l_sc.get(d, 0.0) for d in union], dtype=float))
                a, _ = oracle_alpha_for_query(dv, lv, union, qrels.get(qid, {}), k=cfg.eval_k)
                feats.append(query_features(queries[qid], dv, lv))
                alphas.append(a)
            retriever.predictor = AlphaPredictor(cfg).fit(feats, alphas)

        reranker = Reranker(args.reranker)

        # Retrieve once per first stage at max depth, then rerank prefixes of that list.
        # Reranking is the expensive part, so this keeps the sweep affordable.
        for stage in args.first_stages:
            first_stage_runs, fs_ms = {}, []
            for qid in tqdm(eval_qids, desc=f"{stage} first stage", leave=False):
                t0 = time.perf_counter()
                ranked = retriever.retrieve(queries[qid], strategy=stage, depth=cfg.first_stage_depth)
                fs_ms.append((time.perf_counter() - t0) * 1000)
                first_stage_runs[qid] = ranked

            for depth in [0] + list(args.depths):
                key = Checkpoint.key(dataset=dataset, stage=stage, depth=depth, reranker=args.reranker, n=len(eval_qids))
                if checkpoint.has(key):
                    rows.append(checkpoint.get(key)["row"])
                    continue

                run, rr_ms = {}, []
                for qid, ranked in tqdm(first_stage_runs.items(), desc=f"{stage} depth={depth}", leave=False):
                    if depth == 0:
                        run[qid] = ranked
                        rr_ms.append(0.0)
                        continue
                    cands = [(d, corpus[d], s) for d, s in ranked]
                    t0 = time.perf_counter()
                    run[qid] = reranker.rerank(queries[qid], cands, depth=depth)
                    rr_ms.append((time.perf_counter() - t0) * 1000)

                agg, _ = evaluate_run(run, qrels, eval_k=cfg.eval_k, recall_ks=cfg.recall_ks)
                row = {
                    **agg,
                    "dataset": dataset,
                    "first_stage": stage,
                    "rerank_depth": depth,
                    "reranker": args.reranker if depth else "none",
                    "first_stage_ms_mean": float(np.mean(fs_ms)),
                    "rerank_ms_mean": float(np.mean(rr_ms)),
                    "rerank_ms_p95": float(np.percentile(rr_ms, 95)) if rr_ms else 0.0,
                    "total_ms_mean": float(np.mean(fs_ms)) + float(np.mean(rr_ms)),
                }
                rows.append(row)
                checkpoint.put(key, {"row": row})
                print(
                    f"  {stage:18s} depth={depth:4d}  nDCG@{cfg.eval_k}={agg[f'ndcg@{cfg.eval_k}']:.4f}  "
                    f"{row['total_ms_mean']:7.1f} ms"
                )

    df = pd.DataFrame(rows)
    write_result(
        "a4_ce_budget",
        df,
        config={
            "retrieval": cfg.to_dict(),
            "depths": args.depths,
            "first_stages": args.first_stages,
            "note": (
                "rerank_depth=0 is the first stage alone. The CIKM system used depth 10 "
                "without reporting it; this sweep shows whether that choice is load-bearing."
            ),
        },
    )

    metric = f"ndcg@{cfg.eval_k}"
    print("\n" + "=" * 78)
    print(f"{metric} by rerank depth (mean over datasets)")
    print("=" * 78)
    pivot = df.pivot_table(index="rerank_depth", columns="first_stage", values=metric)
    print(pivot.round(4).to_string())

    # The question the sweep exists to answer: does the spread between first stages
    # shrink as the reranker gets more to work with?
    spread = pivot.max(axis=1) - pivot.min(axis=1)
    print("\nSpread between best and worst first stage, by depth:")
    print((spread * 100).round(3).to_string() + "  (percentage points)")
    write_result("a4_ce_budget__spread", spread.reset_index().rename(columns={0: "spread_ndcg"}))


if __name__ == "__main__":
    main()
