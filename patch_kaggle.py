import json

with open("CogniSync_v3_final.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

def get_cell(substring):
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "code" and any(substring in line for line in c["source"]):
            return i
    raise ValueError(f"Cell with {substring} not found")

def set_code(substring, replacer_func):
    idx = get_cell(substring)
    text = "".join(nb["cells"][idx]["source"])
    text = replacer_func(text)
    nb["cells"][idx]["source"] = [line + "\n" for line in text.split("\n")]


# Optimize pip install for Kaggle
def optimize_pip(text):
    return text.replace("faiss-cpu", "faiss-gpu")
set_code("!pip install datasets", replacer_func=optimize_pip)

# Optimize RetrievalSystem
def optimize_retrieval(text):
    
    # Increase batch size for GPU parallelization
    text = text.replace("doc_embeddings = self.encoder.encode(documents, show_progress_bar=False)",
                        "doc_embeddings = self.encoder.encode(documents, show_progress_bar=False, batch_size=512)")
    
    # Utilize faiss multi-GPU
    text = text.replace("""        index = faiss.IndexFlatIP(doc_embeddings.shape[1])
        faiss.normalize_L2(doc_embeddings)
        index.add(doc_embeddings)""",
                        """        cpu_index = faiss.IndexFlatIP(doc_embeddings.shape[1])
        try:
            # Distribute FAISS computation across all available GPUs (Kaggle dual T4)
            index = faiss.index_cpu_to_all_gpus(cpu_index)
        except Exception:
            index = cpu_index  # Fallback
            
        faiss.normalize_L2(doc_embeddings)
        index.add(doc_embeddings)""")
        
    return text

set_code("class RetrievalSystem:", replacer_func=optimize_retrieval)

# Rename internal save zips to match the new file name
for c in nb["cells"]:
    if c["cell_type"] == "code":
        c["source"] = [s.replace("CogniSync_v3_final", "CogniSync_v3_kaggle") for s in c["source"]]

with open("CogniSync_v3_kaggle.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("Kaggle Optimization complete! Saved to CogniSync_v3_kaggle.ipynb")
