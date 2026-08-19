import database
results = database.query_hybrid('Ghost Swarm architecture logit fusion Mistral TruthfulQA GSM8K results analysis', limit=10)
with open("results.txt", "w", encoding="utf-8") as f:
    if not results['results']:
        f.write("Zero results found.")
    else:
        for r in results['results']:
            content = r.get("content")
            source = r.get("metadata", {}).get("source")
            f.write(f"--- SOURCE: {source} ---\n{content}\n")
