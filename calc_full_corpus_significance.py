import os
import json
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss
import torch
from scipy import stats

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', './cstm_rebuttal_output')
os.makedirs(f'{OUTPUT_DIR}/results/', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/logs/', exist_ok=True)

print("CUDA Available:", torch.cuda.is_available())
encoder = SentenceTransformer(MODEL_NAME)
if torch.cuda.is_available():
    encoder = encoder.to('cuda')

class PersistentHybridIndex:
    def __init__(self, encoder):
        self.encoder = encoder
        self.faiss_index = None
        self.bm25 = None
        self.doc_store = []
        
    def build(self, documents, batch_size=256):
        self.doc_store = documents
        embs = self.encoder.encode(documents, show_progress_bar=True, batch_size=batch_size)
        faiss.normalize_L2(embs)
        d = embs.shape[1]
        self.faiss_index = faiss.IndexFlatIP(d)
        self.faiss_index.add(embs)
        
        tokenized = [doc.split() for doc in tqdm(documents, desc="Tokenizing for BM25")]
        self.bm25 = BM25Okapi(tokenized)
        print(f"Index built with {len(self.doc_store)} documents.")
        
    def retrieve(self, query, top_k=100, alpha=0.5):
        t0 = time.time()
        q_emb = self.encoder.encode([query], show_progress_bar=False)
        faiss.normalize_L2(q_emb)
        d_scores, d_idx = self.faiss_index.search(q_emb, top_k * 2)
        
        q_tokens = query.split()
        b_scores = self.bm25.get_scores(q_tokens)
        b_idx = np.argsort(b_scores)[::-1][:top_k * 2]
        
        dense_norm = {idx: (d_scores[0][i] - np.min(d_scores[0])) / (np.max(d_scores[0]) - np.min(d_scores[0]) + 1e-10) for i, idx in enumerate(d_idx[0])}
        
        b_rel_scores = [b_scores[i] for i in b_idx]
        b_min, b_max = np.min(b_rel_scores), np.max(b_rel_scores)
        bm25_norm = {idx: (b_scores[idx] - b_min) / (b_max - b_min + 1e-10) for idx in b_idx}
        
        fusion_scores = {}
        all_candidates = set(d_idx[0]) | set(b_idx)
        for idx in all_candidates:
            d_val = dense_norm.get(idx, 0.0)
            b_val = bm25_norm.get(idx, 0.0)
            fusion_scores[idx] = alpha * d_val + (1 - alpha) * b_val
            
        ranked = sorted(fusion_scores.keys(), key=lambda x: fusion_scores[x], reverse=True)[:top_k]
        latency = time.time() - t0
        dense_only = list(d_idx[0])[:top_k]
        
        return ranked, dense_only, latency

def main():
    print("Loading MS MARCO (subset=100K) from Hugging Face...")
    marco_ds = load_dataset('Tevatron/msmarco-passage-corpus', split='train')
    marco_subset = marco_ds.select(range(100000))

    marco_queries = load_dataset('Tevatron/msmarco-passage', split='train')
    q_subset = marco_queries.select(range(500))

    print("Injecting positive passages into corpus to guarantee evaluation...")
    documents = list(marco_subset['text'])
    all_docids = list(marco_subset['docid'])

    for item in q_subset:
        for p in item['positive_passages']:
            if p['docid'] not in all_docids:
                documents.append(p['text'])
                all_docids.append(p['docid'])

    print(f"Final corpus size including injected targets: {len(documents)}")

    hybrid_index = PersistentHybridIndex(encoder)
    hybrid_index.build(documents, batch_size=512)

    docid_to_idx = {str(docid): i for i, docid in enumerate(tqdm(all_docids, desc="Mapping DocIDs"))}

    eval_queries = []
    for item in q_subset:
        pos_docids = [str(p['docid']) for p in item['positive_passages']]
        valid_idxs = [docid_to_idx[did] for did in pos_docids if did in docid_to_idx]
        if valid_idxs:
            eval_queries.append((item['query'], valid_idxs))

    print(f"Found {len(eval_queries)} queries where the relevant passage exists within our subset.")

    mrr_hybrid = []
    mrr_dense = []

    for q, rel_idxs in tqdm(eval_queries):
        ranked_hybrid, ranked_dense, _ = hybrid_index.retrieve(q, top_k=10, alpha=0.6)
        
        h_mrr = 0.0
        for rank, idx in enumerate(ranked_hybrid):
            if idx in rel_idxs:
                h_mrr = 1.0 / (rank + 1)
                break
        mrr_hybrid.append(h_mrr)
        
        d_mrr = 0.0
        for rank, idx in enumerate(ranked_dense):
            if idx in rel_idxs:
                d_mrr = 1.0 / (rank + 1)
                break
        mrr_dense.append(d_mrr)

    # Save raw arrays
    raw_df = pd.DataFrame({
        "Query_ID": range(len(eval_queries)),
        "MRR_Hybrid": mrr_hybrid,
        "MRR_Dense": mrr_dense
    })
    raw_df.to_csv(f"{OUTPUT_DIR}/results/full_corpus_raw_mrr.csv", index=False)

    final_mrr_hybrid = np.mean(mrr_hybrid) if mrr_hybrid else 0
    final_mrr_dense = np.mean(mrr_dense) if mrr_dense else 0
    
    print(f"Hybrid MRR@10 (100K Corpus): {final_mrr_hybrid:.4f}")
    print(f"Dense-Only MRR@10 (100K Corpus): {final_mrr_dense:.4f}")

    # Significance Test
    differences = np.array(mrr_hybrid) - np.array(mrr_dense)
    if np.all(differences == 0):
        p_val = 1.0
        print("No difference between Hybrid and Dense MRR arrays. p-value = 1.0")
    else:
        stat, p_val = stats.wilcoxon(mrr_hybrid, mrr_dense, alternative='two-sided')
        print(f"Wilcoxon signed-rank test: statistic={stat}, p-value={p_val}")

    with open(f"{OUTPUT_DIR}/logs/full_corpus_significance.json", "w") as f:
        json.dump({
            "eval_queries": len(eval_queries),
            "hybrid_mrr_10": final_mrr_hybrid,
            "dense_mrr_10": final_mrr_dense,
            "margin": final_mrr_hybrid - final_mrr_dense,
            "wilcoxon_p_value": p_val
        }, f, indent=4)

if __name__ == "__main__":
    main()
