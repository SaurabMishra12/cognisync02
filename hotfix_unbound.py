import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        for i, line in enumerate(c["source"]):
            
            # Revert the faulty true_doc globally unbound check
            if "if doc_dict.get(\"query\") and doc_dict.get(\"documents\") and true_doc:" in line:
                c["source"][i] = "        if doc_dict.get(\"query\") and doc_dict.get(\"documents\"):\n"
                
            # Safely inject the empty filter directly inside the SciQ mapping
            if "true_doc = item.get('support', '')" in line:
                c["source"][i] = "                true_doc = item.get('support', '')\n                if not true_doc: continue\n"

        # Safe SQuAD empty context handling just in case
        for i, line in enumerate(c["source"]):
             if "true_doc = item.get('context', '')" in line:
                 if 'continue' not in c["source"][i]:
                     c["source"][i] = "                true_doc = item.get('context', '')\n                if not true_doc: continue\n"


with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Fixed UnboundLocalError!")
