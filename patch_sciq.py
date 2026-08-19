import json
import re

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        text = "".join(c["source"])
        
        # Remove the hacky streaming logic completely and replace with SciQ
        if 'nq_stream = load_dataset' in text or 'natural_questions' in text:
            # Replace loading block
            text = re.sub(
                r'print\("Streaming natural_questions.*?ds_nq = list\(itertools\.islice\(nq_stream, 2000\)\)', 
                'ds_sciq = load_and_verify("sciq", None, "train", 2000)', 
                text, flags=re.DOTALL
            )
            
            # Replace unifying block
            text = text.replace('unified_nq = unify_dataset(ds_nq, "natural_questions")',
                                'unified_sciq = unify_dataset(ds_sciq, "sciq")')
            text = text.replace('unified_nq', 'unified_sciq')
            
            # Replace specific data wrangling mapped to NQ
            text = text.replace('elif name == "natural_questions":', 'elif name == "sciq":')
            text = text.replace("doc = item.get('document', {})", "")
            text = text.replace("texts_for_noise.append(doc.get('html', '')[:120])", "texts_for_noise.append(item.get('support', ''))")
            text = text.replace("doc_dict[\"query\"] = item.get('question', {}).get('text', '')", "doc_dict[\"query\"] = item.get('question', '')")
            text = text.replace("true_doc = item.get('document', {}).get('html', '')[:120]", "true_doc = item.get('support', '')")
            
        # Write back line by line safely avoiding blank stripping
        if text:
            lines = text.split("\n")
            c["source"] = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Replaced natural_questions completely with SciQ!")
