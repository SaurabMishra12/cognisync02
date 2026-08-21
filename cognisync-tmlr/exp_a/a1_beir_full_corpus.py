"""A1: full-corpus zero-shot retrieval on BEIR.

Replaces the CIKM Table 1. Three protocol changes, each aimed at a specific objection:

* No candidate pools. Retrieval runs against the entire corpus, so first-stage quality is
  actually being measured. (Reviewer 1 W2, reviewer 2 W2, metareview 3.)
* Full factorial over first stage x reranker, so no baseline is handicapped by missing a
  component the proposed system has. (Reviewer 2 W1, reviewer 4 W2, metareview 2.)
* Datasets outside the encoder's published training mixture, so a gain here means
  something. (New; see a2.)

Usage
-----
    python -m exp_a.a1_beir_full_corpus --datasets scifact nfcorpus --rerankers ms-marco
    python -m exp_a.a1_beir_full_corpus --all          # the full sweep, ~4-6h on a T4

The sweep checkpoints per (dataset, first_stage, reranker) cell and resumes, because
Kaggle sessions expire.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import BEIR_DATASETS, RetrievalConfig, set_all_seeds
from common.data import check_expected_sizes, load_beir
from common.io_utils import Checkpoint, write_result
from common.metrics import compare_systems, evaluate_run
from common.retrieval import (
    AlphaPredictor,
    BM25Index,
    DenseIndex,
    HybridRetriever,
    Reranker,
    minmax,
    oracle_alpha_for_query,
    query_features,
)

FIRST_STAGES = ["dense", "lexical", "rrf", "fixed", "learned", "fallback", "learned+fallback"]


def train_alpha_predictor(
    retriever: HybridRetriever,
    corpus: Dict[str, str],
    queries: Dict[str, str],
    qrels: Dict[str, Dict[str, int]],
    cfg: RetrievalConfig,
    tuning_qids: List[str],
) -> AlphaPredictor:
    """Fit the Random Forest on held-out tuning queries.

    The CIKM version took `tuning_set[:300]` from a 15% split without documenting the
    origin (reviewer 2's fifth reproducibility gap). Here the tuning ids are passed in
    explicitly and written to the log.
    """
    features, oracle_alphas = [], []
    for qid in tqdm(tuning_qids, desc="alpha tuning", leave=False):
        query = queries[qid]
        dense_scores, _ = retriever._dense_candidates(query, cfg.first_stage_depth)
        lex_scores = retriever._lexical_candidates(query, cfg.first_stage_depth)
        union = sorted(set(dense_scores) | set(lex_scores))
        if len(union) < 2:
            continue
        d_vec = minmax(np.array([dense_scores.get(d, -1e9) for d in union], dtype=float))
        l_vec = minmax(np.array([lex_scores.get(d, 0.0) for d in union], dtype=float))
        best_alpha, _ = oracle_alpha_for_query(
            d_vec, l_vec, union, qrels.get(qid, {}), steps=cfg.alpha_grid_steps, k=cfg.eval_k
        )
        features.append(query_features(query, d_vec, l_vec))
        oracle_alphas.append(best_alpha)

    predictor = AlphaPredictor(cfg).fit(features, oracle_alphas)
    print(f"[alpha] trained on {len(features)} queries; importances: {predictor.feature_importance()}")
    return predictor


def run_dataset(
    dataset: str,
    cfg: RetrievalConfig,
    first_stages: List[str],
    rerankers: List[Optional[str]],
    checkpoint: Checkpoint,
    query_limit: Optional[int] = None,
) -> tuple[List[dict], List[dict], List[dict]]:
    print(f"\n{'=' * 78}\n{dataset}\n{'=' * 78}")
    corpus, queries, qrels = load_beir(dataset)
    size_report = check_expected_sizes(dataset, corpus, queries)
    print(f"  corpus={len(corpus)}  queries={len(queries)}")

    qids_all = sorted(queries)
    rng = np.random.default_rng(42)
    rng.shuffle(qids_all)

    n_tune = min(cfg.alpha_tuning_queries, max(1, len(qids_all) // 5))
    tuning_qids, eval_qids = qids_all[:n_tune], qids_all[n_tune:]
    if query_limit:
        eval_qids = eval_qids[:query_limit]
    print(f"  alpha tuning queries={len(tuning_qids)}  evaluation queries={len(eval_qids)}")

    doc_ids = list(corpus)
    doc_texts = [corpus[d] for d in doc_ids]

    dense = DenseIndex(cfg.encoder_key, batch_size=cfg.batch_size).build(doc_ids, doc_texts, cache_tag=dataset)
    lexical = BM25Index().build(doc_ids, doc_texts)
    print(f"  bm25 backend={lexical.backend}")

    retriever = HybridRetriever(cfg, dense, lexical)
    needs_alpha = any(s in ("learned", "learned+fallback") for s in first_stages)
    if needs_alpha:
        retriever.predictor = train_alpha_predictor(retriever, corpus, queries, qrels, cfg, tuning_qids)

    reranker_cache: Dict[str, Reranker] = {}
    agg_rows, diag_rows = [], []
    per_query_by_system: Dict[str, Dict[str, Dict[str, float]]] = {}

    for stage in first_stages:
        for rk in rerankers:
            system = stage if rk is None else f"{stage}+{rk}"
            key = Checkpoint.key(
                dataset=dataset, stage=stage, reranker=rk, cfg=cfg.to_dict(), n_eval=len(eval_qids)
            )
            if checkpoint.has(key):
                rec = checkpoint.get(key)
                print(f"  [skip] {system} (cached)")
                agg_rows.append(rec["aggregate"])
                if rec.get("diagnostics"):
                    diag_rows.append(rec["diagnostics"])
                per_query_by_system[system] = rec.get("per_query", {})
                continue

            if rk is not None and rk not in reranker_cache:
                reranker_cache[rk] = Reranker(rk)
            reranker = reranker_cache.get(rk) if rk else None

            retriever.reset_diagnostics()
            run = {}
            for qid in tqdm(eval_qids, desc=f"  {system}", leave=False):
                ranked = retriever.retrieve(queries[qid], strategy=stage, depth=cfg.first_stage_depth)
                if reranker is not None:
                    cands = [(d, corpus[d], s) for d, s in ranked]
                    ranked = reranker.rerank(queries[qid], cands, depth=cfg.rerank_depth)
                run[qid] = ranked

            agg, per_query = evaluate_run(run, qrels, eval_k=cfg.eval_k, recall_ks=cfg.recall_ks)
            agg.update({"dataset": dataset, "first_stage": stage, "reranker": rk or "none", "system": system})
            diag = retriever.diagnostics.summary()
            diag.update({"dataset": dataset, "first_stage": stage, "reranker": rk or "none", "system": system})

            agg_rows.append(agg)
            diag_rows.append(diag)
            per_query_by_system[system] = per_query
            checkpoint.put(key, {"aggregate": agg, "diagnostics": diag, "per_query": per_query})

            print(
                f"  {system:34s} nDCG@{cfg.eval_k}={agg[f'ndcg@{cfg.eval_k}']:.4f}  "
                f"R@100={agg.get('recall@100', float('nan')):.4f}  "
                f"fallback_fire={diag['fallback_fire_rate']:.2f}"
            )

    # Compare everything against the strongest standard baseline rather than the weakest.
    # The CIKM paper compared against Hybrid_Naive, which lacked the reranker its own
    # system had; that is the comparison-fairness objection in one line.
    reference = "dense+ms-marco" if "dense+ms-marco" in per_query_by_system else "dense"
    sig_rows = []
    if reference in per_query_by_system:
        sig_rows = compare_systems(
            per_query_by_system, metric=f"ndcg@{cfg.eval_k}", reference=reference
        )
        for r in sig_rows:
            r["dataset"] = dataset

    for row in agg_rows:
        row["size_report"] = str(size_report)
    return agg_rows, diag_rows, sig_rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datasets", nargs="+", default=["scifact", "nfcorpus"])
    ap.add_argument("--all", action="store_true", help="run every dataset in config.BEIR_DATASETS")
    ap.add_argument("--first-stages", nargs="+", default=FIRST_STAGES, choices=FIRST_STAGES)
    ap.add_argument("--rerankers", nargs="+", default=["none", "ms-marco"])
    ap.add_argument("--encoder", default="minilm")
    ap.add_argument("--rerank-depth", type=int, default=10, help="the number the CIKM code hardcoded")
    ap.add_argument("--first-stage-depth", type=int, default=100)
    ap.add_argument("--query-limit", type=int, default=None)
    ap.add_argument("--tag", default="a1_beir_full_corpus")
    args = ap.parse_args()

    set_all_seeds()
    datasets = list(BEIR_DATASETS) if args.all else args.datasets
    rerankers = [None if r == "none" else r for r in args.rerankers]

    cfg = RetrievalConfig(
        encoder_key=args.encoder,
        rerank_depth=args.rerank_depth,
        first_stage_depth=args.first_stage_depth,
    )
    checkpoint = Checkpoint(args.tag)

    all_agg, all_diag, all_sig = [], [], []
    for ds in datasets:
        try:
            agg, diag, sig = run_dataset(ds, cfg, args.first_stages, rerankers, checkpoint, args.query_limit)
        except Exception as exc:  # noqa: BLE001
            print(f"[error] {ds} failed: {type(exc).__name__}: {exc}")
            continue
        all_agg.extend(agg)
        all_diag.extend(diag)
        all_sig.extend(sig)

    if not all_agg:
        print("[a1] nothing completed")
        return

    agg_df = pd.DataFrame(all_agg)
    write_result(
        args.tag,
        agg_df,
        config={
            "retrieval": cfg.to_dict(),
            "datasets": datasets,
            "first_stages": args.first_stages,
            "rerankers": args.rerankers,
            "note": (
                "Full-corpus retrieval. No per-query candidate pools. Every first stage "
                "is evaluated with and without each reranker so the reranker's "
                "contribution is separable from the fusion strategy's."
            ),
        },
    )
    if all_diag:
        write_result(f"{args.tag}__diagnostics", pd.DataFrame(all_diag))
    if all_sig:
        write_result(f"{args.tag}__significance", pd.DataFrame(all_sig))

    metric = f"ndcg@{cfg.eval_k}"
    if metric in agg_df:
        pivot = agg_df.pivot_table(index="system", columns="dataset", values=metric)
        pivot["mean"] = pivot.mean(axis=1)
        print("\n" + "=" * 78)
        print(f"{metric} by system and dataset (this is the new main table)")
        print("=" * 78)
        print(pivot.sort_values("mean", ascending=False).round(4).to_string())
        write_result(f"{args.tag}__pivot", pivot.reset_index())


if __name__ == "__main__":
    main()
