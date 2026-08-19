# CIKM Rebuttal Extra Experiments (14 May)

This document consolidates all configurations and results generated from the `results 14may` experiment run.

## 1. Security Classifier Baseline

**Configuration (`logs/security_baseline_config.json`)**
```json
{
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "dataset": "deepset/prompt-injections",
    "test_size": 0.2
}
```

**Metrics (`results/security_baseline_metrics.csv`)**
```csv
,precision,recall,f1-score,support
0,0.875,0.9130434782608695,0.8936170212765957,69.0
1,0.8421052631578947,0.7804878048780488,0.810126582278481,41.0
accuracy,0.8636363636363636,0.8636363636363636,0.8636363636363636,0.8636363636363636
macro avg,0.8585526315789473,0.8467656415694591,0.8518718017775384,110.0
weighted avg,0.8627392344497608,0.8636363636363636,0.8624978576500257,110.0
```

---

## 2. Threshold Ablation

**Configuration (`logs/threshold_config.json`)**
```json
{
    "thresholds": [
        0.1,
        0.15000000000000002,
        0.20000000000000004,
        0.25000000000000006,
        0.30000000000000004,
        0.3500000000000001,
        0.40000000000000013,
        0.45000000000000007,
        0.5000000000000001
    ],
    "metric": "cosine_similarity"
}
```

**Results (`results/threshold_ablation.csv`)**
```csv
Threshold,Attack Success Rate,False Positive Rate
0.1,0.65,0.5
0.15,0.5,0.5
0.2,0.45,1.0
0.25,0.45,1.0
0.3,0.45,1.0
0.35,0.45,1.0
0.4,0.45,1.0
0.45,0.45,1.0
0.5,0.45,1.0
```

> [!NOTE]
> A visualization of this data is available at `results 5may/results 14may/plots/sensitivity_curve.pdf`.

---

## 3. Full-Corpus Retrieval Evaluation

**Configuration (`logs/full_corpus_config.json`)**
```json
{
    "corpus_size": 100000,
    "dataset": "Tevatron/msmarco-passage",
    "eval_queries": 0,
    "hybrid_mrr_10": 0,
    "dense_mrr_10": 0
}
```

**Results (`results/full_corpus_retrieval_results.csv`)**
```csv
Metric,Learned-Alpha Hybrid,Dense-Only Baseline,Corpus Size,Queries Evaluated
MRR@10,0,0,100000,0
```
> [!WARNING]
> It appears the full-corpus evaluation resulted in 0 queries evaluated and 0 for MRR@10 scores, likely due to a bug or missing data mapping in the evaluation script where positive passages were not successfully found in the truncated 100K subset.

---

## 4. Amortized Latency

**Configuration (`logs/latency_config.json`)**
```json
{
    "index_size": 100000,
    "queries_run": 1000,
    "average_latency_ms": 282.19877648353577,
    "p95_latency_ms": 484.0395212173461,
    "p99_latency_ms": 623.1118035316467
}
```

**Raw Latencies (`results/amortized_latency_results.csv`)**
*(Showing first 20 queries out of 1000 to save space. The full list is available in the original csv file)*
```csv
latency_ms
293.58434677124023
159.31439399719238
238.2197380065918
187.8640651702881
265.12718200683594
272.86553382873535
295.2916622161865
228.03568840026855
196.84743881225586
156.47625923156738
246.5972900390625
200.71744918823242
204.22840118408203
347.6557731628418
147.4008560180664
297.6565361022949
400.09236335754395
437.9005432128906
415.64154624938965
147.68719673156738
...
```
