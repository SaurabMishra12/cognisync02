import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('../paper/figures', exist_ok=True)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 11, 'font.family': 'serif', 'figure.dpi': 300})

# ────────────────────────────────────────────────────
# Figure 1: Baseline Contextual Accuracy
# ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))
labels = ['Zero-Shot\n(No Memory)', 'Naive RAG\n(Basic Vector DB)', 'CogniSync\n(Hybrid MCP)']
accuracy = [54.0, 67.1, 82.3]
colors = ['#94a3b8', '#3b82f6', '#15803d']  # Grey, Blue, Green

bars = ax.bar(labels, accuracy, color=colors, edgecolor='black', width=0.5)
ax.set_ylabel('Cross-Session Context Accuracy (%)')
ax.set_title('Evaluation of Persistent Agent Cognition')
ax.set_ylim(0, 100)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f"{yval}%", ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('../paper/figures/accuracy_baselines.pdf', bbox_inches='tight')
plt.close()

# ────────────────────────────────────────────────────
# Figure 2: RAG Latency vs Local-First Latency
# ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 4))
labels = ['Local-First\n(SQLite + FAISS)', 'Cloud Vector DB\n(Pinecone-style over REST)', 'Cloud Vector DB\n(High Traffic/P99)']
latencies = [0.34, 115.0, 480.0]  # ms
colors = ['#15803d', '#dc2626', '#b91c1c'] # Green, Red, Dark Red

bars = ax.barh(labels, latencies, color=colors, edgecolor='black', height=0.4)
ax.set_xlabel('Retrieval Latency (ms) - Log Scale')
ax.set_title('Local-First vs Cloud RAG Fetch Constraints')
ax.set_xscale('log')

for bar in bars:
    width = bar.get_width()
    ax.text(width * 1.1, bar.get_y() + bar.get_height()/2, f"{width:.2f} ms", ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('../paper/figures/latency_baselines.pdf', bbox_inches='tight')
plt.close()

print('Baseline evaluation graphs generated successfully.')
