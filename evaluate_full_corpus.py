import os
import json
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from datasets import load_dataset
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder

CORPUS_SIZE = 1000 # 1k shared corpus for tractability
NUM_QUERIES = 10
K = 60
EVAL_K = 10

print("Loading MS MARCO dataset (subset)...")
# Load a small slice of MS MARCO
corpus_ds = load_dataset('ms_marco', 'v1.1', split='train', streaming=True)

queries = []
documents = []
relevant_map = {} # query -> doc text

print("Extracting queries and docs...")
for item in corpus_ds:
    q = item['query']
    passages = item['passages']['passage_text']
    is_selected = item['passages']['is_selected']
    
    # find the relevant passage
    rel_idx = -1
    for i, sel in enumerate(is_selected):
        if sel == 1:
            rel_idx = i
            break
            
    if rel_idx != -1 and q not in queries:
        queries.append(q)
        rel_doc = passages[rel_idx]
        relevant_map[q] = rel_doc
        if rel_doc not in documents:
            documents.append(rel_doc)
            
    if len(queries) >= NUM_QUERIES:
        break

# Fill the rest of the corpus with random passages
print("Filling distractor corpus...")
for item in corpus_ds:
    for p in item['passages']['passage_text']:
        if p not in documents:
            documents.append(p)
            if len(documents) >= CORPUS_SIZE:
                break
    if len(documents) >= CORPUS_SIZE:
        break

print(f"Corpus size: {len(documents)}, Queries: {len(queries)}")

print("Loading models...")
encoder = SentenceTransformer('all-MiniLM-L6-v2')
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)

print("Encoding corpus...")
doc_embs = encoder.encode(documents, show_progress_bar=True, batch_size=512)
faiss.normalize_L2(doc_embs)
index = faiss.IndexFlatIP(doc_embs.shape[1])
index.add(doc_embs)

print("Building BM25...")
tokenized_docs = [doc.split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# Evaluate
dense_mrr = 0
hybrid_mrr = 0

for q in tqdm(queries, desc="Evaluating"):
    true_doc = relevant_map[q]
    
    # Dense
    q_emb = encoder.encode([q], show_progress_bar=False)
    faiss.normalize_L2(q_emb)
    d_scores, d_idx = index.search(q_emb, K)
    
    d_mrr_val = 0
    for rank, idx in enumerate(d_idx[0]):
        if documents[idx] == true_doc:
            if rank < EVAL_K:
                d_mrr_val = 1.0 / (rank + 1)
            break
    dense_mrr += d_mrr_val
    
    # Lexical
    b_scores = bm25.get_scores(q.split())
    
    # Hybrid (Alpha=0.5 for semantic)
    # Min-max normalization
    d_min, d_max = np.min(d_scores[0]), np.max(d_scores[0])
    b_min, b_max = np.min(b_scores), np.max(b_scores)
    
    if d_max > d_min:
        norm_dense_all = np.zeros(len(documents))
        for r, i in enumerate(d_idx[0]):
            norm_dense_all[i] = (d_scores[0][r] - d_min) / (d_max - d_min)
    else:
        norm_dense_all = np.zeros(len(documents))
        
    if b_max > b_min:
        norm_bm25 = (b_scores - b_min) / (b_max - b_min)
    else:
        norm_bm25 = np.zeros(len(documents))
        
    alpha = 0.5
    hybrid_scores = alpha * norm_dense_all + (1 - alpha) * norm_bm25
    
    # Get top K hybrid
    h_idx = np.argsort(hybrid_scores)[::-1][:K]
    
    # Cross-encoder Reranking
    pairs = [[q, documents[i]] for i in h_idx]
    ce_scores = cross_encoder.predict(pairs, show_progress_bar=False)
    
    # Final sort
    final_idx = [h_idx[i] for i in np.argsort(ce_scores)[::-1]]
    
    h_mrr_val = 0
    for rank, idx in enumerate(final_idx):
        if documents[idx] == true_doc:
            if rank < EVAL_K:
                h_mrr_val = 1.0 / (rank + 1)
            break
    hybrid_mrr += h_mrr_val

dense_mrr /= len(queries)
hybrid_mrr /= len(queries)

print("\n--- Shared Corpus Evaluation Results (MS MARCO) ---")
print(f"Corpus Size: {CORPUS_SIZE} passages")
print(f"Queries: {NUM_QUERIES}")
print(f"Dense MRR@{EVAL_K}:     {dense_mrr:.4f}")
print(f"CogniSync MRR@{EVAL_K}: {hybrid_mrr:.4f}")

with open("full_corpus_results.txt", "w") as f:
    f.write(f"Dense MRR: {dense_mrr:.4f}\nCogniSync MRR: {hybrid_mrr:.4f}\n")
