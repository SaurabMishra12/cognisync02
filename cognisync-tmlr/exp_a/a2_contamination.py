"""A2: is the reported gain a benchmark-membership artifact?

Three measurements, cheap, and between them they decide whether the CIKM headline number
means anything.

C1. Train vs dev on one index
    Build the 100K MS MARCO index once. Evaluate 500 train-split queries and 500
    dev-split queries on it, identically. `all-MiniLM-L6-v2` was fit on 9,144,553 MS MARCO
    triplets drawn from the train split, so train-split queries are effectively seen data.
    The CIKM full-corpus experiment used the train split and reported MRR@10 = 0.92. If
    dev comes in far lower on the same index with the same code, the 0.92 was measuring
    memorisation.

C2. Reranker provenance
    The CIKM gain over Dense is +9.1 pp on MS MARCO and under 0.5 pp everywhere else. The
    reranker is `cross-encoder/ms-marco-MiniLM-L-6-v2`, an MS MARCO reranker by
    construction. Swap in `bge-reranker-base` and see whether the concentration survives.

C3. In-mixture vs out-of-mixture
    Group the A1 results by whether the dataset appears in the encoder's published
    training data and report the mean delta per group.

Usage
-----
    python -m exp_a.a2_contamination --contrast train-vs-dev
    python -m exp_a.a2_contamination --contrast reranker-provenance
    python -m exp_a.a2_contamination --contrast mixture-membership --a1-results cognisync_out/results/a1_beir_full_corpus.csv
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

from common.config import ENCODER_TRAINING_MEMBERSHIP, RetrievalConfig, set_all_seeds
from common.data import (
    build_index_with_guaranteed_positives,
    load_msmarco_passage_corpus,
    load_msmarco_queries,
)
from common.io_utils import write_result
from common.metrics import evaluate_run, paired_bootstrap
from common.retrieval import BM25Index, DenseIndex, HybridRetriever, Reranker


def contrast_train_vs_dev(cfg: RetrievalConfig, n_corpus: int, n_queries: int, use_reranker: bool) -> pd.DataFrame:
    print("Loading MS MARCO passage corpus...")
    base_ids, base_texts = load_msmarco_passage_corpus(n_passages=n_corpus)

    print("Loading queries from both splits...")
    splits = {s: load_msmarco_queries(s, n_queries=n_queries) for s in ("train", "dev")}
    for s, recs in splits.items():
        print(f"  {s}: {len(recs)} queries with positives")

    # One index containing the positives of both splits, so the two conditions differ only
    # in which queries are asked. This is the whole point: same corpus, same code, same
    # models, different query provenance.
    all_records = splits["train"] + splits["dev"]
    doc_ids, doc_texts, qrels_all = build_index_with_guaranteed_positives(base_ids, base_texts, all_records)
    print(f"  corpus after appending positives: {len(doc_ids)}")

    dense = DenseIndex(cfg.encoder_key, batch_size=cfg.batch_size).build(
        doc_ids, doc_texts, cache_tag=f"msmarco_contam_{n_corpus}"
    )
    lexical = BM25Index().build(doc_ids, doc_texts)
    retriever = HybridRetriever(cfg, dense, lexical)
    reranker = Reranker(cfg.reranker_key) if use_reranker else None

    corpus_map = dict(zip(doc_ids, doc_texts))
    rows: List[dict] = []
    per_query_store: Dict[str, Dict[str, float]] = {}

    for split, records in splits.items():
        for strategy in ("dense", "fixed", "learned+fallback"):
            run = {}
            for rec in tqdm(records, desc=f"{split}/{strategy}", leave=False):
                ranked = retriever.retrieve(rec["query"], strategy=strategy, depth=cfg.first_stage_depth)
                if reranker is not None:
                    cands = [(d, corpus_map[d], s) for d, s in ranked]
                    ranked = reranker.rerank(rec["query"], cands, depth=cfg.rerank_depth)
                run[rec["query_id"]] = ranked

            qrels = {r["query_id"]: qrels_all[r["query_id"]] for r in records if r["query_id"] in qrels_all}
            agg, per_query = evaluate_run(run, qrels, eval_k=10, recall_ks=(1, 10, 100))
            agg.update({"split": split, "strategy": strategy, "reranker": cfg.reranker_key if use_reranker else "none"})
            rows.append(agg)
            per_query_store[f"{split}/{strategy}"] = {q: v["mrr@10"] for q, v in per_query.items()}
            print(f"  {split:5s} {strategy:18s} MRR@10={agg['mrr@10']:.4f}  nDCG@10={agg['ndcg@10']:.4f}")

    df = pd.DataFrame(rows)

    # The contamination gap: same strategy, different split. Queries differ so this is an
    # unpaired comparison; report the raw gap and a bootstrap on the difference of means.
    gaps = []
    for strategy in df["strategy"].unique():
        tr = df[(df.split == "train") & (df.strategy == strategy)]["mrr@10"].iloc[0]
        dv = df[(df.split == "dev") & (df.strategy == strategy)]["mrr@10"].iloc[0]
        tr_vals = list(per_query_store[f"train/{strategy}"].values())
        dv_vals = list(per_query_store[f"dev/{strategy}"].values())
        n = min(len(tr_vals), len(dv_vals))
        boot = paired_bootstrap(tr_vals[:n], dv_vals[:n]) if n else {}
        gaps.append(
            {
                "strategy": strategy,
                "mrr10_train": tr,
                "mrr10_dev": dv,
                "contamination_gap_pp": (tr - dv) * 100,
                "relative_inflation": (tr / dv) if dv > 0 else float("nan"),
                "bootstrap_ci_low_pp": boot.get("ci_low", float("nan")) * 100,
                "bootstrap_ci_high_pp": boot.get("ci_high", float("nan")) * 100,
                "note": "unpaired across splits; CI is on the difference of matched-size samples",
            }
        )

    gap_df = pd.DataFrame(gaps)
    print("\nContamination gap (train minus dev, same index and code):")
    print(gap_df.round(4).to_string(index=False))

    write_result(
        "a2_contamination_train_vs_dev",
        df,
        config={
            "retrieval": cfg.to_dict(),
            "n_corpus": n_corpus,
            "n_queries": n_queries,
            "encoder_training_note": (
                "all-MiniLM-L6-v2 was trained on 9,144,553 MS MARCO triplets from the "
                "train split (model card, Training Data table). Train-split evaluation "
                "queries are therefore seen data for the encoder."
            ),
            "cikm_protocol_note": (
                "calc_full_corpus_significance.py used Tevatron/msmarco-passage split='train' "
                "with alpha=0.6 fixed and no reranker, and reported MRR@10=0.9216."
            ),
        },
    )
    write_result("a2_contamination_gap", gap_df)
    return gap_df


def contrast_reranker_provenance(cfg: RetrievalConfig, n_corpus: int, n_queries: int) -> pd.DataFrame:
    """Does the MS MARCO gain survive a reranker that was not trained on MS MARCO?"""
    base_ids, base_texts = load_msmarco_passage_corpus(n_passages=n_corpus)
    records = load_msmarco_queries("dev", n_queries=n_queries)
    doc_ids, doc_texts, qrels = build_index_with_guaranteed_positives(base_ids, base_texts, records)
    corpus_map = dict(zip(doc_ids, doc_texts))

    dense = DenseIndex(cfg.encoder_key, batch_size=cfg.batch_size).build(
        doc_ids, doc_texts, cache_tag=f"msmarco_prov_{n_corpus}"
    )
    lexical = BM25Index().build(doc_ids, doc_texts)
    retriever = HybridRetriever(cfg, dense, lexical)

    rows, per_query_by_system = [], {}
    for reranker_key in (None, "ms-marco", "bge-reranker"):
        reranker = Reranker(reranker_key) if reranker_key else None
        for strategy in ("dense", "learned+fallback"):
            system = f"{strategy}+{reranker_key or 'none'}"
            run = {}
            for rec in tqdm(records, desc=system, leave=False):
                ranked = retriever.retrieve(rec["query"], strategy=strategy, depth=cfg.first_stage_depth)
                if reranker is not None:
                    cands = [(d, corpus_map[d], s) for d, s in ranked]
                    ranked = reranker.rerank(rec["query"], cands, depth=cfg.rerank_depth)
                run[rec["query_id"]] = ranked
            agg, per_query = evaluate_run(run, qrels, eval_k=10)
            agg.update({"system": system, "strategy": strategy, "reranker": reranker_key or "none"})
            rows.append(agg)
            per_query_by_system[system] = per_query
            print(f"  {system:30s} nDCG@10={agg['ndcg@10']:.4f}  MRR@10={agg['mrr@10']:.4f}")

    df = pd.DataFrame(rows)

    # The claim under test: "CogniSync beats Dense" should hold under both rerankers if it
    # is about the fusion mechanism, and only under the MS MARCO reranker if it is about
    # reranker provenance.
    deltas = []
    for reranker_key in ("none", "ms-marco", "bge-reranker"):
        a = f"learned+fallback+{reranker_key}"
        b = f"dense+{reranker_key}"
        if a in per_query_by_system and b in per_query_by_system:
            shared = sorted(set(per_query_by_system[a]) & set(per_query_by_system[b]))
            boot = paired_bootstrap(
                [per_query_by_system[a][q]["ndcg@10"] for q in shared],
                [per_query_by_system[b][q]["ndcg@10"] for q in shared],
            )
            deltas.append(
                {
                    "reranker": reranker_key,
                    "delta_ndcg10_pp": boot["delta"] * 100,
                    "ci_low_pp": boot["ci_low"] * 100,
                    "ci_high_pp": boot["ci_high"] * 100,
                    "p_bootstrap": boot["p_value"],
                    "n_queries": boot["n"],
                }
            )

    delta_df = pd.DataFrame(deltas)
    print("\nCogniSync minus Dense, by reranker provenance:")
    print(delta_df.round(4).to_string(index=False))

    write_result("a2_reranker_provenance", df, config={"retrieval": cfg.to_dict(), "n_queries": n_queries})
    write_result("a2_reranker_provenance_delta", delta_df)
    return delta_df


def contrast_mixture_membership(a1_results: Path, eval_k: int = 10) -> pd.DataFrame:
    """Group A1 results by encoder-training membership and report the mean delta."""
    if not a1_results.exists():
        raise FileNotFoundError(f"run a1 first; expected {a1_results}")
    df = pd.read_csv(a1_results)
    metric = f"ndcg@{eval_k}"

    rows = []
    for dataset, group in df.groupby("dataset"):
        membership = ENCODER_TRAINING_MEMBERSHIP.get(dataset, {"in_mixture": None, "pairs": 0})
        def best(prefix: str) -> float:
            sub = group[group["system"].str.startswith(prefix)]
            return float(sub[metric].max()) if len(sub) else float("nan")

        cognisync = best("learned+fallback")
        dense_only = best("dense")
        rows.append(
            {
                "dataset": dataset,
                "in_encoder_training_mixture": membership["in_mixture"],
                "training_pairs": membership.get("pairs", 0),
                "mixture_entry": membership.get("entry"),
                f"cognisync_{metric}": cognisync,
                f"dense_{metric}": dense_only,
                "delta_pp": (cognisync - dense_only) * 100,
            }
        )

    out = pd.DataFrame(rows)
    summary = (
        out.groupby("in_encoder_training_mixture")["delta_pp"]
        .agg(["mean", "std", "count"])
        .reset_index()
        .rename(columns={"mean": "mean_delta_pp", "std": "std_delta_pp", "count": "n_datasets"})
    )
    print("\nGain over Dense, grouped by encoder training-set membership:")
    print(out.round(4).to_string(index=False))
    print()
    print(summary.round(4).to_string(index=False))

    write_result("a2_mixture_membership", out)
    write_result("a2_mixture_membership_summary", summary)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--contrast",
        choices=["train-vs-dev", "reranker-provenance", "mixture-membership", "all"],
        default="train-vs-dev",
    )
    ap.add_argument("--n-corpus", type=int, default=100_000)
    ap.add_argument("--n-queries", type=int, default=500)
    ap.add_argument("--with-reranker", action="store_true")
    ap.add_argument("--a1-results", type=Path, default=Path("cognisync_out/results/a1_beir_full_corpus.csv"))
    args = ap.parse_args()

    set_all_seeds()
    cfg = RetrievalConfig()

    if args.contrast in ("train-vs-dev", "all"):
        contrast_train_vs_dev(cfg, args.n_corpus, args.n_queries, args.with_reranker)
    if args.contrast in ("reranker-provenance", "all"):
        contrast_reranker_provenance(cfg, args.n_corpus, args.n_queries)
    if args.contrast in ("mixture-membership", "all"):
        contrast_mixture_membership(args.a1_results)


if __name__ == "__main__":
    main()
