"""A3: what is the learned-alpha mechanism actually doing?

The CIKM ablation (Table 5) reported Learned-Alpha Only at 0.4584 against Dense at
0.5450, then the full system at 0.6369 against Dense + Cross-Encoder at 0.6384, tied at
p = 1.0. A tie at p = 1.0 over 5,744 queries means the two systems produced identical
rankings on essentially every query. Reading the code explains why:

    if d_max > 0.85 or bm25_cv < 0.1:
        alpha = 1.0  # Force pure dense

That override is not described anywhere in the paper. When it fires, the Random Forest's
output is thrown away and the system is dense retrieval. This script measures how often
that happens and separates four things the CIKM ablation conflated:

    the Random Forest        vs   the override
    per-query alpha          vs   the best fixed alpha
    any alpha selector       vs   its oracle upper bound
    first-stage differences  vs   what the reranker erases

The oracle row is the one to look at first. It bounds every possible per-query alpha
selector, learned or not. If oracle alpha sits close to the best fixed alpha, then no
selector can help much on these datasets, and that is a finding.

Usage
-----
    python -m exp_a.a3_alpha_decomposition --datasets scifact nfcorpus fiqa
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import RetrievalConfig, set_all_seeds
from common.data import load_beir
from common.io_utils import write_result
from common.metrics import compare_systems, evaluate_run, ndcg_at_k
from common.retrieval import (
    AlphaPredictor,
    BM25Index,
    DenseIndex,
    HybridRetriever,
    Reranker,
    minmax,
    oracle_alpha_for_query,
    query_features,
    resolve_alpha,
)

VARIANTS = [
    ("dense", "alpha = 1"),
    ("lexical", "alpha = 0"),
    ("rrf", "rank fusion, k=60"),
    ("fixed", "alpha = 0.5"),
    ("best_fixed", "alpha = argmax over the grid, one value for the whole dataset"),
    ("learned", "Random Forest only, override disabled"),
    ("fallback", "alpha = 0.5 plus the dense-confidence override"),
    ("learned+fallback", "the CIKM system as shipped"),
    ("oracle", "per-query argmax with label access; upper bound on any selector"),
]


def collect_query_state(
    retriever: HybridRetriever,
    queries: Dict[str, str],
    qrels: Dict[str, Dict[str, int]],
    qids: List[str],
    cfg: RetrievalConfig,
    desc: str,
) -> List[dict]:
    """Precompute normalised score vectors once so every variant reranks the same union.

    Doing this once instead of per variant is what makes a nine-way decomposition
    affordable, and it also guarantees every variant sees exactly the same candidate set,
    which the CIKM ablation could not promise because each variant re-ran retrieval.
    """
    states = []
    for qid in tqdm(qids, desc=desc, leave=False):
        query = queries[qid]
        dense_scores, dense_raw_max = retriever._dense_candidates(query, cfg.first_stage_depth)
        lex_scores = retriever._lexical_candidates(query, cfg.first_stage_depth)
        union = sorted(set(dense_scores) | set(lex_scores))
        if len(union) < 2:
            continue
        d_vec = minmax(np.array([dense_scores.get(d, -1e9) for d in union], dtype=float))
        l_vec = minmax(np.array([lex_scores.get(d, 0.0) for d in union], dtype=float))
        oracle_a, oracle_score = oracle_alpha_for_query(
            d_vec, l_vec, union, qrels.get(qid, {}), steps=cfg.alpha_grid_steps, k=cfg.eval_k
        )
        states.append(
            {
                "qid": qid,
                "query": query,
                "doc_ids": union,
                "dense_norm": d_vec,
                "lex_norm": l_vec,
                "dense_raw_max": dense_raw_max,
                "features": query_features(query, d_vec, l_vec),
                "oracle_alpha": oracle_a,
                "oracle_ndcg": oracle_score,
            }
        )
    return states


def rank_with_alpha(state: dict, alpha: float) -> List[str]:
    fused = alpha * state["dense_norm"] + (1.0 - alpha) * state["lex_norm"]
    return [state["doc_ids"][i] for i in np.argsort(-fused)]


def find_best_fixed_alpha(states: List[dict], qrels: Dict[str, Dict[str, int]], cfg: RetrievalConfig) -> tuple[float, float]:
    """One alpha for the whole dataset, chosen with label access.

    This is the baseline a per-query selector has to beat to justify its existence, and
    the CIKM ablation never reported it.
    """
    best_alpha, best_mean = 0.5, -1.0
    for alpha in np.linspace(0.0, 1.0, cfg.alpha_grid_steps):
        scores = [ndcg_at_k(rank_with_alpha(s, alpha), qrels.get(s["qid"], {}), cfg.eval_k) for s in states]
        mean = float(np.mean(scores)) if scores else 0.0
        if mean > best_mean:
            best_alpha, best_mean = float(alpha), mean
    return best_alpha, best_mean


def run_dataset(dataset: str, cfg: RetrievalConfig, with_reranker: bool, query_limit: int | None) -> tuple[pd.DataFrame, pd.DataFrame]:
    print(f"\n{'=' * 78}\n{dataset}\n{'=' * 78}")
    corpus, queries, qrels = load_beir(dataset)
    doc_ids = list(corpus)
    doc_texts = [corpus[d] for d in doc_ids]

    qids = sorted(queries)
    rng = np.random.default_rng(42)
    rng.shuffle(qids)
    n_tune = min(cfg.alpha_tuning_queries, max(1, len(qids) // 5))
    tuning_qids, eval_qids = qids[:n_tune], qids[n_tune:]
    if query_limit:
        eval_qids = eval_qids[:query_limit]

    dense = DenseIndex(cfg.encoder_key, batch_size=cfg.batch_size).build(doc_ids, doc_texts, cache_tag=dataset)
    lexical = BM25Index().build(doc_ids, doc_texts)
    retriever = HybridRetriever(cfg, dense, lexical)

    tune_states = collect_query_state(retriever, queries, qrels, tuning_qids, cfg, "tuning")
    retriever.predictor = AlphaPredictor(cfg).fit(
        [s["features"] for s in tune_states], [s["oracle_alpha"] for s in tune_states]
    )
    importances = retriever.predictor.feature_importance()
    print(f"  RF feature importances: { {k: round(v, 3) for k, v in importances.items()} }")

    eval_states = collect_query_state(retriever, queries, qrels, eval_qids, cfg, "eval")
    best_fixed_alpha, _ = find_best_fixed_alpha(eval_states, qrels, cfg)
    print(f"  best fixed alpha for this dataset: {best_fixed_alpha:.2f}")

    reranker = Reranker(cfg.reranker_key) if with_reranker else None
    corpus_map = corpus

    rows, per_query_by_system, diag_rows = [], {}, []

    for variant, description in VARIANTS:
        run, alphas, predicted, fired, reasons, same_as_dense = {}, [], [], [], [], []

        for state in eval_states:
            dense_order = [state["doc_ids"][i] for i in np.argsort(-state["dense_norm"])]

            if variant == "best_fixed":
                alpha, pred, f, reason = best_fixed_alpha, best_fixed_alpha, False, ""
            elif variant == "rrf":
                alpha = pred = 0.5
                f, reason = False, ""
            else:
                alpha, pred, f, reason = resolve_alpha(
                    variant, cfg, state["features"], state["dense_raw_max"],
                    retriever.predictor, state["oracle_alpha"],
                )

            if variant == "rrf":
                d_rank = {d: i for i, d in enumerate(dense_order)}
                l_order = [state["doc_ids"][i] for i in np.argsort(-state["lex_norm"])]
                l_rank = {d: i for i, d in enumerate(l_order)}
                fused = {
                    d: 1.0 / (cfg.rrf_k + d_rank.get(d, 10**6) + 1) + 1.0 / (cfg.rrf_k + l_rank.get(d, 10**6) + 1)
                    for d in state["doc_ids"]
                }
                order = sorted(fused, key=lambda d: -fused[d])
                scored = [(d, fused[d]) for d in order]
            else:
                order = rank_with_alpha(state, alpha)
                scored = [(d, float(-i)) for i, d in enumerate(order)]

            if reranker is not None:
                cands = [(d, corpus_map[d], s) for d, s in scored]
                scored = reranker.rerank(state["query"], cands, depth=cfg.rerank_depth)
                order = [d for d, _ in scored]

            run[state["qid"]] = scored
            alphas.append(alpha)
            predicted.append(pred)
            fired.append(f)
            reasons.append(reason)
            top = min(10, len(dense_order))
            same_as_dense.append(order[:top] == dense_order[:top])

        agg, per_query = evaluate_run(run, qrels, eval_k=cfg.eval_k, recall_ks=cfg.recall_ks)
        system = f"{variant}+{cfg.reranker_key}" if reranker else variant
        agg.update({"dataset": dataset, "variant": variant, "system": system, "description": description})
        rows.append(agg)
        per_query_by_system[system] = per_query

        diag_rows.append(
            {
                "dataset": dataset,
                "variant": variant,
                "alpha_mean": float(np.mean(alphas)),
                "alpha_std": float(np.std(alphas)),
                "alpha_pred_mean": float(np.mean(predicted)),
                "frac_alpha_eq_1": float(np.mean([a >= 0.999 for a in alphas])),
                # The headline diagnostic: how often does the undisclosed override fire?
                "fallback_fire_rate": float(np.mean(fired)),
                "fire_reason_dmax_only": float(np.mean([r == "dmax" for r in reasons])),
                "fire_reason_cv_only": float(np.mean([r == "cv" for r in reasons])),
                "fire_reason_both": float(np.mean([r == "dmax+cv" for r in reasons])),
                # And the consequence: how often is the "hybrid" system just dense?
                "frac_top10_identical_to_dense": float(np.mean(same_as_dense)),
                "rf_importance_dense_cv": importances.get("dense_cv", float("nan")),
                "rf_importance_lex_cv": importances.get("lex_cv", float("nan")),
                "best_fixed_alpha": best_fixed_alpha,
            }
        )

        print(
            f"  {variant:18s} nDCG@{cfg.eval_k}={agg[f'ndcg@{cfg.eval_k}']:.4f}  "
            f"alpha={np.mean(alphas):.2f}  fire={np.mean(fired):.2f}  "
            f"=dense@10 {np.mean(same_as_dense):.2f}"
        )

    reference = f"dense+{cfg.reranker_key}" if reranker else "dense"
    sig = compare_systems(per_query_by_system, metric=f"ndcg@{cfg.eval_k}", reference=reference)
    for r in sig:
        r["dataset"] = dataset

    return pd.DataFrame(rows), pd.DataFrame(diag_rows), pd.DataFrame(sig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datasets", nargs="+", default=["scifact", "nfcorpus", "fiqa"])
    ap.add_argument("--with-reranker", action="store_true", help="also run every variant with the cross-encoder")
    ap.add_argument("--query-limit", type=int, default=None)
    args = ap.parse_args()

    set_all_seeds()
    cfg = RetrievalConfig()

    aggs, diags, sigs = [], [], []
    for ds in args.datasets:
        for with_rr in ([False, True] if args.with_reranker else [False]):
            try:
                a, d, s = run_dataset(ds, cfg, with_rr, args.query_limit)
            except Exception as exc:  # noqa: BLE001
                print(f"[error] {ds} (reranker={with_rr}) failed: {type(exc).__name__}: {exc}")
                continue
            aggs.append(a)
            diags.append(d)
            sigs.append(s)

    if not aggs:
        print("[a3] nothing completed")
        return

    agg_df = pd.concat(aggs, ignore_index=True)
    diag_df = pd.concat(diags, ignore_index=True)
    sig_df = pd.concat(sigs, ignore_index=True) if sigs else pd.DataFrame()

    write_result(
        "a3_alpha_decomposition",
        agg_df,
        config={
            "retrieval": cfg.to_dict(),
            "datasets": args.datasets,
            "variants": dict(VARIANTS),
            "note": (
                "The 'fallback' variant isolates the undisclosed override from "
                "CogniSync_v3_strong.ipynb cell 6 (d_max > 0.85 or bm25_cv < 0.1 -> alpha = 1). "
                "'oracle' bounds any per-query alpha selector. 'best_fixed' is the single "
                "dataset-level alpha a per-query selector has to beat."
            ),
        },
    )
    write_result("a3_alpha_diagnostics", diag_df)
    if len(sig_df):
        write_result("a3_alpha_significance", sig_df)

    metric = f"ndcg@{cfg.eval_k}"
    print("\n" + "=" * 78)
    print("Decomposition: mean " + metric + " across datasets")
    print("=" * 78)
    print(agg_df.groupby("variant")[metric].mean().sort_values(ascending=False).round(4).to_string())

    print("\nHow often does the undisclosed override fire, and does it matter?")
    cols = ["dataset", "variant", "fallback_fire_rate", "frac_alpha_eq_1", "frac_top10_identical_to_dense"]
    print(diag_df[diag_df.variant.isin(["learned", "fallback", "learned+fallback"])][cols].round(3).to_string(index=False))

    # The headroom question, stated as a number.
    if {"oracle", "best_fixed"}.issubset(set(agg_df["variant"])):
        oracle = agg_df[agg_df.variant == "oracle"][metric].mean()
        best_fixed = agg_df[agg_df.variant == "best_fixed"][metric].mean()
        shipped = agg_df[agg_df.variant == "learned+fallback"][metric].mean()
        print(
            f"\nHeadroom for any per-query alpha selector: "
            f"oracle {oracle:.4f} - best fixed {best_fixed:.4f} = {(oracle - best_fixed) * 100:.2f} pp. "
            f"The shipped selector captures "
            f"{((shipped - best_fixed) / (oracle - best_fixed) * 100) if oracle > best_fixed else float('nan'):.1f}% of it."
        )


if __name__ == "__main__":
    main()
