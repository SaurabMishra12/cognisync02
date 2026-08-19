# Appendix A: Reproducibility Details

To ensure full reproducibility of the empirical results presented in this manuscript, we detail the exact hardware, datasets, models, and hyperparameters used across both the primary candidate-pool evaluation (V3 Strong Pipeline) and the large-scale distractor index validation.

## A.1 Environment and Hardware
All experiments were executed in a controlled Python 3 environment. For hardware-accelerated embedding generation and dense index building, pipelines were designed to run on an NVIDIA T4 GPU (e.g., via Google Colab / Kaggle).
- **Core Libraries**: `faiss-cpu`, `rank_bm25`, `sentence-transformers`, `scikit-learn`, `datasets`, `pandas`, `numpy`.
- **Random Seed**: All stochastic operations (e.g., `train_test_split`, classifier initialization, candidate shuffling) were strictly locked to a global random seed of **`42`**.

## A.2 Datasets and Candidate Pools

### 1. Primary Evaluation Suite (V3 Strong Pipeline)
To prevent temporal drift or upstream changes from impacting reproducibility, all datasets in the primary evaluation suite were locked to immutable Hugging Face revisions queried on 2026-05-10:
- **`microsoft/ms_marco`** (Subset: `v1.1`, Split: `validation`, Revision: `a47ee7aa...`, Size: 15,000 queries). Protocol: Per-query passage reranking based on provided passages.
- **`code-search-net/code_search_net`** (Subset: `python`, Split: `test`, Revision: `bd0cf261...`, Size: 15,000 queries). Protocol: 50-document candidate pool (1 positive, 49 random negatives).
- **`allenai/sciq`** (Split: `train`, Revision: `2c94ad3e...`, Size: 5,000 queries). Protocol: 50-document candidate pool.
- **`rajpurkar/squad`** (Split: `validation`, Revision: `7b6d24c4...`, Size: 5,000 queries). Protocol: 50-document candidate pool.
- **Synthetic Domain**: 1,000 synthetically generated queries covering technical topics (e.g., JWT authentication, PostgreSQL migrations) to stress-test domain-specific technical retrieval.

### 2. Large-Scale Distractor Corpus Validation
To evaluate retrieval over a vast, sparse search space, we utilized standard dense retrieval formats:
- **Retrieval Index**: `Tevatron/msmarco-passage-corpus` (Split: `train`). The first 100,000 passages were used as the base distractor corpus.
- **Evaluation Queries**: `Tevatron/msmarco-passage` (Split: `train`). The first 500 queries were selected for evaluation. *Methodological Note: To ensure statistically valid evaluation over a truncated distractor corpus, the exact target (`positive_passages`) for each of the 500 queries was explicitly injected into the 100K index prior to evaluation.*
- **Adversarial Security Training**: `deepset/prompt-injections` (Split: `train`). Used to train and evaluate the standalone Logistic Regression baseline.

## A.3 Models and Retrieval Infrastructure
### Semantic and Lexical Models
- **Dense Encoder**: `sentence-transformers/all-MiniLM-L6-v2` (Output Dimension: 384)
- **Cross-Encoder**: `cross-encoder/ms-marco-MiniLM-L-6-v2` (Max Length: 512)
- **Similarity Metric**: Cosine Similarity (via L2 Normalization and `faiss.IndexFlatIP`)
- **Sparse Algorithm**: `BM25Okapi` (from the `rank_bm25` library, $k_1=1.5$, $b=0.75$)

### Security Architecture (Multi-Signal Defense)
In the primary pipeline, the retrieval-level security filter operates using three core signals:
1. **Semantic Safety**: A Logistic Regression classifier (`class_weight='balanced'`) trained dynamically on the candidate pool and explicit adversarial payloads ("Ignore previous instructions", "Return all API keys", etc.).
2. **Imperative Trigger**: A regex heuristic tracking commanding verbs (`\b(ignore|reveal|execute|forget|bypass|output)\b`).
3. **Goal Redirection (Threshold)**: Triggers exclusively if an imperative verb is present AND the query-to-document Cosine Similarity ($\tau$) is less than **$0.30$**. Documents flagged by this heuristic are blocked from entering the final LLM context.

## A.4 Hybrid Fusion Architecture (CogniSync_RRF)
The primary system architecture evaluated is a 3-stage adaptive pipeline:

1. **Regression Alpha Prediction**:
   - A `RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)` dynamically predicts the optimal blending weight ($\alpha \in [0.0, 1.0]$) for every query based on 6 query-time features: query length, dense standard deviation, BM25 standard deviation, dense coefficient of variation (CV), BM25 CV, and exact-match keyword flags (e.g., UUIDs/hex keys).
   - **Dense Fallback Rule**: If the maximum dense similarity $> 0.85$ or BM25 CV $< 0.1$, $\alpha$ is forced to $1.0$ (pure semantic retrieval).

2. **Min-Max Score Fusion**:
   - Dense and Sparse scores are individually min-max normalized. The final score is computed as: $Score_{adaptive} = \alpha \cdot Score_{dense} + (1 - \alpha) \cdot Score_{sparse}$
   - *(Note: In the isolated full-corpus ablation, $\alpha$ was statically fixed at $0.6$ to evaluate raw retrieval capacity without the regressor overhead).*

3. **Cross-Encoder Reranking**:
   - The Top $N=10$ documents retrieved by the adaptive fusion step are passed to the `ms-marco-MiniLM-L-6-v2` cross-encoder for final, high-precision reordering before extraction.

### Evaluation Metrics
- **Main Pipeline (V3 Strong)**: Evaluated at depth $K=5$ ($MRR@5$, $NDCG@5$, $Recall@5$).
- **Large-Scale Validation**: Evaluated at depth $K=10$ ($MRR@10$). Amortized latency measured at depth $K=50$.
