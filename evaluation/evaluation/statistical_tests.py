"""
evaluation/statistical_tests.py
---------------------------------
Statistical significance testing for the CogniSync evaluation.

Provides:
  - mcnemar_test     : paired McNemar test on binary hit/miss vectors
  - paired_ttest     : paired Student's t-test on continuous metric vectors
  - wilcoxon_test    : Wilcoxon signed-rank (non-parametric alternative to t-test)
  - cohens_d         : effect size for paired comparisons
  - run_all_tests    : convenience wrapper that runs all tests between two systems

Usage:
  from evaluation.statistical_tests import run_all_tests
  results = run_all_tests(hits_a, hits_b, latencies_a, latencies_b)
"""

import numpy as np
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar
from typing import List, Optional


# ─────────────────────────────────────────────────────────
# McNemar test  (binary hit/miss vectors)
# ─────────────────────────────────────────────────────────

def mcnemar_test(hits_a: List[int], hits_b: List[int]) -> dict:
    """
    McNemar's test on paired binary per-query hit vectors.

    Parameters
    ----------
    hits_a, hits_b : list of 0/1 per query

    Returns
    -------
    dict with 'statistic', 'p_value', 'significant' (at alpha=0.05)
    """
    if len(hits_a) != len(hits_b):
        raise ValueError("hit vectors must have equal length")

    n = len(hits_a)
    # Contingency table: [[both hit, a-hit b-miss], [a-miss b-hit], [both miss]]
    b = sum(1 for a, b_ in zip(hits_a, hits_b) if a == 1 and b_ == 0)
    c = sum(1 for a, b_ in zip(hits_a, hits_b) if a == 0 and b_ == 1)

    # Use the exact binomial when discordant pairs < 25, else chi2 approximation
    table = np.array([[n - b - c - sum(1 for a, b_ in zip(hits_a, hits_b) if a==0 and b_==0), b],
                      [c, sum(1 for a, b_ in zip(hits_a, hits_b) if a==0 and b_==0)]])
    # simpler: construct 2×2 table directly
    n00 = sum(1 for a, b_ in zip(hits_a, hits_b) if a == 0 and b_ == 0)
    n11 = sum(1 for a, b_ in zip(hits_a, hits_b) if a == 1 and b_ == 1)
    table_2x2 = np.array([[n11, b], [c, n00]])

    exact = (b + c) < 25
    result = sm_mcnemar(table_2x2, exact=exact)
    return {
        "test":        "McNemar",
        "statistic":   float(result.statistic),
        "p_value":     float(result.pvalue),
        "significant": bool(result.pvalue < 0.05),
        "b_wins":      b,    # system A wins but B misses
        "c_wins":      c,    # system B wins but A misses
        "exact":       exact,
    }


# ─────────────────────────────────────────────────────────
# Paired t-test  (continuous metrics, e.g. latency)
# ─────────────────────────────────────────────────────────

def paired_ttest(scores_a: List[float], scores_b: List[float]) -> dict:
    """
    Paired two-sided t-test.

    H0: E[A - B] = 0
    Returns dict with t-statistic, p-value, and significance flag.
    """
    a, b = np.array(scores_a), np.array(scores_b)
    t_stat, p_val = stats.ttest_rel(a, b)
    return {
        "test":        "paired_t",
        "statistic":   float(t_stat),
        "p_value":     float(p_val),
        "significant": bool(p_val < 0.05),
        "mean_diff":   float(np.mean(a - b)),
    }


# ─────────────────────────────────────────────────────────
# Wilcoxon signed-rank  (non-parametric)
# ─────────────────────────────────────────────────────────

def wilcoxon_test(scores_a: List[float], scores_b: List[float]) -> dict:
    """
    Wilcoxon signed-rank test (non-parametric paired test).
    Preferred when normality cannot be assumed.
    """
    a, b = np.array(scores_a), np.array(scores_b)
    diff = a - b
    if np.all(diff == 0):
        return {"test": "Wilcoxon", "statistic": 0.0, "p_value": 1.0, "significant": False}
    stat, p_val = stats.wilcoxon(diff)
    return {
        "test":        "Wilcoxon",
        "statistic":   float(stat),
        "p_value":     float(p_val),
        "significant": bool(p_val < 0.05),
        "median_diff": float(np.median(diff)),
    }


# ─────────────────────────────────────────────────────────
# Cohen's d  (effect size)
# ─────────────────────────────────────────────────────────

def cohens_d(scores_a: List[float], scores_b: List[float]) -> dict:
    """
    Cohen's d for paired samples.
    Interpretation: |d| < 0.2 small, 0.2–0.5 medium, > 0.8 large.
    """
    a, b = np.array(scores_a), np.array(scores_b)
    diff = a - b
    d = float(np.mean(diff) / (np.std(diff, ddof=1) + 1e-12))
    magnitude = "negligible"
    if abs(d) >= 0.8:
        magnitude = "large"
    elif abs(d) >= 0.5:
        magnitude = "medium"
    elif abs(d) >= 0.2:
        magnitude = "small"
    return {
        "cohens_d":  d,
        "magnitude": magnitude,
    }


# ─────────────────────────────────────────────────────────
# Combined test suite
# ─────────────────────────────────────────────────────────

def run_all_tests(
    hits_a: List[int],
    hits_b: List[int],
    continuous_a: Optional[List[float]] = None,
    continuous_b: Optional[List[float]] = None,
    label_a: str = "System A",
    label_b: str = "System B",
) -> dict:
    """
    Run the full battery of statistical tests between two systems.

    Parameters
    ----------
    hits_a, hits_b        : per-query binary hit (1) / miss (0) vectors
    continuous_a/b        : optional continuous metric (e.g. latency ms)
    label_a, label_b      : system names for the results dict

    Returns
    -------
    Nested dict suitable for JSON export.
    """
    results = {
        "comparison": f"{label_a} vs {label_b}",
        "n_queries":  len(hits_a),
        "recall_a":   float(np.mean(hits_a)),
        "recall_b":   float(np.mean(hits_b)),
        "mcnemar":    mcnemar_test(hits_a, hits_b),
    }
    if continuous_a is not None and continuous_b is not None:
        results["paired_t"]   = paired_ttest(continuous_a, continuous_b)
        results["wilcoxon"]   = wilcoxon_test(continuous_a, continuous_b)
        results["cohens_d"]   = cohens_d(continuous_a, continuous_b)
    return results


# ─────────────────────────────────────────────────────────
# Multi-trial aggregation
# ─────────────────────────────────────────────────────────

def aggregate_trials(trial_scores: List[List[float]]) -> dict:
    """
    Given a list of per-trial score arrays, return mean ± std ± 95% CI.
    Each inner list is the scores from one trial (e.g., Recall@5 per query).

    Returns per-trial means and aggregate statistics.
    """
    trial_means = [float(np.mean(t)) for t in trial_scores]
    arr = np.array(trial_means)
    # Bootstrapped CI over across-trial means
    rng = np.random.default_rng(42)
    boot = [np.mean(rng.choice(arr, size=len(arr), replace=True)) for _ in range(1000)]
    return {
        "trial_means": trial_means,
        "mean":        float(np.mean(arr)),
        "std":         float(np.std(arr, ddof=1)),
        "ci_95_lower": float(np.percentile(boot, 2.5)),
        "ci_95_upper": float(np.percentile(boot, 97.5)),
        "n_trials":    len(trial_means),
    }


if __name__ == "__main__":
    import random
    rng = random.Random(0)
    hits_a = [rng.randint(0, 1) for _ in range(150)]
    hits_b = [min(1, h + rng.randint(0, 1)) for h in hits_a]   # B slightly better
    r = run_all_tests(hits_a, hits_b, label_a="FTS5", label_b="Hybrid")
    import json
    print(json.dumps(r, indent=2))
    print("✅ statistical_tests.py smoke test passed.")
