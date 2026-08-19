"""
benchmarks/retrieval_eval.py
-----------------------------
Main retrieval evaluation: CogniSync vs all 7 baselines.

Runs 5 independent trials (different random seeds) and reports:
  - Recall@1, Recall@3, Recall@5, Recall@10
  - MRR, MAP, NDCG@5, NDCG@10
  - Mean latency ± std (ms)
  - McNemar test p-values vs CogniSync

Corpus: 20newsgroups technical slice (2,000 docs) + CogniSync Benchmark sessions.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
import random
import sqlite3
import tracemalloc
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

from benchmarks.config import (
    SEEDS, DEFAULT_TOP_K, TOP_K_VALUES, EMBEDDING_MODEL, EMBEDDING_DIM,
    BENCHMARK_JSON, RESULTS_DIR, LOGS_DIR,
)
from evaluation.metrics import full_metric_suite, summarise
from evaluation.statistical_tests import run_all_tests, aggregate_trials
from baselines.vanilla_rag import VanillaRAG
from baselines.memgpt_approx import MemGPTApprox
from baselines.memorybank_approx import MemoryBankApprox
from baselines.amem_approx import AMEMApprox
from baselines.langchain_retrieval import LangChainMMRRetrieval
from baselines.llamaindex_retrieval import LlamaIndexRetrieval
from baselines.pinecone_simulated import PineconeSimulated


# ─────────────────────────────────────────────────────────
# CogniSync Hybrid Retriever
# ─────────────────────────────────────────────────────────

class CogniSyncHybrid:
    """
    CogniSync: FAISS (semantic) ∪ SQLite FTS5 (lexical) union retrieval.
    This is OUR SYSTEM being evaluated.
    """
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index: faiss.IndexFlatIP = None
        self.doc_ids: list = []
        self.db = None
        self.cursor = None

    def build(self, docs: list, doc_ids: list, batch_size: int = 64) -> float:
        self.doc_ids = doc_ids
        t0 = time.perf_counter()

        # FAISS
        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
        self._embs = embs

        # SQLite FTS5
        self.db = sqlite3.connect(":memory:")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE VIRTUAL TABLE fts USING fts5(id, text);")
        self.cursor.executemany(
            "INSERT INTO fts (id, text) VALUES (?, ?)",
            [(did, doc) for did, doc in zip(doc_ids, docs)],
        )
        self.db.commit()
        return time.perf_counter() - t0

    def retrieve(self, query: str, top_k: int = DEFAULT_TOP_K):
        t0 = time.perf_counter()

        # FTS5
        fts_hits = set()
        try:
            safe_query = query.replace('"', '""')
            self.cursor.execute(
                "SELECT id FROM fts WHERE text MATCH ? LIMIT ?", (safe_query, top_k)
            )
            fts_hits = {row[0] for row in self.cursor.fetchall()}
        except sqlite3.OperationalError:
            pass

        # FAISS
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = self.index.search(q_emb, top_k)
        faiss_hits = {self.doc_ids[i] for i in I[0] if i >= 0}

        # Union
        union = list(fts_hits | faiss_hits)[:top_k]
        # Pad with FAISS results if union is short
        if len(union) < top_k:
            for i in I[0]:
                if i >= 0 and self.doc_ids[i] not in union:
                    union.append(self.doc_ids[i])
                if len(union) >= top_k:
                    break

        latency_ms = (time.perf_counter() - t0) * 1000
        return union[:top_k], latency_ms

    def batch_retrieve(self, queries: list, top_k: int = DEFAULT_TOP_K):
        all_ids, all_lat = [], []
        for q in queries:
            ids, lat = self.retrieve(q, top_k)
            all_ids.append(ids)
            all_lat.append(lat)
        return all_ids, all_lat


# ─────────────────────────────────────────────────────────
# Corpus builders
# ─────────────────────────────────────────────────────────

def load_newsgroups_corpus(n_docs: int = 2000, seed: int = 42):
    """Load 20newsgroups technical slice. Returns (docs, doc_ids)."""
    from sklearn.datasets import fetch_20newsgroups
    cats = ["comp.sys.mac.hardware", "comp.windows.x", "sci.electronics", "sci.crypt"]
    ng = fetch_20newsgroups(subset="train", categories=cats)
    rng = random.Random(seed)
    indices = rng.sample(range(len(ng.data)), min(n_docs, len(ng.data)))
    docs = [ng.data[i] for i in indices]
    ids  = [f"ng_{i}" for i in indices]
    return docs, ids


def load_benchmark_corpus():
    """Load CogniSync Benchmark sessions as corpus. Returns (docs, doc_ids, queries, gt)."""
    if not BENCHMARK_JSON.exists():
        raise FileNotFoundError(
            f"Benchmark dataset not found at {BENCHMARK_JSON}. "
            "Run data/generate_benchmark_dataset.py first."
        )
    with open(BENCHMARK_JSON, encoding="utf-8") as f:
        dataset = json.load(f)
    docs, ids = [], []
    for s in dataset["sessions"]:
        docs.append(s["content"])
        ids.append(s["chunk_ids"][0])   # one chunk per session for eval
    queries = [q["query"] for q in dataset["eval_queries"]]
    gt      = [q["ground_truth_chunk_ids"] for q in dataset["eval_queries"]]
    return docs, ids, queries, gt


# ─────────────────────────────────────────────────────────
# Query / ground-truth generation from newsgroups corpus
# ─────────────────────────────────────────────────────────

def make_newsgroups_eval_pairs(docs, doc_ids, n_queries=150, seed=42):
    """
    Generate evaluation (query, ground_truth_id) pairs from newsgroups docs.
    Creates both fuzzy (keyword) and semantic (sentence) queries.
    """
    rng = random.Random(seed)
    fuzzy_queries, semantic_queries, gt_ids_list = [], [], []
    candidates = [(i, d) for i, d in zip(doc_ids, docs) if len(d.split()) > 20]
    sampled = rng.sample(candidates, min(n_queries, len(candidates)))
    for doc_id, doc in sampled:
        words = doc.split()
        fuzzy_queries.append(" ".join(rng.sample(words[:50], min(4, len(words[:50])))))
        semantic_queries.append(" ".join(words[5:15]))
        gt_ids_list.append([doc_id])
    return fuzzy_queries, semantic_queries, gt_ids_list


# ─────────────────────────────────────────────────────────
# Run one trial
# ─────────────────────────────────────────────────────────

SYSTEMS = {
    "Vanilla RAG":         VanillaRAG,
    "MemGPT (approx)":    MemGPTApprox,
    "MemoryBank (approx)":MemoryBankApprox,
    "A-MEM (approx)":     AMEMApprox,
    "LangChain MMR":      LangChainMMRRetrieval,
    "LlamaIndex":         LlamaIndexRetrieval,
    "Pinecone (sim)":     PineconeSimulated,
    "CogniSync (Hybrid)": CogniSyncHybrid,
}


def run_trial(seed: int, docs: list, doc_ids: list, queries: list, gt: list, top_k: int = 5):
    """Run one trial for all systems. Returns results dict keyed by system name."""
    print(f"  [Seed {seed}] Building indexes for {len(docs)} docs, {len(queries)} queries...")
    trial_results = {}

    for name, Cls in SYSTEMS.items():
        system = Cls()
        build_time = system.build(docs, doc_ids)

        # Use no_sleep variant for Pinecone to avoid actual blocking in batch
        if isinstance(system, PineconeSimulated):
            all_ids, all_lat = [], []
            for q in queries:
                ids_, lat_ = system.retrieve_no_sleep(q, top_k)
                all_ids.append(ids_)
                all_lat.append(lat_)
        else:
            all_ids, all_lat = system.batch_retrieve(queries, top_k)

        metrics = full_metric_suite(all_ids, gt, latencies_ms=all_lat)
        metrics["build_time_s"] = build_time
        # Store per-query hit vectors for McNemar later
        metrics["_hits"] = [
            int(bool(set(r[:top_k]) & set(g)))
            for r, g in zip(all_ids, gt)
        ]
        trial_results[name] = metrics
        print(f"    {name:25s} Recall@5={metrics['recall@5']:.4f}  lat={metrics['latency']['mean']:.2f}ms")

    return trial_results


# ─────────────────────────────────────────────────────────
# Main evaluation
# ─────────────────────────────────────────────────────────

def run_retrieval_evaluation(n_docs: int = 2000, n_queries: int = 150, top_k: int = 5):
    """
    Full retrieval evaluation across all seeds.
    Returns a results dict and saves JSON + CSV.
    """
    print("=" * 60)
    print(" CogniSync Retrieval Evaluation — All Baselines")
    print("=" * 60)

    # Load corpora
    ng_docs, ng_ids = load_newsgroups_corpus(n_docs)
    try:
        bm_docs, bm_ids, bm_queries, bm_gt = load_benchmark_corpus()
    except FileNotFoundError as e:
        print(f"  Warning: {e}\n  Using newsgroups-only evaluation.")
        bm_docs = bm_ids = bm_queries = bm_gt = None

    # Combine corpora
    docs    = ng_docs + (bm_docs if bm_docs else [])
    doc_ids = ng_ids  + (bm_ids  if bm_ids  else [])

    all_system_scores = {name: [] for name in SYSTEMS}   # per-trial recall@5 lists
    all_trial_results = []

    for seed in SEEDS:
        rng_seed = seed
        # Generate newsgroups eval pairs
        fuzzy_q, semantic_q, ng_gt = make_newsgroups_eval_pairs(
            ng_docs, ng_ids, n_queries=n_queries // 2, seed=seed
        )
        # Combine with benchmark queries if available
        if bm_queries:
            queries = fuzzy_q + semantic_q + bm_queries[:n_queries // 2]
            gt_all  = ng_gt + ng_gt + bm_gt[:n_queries // 2]      # align lengths
        else:
            queries = fuzzy_q + semantic_q
            gt_all  = ng_gt  + ng_gt

        trial = run_trial(seed, docs, doc_ids, queries, gt_all, top_k)
        all_trial_results.append(trial)
        for name in SYSTEMS:
            all_system_scores[name].append(trial[name]["recall@5"])

    # Aggregate across trials
    print("\n" + "=" * 60)
    print(" Aggregated Results (5 trials)")
    print("=" * 60)
    aggregated = {}
    for name in SYSTEMS:
        per_trial = [t[name]["recall@5"] for t in all_trial_results]
        agg = aggregate_trials([[s] for s in per_trial])   # one score per trial
        aggregated[name] = {
            "recall@5_mean": agg["mean"],
            "recall@5_std":  agg["std"],
            "recall@5_ci95": [agg["ci_95_lower"], agg["ci_95_upper"]],
            "latency_mean_ms": np.mean([t[name]["latency"]["mean"] for t in all_trial_results]),
            "latency_std_ms":  np.std( [t[name]["latency"]["mean"] for t in all_trial_results]),
        }
        print(f"  {name:25s} Recall@5={agg['mean']:.4f} ± {agg['std']:.4f}")

    # Statistical tests: each baseline vs CogniSync
    cognisync_hits = [h for trial in all_trial_results for h in trial["CogniSync (Hybrid)"]["_hits"]]
    stat_tests = {}
    for name in SYSTEMS:
        if name == "CogniSync (Hybrid)":
            continue
        baseline_hits = [h for trial in all_trial_results for h in trial[name]["_hits"]]
        stat_tests[name] = run_all_tests(
            cognisync_hits, baseline_hits,
            label_a="CogniSync", label_b=name,
        )

    output = {
        "experiment": "retrieval_eval",
        "n_docs": len(docs),
        "n_queries_per_trial": len(queries),
        "top_k": top_k,
        "seeds": SEEDS,
        "aggregated": aggregated,
        "statistical_tests": stat_tests,
        "all_trial_results": [
            {name: {k: v for k, v in m.items() if not k.startswith("_")} for name, m in t.items()}
            for t in all_trial_results
        ],
    }

    out_path = RESULTS_DIR / "retrieval_eval.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\n✅ Results saved to {out_path}")

    # Also save a flat CSV
    import csv
    csv_path = RESULTS_DIR / "retrieval_eval.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "System", "Recall@5_Mean", "Recall@5_Std", "CI95_Low", "CI95_High",
            "Latency_Mean_ms", "Latency_Std_ms",
        ])
        writer.writeheader()
        for name, agg in aggregated.items():
            writer.writerow({
                "System":           name,
                "Recall@5_Mean":    round(agg["recall@5_mean"], 4),
                "Recall@5_Std":     round(agg["recall@5_std"],  4),
                "CI95_Low":         round(agg["recall@5_ci95"][0], 4),
                "CI95_High":        round(agg["recall@5_ci95"][1], 4),
                "Latency_Mean_ms":  round(agg["latency_mean_ms"],  3),
                "Latency_Std_ms":   round(agg["latency_std_ms"],   3),
            })
    print(f"✅ CSV saved to {csv_path}")
    return output


if __name__ == "__main__":
    run_retrieval_evaluation(n_docs=2000, n_queries=150, top_k=5)
