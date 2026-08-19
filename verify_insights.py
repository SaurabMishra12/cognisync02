import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv(r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\results 5may\CogniSync_v3_strong_results (1)\MASTER_RAW_EVAL_ALL_QUERIES.csv')

# Pivot the data so each query has a column for each system's MRR
# Since we have query texts, we can use them or just rely on the fact that the dataframe has sequential chunks per system.
# Actually, the dataframe was appended sequentially per query. Let's pivot.
df['Query_ID'] = df.groupby('System').cumcount()
pivot_df = df.pivot(index='Query_ID', columns='System', values='MRR').reset_index()

# Add dataset and query type back
meta_df = df[df['System'] == 'CogniSync'][['Query_ID', 'Dataset', 'Query_Type']].set_index('Query_ID')
pivot_df = pivot_df.join(meta_df, on='Query_ID')

# 1. Hidden Wins
wins = pivot_df[pivot_df['CogniSync'] > pivot_df['Vanilla_RAG']]
print(f"CogniSync > Vanilla RAG count: {len(wins)}")
if len(wins) > 0:
    print(f"Average gain: {(wins['CogniSync'] - wins['Vanilla_RAG']).mean():.3f}")
    ms_marco_wins = len(wins[wins['Dataset'] == 'ms_marco'])
    print(f"MS-MARCO percentage: {ms_marco_wins / len(wins) * 100:.1f}% ({ms_marco_wins} queries)")

# 2. Ranking Error Anomaly
try:
    err_df = pd.read_csv(r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\results 5may\CogniSync_v3_strong_results (1)\error_analysis_extended.csv')
    ranking_errors = err_df[err_df['Failure Type'] == 'Ranking Error']
    print(f"\nRanking Errors count: {len(ranking_errors)}")
    if len(ranking_errors) > 0:
        print(f"Top-5 retention: {ranking_errors['Doc in Top-5'].mean() * 100:.1f}%")
except Exception as e:
    print("Error reading error_analysis_extended.csv:", e)

# 3. CodeSearchNet Immunity
severe_losses = pivot_df[(pivot_df['Vanilla_RAG'] - pivot_df['CogniSync']) >= 0.5]
print(f"\nSevere Losses count: {len(severe_losses)}")
print(severe_losses.groupby('Dataset').size())

# 4. Exact-Match Penalty
exact_severe = len(severe_losses[severe_losses['Query_Type'] == 'exact_match'])
sem_severe = len(severe_losses[severe_losses['Query_Type'] == 'semantic'])

total_exact = len(pivot_df[pivot_df['Query_Type'] == 'exact_match'])
total_sem = len(pivot_df[pivot_df['Query_Type'] == 'semantic'])

if total_exact > 0:
    print(f"\nExact Match severe loss rate: {exact_severe / total_exact * 100:.2f}%")
if total_sem > 0:
    print(f"Semantic severe loss rate: {sem_severe / total_sem * 100:.2f}%")
