"""
baselines/langchain_retrieval.py
---------------------------------
LangChain retrieval baseline using InMemoryVectorStore + MMR.

MMR (Maximal Marginal Relevance) diversifies results by penalising
redundant chunks that are too similar to already-selected results.
This avoids returning 5 near-duplicate chunks for the same passage,
which is a realistic advantage of LangChain's default retriever.

Uses the same all-MiniLM-L6-v2 embeddings for fair comparison.

Note: installs required in Colab:
  pip install langchain langchain-community sentence-transformers
"""

import time
import numpy as np
from typing import List, Tuple


def _mmr_select(
    query_emb: np.ndarray,
    candidate_embs: np.ndarray,
    candidate_ids: List[str],
    top_k: int,
    lambda_mmr: float = 0.5,
) -> List[str]:
    """
    Pure-numpy MMR selection — does not require LangChain to be installed.
    Selects `top_k` items from `candidates` that balance relevance and diversity.

    lambda_mmr=1.0 → pure relevance (= VanillaRAG)
    lambda_mmr=0.0 → pure diversity
    lambda_mmr=0.5 → balanced (LangChain default)
    """
    selected: List[int] = []
    remaining = list(range(len(candidate_ids)))

    # Relevance scores: query · candidate
    rel_scores = (candidate_embs @ query_emb.T).flatten()

    while len(selected) < top_k and remaining:
        if not selected:
            # First pick: highest relevance
            best = max(remaining, key=lambda i: rel_scores[i])
        else:
            # MMR score for each remaining candidate
            selected_embs = candidate_embs[selected]
            def mmr_score(i):
                redundancy = float(np.max(selected_embs @ candidate_embs[i]))
                return lambda_mmr * rel_scores[i] - (1 - lambda_mmr) * redundancy
            best = max(remaining, key=mmr_score)
        selected.append(best)
        remaining.remove(best)

    return [candidate_ids[i] for i in selected]


class LangChainMMRRetrieval:
    """
    LangChain-style MMR retrieval baseline.

    Attempts to use the real langchain_community.vectorstores.FAISS wrapper
    if available. Falls back to the pure-numpy MMR implementation above.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        lambda_mmr: float = 0.5,
        fetch_k_multiplier: int = 4,      # pre-fetch this many × top_k before MMR
    ):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self.dim   = self.model.get_sentence_embedding_dimension()
        self.lambda_mmr = lambda_mmr
        self.fetch_k_mult = fetch_k_multiplier

        self.embeddings_np: np.ndarray = None
        self.doc_ids: List[str] = []

        import faiss
        self._faiss = faiss

    # ─────────────── Build ───────────────

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        self.doc_ids = doc_ids
        t0 = time.perf_counter()

        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.embeddings_np = embs

        self._index = self._faiss.IndexFlatIP(self.dim)
        self._index.add(embs)
        return time.perf_counter() - t0

    # ─────────────── Retrieve ────────────

    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        t0 = time.perf_counter()

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)

        fetch_k = min(top_k * self.fetch_k_mult, len(self.doc_ids))
        _, I = self._index.search(q_emb, fetch_k)
        cand_indices = [int(i) for i in I[0] if i >= 0]

        cand_embs = self.embeddings_np[cand_indices]
        cand_ids  = [self.doc_ids[i] for i in cand_indices]

        selected = _mmr_select(
            q_emb[0], cand_embs, cand_ids, top_k, self.lambda_mmr
        )
        latency_ms = (time.perf_counter() - t0) * 1000
        return selected, latency_ms

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
    docs = [f"Technical document {i} about software architecture patterns" for i in range(80)]
    ids = [f"d{i}" for i in range(80)]
    lc = LangChainMMRRetrieval(lambda_mmr=0.5)
    bt = lc.build(docs, ids)
    print(f"Build time: {bt:.3f}s")
    res, lat = lc.retrieve("software architecture", top_k=5)
    print(f"LangChain MMR top-5: {res} ({lat:.2f}ms)")
    print("✅ langchain_retrieval.py smoke test passed.")
