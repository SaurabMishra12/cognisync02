import os
import random
import time
import json
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import stats
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datasets import load_dataset
import re
import hashlib

# Configuration
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
MODEL_REVISION = 'c9745ed1d9f207416be6d2e6f8de32d1f16199bf'
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', './cstm_rebuttal_output')
os.makedirs(f'{OUTPUT_DIR}/results/', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/logs/', exist_ok=True)

EVAL_K = 5

def stable_id(*parts, prefix='id'):
    joined = '::'.join(str(p) for p in parts)
    digest = hashlib.sha1(joined.encode('utf-8')).hexdigest()[:16]
    return f'{prefix}_{digest}'

def unique_preserve_order(values):
    seen = set()
    out = []
    for value in values:
        text = str(value)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out

class RetrievalSystem:
    def __init__(self):
        self.encoder = SentenceTransformer(MODEL_NAME, revision=MODEL_REVISION)
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)
        self.alpha_model = None

    def _encode_documents(self, documents):
        unique_docs = list(dict.fromkeys(documents))
        unique_embeddings = self.encoder.encode(unique_docs, show_progress_bar=False, batch_size=512)
        embedding_by_doc = dict(zip(unique_docs, unique_embeddings))
        return np.vstack([embedding_by_doc[doc] for doc in documents])

    def extract_features(self, query, documents):
        doc_embeddings = self._encode_documents(documents)
        query_embedding = self.encoder.encode([query], show_progress_bar=False)
        faiss.normalize_L2(doc_embeddings)
        faiss.normalize_L2(query_embedding)
        cpu_index = faiss.IndexFlatIP(doc_embeddings.shape[1])
        cpu_index.add(doc_embeddings)
        dense_scores_raw, dense_indices = cpu_index.search(query_embedding, len(documents))
        dense_full = [int(i) for i in dense_indices[0]]
        dense_sim = np.zeros(len(documents))
        for rank_pos, idx in enumerate(dense_full):
            dense_sim[idx] = float(dense_scores_raw[0][rank_pos])
            
        tokenized_docs = [doc.split() for doc in documents]
        bm25 = BM25Okapi(tokenized_docs)
        bm25_scores = bm25.get_scores(query.split())
        
        d_min, d_max = float(np.min(dense_sim)), float(np.max(dense_sim))
        b_min, b_max = float(np.min(bm25_scores)), float(np.max(bm25_scores))
        norm_dense = (dense_sim - d_min) / (d_max - d_min + 1e-10)
        norm_bm25 = (bm25_scores - b_min) / (b_max - b_min + 1e-10)
        
        dense_std = float(np.std(norm_dense))
        bm25_std = float(np.std(norm_bm25))
        dense_cv = dense_std / (float(np.mean(norm_dense)) + 1e-10)
        bm25_cv = bm25_std / (float(np.mean(norm_bm25)) + 1e-10)
        q_len = len(query.split())
        has_id = 1.0 if re.search(r'\b(id|uuid|hash|key)\b', query, re.IGNORECASE) or re.search(r'0x[0-9a-fA-F]+', query) else 0.0
        
        features = [q_len, dense_std, bm25_std, dense_cv, bm25_cv, has_id]
        return features, norm_dense, norm_bm25, dense_full, dense_sim, bm25_scores

    def retrieve_ablations(self, query, documents, top_k=None):
        if not documents:
            return None
        limit = len(documents) if top_k is None else min(top_k, len(documents))

        features, norm_dense, norm_bm25, dense_full, dense_sim, bm25_scores = self.extract_features(query, documents)
        lex_full = [int(i) for i in np.argsort(bm25_scores)[::-1]]
        dense_ranks = {idx: rank for rank, idx in enumerate(dense_full)}
        lex_ranks = {idx: rank for rank, idx in enumerate(lex_full)}

        # Naive RRF
        k_rrf = 60
        hybrid_scores = {}
        for idx in range(len(documents)):
            rank_dense = dense_ranks.get(idx, len(documents)) + 1
            rank_lex = lex_ranks.get(idx, len(documents)) + 1
            hybrid_scores[idx] = (1 / (k_rrf + rank_dense)) + (1 / (k_rrf + rank_lex))
        hybrid_full = sorted(hybrid_scores.keys(), key=lambda x: hybrid_scores[x], reverse=True)

        # Learned Alpha
        if self.alpha_model is not None:
            alpha = float(self.alpha_model.predict([features])[0])
            alpha = max(0.0, min(1.0, alpha))
        else:
            dense_cv, bm25_cv = features[3], features[4]
            raw_alpha = dense_cv / (dense_cv + bm25_cv + 1e-10)
            alpha = 0.3 + 0.4 * raw_alpha

        d_max = float(np.max(dense_sim))
        bm25_cv = features[4]
        if d_max > 0.85 or bm25_cv < 0.1:
            alpha = 1.0 

        adaptive_scores = {}
        for idx in range(len(documents)):
            adaptive_scores[idx] = alpha * norm_dense[idx] + (1 - alpha) * norm_bm25[idx]
        adaptive_full = sorted(adaptive_scores.keys(), key=lambda x: adaptive_scores[x], reverse=True)
        
        # Dense + CE
        top_n = min(10, len(dense_full))
        rerank_candidates = dense_full[:top_n]
        if len(rerank_candidates) > 1:
            pairs = [[query, documents[idx]] for idx in rerank_candidates]
            ce_scores = self.cross_encoder.predict(pairs, show_progress_bar=False)
            candidate_scores = {idx: score for idx, score in zip(rerank_candidates, ce_scores)}
            reranked_top = sorted(candidate_scores.keys(), key=lambda x: candidate_scores[x], reverse=True)
            dense_ce_full = reranked_top + dense_full[top_n:]
        else:
            dense_ce_full = dense_full

        # Naive RRF + CE
        top_n = min(10, len(hybrid_full))
        rerank_candidates = hybrid_full[:top_n]
        if len(rerank_candidates) > 1:
            pairs = [[query, documents[idx]] for idx in rerank_candidates]
            ce_scores = self.cross_encoder.predict(pairs, show_progress_bar=False)
            candidate_scores = {idx: score for idx, score in zip(rerank_candidates, ce_scores)}
            reranked_top = sorted(candidate_scores.keys(), key=lambda x: candidate_scores[x], reverse=True)
            hybrid_ce_full = reranked_top + hybrid_full[top_n:]
        else:
            hybrid_ce_full = hybrid_full

        # CogniSync (Learned Alpha + CE)
        top_n = min(10, len(adaptive_full))
        rerank_candidates = adaptive_full[:top_n]
        if len(rerank_candidates) > 1:
            pairs = [[query, documents[idx]] for idx in rerank_candidates]
            ce_scores = self.cross_encoder.predict(pairs, show_progress_bar=False)
            candidate_scores = {idx: score for idx, score in zip(rerank_candidates, ce_scores)}
            reranked_top = sorted(candidate_scores.keys(), key=lambda x: candidate_scores[x], reverse=True)
            cognisync_full = reranked_top + adaptive_full[top_n:]
        else:
            cognisync_full = adaptive_full

        return {
            'Dense': dense_full[:limit],
            'Sparse': lex_full[:limit],
            'Naive RRF': hybrid_full[:limit],
            'Dense + CE': dense_ce_full[:limit],
            'Naive RRF + CE': hybrid_ce_full[:limit],
            'Learned-Alpha Only': adaptive_full[:limit],
            'CogniSync (Learned-Alpha + CE)': cognisync_full[:limit]
        }

def compute_mrr(retrieved, relevant, k=5):
    relevant_set = set(relevant)
    if not relevant_set: return 0.0
    for rank, idx in enumerate(retrieved[:k]):
        if idx in relevant_set:
            return 1.0 / (rank + 1)
    return 0.0

def train_alpha_predictor(tuning_set, retrieval_sys):
    print("Training Regression Alpha model on tuning set...")
    X, y = [], []
    for item in tqdm(tuning_set[:300]):
        q = item['query']
        docs = item['documents']
        rels = set(item['relevant_indices'])
        
        features, norm_dense, norm_bm25, _, _, _ = retrieval_sys.extract_features(q, docs)
        best_alpha, best_mrr = 0.5, -1.0
        for alpha in np.linspace(0.0, 1.0, 11):
            adaptive_scores = {}
            for idx in range(len(docs)):
                adaptive_scores[idx] = alpha * norm_dense[idx] + (1 - alpha) * norm_bm25[idx]
            ranked = sorted(adaptive_scores.keys(), key=lambda x: adaptive_scores[x], reverse=True)
            mrr = compute_mrr(ranked, rels, k=5)
            if mrr > best_mrr:
                best_mrr = mrr
                best_alpha = alpha
        X.append(features)
        y.append(best_alpha)
        
    model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=RANDOM_SEED)
    model.fit(X, y)
    retrieval_sys.alpha_model = model

def bootstrap_ci(data, n_bootstraps=1000, ci=95):
    bootstrapped_means = []
    for _ in range(n_bootstraps):
        sample = np.random.choice(data, size=len(data), replace=True)
        bootstrapped_means.append(np.mean(sample))
    lower = np.percentile(bootstrapped_means, (100 - ci) / 2)
    upper = np.percentile(bootstrapped_means, 100 - (100 - ci) / 2)
    return lower, upper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full-benchmark', action='store_true')
    parser.add_argument('--limit', type=int, default=6980)
    args = parser.parse_args()

    # We load microsoft/ms_marco v1.1 validation to mimic exactly the v3 strong pipeline's per-query ranking
    # The validation split of v1.1 has exactly 100,470 queries. The 6,980 number is from Tevatron validation.
    # To keep it completely strictly 6,980 MS MARCO queries, we select the first 6,980 from microsoft/ms_marco validation.
    print(f"Loading microsoft/ms_marco v1.1 validation (subset: {args.limit} queries)...")
    ds = load_dataset('microsoft/ms_marco', 'v1.1', split='validation', revision='a47ee7aae8d7d466ba15f9f0bfac3b3681087b3a')
    ds = ds.shuffle(seed=RANDOM_SEED)
    
    raw = []
    for row_idx, item in enumerate(tqdm(ds.select(range(min(len(ds), args.limit))), desc="Normalizing")):
        query = str(item.get('query', '')).strip()
        docs = item.get('passages', {}).get('passage_text', [])
        selected = item.get('passages', {}).get('is_selected', [])
        rel_source_indices = [i for i, flag in enumerate(selected) if flag == 1]
        if not query or not docs or not rel_source_indices: continue
        unique_docs = unique_preserve_order(docs)
        relevant_indices = [unique_docs.index(str(docs[i])) for i in rel_source_indices if str(docs[i]) in unique_docs]
        relevant_indices = sorted(set(relevant_indices))
        if not relevant_indices: continue
        raw.append({
            'query': query,
            'documents': unique_docs,
            'relevant_indices': relevant_indices
        })
        if len(raw) >= args.limit: break

    print(f"Loaded {len(raw)} valid queries for evaluation.")
    
    tuning_set, test_set = train_test_split(raw, test_size=0.85, random_state=RANDOM_SEED)
    print(f"Tuning set: {len(tuning_set)}, Test set: {len(test_set)}")

    retrieval_system = RetrievalSystem()
    train_alpha_predictor(tuning_set, retrieval_system)

    results_mrr = {
        'Dense': [], 'Sparse': [], 'Naive RRF': [], 
        'Dense + CE': [], 'Naive RRF + CE': [], 
        'Learned-Alpha Only': [], 'CogniSync (Learned-Alpha + CE)': []
    }

    for item in tqdm(test_set, desc="Evaluating Variants"):
        ranks = retrieval_system.retrieve_ablations(item['query'], item['documents'])
        if not ranks: continue
        for variant, ranked_list in ranks.items():
            results_mrr[variant].append(compute_mrr(ranked_list, item['relevant_indices'], k=5))

    # Significance Testing (Wilcoxon) vs CogniSync Full
    base_variant = 'CogniSync (Learned-Alpha + CE)'
    base_scores = np.array(results_mrr[base_variant])
    
    stats_records = []
    num_comparisons = len(results_mrr) - 1
    alpha_corrected = 0.05 / num_comparisons

    for variant, scores in results_mrr.items():
        arr = np.array(scores)
        mean_mrr = np.mean(arr)
        lower, upper = bootstrap_ci(arr)
        
        if variant == base_variant:
            p_val = 1.0
            sig = "-"
        else:
            diffs = arr - base_scores
            if np.all(diffs == 0):
                p_val = 1.0
            else:
                _, p_val = stats.wilcoxon(arr, base_scores, alternative='two-sided')
            sig = "Yes" if p_val < alpha_corrected else "No"
            
        stats_records.append({
            "Variant": variant,
            "MRR@5": mean_mrr,
            "95% CI Lower": lower,
            "95% CI Upper": upper,
            "Wilcoxon p-value": p_val,
            f"Significant (p<{alpha_corrected:.4f})": sig
        })
        
    df_stats = pd.DataFrame(stats_records)
    df_stats.to_csv(f"{OUTPUT_DIR}/results/ablation_fusion_ce_stats.csv", index=False)
    print(df_stats.to_string())

if __name__ == "__main__":
    main()
