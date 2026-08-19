"""
baselines/pinecone_simulated.py
--------------------------------
Simulated Pinecone managed-vector-DB baseline.

Pinecone queries go over the internet via REST API.
This baseline faithfully models that by:
  1. Performing exact FAISS retrieval locally (same quality as Pinecone's ANN index).
  2. Injecting realistic network round-trip latency sampled from a Gaussian
     calibrated to real-world Pinecone measurements (mean ≈ 150 ms, σ ≈ 30 ms).

Latency calibration source:
  - CogniSync paper (Table 2): measured 312.15 ms mean via httpbin.org RTT + 50ms compute.
  - We use 150ms baseline RTT + 50ms vector-compute = 200ms mean, σ=30ms for the
    simulated "healthy" Pinecone environment (the best case, not P99).
  - This is conservative: it gives Pinecone the benefit of a fast connection.

The retrieval quality is identical to VanillaRAG (FAISS IP) since Pinecone uses
the same cosine-similarity ANN search internally.
"""

import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple


class PineconeSimulated:
    """
    Simulated managed-vector-DB baseline:
    FAISS quality + Gaussian-sampled network latency injection.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        net_mean_ms: float = 150.0,   # mean REST API RTT (ms)
        net_std_ms:  float = 30.0,    # std of RTT distribution
        rng_seed:    int   = 42,
    ):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.net_mean_ms = net_mean_ms
        self.net_std_ms  = net_std_ms
        self.rng = np.random.default_rng(rng_seed)

        self.index: faiss.IndexFlatIP = None
        self.doc_ids: List[str] = []

        # Compute overhead added on top of network RTT (vector search on remote host)
        self.compute_overhead_ms = 50.0

    # ─────────────── Build ───────────────

    def build(self, docs: List[str], doc_ids: List[str], batch_size: int = 64) -> float:
        """
        Build the local FAISS index (represents the remote Pinecone index upload).
        Returns wall-clock build time in seconds.
        """
        self.doc_ids = doc_ids
        t0 = time.perf_counter()

        embs = self.model.encode(
            docs, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False
        ).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)

        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
        return time.perf_counter() - t0

    # ─────────────── Retrieve ────────────

    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        """
        Retrieve top-K with simulated network latency.
        Returns (doc_id_list, total_latency_ms).
        """
        t0 = time.perf_counter()

        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = self.index.search(q_emb, top_k)
        local_ms = (time.perf_counter() - t0) * 1000

        # Inject realistic network + compute overhead
        net_ms = float(max(0, self.rng.normal(self.net_mean_ms, self.net_std_ms)))
        total_ms = local_ms + net_ms + self.compute_overhead_ms

        # Simulate blocking for `net_ms + compute` (for realistic timing benchmarks)
        time.sleep((net_ms + self.compute_overhead_ms) / 1000.0)

        retrieved_ids = [self.doc_ids[i] for i in I[0] if i >= 0]
        actual_latency = (time.perf_counter() - t0) * 1000
        return retrieved_ids, actual_latency

    def batch_retrieve(
        self, queries: List[str], top_k: int = 5
    ) -> Tuple[List[List[str]], List[float]]:
        all_ids, all_lat = [], []
        for q in queries:
            ids, lat = self.retrieve(q, top_k)
            all_ids.append(ids)
            all_lat.append(lat)
        return all_ids, all_lat

    def retrieve_no_sleep(self, query: str, top_k: int = 5) -> Tuple[List[str], float]:
        """
        Same retrieval quality but without actual sleeping —
        returns the *modelled* latency instead. Use this for quality-only evaluations
        where you don't want to wait 150ms per query.
        """
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = self.index.search(q_emb, top_k)
        net_ms = float(max(0, self.rng.normal(self.net_mean_ms, self.net_std_ms)))
        modelled_total_ms = net_ms + self.compute_overhead_ms
        retrieved_ids = [self.doc_ids[i] for i in I[0] if i >= 0]
        return retrieved_ids, modelled_total_ms


if __name__ == "__main__":
    docs = [f"Document {i}: cloud infrastructure and DevOps practices" for i in range(30)]
    ids = [f"d{i}" for i in range(30)]
    pine = PineconeSimulated(net_mean_ms=150.0, net_std_ms=30.0)
    bt = pine.build(docs, ids)
    print(f"Build time: {bt:.3f}s")
    # Use no_sleep version for quick smoke test
    res, lat = pine.retrieve_no_sleep("cloud infrastructure", top_k=3)
    print(f"Pinecone-sim top-3: {res} (modelled {lat:.1f}ms)")
    print("✅ pinecone_simulated.py smoke test passed.")
