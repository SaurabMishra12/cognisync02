# CogniSync CIKM Empirical Evaluation Suite

This document outlines the final evaluation suite and ablation studies conducted to address reviewer concerns for the CIKM 2026 submission. The empirical methodology relies strictly on rigorous statistical reporting, isolated component ablations, and scalable hybrid indexing architectures.

## 1. Hybrid Component Ablation
**Objective**: To disentangle the performance contributions of the Learned-Alpha Adaptive Fusion from the Cross-Encoder reranking, proving that the fusion logic contributes independently of the heavy reranker.

**Methodology**:
We evaluate 7 architectural variants on the public validation split of MS MARCO (`v1.1`, $n=6,980$). The components evaluated include Dense Only (`all-MiniLM-L6-v2`), Sparse Only (`BM25Okapi`), Naive Rank-Based RRF, and our CogniSync Full System.
- **Statistical Rigor**: 95% Bootstrap Confidence Intervals are reported for all MRR@5 scores. Statistical significance is computed against the full CogniSync system using a **Wilcoxon signed-rank test** coupled with a **Bonferroni correction** ($\alpha = 0.05 / 6 = 0.0083$).

**Execution Script**: `ablation_fusion_reranker.py`
*(To execute on full public candidate pool instead of just MS MARCO, append the `--full-benchmark` flag).*

## 2. Security Component Ablation
**Objective**: To validate that the custom Goal-Redirection Heuristic improves security filtering above a standard machine-learning baseline.

**Methodology**:
We evaluate against the standard `deepset/prompt-injections` dataset.
- **Dataset Composition**: **343 Benign** instances, **203 Malicious** instances.
- **Evaluation**: We report Macro F1 and per-class F1 to account for the class imbalance.

**Results** (Generated locally via `ablation_security.py`):
| Variant | Benign F1 | Malicious F1 | Macro F1 |
| :--- | :--- | :--- | :--- |
| **Classifier Only Baseline** | 0.893 | 0.810 | 0.851 |
| **Classifier + Goal-Redirection** | **0.900** | **0.825** | **0.862** |

*Conclusion: The heuristic safely increases both Benign and Malicious F1 scores.*

## 3. Full-Corpus Validation & Significance Testing
**Objective**: To prove that the hybrid architecture successfully scales to massive distractors without deteriorating performance, and to prove the margin of improvement is statistically significant.

**Methodology**:
We inject 500 evaluation queries into a 100,000-passage MS MARCO distractor corpus. We compute the per-query MRR@10 for the Dense baseline and the Hybrid pipeline. We then run a paired Wilcoxon signed-rank test to calculate the `p-value` for the $+0.19$ percentage point margin.

**Execution Script**: `calc_full_corpus_significance.py`

---

## Instructions for GitHub Reproducibility
To execute these scripts and generate the final `p-values` and CSV artifacts for the paper:
1. Ensure you are running on an environment with CUDA available (e.g., Kaggle T4x2 or Google Colab) to prevent the FAISS encoding from running slowly on CPU.
2. Run `python calc_full_corpus_significance.py` to generate the Wilcoxon p-value for the $+0.19$ pp full-corpus margin.
3. Run `python ablation_fusion_reranker.py` to generate the massive MRR@5 bootstrap tables.
4. Update the abstract and conclusion of the LaTeX manuscript to feature the balanced reporting of the **+2.75 pp** margin (Public Benchmark) and the **+0.19 pp** margin (Full-Corpus 100K).
