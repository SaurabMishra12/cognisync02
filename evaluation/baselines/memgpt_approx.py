"""
baselines/memgpt_approx.py
---------------------------
MemGPT-approximation baseline.

MemGPT [Packer et al., 2023] uses a two-tier memory model:
  - In-context (main) memory: a sliding window of the most recently accessed chunks
  - External (archival) memory: full document store, retrieved on demand

This approximation models that behaviour faithfully:
  1. Maintain an "active window" of the MEMGPT_WINDOW_SIZE most recently seen chunks.
  2. For a query, first search the active window by cosine similarity.
  3. If not found in the window, fall back to full FAISS search (archival retrieval).
  4. Move retrieved chunks to the front of the window (LRU eviction).

References
----------
Packer et al. "MemGPT: Towards LLMs as Operating Systems." arXiv:2310.08560, 2023.
"""

import time
import collections
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class MemGPTApprox:
    """
    MemGPT-style memory with sliding active-window + archival FAISS fallback.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        window_size: int = 20,
    ):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.window_size = window_size

        # Full archival store
        self.archival_index: faiss.IndexFlatIP = None
        self.all_embeddings: np.ndarray = None
        self.doc_ids: List[str] = []

        # Active window: ordered deque of (doc_id, embedding)
        self.active_window: collections.deque = collections.deque(maxlen=window_size)

    # ─────────────── Build ───────────────

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        self.doc_ids = doc_ids
        t0 = time.perf_counter()
        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.all_embeddings = embs

        self.archival_index = faiss.IndexFlatIP(self.dim)
        self.archival_index.add(embs)

        # Seed the active window with the first `window_size` chunks
        for i in range(min(self.window_size, len(doc_ids))):
            self.active_window.append((doc_ids[i], embs[i]))

        return time.perf_counter() - t0

    # ─────────────── Retrieve ────────────

    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        t0 = time.perf_counter()

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)

        # Step 1: score active window
        window_ids    = [item[0] for item in self.active_window]
        window_embs   = np.vstack([item[1] for item in self.active_window])
        window_scores = (window_embs @ q_emb.T).flatten()
        window_ranked = sorted(
            zip(window_ids, window_scores), key=lambda x: x[1], reverse=True
        )
        in_window_hits = [wid for wid, _ in window_ranked[:top_k]]

        # Step 2: archival fallback to fill remaining slots
        _, I = self.archival_index.search(q_emb, top_k * 2)
        archival_hits = [self.doc_ids[i] for i in I[0] if i >= 0 and self.doc_ids[i] not in in_window_hits]

        # Merge: prefer window hits first
        merged = (in_window_hits + archival_hits)[:top_k]

        # Step 3: promote retrieved docs to front of active window (LRU)
        for doc_id in reversed(merged):
            idx = self.doc_ids.index(doc_id)
            self.active_window.append((doc_id, self.all_embeddings[idx]))

        latency_ms = (time.perf_counter() - t0) * 1000
        return merged, latency_ms

    def batch_retrieve(
        self, queries: List[str], top_k: int = 5
    ) -> Tuple[List[List[str]], List[float]]:
        all_ids, all_lat = [], []
        for q in queries:
            ids, lat = self.retrieve(q, top_k)
            all_ids.append(ids)
            all_lat.append(lat)
        return all_ids, all_lat


if __name__ == "__main__":
    docs = [f"Technical document number {i} about software engineering topics" for i in range(50)]
    ids = [f"d{i}" for i in range(50)]
    m = MemGPTApprox(window_size=10)
    m.build(docs, ids)
    res, lat = m.retrieve("software engineering documentation", top_k=3)
    print(f"MemGPT top-3: {res} ({lat:.2f}ms)")
    print("✅ memgpt_approx.py smoke test passed.")
