import json

with open("CogniSync_v3_kaggle.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for c in nb["cells"]:
    if c["cell_type"] == "code":
        text = "".join(c["source"])
        if 'ds_nq = load_and_verify("natural_questions"' in text:
            new_text = text.replace(
                'ds_nq = load_and_verify("natural_questions", None, "validation", 2000)',
                '''print("Streaming natural_questions to avoid 50GB Kaggle Disk crash...")
    nq_stream = load_dataset("natural_questions", split="validation", streaming=True, trust_remote_code=True)
    import itertools
    ds_nq = list(itertools.islice(nq_stream, 2000))'''
            )
            c["source"] = [line + "\n" for line in new_text.split("\n")[:-1] if new_text] # quick fix

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Patched NQ to stream natively.")
