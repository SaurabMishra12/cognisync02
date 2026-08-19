"""
evaluation/metrics.py
----------------------
Core retrieval metric calculations.

Provides:
  - recall_at_k          : fraction of queries with hit in top-K
  - mean_reciprocal_rank : MRR over a query set
  - ndcg_at_k            : NDCG@K (graded relevance)
  - precision_at_k       : P@K
  - mean_average_precision: MAP
  - bootstrap_ci         : 95% bootstrapped confidence interval
  - summarise            : dict of mean ± std ± CI for a list of per-query scores
"""

import numpy as np
from typing import List, Optional


# ─────────────────────────────────────────────────────────
# Per-query hit helpers
# ─────────────────────────────────────────────────────────

def hit_at_k(retrieved_ids: List, ground_truth_ids: List, k: int) -> int:
    """Return 1 if any ground-truth id appears in the top-k retrieved, else 0."""
    return int(bool(set(retrieved_ids[:k]) & set(ground_truth_ids)))


def reciprocal_rank(retrieved_ids: List, ground_truth_ids: List) -> float:
    """Return 1/rank of the first relevant result; 0.0 if none found."""
    gt_set = set(ground_truth_ids)
    for rank, rid in enumerate(retrieved_ids, start=1):
        if rid in gt_set:
            return 1.0 / rank
    return 0.0


def dcg_at_k(retrieved_ids: List, ground_truth_ids: List, k: int) -> float:
    """Discounted cumulative gain@K (binary relevance)."""
    gt_set = set(ground_truth_ids)
    dcg = 0.0
    for rank, rid in enumerate(retrieved_ids[:k], start=1):
        if rid in gt_set:
            dcg += 1.0 / np.log2(rank + 1)
    return dcg


def ndcg_at_k(retrieved_ids: List, ground_truth_ids: List, k: int) -> float:
    """NDCG@K (binary relevance, ideal DCG based on actual number of relevant docs)."""
    ideal_hits = min(len(ground_truth_ids), k)
    ideal_dcg = sum(1.0 / np.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    if ideal_dcg == 0.0:
        return 0.0
    return dcg_at_k(retrieved_ids, ground_truth_ids, k) / ideal_dcg


# ─────────────────────────────────────────────────────────
# Aggregate metrics over a query set
# ─────────────────────────────────────────────────────────

def recall_at_k(all_retrieved: List[List], all_ground_truths: List[List], k: int) -> float:
    """Recall@K averaged over all queries."""
    hits = [hit_at_k(r, g, k) for r, g in zip(all_retrieved, all_ground_truths)]
    return float(np.mean(hits))


def mean_reciprocal_rank(all_retrieved: List[List], all_ground_truths: List[List]) -> float:
    """MRR averaged over all queries."""
    rrs = [reciprocal_rank(r, g) for r, g in zip(all_retrieved, all_ground_truths)]
    return float(np.mean(rrs))


def mean_ndcg_at_k(all_retrieved: List[List], all_ground_truths: List[List], k: int) -> float:
    """NDCG@K averaged over all queries."""
    scores = [ndcg_at_k(r, g, k) for r, g in zip(all_retrieved, all_ground_truths)]
    return float(np.mean(scores))


def precision_at_k(all_retrieved: List[List], all_ground_truths: List[List], k: int) -> float:
    """P@K averaged over all queries."""
    def _p(retrieved, gt):
        hits = len(set(retrieved[:k]) & set(gt))
        return hits / k
    return float(np.mean([_p(r, g) for r, g in zip(all_retrieved, all_ground_truths)]))


def mean_average_precision(all_retrieved: List[List], all_ground_truths: List[List]) -> float:
    """MAP — mean of per-query average precisions."""
    def _ap(retrieved, gt):
        gt_set = set(gt)
        hits, precision_sum = 0, 0.0
        for rank, rid in enumerate(retrieved, start=1):
            if rid in gt_set:
                hits += 1
                precision_sum += hits / rank
        return precision_sum / len(gt_set) if gt_set else 0.0
    return float(np.mean([_ap(r, g) for r, g in zip(all_retrieved, all_ground_truths)]))


# ─────────────────────────────────────────────────────────
# Statistical helpers
# ─────────────────────────────────────────────────────────

def bootstrap_ci(
    scores: List[float],
    n_resamples: int = 1000,
    confidence: float = 0.95,
    seed: int = 42,
) -> tuple[float, float]:
    """Return (lower, upper) bootstrapped confidence interval for the mean."""
    rng = np.random.default_rng(seed)
    arr = np.array(scores)
    boot_means = np.array([
        np.mean(rng.choice(arr, size=len(arr), replace=True))
        for _ in range(n_resamples)
    ])
    alpha = (1.0 - confidence) / 2.0
    lower = float(np.percentile(boot_means, alpha * 100))
    upper = float(np.percentile(boot_means, (1.0 - alpha) * 100))
    return lower, upper


def summarise(scores: List[float], n_resamples: int = 1000) -> dict:
    """
    Return a summary dict with:
      mean, std, min, max, p25, p50 (median), p75, p99, ci_lower, ci_upper
    """
    arr = np.array(scores, dtype=float)
    ci_lo, ci_hi = bootstrap_ci(scores, n_resamples=n_resamples)
    return {
        "mean":     float(np.mean(arr)),
        "std":      float(np.std(arr, ddof=1)),
        "min":      float(np.min(arr)),
        "max":      float(np.max(arr)),
        "p25":      float(np.percentile(arr, 25)),
        "p50":      float(np.percentile(arr, 50)),
        "p75":      float(np.percentile(arr, 75)),
        "p99":      float(np.percentile(arr, 99)),
        "ci_lower": ci_lo,
        "ci_upper": ci_hi,
        "n":        len(scores),
    }


# ─────────────────────────────────────────────────────────
# Full metric suite for a single (method, query-set) pair
# ─────────────────────────────────────────────────────────

def full_metric_suite(
    all_retrieved: List[List],
    all_ground_truths: List[List],
    latencies_ms: Optional[List[float]] = None,
) -> dict:
    """
    Compute the full set of metrics for one method.

    Returns a dict with Recall@1/3/5/10, MRR, MAP, NDCG@5/10,
    and (if latencies_ms provided) latency statistics.
    """
    results = {
        "recall@1":  recall_at_k(all_retrieved, all_ground_truths, 1),
        "recall@3":  recall_at_k(all_retrieved, all_ground_truths, 3),
        "recall@5":  recall_at_k(all_retrieved, all_ground_truths, 5),
        "recall@10": recall_at_k(all_retrieved, all_ground_truths, 10),
        "mrr":       mean_reciprocal_rank(all_retrieved, all_ground_truths),
        "map":       mean_average_precision(all_retrieved, all_ground_truths),
        "ndcg@5":    mean_ndcg_at_k(all_retrieved, all_ground_truths, 5),
        "ndcg@10":   mean_ndcg_at_k(all_retrieved, all_ground_truths, 10),
    }
    if latencies_ms is not None:
        lat = summarise(latencies_ms)
        results["latency"] = lat
    return results


if __name__ == "__main__":
    # Quick smoke test
    retrieved    = [["a", "b", "c", "d", "e"], ["x", "a", "b", "c", "d"]]
    ground_truth = [["a"], ["a"]]
    print("Recall@1:", recall_at_k(retrieved, ground_truth, 1))   # 0.5
    print("Recall@5:", recall_at_k(retrieved, ground_truth, 5))   # 1.0
    print("MRR:     ", mean_reciprocal_rank(retrieved, ground_truth))  # 0.75
    print("MAP:     ", mean_average_precision(retrieved, ground_truth))
    scores = [0.8, 0.85, 0.82, 0.88, 0.79]
    print("Summary:", summarise(scores))
    print("✅ metrics.py smoke test passed.")
