import matplotlib.pyplot as plt
import seaborn as sns
import sys
import traceback

try:
    systems = ['Dense/Vanilla RAG', 'CogniSync', 'Hybrid-Naive', 'Lexical (BM25)']
    mrr = [0.867, 0.856, 0.844, 0.796]
    asr = [3.20, 0.00, 3.20, 3.20]

    plt.figure(figsize=(8, 6))
    sns.set_theme(style='ticks')
    colors = ['red', 'green', 'orange', 'gray']
    markers = ['o', '*', 's', '^']

    for i in range(len(systems)):
        plt.scatter(asr[i], mrr[i], label=systems[i], color=colors[i], marker=markers[i], s=250 if systems[i]=='CogniSync' else 150, zorder=3)

    for i, txt in enumerate(systems):
        if txt == 'CogniSync':
            plt.annotate(txt, (asr[i], mrr[i]), xytext=(asr[i]+0.1, mrr[i]), fontsize=12, fontweight='bold', color='green')
        elif txt == 'Dense/Vanilla RAG':
            plt.annotate(txt, (asr[i], mrr[i]), xytext=(asr[i]-0.20, mrr[i]+0.004), fontsize=11, ha='right')
        elif txt == 'Hybrid-Naive':
            plt.annotate(txt, (asr[i], mrr[i]), xytext=(asr[i]-0.15, mrr[i]-0.004), fontsize=11, ha='right')
        else:
            plt.annotate(txt, (asr[i], mrr[i]), xytext=(asr[i]-0.15, mrr[i]), fontsize=11, ha='right')

    # plt.title('CogniSync: Security-Quality Tradeoff', fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Attack Success Rate (%)', fontsize=12)
    plt.ylabel('Mean Reciprocal Rank (MRR)', fontsize=12)
    plt.xlim(-0.2, 3.6)
    plt.ylim(0.78, 0.88)
    plt.axvline(x=0, color='black', linewidth=1, linestyle='--')
    plt.text(-0.06, 0.83, 'Ideal Security Boundary', rotation=90, fontsize=10, color='gray', va='center', ha='center')
    plt.tight_layout()
    
    save_path = r'C:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\evaluation\results\Paper\security_tradeoff_plot.png'
    plt.savefig(save_path, dpi=300)
    print("Successfully saved plot to:", save_path)
except Exception as e:
    print("Error:", e)
    traceback.print_exc()
    sys.exit(1)
