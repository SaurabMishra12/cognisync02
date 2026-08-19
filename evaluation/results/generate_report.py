import pandas as pd
import json

base = "c:/Users/msaur/OneDrive/Desktop/Obsidian/obsidian/Faraday/evaluation/results/CogniSync_v2_results/results/"
out_path = "c:/Users/msaur/OneDrive/Desktop/Obsidian/obsidian/Faraday/evaluation/results/CogniSync_v2_Comprehensive_Report.md"

def to_md(df):
    header = "|" + "|".join(str(c) for c in df.columns) + "|"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    rows = []
    for _, row in df.iterrows():
        rows.append("|" + "|".join(str(x) for x in row.values) + "|")
    return "\n".join([header, sep] + rows)

md_lines = []
md_lines.append("# CogniSync v2 Evaluation - Comprehensive Results\n")

# Run Metadata
try:
    with open(base + "run_metadata.json") as f:
        meta = json.load(f)
    md_lines.append("## Run Metadata")
    for k, v in meta.items():
        md_lines.append(f"- **{k}**: {v}")
    md_lines.append("\n")
except Exception as e:
    pass

# Cross Domain
try:
    md_lines.append("## 1. Cross-Domain Retrieval Performance")
    cd = pd.read_csv(base + "cross_domain_aggregate.csv")
    md_lines.append(to_md(cd))
    md_lines.append("\n")
except: pass

# Episodic
try:
    md_lines.append("## 2. Episodic Memory Ablation")
    ep = pd.read_csv(base + "episodic_ablation.csv")
    ep_agg = ep.groupby(["mode"])[["mrr_mean", "recall5_mean", "latency_ms"]].mean().reset_index()
    md_lines.append(to_md(ep_agg))
    md_lines.append("\n")
except: pass

# Long Horizon
try:
    md_lines.append("## 3. Long-Horizon Evaluation")
    lh = pd.read_csv(base + "long_horizon.csv")
    md_lines.append(to_md(lh))
    md_lines.append("\n")
except: pass

# Memory Quality
try:
    md_lines.append("## 4. Memory Quality")
    mq = pd.read_csv(base + "memory_quality.csv")
    mq_agg = mq[["precision", "redundancy", "recall@5", "mrr", "latency_ms"]].mean().to_frame("Average").reset_index()
    md_lines.append(to_md(mq_agg))
    md_lines.append("\n")
except: pass

# Security
try:
    md_lines.append("## 5. Security Evaluation")
    sec = pd.read_csv(base + "security_eval.csv")
    sec_agg = pd.DataFrame({
        "Metric": ["Attack Success Rate", "Average MRR Delta (Poisoned - Clean)", "Clean MRR", "Poisoned MRR"],
        "Value": [f"{sec['attack_success'].mean()*100:.1f}%", f"{sec['mrr_delta'].mean():.4f}", f"{sec['mrr_clean'].mean():.4f}", f"{sec['mrr_poisoned'].mean():.4f}"]
    })
    md_lines.append(to_md(sec_agg))
    md_lines.append("\n")
except: pass

# Statistics
try:
    md_lines.append("## 6. Statistical Test Results")
    st = pd.read_csv(base + "statistics.csv")
    md_lines.append(to_md(st))
    md_lines.append("\n")
except: pass

# Hybrid Validation
try:
    md_lines.append("## 7. Hybrid Query Type Validation")
    he = pd.read_csv(base + "hybrid_exact.csv")
    try:
        hs = pd.read_csv(base + "hybrid_semantic.csv")
        hs["query_type"] = "semantic"
    except:
        hs = pd.DataFrame()
    he["query_type"] = "exact"
    comb = pd.concat([he, hs])
    if not comb.empty:
        comb_agg = comb.groupby(["query_type", "system"])[["mrr", "recall@5", "latency_ms"]].mean().reset_index()
        md_lines.append(to_md(comb_agg))
    md_lines.append("\n")
except: pass

with open(out_path, "w", encoding='utf-8') as f:
    f.write("\n".join(md_lines))
print("Saved to", out_path)
