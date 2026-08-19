"""
baselines/amem_approx.py
-------------------------
A-MEM (Agentic Memory) approximation baseline.

A-MEM [Xu et al., 2025] organises memory as a dynamic graph where nodes are
memory chunks and edges represent semantic similarity links. Retrieval performs
a graph walk (BFS/neighbour expansion) starting from the highest-similarity node.

This approximation:
  1. Builds a FAISS index for initial seed retrieval.
  2. Precomputes a sparse adjacency graph where each node is linked to its
     top-M semantic neighbours (edges weighted by cosine similarity).
  3. At query time:
       a. Find the top-K seed nodes via FAISS.
       b. Expand each seed's graph neighbours by one hop.
       c. Re-rank all expanded candidates by FAISS similarity and return top-K.

References
----------
Xu et al. "A-MEM: Agentic Memory for LLM Agents." arXiv:2502.12110, 2025.
"""

import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class AMEMApprox:
    """
    A-MEM-style dynamic graph memory with BFS neighbour expansion.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        graph_neighbors: int = 5,   # edges per node in the memory graph
    ):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.graph_neighbors = graph_neighbors

        self.index: faiss.IndexFlatIP = None
        self.embeddings: np.ndarray = None
        self.doc_ids: List[str] = []
        # adj[i] = list of (j, weight) neighbour entries
        self.adj: List[List[Tuple[int, float]]] = []

    # ─────────────── Build ───────────────

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        self.doc_ids = doc_ids
        t0 = time.perf_counter()

        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.embeddings = embs

        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)

        # Build adjacency graph: for each node find top-(graph_neighbors+1) neighbours
        # (+1 to exclude self)
        k_graph = min(self.graph_neighbors + 1, len(doc_ids))
        scores, I = self.index.search(embs, k_graph)
        self.adj = []
        for i in range(len(doc_ids)):
            neighbours = [
                (int(I[i, j]), float(scores[i, j]))
                for j in range(k_graph)
                if I[i, j] != i and I[i, j] >= 0
            ][:self.graph_neighbors]
            self.adj.append(neighbours)

        return time.perf_counter() - t0

    # ─────────────── Retrieve ────────────

    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        t0 = time.perf_counter()

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)

        # Step 1: seed retrieval
        seed_k = min(top_k, len(self.doc_ids))
        seed_scores, I = self.index.search(q_emb, seed_k)
        seeds = [int(I[0, j]) for j in range(seed_k) if I[0, j] >= 0]

        # Step 2: graph expansion — collect all 1-hop neighbours
        expanded = set(seeds)
        for seed in seeds:
            for nbr, _ in self.adj[seed]:
                expanded.add(nbr)

        # Step 3: re-rank all expanded nodes by cosine similarity to query
        expanded_list = list(expanded)
        # Batch dot products
        cand_embs = self.embeddings[expanded_list]
        cand_scores = (cand_embs @ q_emb.T).flatten()
        ranked = sorted(
            zip(expanded_list, cand_scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        retrieved_ids = [self.doc_ids[idx] for idx, _ in ranked]
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
    docs = [f"Software concept {i}: design patterns and architecture" for i in range(60)]
    ids = [f"d{i}" for i in range(60)]
    amem = AMEMApprox(graph_neighbors=5)
    bt = amem.build(docs, ids)
    print(f"Build time: {bt:.3f}s")
    res, lat = amem.retrieve("design patterns architecture", top_k=5)
    print(f"A-MEM top-5: {res} ({lat:.2f}ms)")
    print("✅ amem_approx.py smoke test passed.")
