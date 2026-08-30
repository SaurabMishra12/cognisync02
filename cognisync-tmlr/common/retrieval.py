"""Retrieval components: dense index, BM25, fusion, reranking.

Design notes that matter for the paper:

* Fusion is defined once, with `use_dense_fallback` as an explicit flag rather than an
  unconditional branch. The CIKM implementation applied the override silently, which is
  why a3_alpha_decomposition.py can now measure it.
* `HybridRetriever.retrieve` returns a diagnostics dict alongside the ranking. The
  fallback firing rate and the predicted-alpha distribution are results, not debug output.
* Everything caches embeddings to disk keyed by (encoder, corpus fingerprint) so the
  seven-dataset sweep encodes each corpus exactly once across all six first stages.
"""
from __future__ import annotations

import hashlib
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .config import CROSS_ENCODERS, DENSE_ENCODERS, RetrievalConfig, SEED
from .io_utils import cache_path

_ID_PATTERN = re.compile(r"\b(id|uuid|hash|key|sha|md5)\b", re.IGNORECASE)
_HEX_PATTERN = re.compile(r"\b(0x[0-9a-fA-F]+|[0-9a-fA-F]{16,})\b")
_UUID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def corpus_fingerprint(texts: Sequence[str]) -> str:
    """Stable id for a corpus, for cache keys. Samples rather than hashing everything."""
    h = hashlib.sha1()
    h.update(str(len(texts)).encode())
    step = max(1, len(texts) // 512)
    for t in texts[::step]:
        h.update(t[:256].encode("utf-8", errors="ignore"))
    return h.hexdigest()[:16]


# --------------------------------------------------------------------------------------
# Dense
# --------------------------------------------------------------------------------------

class DenseIndex:
    """FAISS inner-product index over L2-normalised embeddings."""

    def __init__(self, encoder_key: str = "minilm", batch_size: int = 256, device: Optional[str] = None):
        from sentence_transformers import SentenceTransformer

        spec = DENSE_ENCODERS[encoder_key]
        self.encoder_key = encoder_key
        self.model_name = spec["name"]
        self.revision = spec["revision"]
        kwargs = {}
        if self.revision and self.revision != "main":
            kwargs["revision"] = self.revision
        self.model = SentenceTransformer(self.model_name, **kwargs)
        if device:
            self.model = self.model.to(device)
        self.batch_size = batch_size
        self.index = None
        self.doc_ids: List[str] = []
        self.embeddings: Optional[np.ndarray] = None

    def encode(self, texts: Sequence[str], cache_tag: Optional[str] = None) -> np.ndarray:
        """Encode with an on-disk cache. `cache_tag` should identify the corpus."""
        path = None
        if cache_tag:
            path = cache_path("emb", self.encoder_key, cache_tag, corpus_fingerprint(texts))
            if path.exists():
                arr = np.load(path)
                if arr.shape[0] == len(texts):
                    return arr
                print(f"[dense] cache size mismatch at {path.name}, re-encoding")

        arr = self.model.encode(
            list(texts),
            batch_size=self.batch_size,
            show_progress_bar=len(texts) > 5000,
            convert_to_numpy=True,
            normalize_embeddings=False,
        ).astype("float32")

        if path is not None:
            np.save(path, arr)
        return arr

    def build(self, doc_ids: Sequence[str], texts: Sequence[str], cache_tag: Optional[str] = None) -> "DenseIndex":
        import faiss

        embs = self.encode(texts, cache_tag=cache_tag).copy()
        faiss.normalize_L2(embs)
        idx = faiss.IndexFlatIP(embs.shape[1])
        idx.add(embs)
        self.index, self.doc_ids, self.embeddings = idx, list(doc_ids), embs
        return self

    def search(self, queries: Sequence[str], top_k: int) -> Tuple[np.ndarray, np.ndarray]:
        import faiss

        if self.index is None:
            raise RuntimeError("DenseIndex.build must be called before search")
        q = self.model.encode(
            list(queries), batch_size=self.batch_size, convert_to_numpy=True
        ).astype("float32")
        faiss.normalize_L2(q)
        k = min(top_k, len(self.doc_ids))
        return self.index.search(q, k)


# --------------------------------------------------------------------------------------
# Lexical
# --------------------------------------------------------------------------------------

class BM25Index:
    """BM25 with `bm25s` when available and `rank_bm25` as a fallback.

    `rank_bm25` scores every document in pure Python on every query. On the 382k-document
    Touche corpus that is minutes per query, which is why the CIKM evaluation never ran a
    full corpus. `bm25s` uses a sparse matrix and is roughly three orders of magnitude
    faster, which is what makes the full-corpus protocol affordable on a T4.
    """

    def __init__(self, k1: float = 0.9, b: float = 0.4):
        # BEIR's Anserini defaults, not rank_bm25's (1.5, 0.75). Worth stating in the
        # paper: BM25 baselines are notoriously sensitive to this and under-tuned BM25 is
        # the most common way to make a dense retriever look better than it is.
        self.k1, self.b = k1, b
        self.backend = None
        self.retriever = None
        self.doc_ids: List[str] = []

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def build(self, doc_ids: Sequence[str], texts: Sequence[str]) -> "BM25Index":
        self.doc_ids = list(doc_ids)
        try:
            import bm25s

            tokens = bm25s.tokenize(list(texts), stopwords="en", show_progress=False)
            self.retriever = bm25s.BM25(k1=self.k1, b=self.b)
            self.retriever.index(tokens, show_progress=False)
            self.backend = "bm25s"
        except ImportError:
            from rank_bm25 import BM25Okapi

            self.retriever = BM25Okapi(
                [self._tokenize(t) for t in texts], k1=self.k1, b=self.b
            )
            self.backend = "rank_bm25"
            if len(texts) > 100_000:
                print(
                    "[bm25] rank_bm25 on >100k docs will be slow. `pip install bm25s` "
                    "is strongly recommended for the full-corpus runs."
                )
        return self

    def search(self, query: str, top_k: int) -> Tuple[List[int], np.ndarray]:
        if self.backend == "bm25s":
            import bm25s

            q = bm25s.tokenize([query], stopwords="en", show_progress=False)
            idx, scores = self.retriever.retrieve(q, k=min(top_k, len(self.doc_ids)), show_progress=False)
            return list(idx[0]), np.asarray(scores[0], dtype=float)
        scores = np.asarray(self.retriever.get_scores(self._tokenize(query)), dtype=float)
        top = np.argsort(scores)[::-1][:top_k]
        return list(top), scores[top]


# --------------------------------------------------------------------------------------
# Fusion
# --------------------------------------------------------------------------------------

def minmax(scores: np.ndarray) -> np.ndarray:
    if scores.size == 0:
        return scores
    lo, hi = float(scores.min()), float(scores.max())
    if hi - lo < 1e-12:
        # The CIKM code divided by (hi - lo + 1e-10), which maps a degenerate channel to
        # ~0 for every document rather than flagging it. Explicit zeros are equivalent in
        # effect but the caller can now detect the case.
        return np.zeros_like(scores)
    return (scores - lo) / (hi - lo)


def query_features(
    query: str,
    norm_dense: np.ndarray,
    norm_lex: np.ndarray,
) -> List[float]:
    """The six features from the CIKM paper, unchanged, so results stay comparable."""
    dense_std = float(np.std(norm_dense)) if norm_dense.size else 0.0
    lex_std = float(np.std(norm_lex)) if norm_lex.size else 0.0
    dense_mean = float(np.mean(norm_dense)) if norm_dense.size else 0.0
    lex_mean = float(np.mean(norm_lex)) if norm_lex.size else 0.0
    dense_cv = dense_std / dense_mean if dense_mean > 1e-12 else 0.0
    lex_cv = lex_std / lex_mean if lex_mean > 1e-12 else 0.0
    has_id = float(
        bool(_ID_PATTERN.search(query) or _HEX_PATTERN.search(query) or _UUID_PATTERN.search(query))
    )
    return [float(len(query.split())), dense_std, lex_std, dense_cv, lex_cv, has_id]


def rrf_fuse(dense_rank: Dict[str, int], lex_rank: Dict[str, int], k: int = 60) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for d in set(dense_rank) | set(lex_rank):
        out[d] = 1.0 / (k + dense_rank.get(d, 10**6) + 1) + 1.0 / (k + lex_rank.get(d, 10**6) + 1)
    return out


@dataclass
class FusionDiagnostics:
    """Instrumentation that the CIKM run did not record and the paper needs."""

    alpha_used: List[float] = field(default_factory=list)
    alpha_predicted: List[float] = field(default_factory=list)
    fallback_fired: List[bool] = field(default_factory=list)
    fallback_reason: List[str] = field(default_factory=list)
    identical_to_dense: List[bool] = field(default_factory=list)

    def summary(self) -> Dict[str, float]:
        n = max(1, len(self.alpha_used))
        fired = sum(self.fallback_fired)
        return {
            "n_queries": len(self.alpha_used),
            "alpha_mean": float(np.mean(self.alpha_used)) if self.alpha_used else 0.0,
            "alpha_std": float(np.std(self.alpha_used)) if self.alpha_used else 0.0,
            "alpha_pred_mean": float(np.mean(self.alpha_predicted)) if self.alpha_predicted else 0.0,
            "alpha_pred_std": float(np.std(self.alpha_predicted)) if self.alpha_predicted else 0.0,
            "frac_alpha_eq_1": float(np.mean([a >= 0.999 for a in self.alpha_used])) if self.alpha_used else 0.0,
            "fallback_fire_rate": fired / n,
            "fallback_reason_dmax": sum(1 for r in self.fallback_reason if "dmax" in r) / n,
            "fallback_reason_cv": sum(1 for r in self.fallback_reason if "cv" in r) / n,
            "frac_ranking_identical_to_dense": (
                float(np.mean(self.identical_to_dense)) if self.identical_to_dense else 0.0
            ),
        }


class AlphaPredictor:
    """Random Forest over the six query features, trained against oracle alpha."""

    def __init__(self, cfg: RetrievalConfig):
        self.cfg = cfg
        self.model = None
        self.train_alphas: List[float] = []

    def fit(self, features: Sequence[Sequence[float]], oracle_alphas: Sequence[float]) -> "AlphaPredictor":
        from sklearn.ensemble import RandomForestRegressor

        self.model = RandomForestRegressor(
            n_estimators=self.cfg.alpha_model_trees,
            max_depth=self.cfg.alpha_model_depth,
            random_state=SEED,
        )
        self.model.fit(np.asarray(features), np.asarray(oracle_alphas))
        self.train_alphas = list(oracle_alphas)
        return self

    def predict(self, features: Sequence[float]) -> float:
        if self.model is None:
            return self.cfg.fixed_alpha
        return float(np.clip(self.model.predict([list(features)])[0], 0.0, 1.0))

    def feature_importance(self) -> Dict[str, float]:
        names = ["q_len", "dense_std", "lex_std", "dense_cv", "lex_cv", "has_id"]
        if self.model is None:
            return {}
        return dict(zip(names, (float(x) for x in self.model.feature_importances_)))


def resolve_alpha(
    strategy: str,
    cfg: RetrievalConfig,
    features: Sequence[float],
    dense_raw_max: float,
    predictor: Optional[AlphaPredictor] = None,
    oracle_alpha: Optional[float] = None,
) -> Tuple[float, float, bool, str]:
    """Return (alpha_used, alpha_predicted, fallback_fired, reason).

    Strategies:
      dense / lexical            - degenerate endpoints
      fixed                      - cfg.fixed_alpha
      learned                    - Random Forest only
      fallback                   - cfg.fixed_alpha plus the dense-confidence override
      learned+fallback           - the CIKM system as shipped
      oracle                     - per-query argmax, an upper bound on any alpha selector
    """
    if strategy == "dense":
        return 1.0, 1.0, False, ""
    if strategy == "lexical":
        return 0.0, 0.0, False, ""
    if strategy == "oracle":
        a = 0.5 if oracle_alpha is None else float(oracle_alpha)
        return a, a, False, ""

    if strategy in ("learned", "learned+fallback"):
        predicted = predictor.predict(features) if predictor is not None else cfg.fixed_alpha
    else:
        predicted = cfg.fixed_alpha

    alpha, fired, reason = predicted, False, ""
    if strategy in ("fallback", "learned+fallback"):
        lex_cv = features[4]
        hit_dmax = dense_raw_max > cfg.fallback_dmax_threshold
        hit_cv = lex_cv < cfg.fallback_bm25_cv_threshold
        if hit_dmax or hit_cv:
            alpha, fired = 1.0, True
            reason = ("dmax" if hit_dmax else "") + ("+" if hit_dmax and hit_cv else "") + ("cv" if hit_cv else "")

    return alpha, predicted, fired, reason


# --------------------------------------------------------------------------------------
# Reranking
# --------------------------------------------------------------------------------------

class Reranker:
    def __init__(self, reranker_key: str = "ms-marco", batch_size: int = 64, max_length: int = 512):
        from sentence_transformers import CrossEncoder

        spec = CROSS_ENCODERS[reranker_key]
        self.key = reranker_key
        self.model_name = spec["name"]
        kwargs = {}
        if spec.get("revision") and spec["revision"] != "main":
            kwargs["revision"] = spec["revision"]
        self.model = CrossEncoder(self.model_name, max_length=max_length, **kwargs)
        self.batch_size = batch_size

    def rerank(
        self,
        query: str,
        candidates: List[Tuple[str, str, float]],
        depth: int,
    ) -> List[Tuple[str, float]]:
        """Rerank the top `depth` candidates; everything below keeps its first-stage order.

        `candidates` is [(doc_id, text, first_stage_score)] already sorted descending.
        Scores below the rerank depth are shifted so the reranked block always sits above
        the tail, which keeps the concatenation a valid ranking.
        """
        head, tail = candidates[:depth], candidates[depth:]
        if len(head) <= 1:
            return [(d, s) for d, _, s in candidates]

        pairs = [[query, text] for _, text, _ in head]
        scores = self.model.predict(pairs, batch_size=self.batch_size, show_progress_bar=False)
        reranked = sorted(zip((d for d, _, _ in head), (float(s) for s in scores)), key=lambda x: -x[1])

        if tail:
            floor = reranked[-1][1]
            tail_scored = [(d, floor - 1.0 - i * 1e-6) for i, (d, _, _) in enumerate(tail)]
            return reranked + tail_scored
        return reranked


# --------------------------------------------------------------------------------------
# The full first stage
# --------------------------------------------------------------------------------------

class HybridRetriever:
    """Full-corpus hybrid retrieval. No candidate pools anywhere in this class."""

    def __init__(
        self,
        cfg: RetrievalConfig,
        dense: DenseIndex,
        lexical: Optional[BM25Index] = None,
        predictor: Optional[AlphaPredictor] = None,
    ):
        self.cfg, self.dense, self.lexical, self.predictor = cfg, dense, lexical, predictor
        self.diagnostics = FusionDiagnostics()

    def _dense_candidates(self, query: str, depth: int) -> Tuple[Dict[str, float], float]:
        scores, idx = self.dense.search([query], depth)
        out = {self.dense.doc_ids[int(i)]: float(s) for i, s in zip(idx[0], scores[0]) if i >= 0}
        raw_max = float(scores[0].max()) if scores[0].size else 0.0
        return out, raw_max

    def _lexical_candidates(self, query: str, depth: int) -> Dict[str, float]:
        if self.lexical is None:
            return {}
        idx, scores = self.lexical.search(query, depth)
        return {self.lexical.doc_ids[int(i)]: float(s) for i, s in zip(idx, scores)}

    def retrieve(
        self,
        query: str,
        strategy: str = "learned+fallback",
        depth: Optional[int] = None,
        oracle_alpha: Optional[float] = None,
        record: bool = True,
    ) -> List[Tuple[str, float]]:
        cfg = self.cfg
        depth = depth or cfg.first_stage_depth

        dense_scores, dense_raw_max = self._dense_candidates(query, depth)
        dense_order = sorted(dense_scores, key=lambda d: -dense_scores[d])

        if strategy == "dense":
            if record:
                self._record(1.0, 1.0, False, "", True)
            return [(d, dense_scores[d]) for d in dense_order]

        lex_scores = self._lexical_candidates(query, depth)
        if strategy == "lexical":
            order = sorted(lex_scores, key=lambda d: -lex_scores[d])
            if record:
                self._record(0.0, 0.0, False, "", False)
            return [(d, lex_scores[d]) for d in order]

        if strategy == "rrf":
            dr = {d: i for i, d in enumerate(dense_order)}
            lr = {d: i for i, d in enumerate(sorted(lex_scores, key=lambda x: -lex_scores[x]))}
            fused = rrf_fuse(dr, lr, k=cfg.rrf_k)
            order = sorted(fused, key=lambda d: -fused[d])
            if record:
                self._record(0.5, 0.5, False, "", order[: len(dense_order)] == dense_order)
            return [(d, fused[d]) for d in order]

        # Score-level fusion. Union of both candidate sets; a document missing from one
        # channel gets 0 on that channel after normalisation, which is the standard
        # treatment and matches the CIKM implementation.
        union = sorted(set(dense_scores) | set(lex_scores))
        d_vec = minmax(np.array([dense_scores.get(d, -1e9) for d in union], dtype=float))
        l_vec = minmax(np.array([lex_scores.get(d, 0.0) for d in union], dtype=float))
        feats = query_features(query, d_vec, l_vec)

        alpha, predicted, fired, reason = resolve_alpha(
            strategy, cfg, feats, dense_raw_max, self.predictor, oracle_alpha
        )
        fused_vec = alpha * d_vec + (1.0 - alpha) * l_vec
        order = [union[i] for i in np.argsort(-fused_vec)]

        if record:
            same = order[: min(10, len(dense_order))] == dense_order[: min(10, len(dense_order))]
            self._record(alpha, predicted, fired, reason, same)

        return [(d, float(fused_vec[union.index(d)])) for d in order]

    def _record(self, alpha, predicted, fired, reason, same_as_dense) -> None:
        d = self.diagnostics
        d.alpha_used.append(alpha)
        d.alpha_predicted.append(predicted)
        d.fallback_fired.append(fired)
        d.fallback_reason.append(reason)
        d.identical_to_dense.append(bool(same_as_dense))

    def reset_diagnostics(self) -> None:
        self.diagnostics = FusionDiagnostics()


def oracle_alpha_for_query(
    dense_norm: np.ndarray,
    lex_norm: np.ndarray,
    doc_ids: Sequence[str],
    rels: Dict[str, int],
    steps: int = 11,
    k: int = 10,
) -> Tuple[float, float]:
    """Best per-query alpha under label access, and the nDCG it achieves.

    This bounds every possible per-query alpha selector, learned or otherwise. If it sits
    close to the best fixed alpha, no amount of feature engineering on the selector will
    help, and that is worth reporting as a result rather than discovering by accident.
    """
    from .metrics import ndcg_at_k

    best_alpha, best_score = 0.5, -1.0
    for alpha in np.linspace(0.0, 1.0, steps):
        fused = alpha * dense_norm + (1.0 - alpha) * lex_norm
        order = [doc_ids[i] for i in np.argsort(-fused)]
        score = ndcg_at_k(order, rels, k)
        if score > best_score:
            best_alpha, best_score = float(alpha), score
    return best_alpha, best_score


def timed(fn, *args, **kwargs):
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    return out, (time.perf_counter() - t0) * 1000.0
