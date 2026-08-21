"""IR metrics and significance testing.

Two things here that the CIKM code did not have:

1. Graded-relevance nDCG. BEIR qrels are graded (0/1/2), and treating them as binary
   changes the ranking of systems on trec-covid and touche in particular.
2. A paired bootstrap. Wilcoxon on per-query MRR is what the CIKM version used; it is
   fine, but it is a test on ranks of differences and it is easy to get a vanishing
   p-value from a large N with a trivial effect (which is exactly what
   `p < 1e-100` in the CIKM Table 2 is). The paired bootstrap gives a confidence
   interval on the difference itself, which is the number a reader actually wants.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

Qrels = Dict[str, Dict[str, int]]          # qid -> docid -> grade
Run = Dict[str, List[Tuple[str, float]]]   # qid -> ranked [(docid, score)]


# --------------------------------------------------------------------------------------
# Per-query metrics
# --------------------------------------------------------------------------------------

def dcg(gains: Sequence[float]) -> float:
    return float(sum(g / np.log2(i + 2) for i, g in enumerate(gains)))


def ndcg_at_k(ranked_docids: Sequence[str], rels: Dict[str, int], k: int) -> float:
    """Graded nDCG@k with the standard 2^rel - 1 gain."""
    gains = [(2 ** rels.get(d, 0)) - 1 for d in ranked_docids[:k]]
    ideal = sorted(((2 ** g) - 1 for g in rels.values()), reverse=True)[:k]
    idcg = dcg(ideal)
    return dcg(gains) / idcg if idcg > 0 else 0.0


def mrr_at_k(ranked_docids: Sequence[str], rels: Dict[str, int], k: int) -> float:
    for rank, d in enumerate(ranked_docids[:k]):
        if rels.get(d, 0) > 0:
            return 1.0 / (rank + 1)
    return 0.0


def recall_at_k(ranked_docids: Sequence[str], rels: Dict[str, int], k: int) -> float:
    positives = {d for d, g in rels.items() if g > 0}
    if not positives:
        return 0.0
    hit = sum(1 for d in ranked_docids[:k] if d in positives)
    return hit / len(positives)


def precision_at_k(ranked_docids: Sequence[str], rels: Dict[str, int], k: int) -> float:
    if k == 0:
        return 0.0
    return sum(1 for d in ranked_docids[:k] if rels.get(d, 0) > 0) / k


def evaluate_run(
    run: Run,
    qrels: Qrels,
    eval_k: int = 10,
    recall_ks: Iterable[int] = (1, 5, 10, 100),
) -> Tuple[Dict[str, float], Dict[str, Dict[str, float]]]:
    """Return (aggregate means, per-query values).

    Queries with no positive judgement are skipped, and the count of skipped queries is
    returned in the aggregate under `n_skipped` so it appears in the logs instead of
    silently shrinking the denominator. The CIKM notebook tracked this with a global
    counter that never made it into the paper.
    """
    per_query: Dict[str, Dict[str, float]] = {}
    skipped = 0

    for qid, ranked in run.items():
        rels = qrels.get(qid, {})
        if not any(g > 0 for g in rels.values()):
            skipped += 1
            continue
        docids = [d for d, _ in ranked]
        row = {
            f"ndcg@{eval_k}": ndcg_at_k(docids, rels, eval_k),
            f"mrr@{eval_k}": mrr_at_k(docids, rels, eval_k),
            f"p@{eval_k}": precision_at_k(docids, rels, eval_k),
        }
        for k in recall_ks:
            row[f"recall@{k}"] = recall_at_k(docids, rels, k)
        per_query[qid] = row

    if not per_query:
        return {"n_queries": 0, "n_skipped": skipped}, {}

    keys = next(iter(per_query.values())).keys()
    agg = {k: float(np.mean([r[k] for r in per_query.values()])) for k in keys}
    agg["n_queries"] = len(per_query)
    agg["n_skipped"] = skipped
    return agg, per_query


# --------------------------------------------------------------------------------------
# Significance
# --------------------------------------------------------------------------------------

def paired_bootstrap(
    a: Sequence[float],
    b: Sequence[float],
    n_resamples: int = 10_000,
    ci: float = 95.0,
    seed: int = 42,
) -> Dict[str, float]:
    """Paired bootstrap on the mean difference a - b.

    Returns the observed difference, a CI on it, and a two-sided p-value computed by
    recentring the bootstrap distribution on zero (the usual bootstrap hypothesis test).
    """
    a_arr, b_arr = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a_arr.shape != b_arr.shape:
        raise ValueError(f"paired arrays must match: {a_arr.shape} vs {b_arr.shape}")
    n = len(a_arr)
    if n == 0:
        return {"delta": 0.0, "ci_low": 0.0, "ci_high": 0.0, "p_value": 1.0, "n": 0}

    diff = a_arr - b_arr
    observed = float(diff.mean())

    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_resamples, n))
    boot = diff[idx].mean(axis=1)

    lo = float(np.percentile(boot, (100 - ci) / 2))
    hi = float(np.percentile(boot, 100 - (100 - ci) / 2))

    centred = boot - boot.mean()
    p = float((np.abs(centred) >= abs(observed)).mean())
    p = max(p, 1.0 / n_resamples)  # never report p = 0 from a finite resample

    return {"delta": observed, "ci_low": lo, "ci_high": hi, "p_value": p, "n": n}


def wilcoxon_safe(a: Sequence[float], b: Sequence[float]) -> Dict[str, float]:
    """Wilcoxon signed-rank, returning p = 1.0 when every pair is tied.

    scipy raises on all-zero differences. The CIKM ablation hit that case and reported
    `p = 1.0`, which read as "no difference" when it actually meant "the two systems
    produced identical rankings on every query" - a much stronger statement, and one
    worth surfacing. `n_ties` makes it visible.
    """
    from scipy import stats

    a_arr, b_arr = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    diff = a_arr - b_arr
    n_ties = int((diff == 0).sum())
    if np.all(diff == 0):
        return {"statistic": 0.0, "p_value": 1.0, "n_ties": n_ties, "all_tied": True}
    stat, p = stats.wilcoxon(a_arr, b_arr, alternative="two-sided")
    return {"statistic": float(stat), "p_value": float(p), "n_ties": n_ties, "all_tied": False}


def holm_correct(p_values: Dict[str, float], alpha: float = 0.05) -> Dict[str, dict]:
    """Holm-Bonferroni. Uniformly more powerful than plain Bonferroni at the same FWER."""
    ordered = sorted(p_values.items(), key=lambda kv: kv[1])
    m = len(ordered)
    out: Dict[str, dict] = {}
    prev_adjusted = 0.0
    for i, (name, p) in enumerate(ordered):
        adjusted = min(1.0, max(prev_adjusted, (m - i) * p))
        prev_adjusted = adjusted
        out[name] = {
            "p_raw": p,
            "p_holm": adjusted,
            "significant": bool(adjusted < alpha),
            "rank": i + 1,
        }
    return out


def compare_systems(
    per_query: Dict[str, Dict[str, Dict[str, float]]],
    metric: str,
    reference: str,
    alpha: float = 0.05,
    seed: int = 42,
) -> List[dict]:
    """Compare every system against `reference` on `metric`, aligned by query id.

    `per_query` is {system -> {qid -> {metric -> value}}}.
    """
    if reference not in per_query:
        raise KeyError(f"reference system {reference!r} not in {list(per_query)}")

    shared = set(per_query[reference])
    for sys_qs in per_query.values():
        shared &= set(sys_qs)
    qids = sorted(shared)
    if not qids:
        return []

    ref_vals = [per_query[reference][q][metric] for q in qids]

    rows, raw_p = [], {}
    for system, qmap in per_query.items():
        if system == reference:
            continue
        sys_vals = [qmap[q][metric] for q in qids]
        boot = paired_bootstrap(sys_vals, ref_vals, seed=seed)
        wil = wilcoxon_safe(sys_vals, ref_vals)
        raw_p[system] = boot["p_value"]
        rows.append(
            {
                "system": system,
                "reference": reference,
                "metric": metric,
                "mean_system": float(np.mean(sys_vals)),
                "mean_reference": float(np.mean(ref_vals)),
                "delta": boot["delta"],
                "ci_low": boot["ci_low"],
                "ci_high": boot["ci_high"],
                "p_bootstrap": boot["p_value"],
                "p_wilcoxon": wil["p_value"],
                "n_tied_queries": wil["n_ties"],
                "identical_rankings": wil["all_tied"],
                "n_queries": len(qids),
            }
        )

    corrected = holm_correct(raw_p, alpha=alpha)
    for row in rows:
        row.update(
            {
                "p_holm": corrected[row["system"]]["p_holm"],
                "significant": corrected[row["system"]]["significant"],
            }
        )
    return sorted(rows, key=lambda r: -r["delta"])
