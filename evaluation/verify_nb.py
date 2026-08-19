import json
nb = json.load(open("CogniSync_NeurIPS_Eval.ipynb", encoding="utf-8"))
code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
md_cells   = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
print(f"Notebook valid: {len(nb['cells'])} total cells")
print(f"  Code cells:     {len(code_cells)}")
print(f"  Markdown cells: {len(md_cells)}")
print(f"  nbformat:       {nb['nbformat']}.{nb['nbformat_minor']}")
print()
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])[:80].replace("\n", " ")
    print(f"  [{c['cell_type'][:4]}] Cell {i}: {src}")
