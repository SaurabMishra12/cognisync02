"""
benchmarks/ablation_study.py
-----------------------------
Systematic ablation over CogniSync configuration axes:

  - Retrieval mode : faiss_only | fts5_only | hybrid
  - Top-K          : 1, 3, 5, 10
  - Chunk size     : 100, 200, 300, 500 words
  - Deduplication  : enabled | disabled

For each of the 3 × 4 × 4 × 2 = 96 configurations, measures:
  - Recall@K (K = current Top-K value)
  - Mean query latency (ms)
  - Mean token usage (tokens retrieved = top_k × avg_tokens_per_chunk)

Results saved as:
  results/ablation_results.json
  results/ablation_results.csv
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import csv
import time
import random
import sqlite3
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

from benchmarks.config import (
    SEEDS, EMBEDDING_MODEL, EMBEDDING_DIM,
    ABLATION_CHUNK_SIZES, ABLATION_TOP_K_VALUES, ABLATION_MODES, ABLATION_DEDUP,
    AVG_TOKENS_PER_CHUNK, RESULTS_DIR,
)
from evaluation.metrics import recall_at_k, summarise
from evaluation.statistical_tests import aggregate_trials


# ─────────────────────────────────────────────────────────
# Chunker
# ─────────────────────────────────────────────────────────

def chunk_doc(text: str, max_words: int, overlap: int = 10) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks, i = [], 0
    step = max(1, max_words - overlap)
    while i < len(words):
        chunk_words = words[i: i + max_words]
        if len(chunk_words) >= 5:          # skip trivially short trailing chunks
            chunks.append(" ".join(chunk_words))
        i += step
    return chunks


def build_corpus_from_docs(docs: list, doc_ids_base: list, chunk_size: int):
    """Chunk all docs and return (chunks, chunk_ids, doc_id_of_chunk)."""
    chunks, chunk_ids, source_ids = [], [], []
    for base_id, doc in zip(doc_ids_base, docs):
        parts = chunk_doc(doc, max_words=chunk_size)
        for k, part in enumerate(parts):
            chunks.append(part)
            chunk_ids.append(f"{base_id}_c{k}")
            source_ids.append(base_id)
    return chunks, chunk_ids, source_ids


# ─────────────────────────────────────────────────────────
# Ablation Retriever
# ─────────────────────────────────────────────────────────

class AblationRetriever:
    """
    Configurable retriever that supports fts5_only / faiss_only / hybrid modes
    and optional deduplication.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
        mode: str = "hybrid",         # faiss_only | fts5_only | hybrid
        deduplicate: bool = True,
    ):
        assert mode in ("faiss_only", "fts5_only", "hybrid")
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.mode = mode
        self.deduplicate = deduplicate
        self.index = None
        self.db = None
        self.cursor = None
        self.chunk_ids = []
        self._seen_hashes = set()

    def build(self, chunks: list, chunk_ids: list, batch_size: int = 64) -> float:
        t0 = time.perf_counter()

        if self.deduplicate:
            unique_chunks, unique_ids = [], []
            for ch, cid in zip(chunks, chunk_ids):
                h = hash(ch)
                if h not in self._seen_hashes:
                    self._seen_hashes.add(h)
                    unique_chunks.append(ch)
                    unique_ids.append(cid)
        else:
            unique_chunks, unique_ids = chunks, chunk_ids

        self.chunk_ids = unique_ids

        if self.mode in ("faiss_only", "hybrid"):
            embs = self.model.encode(
                unique_chunks, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
            ).astype("float32")
            embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
            self.index = faiss.IndexFlatIP(self.dim)
            self.index.add(embs)

        if self.mode in ("fts5_only", "hybrid"):
            self.db = sqlite3.connect(":memory:")
            self.cursor = self.db.cursor()
            self.cursor.execute("CREATE VIRTUAL TABLE fts USING fts5(id, text);")
            self.cursor.executemany(
                "INSERT INTO fts (id, text) VALUES (?, ?)",
                list(zip(unique_ids, unique_chunks)),
            )
            self.db.commit()

        return time.perf_counter() - t0

    def retrieve(self, query: str, top_k: int = 5):
        t0 = time.perf_counter()
        hits = []

        if self.mode in ("fts5_only", "hybrid") and self.cursor:
            try:
                safe = query.replace('"', '""')
                self.cursor.execute(
                    "SELECT id FROM fts WHERE text MATCH ? LIMIT ?", (safe, top_k)
                )
                hits += [row[0] for row in self.cursor.fetchall()]
            except sqlite3.OperationalError:
                pass

        if self.mode in ("faiss_only", "hybrid") and self.index:
            q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
            q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
            _, I = self.index.search(q_emb, top_k)
            for i in I[0]:
                if i >= 0:
                    cid = self.chunk_ids[i]
                    if cid not in hits:
                        hits.append(cid)

        latency_ms = (time.perf_counter() - t0) * 1000
        return hits[:top_k], latency_ms


# ─────────────────────────────────────────────────────────
# Ablation runner
# ─────────────────────────────────────────────────────────

def run_ablation(n_docs: int = 2000, n_queries: int = 100):
    """Run the full ablation grid. Returns list of result dicts."""
    from sklearn.datasets import fetch_20newsgroups

    print("=" * 60)
    print(" CogniSync Ablation Study")
    print("=" * 60)

    cats = ["comp.sys.mac.hardware", "comp.windows.x", "sci.electronics", "sci.crypt"]
    ng = fetch_20newsgroups(subset="train", categories=cats)
    rng = random.Random(SEEDS[0])
    indices = rng.sample(range(len(ng.data)), min(n_docs, len(ng.data)))
    raw_docs = [ng.data[i] for i in indices]
    raw_ids  = [f"ng_{i}" for i in indices]

    all_results = []
    config_count = (len(ABLATION_MODES) * len(ABLATION_TOP_K_VALUES)
                    * len(ABLATION_CHUNK_SIZES) * len(ABLATION_DEDUP))
    done = 0

    for chunk_size in ABLATION_CHUNK_SIZES:
        chunks, chunk_ids, source_ids = build_corpus_from_docs(raw_docs, raw_ids, chunk_size)
        print(f"\nChunk size={chunk_size}w → {len(chunks)} chunks")

        # Build evaluation queries from raw docs (seed=42 always)
        query_rng = random.Random(42)
        query_meta = [
            (raw_ids[i], raw_docs[i])
            for i in query_rng.sample(range(n_docs), min(n_queries, n_docs))
            if len(raw_docs[i].split()) > 20
        ][:n_queries]
        queries    = [" ".join(doc.split()[5:15]) for _, doc in query_meta]
        gt_sources = [[did] for did, _ in query_meta]

        # Map source doc id → chunk ids for this chunk size
        source_to_chunks = {}
        for cid, sid in zip(chunk_ids, source_ids):
            source_to_chunks.setdefault(sid, []).append(cid)

        gt_chunk_ids = [
            sum([source_to_chunks.get(sid, []) for sid in gt], [])
            for gt in gt_sources
        ]

        for mode in ABLATION_MODES:
            for top_k in ABLATION_TOP_K_VALUES:
                for dedup in ABLATION_DEDUP:
                    seed_recalls, seed_latencies = [], []

                    for seed in SEEDS[:3]:   # 3 seeds for ablation (speed vs rigour)
                        random.seed(seed)
                        ret = AblationRetriever(mode=mode, deduplicate=dedup)
                        ret.build(chunks, chunk_ids)

                        per_query_hits, per_query_lats = [], []
                        for q, gt_cids in zip(queries, gt_chunk_ids):
                            retrieved, lat = ret.retrieve(q, top_k)
                            hit = int(bool(set(retrieved) & set(gt_cids)))
                            per_query_hits.append(hit)
                            per_query_lats.append(lat)

                        seed_recalls.append(float(np.mean(per_query_hits)))
                        seed_latencies.append(float(np.mean(per_query_lats)))

                    config = {
                        "mode":       mode,
                        "top_k":      top_k,
                        "chunk_size": chunk_size,
                        "dedup":      dedup,
                        "recall":     round(float(np.mean(seed_recalls)), 4),
                        "recall_std": round(float(np.std(seed_recalls,  ddof=1)), 4),
                        "latency_ms": round(float(np.mean(seed_latencies)), 3),
                        "token_usage": top_k * AVG_TOKENS_PER_CHUNK,
                    }
                    all_results.append(config)
                    done += 1
                    print(f"  [{done}/{config_count}] mode={mode:10s} k={top_k} cs={chunk_size:3d} dedup={dedup} "
                          f"→ recall={config['recall']:.4f}")

    # Save JSON
    out_json = RESULTS_DIR / "ablation_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"experiment": "ablation_study", "results": all_results}, f, indent=2)

    # Save CSV
    out_csv = RESULTS_DIR / "ablation_results.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\n✅ Ablation results → {out_json}")
    print(f"✅ Ablation CSV     → {out_csv}")
    return all_results


if __name__ == "__main__":
    run_ablation(n_docs=2000, n_queries=100)
