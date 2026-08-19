import json

with open("CogniSync_v3_fixed.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

def get_cell(substring):
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code" and any(substring in line for line in c["source"]):
            return i
    raise ValueError(f"Cell with {substring} not found")

def set_code(substring, replacer_func=None, full_text=None):
    idx = get_cell(substring)
    if full_text is not None:
        nb["cells"][idx]["source"] = [line + "\n" for line in full_text.split("\n")]
    else:
        text = "".join(nb["cells"][idx]["source"])
        text = replacer_func(text)
        nb["cells"][idx]["source"] = [line + "\n" for line in text.split("\n")]


# FIX 1: REMOVE INCORRECT MRR ASSERTION
def fix_mrr(text):
    return text.replace("assert metrics['MRR'] <= metrics['Recall@1'] + 1e-5", "assert 0 <= metrics['MRR'] <= 1")
set_code("def compute_metrics", replacer_func=fix_mrr)

# Helper: Need dataset label to do IMPROVEMENT 1
def add_dataset_label(text):
    text = text.replace('doc_dict["relevant_indices"] = [true_idx]',
                        'doc_dict["relevant_indices"] = [true_idx]\n            doc_dict["dataset"] = name')
    text = text.replace('doc_dict["documents"] = unique_docs',
                        'doc_dict["dataset"] = name\n            doc_dict["documents"] = unique_docs')
    return text
set_code("def unify_dataset", replacer_func=add_dataset_label)

# FIX 2: ADD QUERY-TYPE DISTRIBUTION CHECK
def update_classify(text):
    new_tail = """
query_types = [classify_query(x['query']) for x in all_unified]
total = len(query_types)
exact_count = sum(1 for q in query_types if q == "exact_match")
semantic_count = total - exact_count
exact_ratio = exact_count / total

print(f"Total queries: {total}")
print(f"Semantic queries: {semantic_count} ({semantic_count/total*100:.2f}%)")
print(f"Exact-match queries: {exact_count} ({exact_ratio*100:.2f}%)")

if exact_ratio < 0.1:
    print("WARNING: Low proportion of exact-match queries. Hybrid evaluation may be under-represented.")

dist_df = pd.DataFrame([{"semantic_queries": semantic_count, "exact_match_queries": exact_count, "exact_ratio": exact_ratio}])
dist_df.to_csv('/content/results/query_type_distribution.csv', index=False)
"""
    idx = text.find("query_types = [classify_query")
    return text[:idx] + new_tail
set_code("def classify_query", replacer_func=update_classify)


# IMPROVEMENT 1, 2, 3
full_bench_text = """error_logs = []
latencies = {'embedding_time': [], 'faiss_retrieval_time': [], 'bm25_retrieval_time': [], 'fusion_time': []}
domain_results = []
final_retrieval = []

per_dataset = {}

for item in tqdm(all_unified[:200]):
    ds_name = item.get('dataset', 'unknown')
    
    d_idx, l_idx, h_idx, times = retrieval_system.retrieve(item['query'], item['documents'], top_k=5)
    
    latencies['embedding_time'].append(times[0] * 1000)
    latencies['faiss_retrieval_time'].append(times[1] * 1000)
    latencies['bm25_retrieval_time'].append(times[2] * 1000)
    latencies['fusion_time'].append(times[3] * 1000)
    
    metrics = compute_metrics(h_idx, item['relevant_indices'])
    if not metrics: continue
    
    domain_results.append(metrics['MRR'])
    final_retrieval.append({'query': item['query'], 'MRR': metrics['MRR'], 'Recall@1': metrics['Recall@1']})
    
    if ds_name not in per_dataset:
        per_dataset[ds_name] = []
    
    per_dataset[ds_name].append({
        'Recall@1': metrics['Recall@1'],
        'Recall@3': metrics['Recall@3'],
        'Recall@5': metrics['Recall@5'],
        'MRR': metrics['MRR'],
        'NDCG@5': metrics['NDCG@5']
    })
    
    q_type = classify_query(item['query'])
    
    failure_type = None
    if metrics['Recall@5'] == 0:
        if q_type == 'semantic': failure_type = 'semantic_miss'
        else: failure_type = 'lexical_miss'
    elif metrics['Recall@1'] == 0:
        failure_type = 'ranking_error'
        
    if failure_type:
        error_logs.append({
            'query': item['query'],
            'failure_type': failure_type
        })

# IMPROVEMENT 1: PER DATASET METRICS
ds_summary = []
for ds, m_list in per_dataset.items():
    df_ds = pd.DataFrame(m_list)
    ds_summary.append({
        'Dataset': ds,
        'System': 'Hybrid-RRF',
        'Recall@1': df_ds['Recall@1'].mean(),
        'Recall@3': df_ds['Recall@3'].mean(),
        'Recall@5': df_ds['Recall@5'].mean(),
        'MRR': df_ds['MRR'].mean(),
        'NDCG@5': df_ds['NDCG@5'].mean()
    })
pd.DataFrame(ds_summary).to_csv('/content/results/per_dataset_metrics.csv', index=False)

# IMPROVEMENT 2: ERROR ANALYSIS SUMMARY TABLE
error_counts = {
    "semantic_miss": sum(1 for e in error_logs if e['failure_type'] == 'semantic_miss'),
    "lexical_miss": sum(1 for e in error_logs if e['failure_type'] == 'lexical_miss'),
    "ranking_error": sum(1 for e in error_logs if e['failure_type'] == 'ranking_error'),
    "routing_error": 0  # No routing in pure RRF
}
total_errors = max(1, len(error_logs))
err_df = pd.DataFrame([{k: v/total_errors*100 for k,v in error_counts.items()}])
err_df.to_csv('/content/results/error_summary.csv', index=False)

# FIX 7: Latency breakdown
latency_df = pd.DataFrame(latencies).mean().reset_index()
latency_df.columns = ['Component', 'Time (ms)']
latency_df.to_csv('/content/results/latency_breakdown.csv', index=False)

# FIX 10: Clean save
pd.DataFrame(final_retrieval).to_csv('/content/results/final_retrieval.csv', index=False)
pd.DataFrame(final_retrieval).to_csv('/content/results/hybrid_fusion_results.csv', index=False)

# IMPROVEMENT 3: Final sanity log
print("\\n========================================")
print("FINAL SANITY CHECK LOG")
print("========================================")
print(f"Total Queries Generated: {len(all_unified)}")
print(f"Dataset evaluated queries map: " + ", ".join([f"{k}: {len(v)}" for k,v in per_dataset.items()]))
print(f"Valid Queries Evaluated (total after skips): {total_valid_queries}")
print(f"Skipped Queries (empty grounding): {skipped_queries_count}")
print(f"\\nQuery-type distribution:")
total_eval = sum([len(v) for v in per_dataset.values()])
exact_count = sum(1 for x in all_unified[:200] if classify_query(x['query']) == 'exact_match' and x.get('dataset', 'unknown') in per_dataset)
print(f"Semantic: {total_eval - exact_count} ({((total_eval-exact_count)/max(1,total_eval))*100:.1f}%)")
print(f"Exact-Match: {exact_count} ({(exact_count/max(1,total_eval))*100:.1f}%)")
print("========================================")

if len(domain_results) > 1:
    print(f"\\nStats - Mean MRR: {np.mean(domain_results):.4f}")
    ci = stats.t.interval(0.95, len(domain_results)-1, loc=np.mean(domain_results), scale=stats.sem(domain_results))
"""

set_code("error_logs =", full_text=full_bench_text)

# Fix the zip file download name update
for c in nb["cells"]:
    if c["cell_type"] == "code":
        c["source"] = [s.replace("CogniSync_v3_fixed_results", "CogniSync_v3_final_results") for s in c["source"]]


with open("CogniSync_v3_final.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Final patch complete! Saved to CogniSync_v3_final.ipynb")
