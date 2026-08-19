import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar
import json

df = pd.read_csv(r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\results 5may\CogniSync_v3_strong_results (1)\MASTER_RAW_EVAL_ALL_QUERIES.csv')

def cohens_d(a, b):
    diff = a - b
    d = float(np.mean(diff) / (np.std(diff, ddof=1) + 1e-12))
    return d

def compare_systems(sys_a_name, sys_b_name, df_subset=df):
    sys_a = df_subset[df_subset['System'] == sys_a_name].reset_index(drop=True)
    sys_b = df_subset[df_subset['System'] == sys_b_name].reset_index(drop=True)
    
    if len(sys_a) != len(sys_b) or len(sys_a) == 0:
        return None
        
    mrr_a = sys_a['MRR'].values
    mrr_b = sys_b['MRR'].values
    
    diff = mrr_a - mrr_b
    stat, wilcox_p = stats.wilcoxon(diff)
    
    hits_a = (sys_a['Recall@5'] > 0).astype(int).values
    hits_b = (sys_b['Recall@5'] > 0).astype(int).values
    b = sum(1 for a, b_ in zip(hits_a, hits_b) if a == 1 and b_ == 0)
    c = sum(1 for a, b_ in zip(hits_a, hits_b) if a == 0 and b_ == 1)
    table_2x2 = np.array([[sum(1 for a, b_ in zip(hits_a, hits_b) if a == 1 and b_ == 1), b],
                          [c, sum(1 for a, b_ in zip(hits_a, hits_b) if a == 0 and b_ == 0)]])
    mcnemar_res = sm_mcnemar(table_2x2, exact=(b + c) < 25)
    
    d_val = cohens_d(mrr_a, mrr_b)
    
    return {
        'comparison': f'{sys_a_name} vs {sys_b_name}',
        'wilcoxon_p': wilcox_p,
        'mcnemar_p': mcnemar_res.pvalue,
        'cohens_d': d_val,
        'mean_diff': np.mean(diff)
    }

results = {
    'Macro_Comparisons': [
        compare_systems('CogniSync', 'Hybrid_Naive'),
        compare_systems('CogniSync', 'Lexical'),
        compare_systems('Vanilla_RAG', 'CogniSync'),
        compare_systems('Vanilla_RAG', 'Lexical')
    ],
    'Domain_Specific (CogniSync_v1.0)': [
        compare_systems('CogniSync', 'Hybrid_Naive', df[df['Dataset'] == 'CogniSync_v1.0']),
        compare_systems('CogniSync', 'Lexical', df[df['Dataset'] == 'CogniSync_v1.0']),
        compare_systems('Vanilla_RAG', 'CogniSync', df[df['Dataset'] == 'CogniSync_v1.0'])
    ]
}

print(json.dumps(results, indent=2))
