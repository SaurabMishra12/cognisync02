import json

filepath = r"c:\Users\msaur\OneDrive\Desktop\Obsidian\obsidian\Faraday\v2_extraExperimentsCIKM.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        # Fix FPR logic
        if "fp_queries = safe_texts[100:100+len(fp_docs_with_imperative)]" in "".join(cell['source']):
            new_source = []
            for line in cell['source']:
                if "fp_queries = safe_texts[100:100+len(fp_docs_with_imperative)]" in line:
                    new_source.append("    fp_queries = fp_docs_with_imperative\n")
                else:
                    new_source.append(line)
            cell['source'] = new_source

        # Fix docid mapping logic
        if "docid_to_idx = {docid: i" in "".join(cell['source']):
            new_source = []
            for line in cell['source']:
                if "docid_to_idx = {docid: i" in line:
                    new_source.append('docid_to_idx = {str(docid): i for i, docid in enumerate(tqdm(marco_subset[\'docid\'], desc="Mapping DocIDs"))}\n')
                elif "pos_docids = [p['docid']" in line:
                    new_source.append("    pos_docids = [str(p['docid']) for p in item['positive_passages']]\n")
                else:
                    new_source.append(line)
            cell['source'] = new_source

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print("Notebook patched successfully.")
