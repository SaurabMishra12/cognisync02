import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar
import matplotlib.pyplot as plt
import os
import json

df = pd.read_csv(r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\results 5may\CogniSync_v3_strong_results (1)\MASTER_RAW_EVAL_ALL_QUERIES.csv')
out_dir = r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\results 5may'

# Isolate systems
sys_cog = df[df['System'] == 'CogniSync'].reset_index(drop=True)
sys_van = df[df['System'] == 'Vanilla_RAG'].reset_index(drop=True)

if len(sys_cog) == len(sys_van):
    print("Computing stats for CogniSync vs Vanilla RAG")
    # MRR Continuous
    mrr_cog = sys_cog['MRR'].values
    mrr_van = sys_van['MRR'].values
    
    # Wilcoxon signed-rank
    diff = mrr_cog - mrr_van
    stat, p_val = stats.wilcoxon(diff)
    
    # Bootstrapped CI for CogniSync MRR
    rng = np.random.default_rng(42)
    boot = [np.mean(rng.choice(mrr_cog, size=len(mrr_cog), replace=True)) for _ in range(1000)]
    ci_lower = np.percentile(boot, 2.5)
    ci_upper = np.percentile(boot, 97.5)
    
    # McNemar for Recall@5
    hits_cog = (sys_cog['Recall@5'] > 0).astype(int).values
    hits_van = (sys_van['Recall@5'] > 0).astype(int).values
    b = sum(1 for a, b_ in zip(hits_cog, hits_van) if a == 1 and b_ == 0)
    c = sum(1 for a, b_ in zip(hits_cog, hits_van) if a == 0 and b_ == 1)
    table_2x2 = np.array([[sum(1 for a, b_ in zip(hits_cog, hits_van) if a == 1 and b_ == 1), b],
                          [c, sum(1 for a, b_ in zip(hits_cog, hits_van) if a == 0 and b_ == 0)]])
    exact = (b + c) < 25
    mcnemar_res = sm_mcnemar(table_2x2, exact=exact)
    
    results = {
        'CogniSync_MRR_95_CI': f"[{ci_lower:.4f}, {ci_upper:.4f}]",
        'Wilcoxon_p_value': p_val,
        'McNemar_p_value': mcnemar_res.pvalue,
        'CogniSync_Wins_Recall': int(b),
        'Vanilla_Wins_Recall': int(c)
    }
    with open(os.path.join(out_dir, 'stats.json'), 'w') as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))

# Graph 1: MRR by System
t1 = df.groupby('System')['MRR'].mean().reset_index()
plt.figure(figsize=(8, 5))
plt.bar(t1['System'], t1['MRR'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
plt.title('Mean Reciprocal Rank (MRR) by System')
plt.ylabel('MRR')
plt.ylim(0.7, 0.9)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(os.path.join(out_dir, 'mrr_comparison.png'), bbox_inches='tight')
plt.close()

# Graph 2: Query Type Breakdown
t2 = df.groupby(['System', 'Query_Type'])['MRR'].mean().unstack()
t2.plot(kind='bar', figsize=(10, 6))
plt.title('MRR by Query Type')
plt.ylabel('MRR')
plt.ylim(0.7, 1.0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Query Type')
plt.savefig(os.path.join(out_dir, 'query_type_mrr.png'), bbox_inches='tight')
plt.close()

print('Graphs saved to results 5may.')
