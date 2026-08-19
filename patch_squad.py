import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        text = "".join(c["source"])
        
        # Replace dataset load for fiqa -> squad
        if 'load_and_verify("fiqa"' in text:
            text = text.replace('load_and_verify("fiqa", None, "train", 2000)',
                                'load_and_verify("squad", None, "validation", 2000)')
            text = text.replace('ds_fiqa =', 'ds_squad =')
            text = text.replace('unified_fiqa = unify_dataset(ds_fiqa, "fiqa")',
                                'unified_squad = unify_dataset(ds_squad, "squad")')
            text = text.replace('unified_fiqa', 'unified_squad')
        
        # Replace mapping logic for fiqa -> squad
        if 'elif name == "fiqa":' in text:
            text = text.replace('elif name == "fiqa":', 'elif name == "squad":')
            text = text.replace("texts_for_noise.append(item.get('doc', ''))", 
                                "texts_for_noise.append(item.get('context', ''))")
            text = text.replace("true_doc = item.get('doc', '')", 
                                "true_doc = item.get('context', '')")
            text = text.replace("doc_dict[\"query\"] = item.get('question', {})", 
                                "doc_dict[\"query\"] = item.get('question', '')") # for squad this uses question directly. Wait, natural_questions uses question.text. Let's make sure it handles squad properly.
        
        c["source"] = [line + "\n" for line in text.split("\n")[:-1] if text]

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Replaced fiqa with standard squad.")
