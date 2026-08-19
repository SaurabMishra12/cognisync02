import json

with open("CogniSync_v3_strong.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        # Bump the initial dataset loading sizes by 2x-3x for rigor
        if "ds_ms = load_and_verify" in "".join(c["source"]):
            for i, line in enumerate(c["source"]):
                if "ds_ms = load_and_verify" in line:
                    c["source"][i] = line.replace("5000)", "15000)")
                if "ds_code = load_and_verify" in line:
                    c["source"][i] = line.replace("5000)", "15000)")
                if "ds_sciq = load_and_verify" in line:
                    c["source"][i] = line.replace("2000)", "5000)")
                if "ds_squad = load_and_verify" in line:
                    c["source"][i] = line.replace("2000)", "5000)")

        # Expand the slices in ablation and security tests significantly
        if "def run_ablation" in "".join(c["source"]):
            for i, line in enumerate(c["source"]):
                if "tqdm(data[:200])" in line:
                    c["source"][i] = line.replace("data[:200]", "data[:5000]")

        if "def security_baseline_eval" in "".join(c["source"]):
            for i, line in enumerate(c["source"]):
                if "tqdm(data[:100])" in line:
                    c["source"][i] = line.replace("data[:100]", "data[:2500]")

with open("CogniSync_v3_strong.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Scaled up datasets and sample slices for CIKM-level statistical significance.")
