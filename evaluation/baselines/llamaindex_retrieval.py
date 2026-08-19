"""
baselines/llamaindex_retrieval.py
----------------------------------
LlamaIndex-style retrieval baseline.

LlamaIndex's default VectorStoreIndex retriever uses cosine similarity with
an optional similarity_cutoff to filter out low-confidence results.
This captures LlamaIndex's characteristic behaviour: it does not apply MMR
but does apply a threshold filter — chunks below the cutoff are excluded even
if they would otherwise be in the top-K.

This baseline:
  1. Builds a FAISS index (same as all other baselines).
  2. Retrieves top-(K × fetch_multiplier) candidates.
  3. Filters out candidates below `similarity_cutoff`.
  4. Returns the top-K remaining by cosine similarity.

If fewer than K candidates survive the cutoff, returns all above-threshold ones.

Uses the same all-MiniLM-L6-v2 embeddings for fair comparison.
"""

import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class LlamaIndexRetrieval:
    """
    LlamaIndex-style cosine-similarity retrieval with similarity threshold.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        similarity_cutoff: float = 0.30,   # LlamaIndex default is ~0.3
        fetch_k_multiplier: int = 3,
    ):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.similarity_cutoff = similarity_cutoff
        self.fetch_k_mult = fetch_k_multiplier

        self.index: faiss.IndexFlatIP = None
        self.embeddings_np: np.ndarray = None
        self.doc_ids: List[str] = []

    # ─────────────── Build ───────────────

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        self.doc_ids = doc_ids
        t0 = time.perf_counter()

        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.embeddings_np = embs

        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
        return time.perf_counter() - t0

    # ─────────────── Retrieve ────────────

    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        t0 = time.perf_counter()

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)

        fetch_k = min(top_k * self.fetch_k_mult, len(self.doc_ids))
        scores, I = self.index.search(q_emb, fetch_k)
        scores, I = scores[0], I[0]

        # Apply similarity cutoff (IndexFlatIP with normalised vectors → scores = cosine)
        passed = [
            (int(idx), float(sc))
            for idx, sc in zip(I, scores)
            if idx >= 0 and sc >= self.similarity_cutoff
        ]

        # Take top-K from filtered
        top = passed[:top_k]
        retrieved_ids = [self.doc_ids[idx] for idx, _ in top]
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
    docs = [f"Document {i}: software engineering principles and best practices" for i in range(100)]
    ids = [f"d{i}" for i in range(100)]
    li = LlamaIndexRetrieval(similarity_cutoff=0.3)
    bt = li.build(docs, ids)
    print(f"Build time: {bt:.3f}s")
    res, lat = li.retrieve("engineering principles", top_k=5)
    print(f"LlamaIndex top-5: {res} ({lat:.2f}ms)")
    print("✅ llamaindex_retrieval.py smoke test passed.")
