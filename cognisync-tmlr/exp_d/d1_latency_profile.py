"""D1: what does the pipeline actually cost, on text that exists?

The CIKM latency number came from `latency_amortized.py`, which builds its corpus like
this:

    words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", ...]
    documents = [" ".join(np.random.choice(words, size=...)) for _ in range(N_DOCS)]

Nineteen words sampled uniformly. BM25 posting lists, tokenizer behaviour and cross-encoder
cost all depend on realistic term distributions, so that number does not transfer. The
adversarial filter, whose cost is the paper's whole subject, was not in the timed loop at
all.

This measures per stage, on real corpora, at three scales, with the filter included, on
both GPU and CPU. The CPU numbers are the ones that matter for the local-first claim:
"8-24 GB RAM" describes a machine without a T4 in it.

Usage
-----
    python -m exp_d.d1_latency_profile --sizes 10000 100000 --device cuda
    python -m exp_d.d1_latency_profile --sizes 10000 --device cpu
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DefenseConfig, RetrievalConfig, set_all_seeds
from common.data import load_beir, load_msmarco_passage_corpus
from common.io_utils import write_result
from common.retrieval import BM25Index, DenseIndex, HybridRetriever, Reranker

from exp_b.defenses import MultiSignalFilter, sample_holdout_clean_corpus


def percentiles(values: Sequence[float]) -> Dict[str, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"mean": 0.0, "p50": 0.0, "p95": 0.0, "p99": 0.0, "max": 0.0}
    return {
        "mean": float(arr.mean()),
        "p50": float(np.percentile(arr, 50)),
        "p95": float(np.percentile(arr, 95)),
        "p99": float(np.percentile(arr, 99)),
        "max": float(arr.max()),
    }


def gather_corpus(size: int, source: str) -> tuple[List[str], List[str], List[str]]:
    """Real passages, plus real queries to run against them."""
    if source == "msmarco":
        ids, texts = load_msmarco_passage_corpus(n_passages=size)
        queries = [
            "how long does it take for a wound to heal",
            "what is the average temperature in death valley",
            "symptoms of vitamin d deficiency in adults",
            "difference between llc and s corporation",
            "how to calculate compound interest monthly",
        ]
        return ids, texts, queries

    corpus, queries_map, _ = load_beir(source)
    ids = list(corpus)[:size]
    return ids, [corpus[d] for d in ids], list(queries_map.values())[:200]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sizes", nargs="+", type=int, default=[10_000, 100_000])
    ap.add_argument("--source", default="msmarco", help="'msmarco' or a BEIR dataset name")
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    ap.add_argument("--n-queries", type=int, default=300)
    ap.add_argument("--rerank-depths", nargs="+", type=int, default=[10, 50])
    ap.add_argument("--warmup", type=int, default=10)
    ap.add_argument("--tag", default="d1_latency_profile")
    args = ap.parse_args()

    set_all_seeds()
    rcfg = RetrievalConfig()
    dcfg = DefenseConfig()

    rows, stage_rows = [], []

    for size in args.sizes:
        print(f"\n{'=' * 78}\ncorpus size {size:,} on {args.device}\n{'=' * 78}")
        ids, texts, base_queries = gather_corpus(size, args.source)
        queries = (base_queries * ((args.n_queries // max(1, len(base_queries))) + 1))[: args.n_queries]
        corpus_map = dict(zip(ids, texts))

        t0 = time.perf_counter()
        dense = DenseIndex(rcfg.encoder_key, batch_size=rcfg.batch_size, device=args.device).build(
            ids, texts, cache_tag=f"{args.source}_{size}"
        )
        dense_build_s = time.perf_counter() - t0

        t0 = time.perf_counter()
        lexical = BM25Index().build(ids, texts)
        bm25_build_s = time.perf_counter() - t0
        print(f"  index build: dense {dense_build_s:.1f}s, bm25 {bm25_build_s:.1f}s (backend {lexical.backend})")

        retriever = HybridRetriever(rcfg, dense, lexical)
        reranker = Reranker(rcfg.reranker_key)

        calib = sample_holdout_clean_corpus(corpus_map, exclude_ids=[], n=1000)
        flt = MultiSignalFilter(dense.model, dcfg).fit(
            calib[:250], centroid_docs=calib, centroid_source="holdout"
        )

        for _ in range(args.warmup):
            q = queries[0]
            r = retriever.retrieve(q, strategy="learned+fallback", depth=rcfg.first_stage_depth, record=False)
            reranker.rerank(q, [(d, corpus_map[d], s) for d, s in r], depth=10)
            flt.decide(q, [corpus_map[d] for d, _ in r[:10]])

        for depth in args.rerank_depths:
            stages: Dict[str, List[float]] = {k: [] for k in ("dense", "bm25", "fusion", "rerank", "filter", "total")}

            for q in tqdm(queries, desc=f"size={size} depth={depth}", leave=False):
                t_total = time.perf_counter()

                t0 = time.perf_counter()
                d_scores, _ = retriever._dense_candidates(q, rcfg.first_stage_depth)
                stages["dense"].append((time.perf_counter() - t0) * 1000)

                t0 = time.perf_counter()
                retriever._lexical_candidates(q, rcfg.first_stage_depth)
                stages["bm25"].append((time.perf_counter() - t0) * 1000)

                t0 = time.perf_counter()
                ranked = retriever.retrieve(q, strategy="learned+fallback", depth=rcfg.first_stage_depth, record=False)
                stages["fusion"].append((time.perf_counter() - t0) * 1000 - stages["dense"][-1] - stages["bm25"][-1])

                t0 = time.perf_counter()
                reranked = reranker.rerank(q, [(d, corpus_map[d], s) for d, s in ranked], depth=depth)
                stages["rerank"].append((time.perf_counter() - t0) * 1000)

                # The stage the CIKM measurement omitted entirely.
                t0 = time.perf_counter()
                flt.decide(q, [corpus_map[d] for d, _ in reranked[:10] if d in corpus_map])
                stages["filter"].append((time.perf_counter() - t0) * 1000)

                stages["total"].append((time.perf_counter() - t_total) * 1000)

            for stage, values in stages.items():
                stage_rows.append(
                    {
                        "corpus_size": size,
                        "device": args.device,
                        "rerank_depth": depth,
                        "stage": stage,
                        "n_queries": len(values),
                        **percentiles(values),
                    }
                )

            total = percentiles(stages["total"])
            rows.append(
                {
                    "corpus_size": size,
                    "device": args.device,
                    "rerank_depth": depth,
                    "source": args.source,
                    "dense_index_build_s": dense_build_s,
                    "bm25_index_build_s": bm25_build_s,
                    "bm25_backend": lexical.backend,
                    "n_queries": len(queries),
                    **{f"total_{k}": v for k, v in total.items()},
                    "filter_mean_ms": percentiles(stages["filter"])["mean"],
                    "filter_share_of_total": (
                        percentiles(stages["filter"])["mean"] / total["mean"] if total["mean"] else 0.0
                    ),
                }
            )
            print(
                f"  depth={depth:3d}  total mean {total['mean']:7.1f} ms  "
                f"p95 {total['p95']:7.1f}  p99 {total['p99']:7.1f}  "
                f"filter {percentiles(stages['filter'])['mean']:.1f} ms"
            )

    df = pd.DataFrame(rows)
    stage_df = pd.DataFrame(stage_rows)

    write_result(
        args.tag,
        df,
        per_query=stage_df,
        config={
            "retrieval": rcfg.to_dict(),
            "defense": dcfg.to_dict(),
            "sizes": args.sizes,
            "device": args.device,
            "source": args.source,
            "replaces": (
                "latency_amortized.py, which timed a corpus of documents sampled uniformly "
                "from a 19-word vocabulary and excluded the adversarial filter from the "
                "measured loop."
            ),
        },
    )

    print("\n" + "=" * 92)
    print("Per-stage latency (ms)")
    print("=" * 92)
    pivot = stage_df.pivot_table(index=["corpus_size", "rerank_depth"], columns="stage", values="mean")
    print(pivot.round(2).to_string())


if __name__ == "__main__":
    main()
