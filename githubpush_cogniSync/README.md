# CogniSync: Learned-Alpha Hybrid Retrieval with Multi-Signal Adversarial Filtering

This repository contains the empirical artifacts, reproducibility scripts, raw evaluation results, and pseudocode for **CogniSync**, as detailed in the CIKM 2026 paper.

## Directory Structure

*   `results/`: Contains the raw CSVs mirroring all empirical tables in the manuscript, as well as raw output files.
    *   `MASTER_RAW_EVAL_ALL_QUERIES.csv`: The complete 119,612-row dataset containing per-query evaluation data backing Tables 1, 3, 4, and 6.
    *   `security_comparison_raw.csv`: Per-query security evaluation logs.
    *   `security_baseline_metrics.csv`: Raw deepset baseline classifier evaluation (Accuracy/Precision/Recall/F1).
    *   `security_heuristic_ablation.csv`: Ablation demonstrating the Macro F1 improvement from the Goal-Redirection heuristic.
    *   `table1_main_retrieval.csv`: Main MRR@5 and Recall metrics on the 29,011-query evaluation set.
    *   `table2_full_corpus.csv`: Full-corpus evaluation on a 100K-passage MS MARCO index.
    *   `table3_statistical_significance.csv`: Wilcoxon signed-rank tests and 95% Bootstrap Confidence Intervals.
    *   `table4_per_dataset.csv`: Dataset breakdown (MS-MARCO, CodeSearchNet, SQuAD, SciQ).
    *   `table5_component_ablation.csv`: 40-distractor injection component ablation on MS MARCO.
    *   `table6_query_type.csv`: Exact-Match vs Semantic query performance breakdown.
    *   `table7_security_evaluation.csv`: Adversarial filtering metrics (ASR, FPR, MRR Drop).
    *   `table8_jailbreak_stress_test.csv`: 8-family public jailbreak stress test.
    *   `table9_threshold_sensitivity.csv`: Threshold ($\tau$) sensitivity for goal-redirection heuristic.
    *   `table10_context_ablation.csv`: Synthetic episodic memory context ablation.
*   `logs/`: Contains configuration files ensuring hyperparameter reproducibility.
    *   `full_corpus_config.json`
    *   `latency_config.json`
    *   `security_baseline_config.json`
    *   `threshold_config.json`
*   `plots/`: Visual output artifacts.
    *   `sensitivity_curve.pdf`: Generates the Security-Accuracy tradeoff curve (Figure 3 in the paper).
    *   `main_retrieval_performance.pdf`: Grouped bar chart comparing MRR@5 and Recall@5 across all systems.
    *   `per_dataset_mrr.pdf`: Visualization of MRR@5 breakdown across MS MARCO, CodeSearchNet, SciQ, and SQuAD.
    *   `query_type_comparison.pdf`: Visualization of exact-match vs semantic intent performance.
    *   `context_ablation.pdf`: Bar chart demonstrating the impact of synthetic episodic memory context.
*   `CogniSync_Final_CIKM_Ablations.ipynb`: The primary experiment notebook generating the empirical results.
*   `pseudocode_and_hyperparameters.md`: Standalone algorithmic descriptions of the Multi-Signal Adversarial Filtering layer, the Learned-Alpha Hybrid Retrieval mechanism, and exact parameter bounds.

## Reproducibility Protocol

To ensure anonymous, zero-fabrication reproducibility without releasing raw codebase scripts during double-blind review, we provide exact pseudocode blocks and precise configuration telemetry:

1.  **Algorithms**: See `pseudocode_and_hyperparameters.md` for exact logic gates, threshold checks, and fusion arithmetic.
2.  **Dataset Revisions (Pinned for Reproducibility):**
    *   `microsoft/ms_marco`: `a47ee7a`
    *   `code_search_net`: `bd0cf26`
    *   `sciq`: `2c94ad3`
    *   `squad`: `7b6d24c`
    *   `deepset/prompt-injections`: `1c5d985` (Security Classifier Baseline)
3.  **Model Revisions (Pinned for Reproducibility):**
    *   Dense Retrieval: `sentence-transformers/all-MiniLM-L6-v2` (`c9745ed`)
    *   Cross-Encoder: `cross-encoder/ms-marco-MiniLM-L-6-v2` (`f956cce`)
4.  **Hardware & Environment Config**: See `logs/` directory for exhaustive hyperparameter json outputs logged during the evaluation runs on the T4 GPU framework.

## Dependencies
*   `torch >= 2.0`
*   `sentence-transformers`
*   `faiss-cpu` (CPU used to prevent Colab GPU OOM constraints during dense index creation)
*   `rank_bm25`
*   `scikit-learn`
*   `datasets`
*   `pandas`, `numpy`
