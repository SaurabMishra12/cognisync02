import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)
sns.set_palette("Set2")

base_dir = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\githubpush_cogniSync"
results_dir = os.path.join(base_dir, "results")
plots_dir = os.path.join(base_dir, "plots")

if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

# 1. Main Retrieval Performance Plot (Table 1)
def plot_main_retrieval():
    df = pd.read_csv(os.path.join(results_dir, "table1_main_retrieval.csv"))
    # Expected: ['System', 'Rec@1', 'Rec@5', 'MRR@5', 'NDCG@5']
    
    # Melt the dataframe for seaborn grouped barplot
    df_melted = df.melt(id_vars='System', value_vars=['MRR@5', 'Rec@5'], 
                        var_name='Metric', value_name='Score')
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='System', y='Score', hue='Metric', data=df_melted, palette='viridis')
    plt.title('Main Retrieval Performance (CogniSync vs Baselines)')
    plt.ylim(0.6, 1.0)
    plt.ylabel('Score')
    plt.xlabel('')
    
    # Add values on top of bars
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.3f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points',
                    fontsize=12)
                    
    plt.legend(title='', loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'main_retrieval_performance.pdf'))
    plt.close()

# 2. Per-Dataset MRR@5 (Table 4)
def plot_per_dataset():
    df = pd.read_csv(os.path.join(results_dir, "table4_per_dataset.csv"))
    # Expected: ['Dataset', 'CogniSync', 'Dense', 'Hybrid_N', 'Lexical']
    
    df_melted = df.melt(id_vars='Dataset', 
                        value_vars=['CogniSync', 'Dense', 'Hybrid_N', 'Lexical'], 
                        var_name='System', value_name='MRR@5')
    
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='Dataset', y='MRR@5', hue='System', data=df_melted, palette='mako')
    plt.title('MRR@5 Across Diverse Datasets')
    plt.ylim(0.0, 1.1)
    plt.ylabel('MRR@5')
    plt.xlabel('Dataset')
    
    plt.legend(title='System', loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'per_dataset_mrr.pdf'))
    plt.close()

# 3. Query Type Comparison (Table 6)
def plot_query_type():
    df = pd.read_csv(os.path.join(results_dir, "table6_query_type.csv"))
    # Expected: ['System', 'Exact-Match', 'Semantic']
    
    df_melted = df.melt(id_vars='System', value_vars=['Exact-Match', 'Semantic'], 
                        var_name='Query Type', value_name='MRR@5')
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='System', y='MRR@5', hue='Query Type', data=df_melted, palette='flare')
    plt.title('Performance by Query Type (Lexical vs Semantic Intent)')
    plt.ylim(0.5, 1.05)
    plt.ylabel('MRR@5')
    plt.xlabel('')
    
    plt.legend(title='Query Type', loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'query_type_comparison.pdf'))
    plt.close()

# 4. Context Ablation (Table 10)
def plot_context_ablation():
    df = pd.read_csv(os.path.join(results_dir, "table10_context_ablation.csv"))
    # Expected: ['Variant', 'MRR@5', 'Recall@5']
    
    # We only care about MRR@5 for a clean plot
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Variant', y='MRR@5', data=df, palette='crest')
    plt.title('Impact of Synthetic Episodic Memory Context on Retrieval')
    plt.ylim(0.8, 0.9) # Zoomed in to show the difference
    plt.ylabel('MRR@5')
    plt.xlabel('')
    plt.xticks(rotation=45, ha='right')
    
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.4f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points',
                    fontsize=12)
                    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'context_ablation.pdf'))
    plt.close()

print("Generating plots...")
try:
    plot_main_retrieval()
    print(" - main_retrieval_performance.pdf created")
    plot_per_dataset()
    print(" - per_dataset_mrr.pdf created")
    plot_query_type()
    print(" - query_type_comparison.pdf created")
    plot_context_ablation()
    print(" - context_ablation.pdf created")
    print("Done!")
except Exception as e:
    print(f"Error generating plots: {e}")
