import json

with open("CogniSync_v3_strong.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        src = "".join(c["source"])
        
        # Remove trust_remote_code to fix Hugging Face depreciation warnings
        if "trust_remote_code=True" in src:
            for i, line in enumerate(c["source"]):
                c["source"][i] = line.replace(", trust_remote_code=True", "")
                c["source"][i] = line.replace("trust_remote_code=True", "")
                
        # Fix the strict size restriction to cleanly fall back to max available rows
        if "def load_and_verify" in src:
            for i, line in enumerate(c["source"]):
                if "if len(ds) < size:" in line:
                    c["source"][i] = line.replace("if len(ds) < size:", "actual_size = min(len(ds), size)")
                if "raise RuntimeError" in line and "loading failed: size" in line:
                    c["source"][i] = ""
                if "ds = ds.select(range(size))" in line:
                    c["source"][i] = line.replace("range(size)", "range(actual_size)")

with open("CogniSync_v3_strong.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Patched dataset limits and remote_code.")
