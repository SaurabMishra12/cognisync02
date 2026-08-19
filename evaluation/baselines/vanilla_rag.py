"""
baselines/vanilla_rag.py
-------------------------
Vanilla RAG baseline: FAISS IndexFlatIP only (dense vector search).

This is the simplest possible RAG baseline:
  - Encode all documents once with the shared embedding model
  - At query time, encode the query and retrieve top-K by cosine similarity

No keyword search, no re-ranking, no MMR.
Uses the same embedding model as CogniSync for a fair comparison.
"""

import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class VanillaRAG:
    """Pure dense-vector RAG baseline using FAISS IndexFlatIP."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index: faiss.IndexFlatIP = None
        self.doc_ids: List[str] = []
        self.corpus: List[str] = []

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        """
        Encode corpus and build FAISS index.
        Returns build time in seconds.
        """
        assert len(docs) == len(doc_ids), "docs and doc_ids must match"
        self.corpus = docs
        self.doc_ids = doc_ids

        t0 = time.perf_counter()
        embeddings = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        )
        embeddings = embeddings.astype("float32")
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / np.maximum(norms, 1e-12)

        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embeddings)
        build_time = time.perf_counter() - t0
        return build_time

    def retrieve(
        self, query: str, top_k: int = 5
    ) -> Tuple[List[str], float]:
        """
        Retrieve top-K doc IDs for a query.
        Returns (ordered list of doc_ids, latency_ms).
        """
        t0 = time.perf_counter()
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb = q_emb / np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = self.index.search(q_emb, top_k)
        latency_ms = (time.perf_counter() - t0) * 1000
        retrieved_ids = [self.doc_ids[i] for i in I[0] if i >= 0]
        return retrieved_ids, latency_ms

    def batch_retrieve(
        self, queries: List[str], top_k: int = 5
    ) -> Tuple[List[List[str]], List[float]]:
        """Retrieve top-K for multiple queries. Returns (list of id-lists, latencies_ms)."""
        all_ids, all_lat = [], []
        for q in queries:
            ids, lat = self.retrieve(q, top_k)
            all_ids.append(ids)
            all_lat.append(lat)
        return all_ids, all_lat


if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")
    docs = ["Python exception handling with try except", "React useState hook for state management",
            "Docker compose multi-service setup", "FAISS vector search index building"]
    ids = [f"d{i}" for i in range(len(docs))]
    rag = VanillaRAG()
    bt = rag.build(docs, ids)
    print(f"Build time: {bt:.3f}s")
    res, lat = rag.retrieve("docker containers", top_k=2)
    print(f"Top-2 for 'docker containers': {res} ({lat:.2f}ms)")
    print("✅ vanilla_rag.py smoke test passed.")
