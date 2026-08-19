"""
baselines/memorybank_approx.py
-------------------------------
MemoryBank approximation baseline.

MemoryBank [Zhong et al., 2024] enhances LLMs with long-term memory by
applying an Ebbinghaus forgetting-curve decay to memory importance scores.
Memories that haven't been accessed recently are down-weighted.

This approximation:
  1. Stores all chunk embeddings in a FAISS index.
  2. Maintains an "access time" and "access count" for each chunk.
  3. At retrieval time, computes cosine_similarity × memory_strength, where
     memory_strength follows the Ebbinghaus formula:
       strength(t) = exp(-decay × Δt)
     and Δt is time since last access (in query-step units).

References
----------
Zhong et al. "MemoryBank: Enhancing Large Language Models with Long-Term Memory."
AAAI 2024.
"""

import time
import math
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class MemoryBankApprox:
    """
    MemoryBank-style retrieval with Ebbinghaus forgetting-curve re-weighting.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        decay: float = 0.5,
    ):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.decay = decay   # larger = faster forgetting

        self.index: faiss.IndexFlatIP = None
        self.embeddings: np.ndarray = None
        self.doc_ids: List[str] = []

        # Memory bookkeeping per chunk
        self._access_count: np.ndarray = None   # times accessed
        self._last_access:  np.ndarray = None   # query step of last access
        self._query_step: int = 0

    # ─────────────── Build ───────────────

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        self.doc_ids = doc_ids
        n = len(docs)
        t0 = time.perf_counter()

        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.embeddings = embs

        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)

        # Initialise memory tracking — all chunks "accessed" at step 0
        self._access_count = np.ones(n, dtype=float)
        self._last_access  = np.zeros(n, dtype=float)
        self._query_step   = 0

        return time.perf_counter() - t0

    # ─────────────── Memory strength ─────

    def _strength(self, idx: int) -> float:
        """Ebbinghaus retention: exp(-decay × Δt) scaled by access count."""
        delta_t = self._query_step - self._last_access[idx]
        # Access count bonus: more accesses = slower forgetting
        effective_decay = self.decay / (1.0 + math.log1p(self._access_count[idx]))
        return math.exp(-effective_decay * delta_t)

    # ─────────────── Retrieve ────────────

    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        t0 = time.perf_counter()
        self._query_step += 1

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)

        # Retrieve more candidates than needed, then re-rank with memory strength
        candidate_k = min(top_k * 4, len(self.doc_ids))
        scores, I = self.index.search(q_emb, candidate_k)
        scores = scores[0]

        # Re-rank by cosine × memory_strength
        candidates = [(int(I[0][j]), float(scores[j])) for j in range(candidate_k) if I[0][j] >= 0]
        reranked = sorted(
            candidates,
            key=lambda x: x[1] * self._strength(x[0]),
            reverse=True,
        )[:top_k]

        # Update access bookkeeping
        for idx, _ in reranked:
            self._access_count[idx] += 1
            self._last_access[idx]  = self._query_step

        retrieved_ids = [self.doc_ids[idx] for idx, _ in reranked]
        latency_ms = (time.perf_counter() - t0) * 1000
        return retrieved_ids, latency_ms

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
    docs = [f"Software engineering concept {i}: architecture and design" for i in range(100)]
    ids = [f"d{i}" for i in range(100)]
    mb = MemoryBankApprox(decay=0.5)
    mb.build(docs, ids)
    res, lat = mb.retrieve("software architecture", top_k=5)
    print(f"MemoryBank top-5: {res} ({lat:.2f}ms)")
    print("✅ memorybank_approx.py smoke test passed.")
