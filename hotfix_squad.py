import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        for i, line in enumerate(c["source"]):
            # SQuAD uses 'question' in Hugging Face datasets, not 'query'
            if "doc_dict[\"query\"] = item.get('query', '')" in line and 'elif name == "squad":' in c["source"][i-1]:
                c["source"][i] = "                doc_dict[\"query\"] = item.get('question', '')\n"

            # Filter out empty truths for sciq implicitly ensuring data rigor
            if "if doc_dict.get(\"query\") and doc_dict.get(\"documents\"):" in line:
                c["source"][i] = "        if doc_dict.get(\"query\") and doc_dict.get(\"documents\") and true_doc:\n"

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Fixed SQuAD key mapping and zero-length document bugs!")
