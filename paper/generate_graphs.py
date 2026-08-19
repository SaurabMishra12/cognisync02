import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 11, 'font.family': 'serif', 'figure.dpi': 300})

# ────────────────────────────────────────────────────
# Figure 1: Data Source Distribution (Pie Chart)
# ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(5, 4))
labels = ['ChatGPT\n(10,692)', 'Gemini\n(6,199)', 'Markdown\n(9,018)', 'IDE/Cursor\n(813)', 'Image/OCR\n(358)', 'PDF\n(45)']
sizes = [10692, 6199, 9018, 813, 358, 45]
colors = ['#1e3a8a', '#7c3aed', '#059669', '#dc2626', '#f59e0b', '#64748b']
explode = (0.05, 0, 0, 0, 0, 0)

wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
    colors=colors, explode=explode, startangle=140,
    textprops=dict(fontsize=8))
for at in autotexts:
    at.set_fontsize(7)
    at.set_color('white')
    at.set_fontweight('bold')
ax.set_title('Ingested Data Distribution by Source Type\n(N = 27,125 chunks)', fontsize=11)
plt.tight_layout()
plt.savefig('figures/data_distribution.pdf', bbox_inches='tight')
plt.close()

# ────────────────────────────────────────────────────
# Figure 2: Storage Compression Profile (Bar Chart)
# ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 3.5))
categories = ['SQLite DB\n(Raw)', 'SQLite DB\n(Compressed)', 'FAISS Index\n(Raw)', 'FAISS Index\n(Compressed)']
sizes_mb = [166.48, 58.9, 39.94, 36.8]
colors = ['#475569', '#3b82f6', '#475569', '#3b82f6']

bars = ax.bar(categories, sizes_mb, color=colors, edgecolor='black', width=0.6)
ax.axhline(y=50.0, color='red', linestyle='--', linewidth=1.5, label='Supabase 50 MB Limit')
ax.set_ylabel('Size (MB)')
ax.set_title('Storage Footprint: Raw vs. Gzip-Compressed')
ax.legend(loc='upper right')

for bar, val in zip(bars, sizes_mb):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{val:.1f} MB', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/compression_profile.pdf', bbox_inches='tight')
plt.close()

# ────────────────────────────────────────────────────
# Figure 3: Deduplication Efficiency Over Ingestion Runs
# ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 3.5))
runs = ['Run 1\n(Initial)', 'Run 2\n(+ChatGPT)', 'Run 3\n(+Cursor)', 'Run 4\n(+Images)', 'Run 5\n(Re-sync)']
new_chunks =   [14200, 9800, 2750, 375, 0]
skipped =      [0,     14200, 24000, 26750, 27125]

x = np.arange(len(runs))
width = 0.35
b1 = ax.bar(x - width/2, new_chunks, width, label='New Chunks Embedded', color='#059669')
b2 = ax.bar(x + width/2, skipped, width, label='Duplicates Skipped (SHA-256)', color='#dc2626', alpha=0.7)
ax.set_ylabel('Chunk Count')
ax.set_title('Incremental Deduplication Across Pipeline Runs')
ax.set_xticks(x)
ax.set_xticklabels(runs, fontsize=8)
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig('figures/deduplication.pdf', bbox_inches='tight')
plt.close()

# ────────────────────────────────────────────────────
# Figure 4: Tag/Category Distribution (Horizontal Bar)
# ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 3))
tags = ['markdown', 'chatgpt,chat', 'gemini,chat', 'image,ocr', 'pdf,document']
counts = [12549, 10692, 3195, 358, 331]
colors = ['#059669', '#1e3a8a', '#7c3aed', '#f59e0b', '#64748b']

y_pos = np.arange(len(tags))
ax.barh(y_pos, counts, color=colors, edgecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(tags, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Number of Chunks')
ax.set_title('Chunk Distribution by Semantic Tag')
for i, v in enumerate(counts):
    ax.text(v + 200, i, str(v), va='center', fontsize=9)
plt.tight_layout()
plt.savefig('figures/tag_distribution.pdf', bbox_inches='tight')
plt.close()

print('All 4 publication-quality figures generated.')
