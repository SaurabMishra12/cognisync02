import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        for i, line in enumerate(c["source"]):
            if "unified_fiqa = unify_dataset(ds_fiqa, \"fiqa\")" in line:
                c["source"][i] = line.replace("unified_fiqa = unify_dataset(ds_fiqa, \"fiqa\")", "unified_squad = unify_dataset(ds_squad, \"squad\")")
            if "all_unified = unified_ms + unified_code + unified_sciq + unified_fiqa" in line:
                c["source"][i] = line.replace("+ unified_fiqa", "+ unified_squad")

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Renamed missing fiqa references to squad!")
