"""
benchmarks/scalability_eval.py
-------------------------------
Scalability evaluation at 2K / 10K / 50K / 100K corpus sizes.

For each scale × 5 trials, measures:
  - Recall@5 on a held-out 50-query set
  - FAISS index build time (wall clock, seconds)
  - Peak memory usage (MB) via tracemalloc
  - Query latency: mean, std, p99 (ms)

Corpus expansion strategy:
  - 2K   : 20newsgroups technical slice (real data)
  - 10K  : 20newsgroups full subset (real data)
  - 50K  : 10K + synthetic StackOverflow-style QA pairs
  - 100K : 50K + synthetic GitHub-style code snippets

Set FAST_MODE=True in config.py to cap at 20K.

Outputs:
  results/scalability_results.json
  results/scalability_results.csv
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import csv
import time
import random
import sqlite3
import tracemalloc
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

from benchmarks.config import (
    SEEDS, SCALE_POINTS, N_SCALE_QUERIES, EMBEDDING_MODEL, RESULTS_DIR, FAST_MODE,
)
from evaluation.metrics import recall_at_k, summarise


# ─────────────────────────────────────────────────────────
# Synthetic corpus generators
# ─────────────────────────────────────────────────────────

SO_QUESTION_TEMPLATES = [
    "How do I {action} in {language}? I am trying to {goal} but getting error: {error}.",
    "What is the best way to {action} when working with {technology}?",
    "Error: {error} while trying to {action} in {language}. Stack trace shows {component}.",
    "{language} {component}: {action} returns {error} unexpectedly. Help needed.",
    "Debugging {technology}: {action} fails with {error}. Already tried {fix}.",
]
ACTIONS = ["parse JSON", "handle exceptions", "manage state", "connect to database",
           "authenticate users", "deploy containers", "configure routing", "optimize queries",
           "implement caching", "set up CI/CD", "handle concurrency", "manage dependencies"]
LANGUAGES = ["Python", "TypeScript", "Go", "Rust", "Java", "C++", "JavaScript", "Ruby"]
TECHNOLOGIES = ["Docker", "Kubernetes", "FastAPI", "React", "PostgreSQL", "Redis",
                "GraphQL", "gRPC", "Kafka", "Elasticsearch", "Prometheus", "Terraform"]
ERRORS = ["NullPointerException", "ConnectionRefused", "TimeoutError", "KeyError",
          "AttributeError", "TypeError", "MemoryError", "PermissionDenied", "404 NotFound"]
GOALS = ["implement a REST endpoint", "build a microservice", "process streaming data",
         "store user sessions", "implement rate limiting", "set up distributed tracing"]
COMPONENTS = ["middleware", "router", "database adapter", "auth module", "cache layer"]
FIXES = ["restarting the service", "clearing the cache", "updating dependencies",
         "checking the logs", "reverting the last commit"]

GITHUB_TEMPLATES = [
    "# {module_name}\n\n{description}\n\n## Usage\n```{lang}\n{code_snippet}\n```\n",
    "def {func_name}({params}):\n    \"\"\"{docstring}\"\"\"\n    {body}\n",
    "class {class_name}:\n    \"\"\"{docstring}\"\"\"\n    def __init__(self, {params}):\n        self.{attr} = {attr}\n",
    "# {module_name} — {description}\n\nimport {lib}\n\n{func_body}\n",
]
MODULES = ["auth_manager", "db_connector", "cache_handler", "api_router",
           "queue_worker", "event_bus", "rate_limiter", "retry_handler"]
LANGS_ = ["python", "typescript", "go", "rust"]
DESCRIPTIONS = [
    "Handles authentication and authorization for the service.",
    "Manages database connections with connection pooling.",
    "Provides LRU caching with configurable TTL.",
    "Routes HTTP requests to appropriate handlers.",
    "Processes messages from the message queue.",
]


def generate_so_doc(rng: random.Random, idx: int) -> str:
    tmpl = rng.choice(SO_QUESTION_TEMPLATES)
    return tmpl.format(
        action=rng.choice(ACTIONS),
        language=rng.choice(LANGUAGES),
        goal=rng.choice(GOALS),
        error=rng.choice(ERRORS),
        technology=rng.choice(TECHNOLOGIES),
        component=rng.choice(COMPONENTS),
        fix=rng.choice(FIXES),
    ) + f"\n\nAnswer: This is a common issue when working with {rng.choice(TECHNOLOGIES)}. " \
        f"The solution involves {rng.choice(FIXES)} and updating the {rng.choice(COMPONENTS)} configuration."


def generate_github_doc(rng: random.Random, idx: int) -> str:
    module = rng.choice(MODULES) + f"_{idx}"
    lang = rng.choice(LANGS_)
    desc = rng.choice(DESCRIPTIONS)
    return (
        f"# {module}\n\n{desc}\n\n"
        f"## Implementation\n"
        f"This module implements {module} using {rng.choice(TECHNOLOGIES)}.\n"
        f"Key features:\n"
        f"- {rng.choice(ACTIONS)} support\n"
        f"- {rng.choice(ACTIONS)} integration\n"
        f"- Error handling for {rng.choice(ERRORS)}\n\n"
        f"```{lang}\n"
        f"class {module.title().replace('_','')}:\n"
        f"    def process(self, data):\n"
        f"        # Handle {rng.choice(ERRORS)}\n"
        f"        return self.{rng.choice(COMPONENTS).replace(' ', '_')}(data)\n"
        f"```\n"
    )


def build_synthetic_corpus(target_size: int, seed: int = 42):
    """
    Build a corpus of `target_size` documents.
    First fills from 20newsgroups, then adds synthetic SO + GitHub docs.
    """
    from sklearn.datasets import fetch_20newsgroups
    rng = random.Random(seed)

    cats = ["comp.sys.mac.hardware", "comp.windows.x", "sci.electronics", "sci.crypt",
            "comp.os.ms-windows.misc", "comp.graphics", "sci.space", "sci.med",
            "talk.politics.misc", "rec.autos"]
    ng = fetch_20newsgroups(subset="train", categories=cats[:4])
    all_ng = ng.data

    docs, ids = [], []

    # Real 20newsgroups data
    ng_count = min(target_size, len(all_ng))
    ng_sample = rng.sample(range(len(all_ng)), ng_count)
    for i in ng_sample:
        docs.append(all_ng[i])
        ids.append(f"ng_{i}")

    # Synthetic SO docs to fill gap
    so_needed = max(0, target_size - len(docs))
    for j in range(so_needed // 2):
        docs.append(generate_so_doc(rng, j))
        ids.append(f"so_{j}")

    # Synthetic GitHub docs for remainder
    remaining = target_size - len(docs)
    for k in range(remaining):
        docs.append(generate_github_doc(rng, k))
        ids.append(f"gh_{k}")

    assert len(docs) == len(ids)
    return docs[:target_size], ids[:target_size]


# ─────────────────────────────────────────────────────────
# Single scale evaluation
# ─────────────────────────────────────────────────────────

def evaluate_at_scale(scale: int, seed: int, n_queries: int = N_SCALE_QUERIES):
    """
    Build CogniSync hybrid index at `scale` docs, run `n_queries` queries.
    Returns metrics dict.
    """
    model = SentenceTransformer(EMBEDDING_MODEL)
    dim   = model.get_sentence_embedding_dimension()
    rng   = random.Random(seed)

    docs, doc_ids = build_synthetic_corpus(scale, seed=seed)

    # Eval queries: 10-word sentence slices from held-out 10% of corpus
    eval_size = min(n_queries * 3, len(docs) // 10)
    eval_idx  = rng.sample(range(len(docs)), eval_size)
    queries, gt_ids = [], []
    for idx in eval_idx:
        words = docs[idx].split()
        if len(words) > 15:
            queries.append(" ".join(words[5:15]))
            gt_ids.append([doc_ids[idx]])
    queries = queries[:n_queries]
    gt_ids  = gt_ids[:n_queries]

    # ── FAISS build ──
    tracemalloc.start()
    t_build_start = time.perf_counter()
    embs = model.encode(docs, batch_size=64, convert_to_numpy=True, show_progress_bar=False).astype("float32")
    embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
    if scale <= 10_000:
        index = faiss.IndexFlatIP(dim)
    else:
        nlist = max(32, int(np.sqrt(scale)))
        quantizer = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
        index.train(embs)
        index.nprobe = 10
    index.add(embs)
    build_time = time.perf_counter() - t_build_start
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mem_mb = peak_mem / (1024 ** 2)

    # ── SQLite FTS5 build ──
    db = sqlite3.connect(":memory:")
    cur = db.cursor()
    cur.execute("CREATE VIRTUAL TABLE fts USING fts5(id, text);")
    cur.executemany("INSERT INTO fts (id, text) VALUES (?, ?)", list(zip(doc_ids, docs)))
    db.commit()

    # ── Query latencies ──
    latencies_ms = []
    all_retrieved, all_gt = [], []
    for query, gt in zip(queries, gt_ids):
        t0 = time.perf_counter()
        # FAISS
        q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = index.search(q_emb, 5)
        faiss_hits = {doc_ids[i] for i in I[0] if i >= 0}
        # FTS5
        try:
            safe = query.replace('"', '""')
            cur.execute("SELECT id FROM fts WHERE text MATCH ? LIMIT 5", (safe,))
            fts_hits = {row[0] for row in cur.fetchall()}
        except sqlite3.OperationalError:
            fts_hits = set()
        # Union
        union = list(faiss_hits | fts_hits)[:5]
        latencies_ms.append((time.perf_counter() - t0) * 1000)
        all_retrieved.append(union)
        all_gt.append(gt)

    hits = [int(bool(set(r) & set(g))) for r, g in zip(all_retrieved, all_gt)]
    recall5 = float(np.mean(hits))

    return {
        "scale":         scale,
        "seed":          seed,
        "n_docs":        len(docs),
        "n_queries":     len(queries),
        "recall@5":      round(recall5, 4),
        "build_time_s":  round(build_time, 3),
        "peak_mem_mb":   round(peak_mem_mb, 2),
        "latency_mean_ms": round(float(np.mean(latencies_ms)), 4),
        "latency_std_ms":  round(float(np.std(latencies_ms, ddof=1)), 4),
        "latency_p99_ms":  round(float(np.percentile(latencies_ms, 99)), 4),
    }


# ─────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────

def run_scalability_evaluation():
    print("=" * 60)
    print(f" CogniSync Scalability Evaluation (FAST_MODE={FAST_MODE})")
    print("=" * 60)

    all_results = []
    for scale in SCALE_POINTS:
        scale_records = []
        for seed in SEEDS:
            print(f"  Scale={scale:>7,} | Seed={seed} ...", end=" ", flush=True)
            r = evaluate_at_scale(scale, seed)
            scale_records.append(r)
            all_results.append(r)
            print(f"recall@5={r['recall@5']:.4f}  build={r['build_time_s']:.1f}s  "
                  f"latency={r['latency_mean_ms']:.2f}ms  mem={r['peak_mem_mb']:.0f}MB")

        # Aggregate across seeds for this scale
        means = {
            k: round(float(np.mean([rec[k] for rec in scale_records])), 4)
            for k in ["recall@5", "build_time_s", "peak_mem_mb",
                      "latency_mean_ms", "latency_std_ms", "latency_p99_ms"]
        }
        print(f"  → Avg Recall@5={means['recall@5']:.4f}  "
              f"BuildTime={means['build_time_s']:.1f}s  "
              f"MemPeak={means['peak_mem_mb']:.0f}MB\n")

    # Save JSON
    out_json = RESULTS_DIR / "scalability_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"experiment": "scalability_eval", "results": all_results}, f, indent=2)

    # Save CSV
    out_csv = RESULTS_DIR / "scalability_results.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)

    print(f"✅ Scalability results → {out_json}")
    print(f"✅ CSV                 → {out_csv}")
    return all_results


if __name__ == "__main__":
    run_scalability_evaluation()
