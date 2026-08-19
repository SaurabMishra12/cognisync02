import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        c["source"] = [s.replace("faiss-gpu", "faiss-cpu") for s in c["source"]]

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Reverted to faiss-cpu.")
