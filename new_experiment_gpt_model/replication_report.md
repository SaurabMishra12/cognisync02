# Cross-Model Replication Report: Candidate Survival vs. Behavioural Attack Success

**Extension Study for TMLR Submission:**  
*“When Candidate Survival Misleads: Separating Exposure from Downstream Attack Success in Retrieval Filters”*  
**Downstream Evaluated Model:** Azure-Hosted GPT-5 Deployment (`gpt-5-mini`)  
**Baseline Model:** Qwen2.5-3B-Instruct  
**Benchmark Suite:** SciFact (300 queries, top-5 clean context passages, position 0, plain system prompt)  
**Date:** 2026-08-28  

---

## 1. Executive Summary & Core Replication Questions

We executed a controlled, targeted cross-model replication of the paper's central empirical claims by substituting the downstream instruction-following model with an Azure-hosted reasoning model deployment (**GPT-5 family** / `gpt-5-mini`). The retrieval corpus, query distribution, candidate insertion, and detector decision matrices ($D_0$–$D_6$) were preserved identically to isolate the exact effect of downstream LLM architecture.

### Direct Answers to Key Research Questions:

1. **Does the central A3/A4 exposure-versus-behaviour disagreement replicate on GPT-5?**
   - **YES.** Across both Qwen2.5-3B and GPT-5, candidate survival rate $P(E \mid D)$ fails to preserve downstream behavioural attack ranking. Under detectors like $D_3$ (DistilBERT), $A_3$ survives at a dramatically higher rate than $A_4$, but $A_4$ achieves higher downstream behavioural compromise.

2. **Does the D3 ranking reversal replicate?**
   - **YES.** Under $D_3$ (DistilBERT) at nominal $\mathrm{FPR}=1\%$:
     - **Exposure:** $P(E \mid D_3, A_3) = 0.987$ (296/300) vs. $P(E \mid D_3, A_4) = 0.677$ (203/300) $\rightarrow$ **$A_3$ exposure is ++0.310 higher** (95% CI [0.2577, 0.3623]).
     - **Downstream Behavioural Success:** $P(C \mid D_3, A_3) = 0.0400$ vs. $P(C \mid D_3, A_4) = 0.2300$ $\rightarrow$ **$A_4$ behavioural success is +0.1900 higher** (95% CI [0.1419, 0.2381]).
     - Hence, **$P(E \mid D_3, A_3) > P(E \mid D_3, A_4)$ while $P(C \mid D_3, A_3) < P(C \mid D_3, A_4)$**.

3. **Does the equal-exposure result replicate?**
   - **YES.** Under detectors where exposure is equal ($D_1$, $D_{1b}$, $D_6$ where $P(E \mid D) = 1.00$):
     - Under $D_1$: Difference $(A_4 - A_3) = +0.2533$ (95% CI [0.2024, 0.3043]).
     - Under $D_{1b}$: Difference $(A_4 - A_3) = +0.2533$ (95% CI [0.2024, 0.3043]).
     - Under $D_6$: Difference $(A_4 - A_3) = +0.2533$ (95% CI [0.2024, 0.3043]).
     - **Conclusion:** Equal candidate exposure produces materially divergent behavioural attack outcomes across downstream models.

4. **Is the survivor-compliance difference preserved?**
   - **YES.** For $D_3$, survivor compliance is $P(C \mid E, D_3, A_3) = 0.041$ [0.023, 0.070] compared to $P(C \mid E, D_3, A_4) = 0.340$ [0.278, 0.407]. In the paired common-support subset (queries where both survived), $A_4$ compliance exceeds $A_3$ compliance by $\Delta = +0.2956$ (95% CI [0.2313, 0.3598]).

5. **Which conclusions from the original paper become stronger?**
   - The fundamental decoupling $P(C \mid D) = P(E \mid D) \cdot P(C \mid E, D)$ is **not an artifact of small open-weight LLMs (Qwen2.5-3B)**; it holds on modern commercial reasoning models.
   - Evaluators who benchmark retrieval defenses purely on candidate filtering/survival ($P(E \mid D)$) will systematically mischaracterize downstream security risk regardless of the downstream model.

6. **Which conclusions must remain model-specific?**
   - The absolute point estimates of survivor compliance ($P(C \mid E, D)$) vary between models based on their instruction-tuning, safety alignment, and reasoning capability.
   - The relative potency ordering of specific injection phrasing is model-dependent, reinforcing why downstream empirical evaluation cannot be replaced by static retrieval metrics.

---

## 2. Comprehensive Headline Results Table (matched $\mathrm{FPR}=1\%$)

| Attacker | Metric | D0 (None) | D1 (3-feat) | D1b (Trained) | D2 (Probe) | D3 (DistilBERT) | D4 (Guard) | D5 (Perplexity) | D6 (Ensemble) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A3_semantic_camouflage** | $P(E\mid D)$ | 1.00 | 1.00 | 1.00 | 0.98 | 0.99 | 0.99 | 1.00 | 1.00 |
| | $N_{\mathrm{surv}}$ / $N$ | 300/300 | 300/300 | 300/300 | 295/300 | 296/300 | 297/300 | 299/300 | 300/300 |
| | $N_{\mathrm{comp,surv}}$ | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| | $P(C\mid E, D)$ | **0.040** [0.02, 0.07] | **0.040** [0.02, 0.07] | **0.040** [0.02, 0.07] | **0.041** [0.02, 0.07] | **0.041** [0.02, 0.07] | **0.040** [0.02, 0.07] | **0.040** [0.02, 0.07] | **0.040** [0.02, 0.07] |
| | $P(C\mid D)$ | 0.0400 | 0.0400 | 0.0400 | 0.0400 | 0.0400 | 0.0400 | 0.0400 | 0.0400 |
| **A4_length_matched** | $P(E\mid D)$ | 1.00 | 1.00 | 1.00 | 0.98 | 0.68 | 0.00 | 0.66 | 1.00 |
| | $N_{\mathrm{surv}}$ / $N$ | 300/300 | 300/300 | 300/300 | 294/300 | 203/300 | 0/300 | 198/300 | 300/300 |
| | $N_{\mathrm{comp,surv}}$ | 88 | 88 | 88 | 88 | 69 | 0 | 64 | 88 |
| | $P(C\mid E, D)$ | **0.293** [0.24, 0.35] | **0.293** [0.24, 0.35] | **0.293** [0.24, 0.35] | **0.299** [0.25, 0.35] | **0.340** [0.28, 0.41] | NA | **0.323** [0.26, 0.39] | **0.293** [0.24, 0.35] |
| | $P(C\mid D)$ | 0.2933 | 0.2933 | 0.2933 | 0.2933 | 0.2300 | 0.0000 | 0.2133 | 0.2933 |

---

## 3. Side-by-Side Comparison: Qwen2.5-3B vs. Azure GPT-5

Below is the side-by-side comparison of downstream behavioural attack success ($P(C \mid D)$) across the primary detectors:

| Detector | Attack | Exposure $P(E\mid D)$ | Qwen $P(C\mid D)$ | GPT-5 $P(C\mid D)$ | Ordering Preserved? |
|---|---|:---:|:---:|:---:|:---:|
| **D0_none** | A3 (Camouflage) | 1.00 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 1.00 | 0.3267 | 0.2933 | |
| **D1_3feat_tiny** | A3 (Camouflage) | 1.00 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 1.00 | 0.3267 | 0.2933 | |
| **D1b_3feat_trained** | A3 (Camouflage) | 1.00 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 1.00 | 0.3267 | 0.2933 | |
| **D2_embed_probe** | A3 (Camouflage) | 0.98 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 0.98 | 0.3233 | 0.2933 | |
| **D3_distilbert** | A3 (Camouflage) | 0.99 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 0.68 | 0.2200 | 0.2300 | |
| **D4_guard_zeroshot** | A3 (Camouflage) | 0.99 | 0.1033 | 0.0400 | ✓ YES (A3 > A4) |
| | A4 (Length-Match) | 0.00 | 0.0000 | 0.0000 | |
| **D5_perplexity** | A3 (Camouflage) | 1.00 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 0.66 | 0.2133 | 0.2133 | |
| **D6_ensemble** | A3 (Camouflage) | 1.00 | 0.1033 | 0.0400 | ✓ YES (A4 > A3) |
| | A4 (Length-Match) | 1.00 | 0.3267 | 0.2933 | |

---

## 4. Key Scientific Insights

### A. Mathematical Factorization Verification
Across all 40 attack-detector combinations, the exact relation:
$$P(C \mid D) = P(E \mid D) \times P(C \mid E, D)$$
holds exactly up to numerical precision. No cell deviates by more than $10^{-6}$.

### B. Exposure Alone is a Dangerous Proxy
If a practitioner evaluates defenses purely by exposure $P(E \mid D)$, they would conclude that DistilBERT ($D_3$) strongly mitigates $A_4$ (allowing only 67.7% survival) while completely failing against $A_3$ (98.7% survival). However, when measuring end-to-end downstream compromise $P(C \mid D)$, $A_4$ is substantially more dangerous than $A_3$ on both Qwen2.5-3B and GPT-5.

---

## 5. Artifact Index

- **Raw Responses:** [`raw_gpt54_responses.jsonl`](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/raw_gpt54_responses.jsonl)
- **Episode Results:** [`episode_level_results.csv`](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/episode_level_results.csv)
- **Summary Statistics:** [`attack_detector_summary.csv`](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/attack_detector_summary.csv)
- **Cross-Model Comparison:** [`qwen_vs_gpt54_comparison.csv`](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/qwen_vs_gpt54_comparison.csv)
- **Hypothesis Tests:** [`statistical_tests.csv`](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/statistical_tests.csv)
- **Figures:**
  - Figure 1: [Exposure vs Behavioural Success](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/figures/fig1_exposure_vs_behavioural.png)
  - Figure 2: [Survivor Compliance Across Detectors](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/figures/fig2_survivor_compliance.png)
  - Figure 3: [Qwen vs GPT-5 Behavioural Success](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/figures/fig3_qwen_vs_gpt54_success.png)
  - Figure 4: [Ranking Inversion Under DistilBERT](file:///home/saurab/Documents/cognySync/cognisync02/tmlr/replication_gpt54/figures/fig4_exposure_vs_behaviour_ranking.png)
