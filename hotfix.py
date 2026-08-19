import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        for i, line in enumerate(c["source"]):
            if "doc_dict[\"query\"] = item.get('question', '').get('text', '')" in line:
                c["source"][i] = "                doc_dict[\"query\"] = item.get('question', '')\n"
            elif "true_.get('html', '')[:120]" in line:
                c["source"][i] = "                true_doc = item.get('support', '')\n"

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Fixed syntax error in unify_dataset!")
