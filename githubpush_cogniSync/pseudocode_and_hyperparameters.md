# CogniSync Pseudocode & Configuration

To preserve double-blind anonymity, we provide high-level pseudocode and all principal hyperparameters, while withholding the full source code and exact engineering utilities. The described algorithms and configurations are sufficient to understand the methodological design and independently validate our claims.

## Algorithm 1: Multi-Signal Adversarial Filtering

```text
Require: chunk c; mean clean embedding μ; logistic classifier F; query embedding q_emb
Ensure: decision ∈ {admit, filter}

1:  Encode c to embedding e_c
2:  s_cos ← cos(e_c / ||e_c||, μ)
3:  has_imperative ← 1 [c matches I]  {I: {ignore, reveal, execute, forget, bypass, output}}
4:  len_ratio ← |c| / |c_clean|
5:  p ← F([s_cos, has_imperative, len_ratio])
6:  if p > 0.5 then
7:      return filter
8:  end if
9:  if has_imperative = 1 and cos(e_c / ||e_c||, q_emb) < 0.3 then
10:     return filter   {goal-redirection heuristic}
11: end if
12: return admit
```

## Algorithm 2: Learned-Alpha Hybrid Retrieval

```text
Require: query q; candidate documents D; Random Forest Regressor R; Cross-Encoder C
Ensure: ranked list D_ranked

1: dense_scores ← normalize(FAISS.search(q, D))
2: lexical_scores ← normalize(BM25.search(q, D))
3: features ← extract_features(q, dense_scores, lexical_scores)
4: alpha ← clip(R.predict(features), 0, 1)
5: fusion_scores[d] ← alpha · dense_scores[d] + (1 - alpha) · lexical_scores[d]
6: D_fused ← sort_descending(fusion_scores)
7: D_topK ← top_k(D_fused, 10)
8: rerank_scores[d] ← C.predict(q, d)
9: D_ranked ← append(sort_descending(rerank_scores), D_fused[10:])
10: return D_ranked
```

## Principal Hyperparameters & Models

*   **Dense Model**: `sentence-transformers/all-MiniLM-L6-v2`
*   **Cross-Encoder**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
*   **Learned-Alpha Regressor**: `RandomForestRegressor(n_estimators=50, max_depth=5)`
*   **Security Classifier**: Logistic Regression with `class_weight='balanced'`
*   **Random Seed**: `42`
*   **Cross-Encoder Max Tokens**: `512`
*   **BM25 Parameters**: `k1=1.5`, `b=0.75`
*   **Goal-Redirection Threshold**: $\tau = 0.30$
