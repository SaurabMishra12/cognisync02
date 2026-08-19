"""
benchmarks/agent_task_eval.py
------------------------------
End-to-end task evaluation using a context-sufficiency oracle.

No LLM API key required. The oracle scores whether the retrieved context
*contains* the ground-truth constraint/chunk needed to complete a task.
This is equivalent to asking: "Would the agent have succeeded if given
only this retrieved context?"

Tasks (from CogniSync Benchmark):
  - code_generation  (20 instances)
  - debugging        (20 instances)
  - api_integration  (20 instances)
  - cross_session    (20 instances)

Systems:
  - CogniSync Hybrid   (WITH memory)
  - Zero-Shot Baseline (WITHOUT memory = empty retrieval)
  - Vanilla RAG        (FAISS-only retrieval for comparison)

Metrics per task type × system:
  - Task success rate (%)
  - Mean rank of correct chunk (proxy for iterations-to-success)
  - Token usage (= top_k × AVG_TOKENS_PER_CHUNK)
  - Latency per task (ms)

Outputs:
  results/agent_task_eval.json
  results/agent_task_eval.csv
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import csv
import time
import sqlite3
import random
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

from benchmarks.config import (
    SEEDS, DEFAULT_TOP_K, AVG_TOKENS_PER_CHUNK, EMBEDDING_MODEL,
    BENCHMARK_JSON, RESULTS_DIR, TASK_TYPES, N_TASKS_PER_TYPE,
)
from evaluation.metrics import summarise
from evaluation.statistical_tests import run_all_tests, aggregate_trials


# ─────────────────────────────────────────────────────────
# Load benchmark
# ─────────────────────────────────────────────────────────

def load_tasks():
    """
    Load CogniSync Benchmark and return per-task-type query lists.
    Returns: {task_type: [(query, gt_chunk_ids, required_constraints), ...]}
    """
    if not BENCHMARK_JSON.exists():
        raise FileNotFoundError(
            f"Benchmark not found at {BENCHMARK_JSON}. "
            "Run data/generate_benchmark_dataset.py first."
        )
    with open(BENCHMARK_JSON, encoding="utf-8") as f:
        dataset = json.load(f)

    # Build corpus
    docs   = [s["content"] for s in dataset["sessions"]]
    ids    = [s["chunk_ids"][0] for s in dataset["sessions"]]

    # Group queries by task type
    tasks_by_type = {tt: [] for tt in TASK_TYPES}
    for q in dataset["eval_queries"]:
        tt = q["task_type"]
        if tt in tasks_by_type:
            tasks_by_type[tt].append({
                "query":       q["query"],
                "gt_ids":      q["ground_truth_chunk_ids"],
                "constraints": q["required_constraints"],
                "workflow":    q["workflow_id"],
            })

    # Cap to N_TASKS_PER_TYPE each
    for tt in tasks_by_type:
        tasks_by_type[tt] = tasks_by_type[tt][:N_TASKS_PER_TYPE]

    return docs, ids, tasks_by_type


# ─────────────────────────────────────────────────────────
# Retrieval systems
# ─────────────────────────────────────────────────────────

class _CogniSyncTask:
    def __init__(self, model):
        self.model = model
        self.dim = model.get_sentence_embedding_dimension()
        self.index = None
        self.doc_ids = []
        self.db = None
        self.cursor = None

    def build(self, docs, doc_ids):
        embs = self.model.encode(docs, batch_size=64, convert_to_numpy=True, show_progress_bar=False).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
        self.doc_ids = doc_ids
        self.db = sqlite3.connect(":memory:")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE VIRTUAL TABLE fts USING fts5(id, text);")
        self.cursor.executemany("INSERT INTO fts (id, text) VALUES (?, ?)", zip(doc_ids, docs))
        self.db.commit()

    def retrieve(self, query, top_k=DEFAULT_TOP_K):
        t0 = time.perf_counter()
        fts_hits = set()
        try:
            safe = query.replace('"', '""')
            self.cursor.execute("SELECT id FROM fts WHERE text MATCH ? LIMIT ?", (safe, top_k))
            fts_hits = {row[0] for row in self.cursor.fetchall()}
        except sqlite3.OperationalError:
            pass
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = self.index.search(q_emb, top_k)
        faiss_hits = {self.doc_ids[i] for i in I[0] if i >= 0}
        union = list(fts_hits | faiss_hits)[:top_k]
        for i in I[0]:
            if i >= 0 and self.doc_ids[i] not in union:
                union.append(self.doc_ids[i])
        return union[:top_k], (time.perf_counter() - t0) * 1000


class _VanillaRAGTask:
    def __init__(self, model):
        self.model = model
        self.dim = model.get_sentence_embedding_dimension()
        self.index = None
        self.doc_ids = []

    def build(self, docs, doc_ids):
        embs = self.model.encode(docs, batch_size=64, convert_to_numpy=True, show_progress_bar=False).astype("float32")
        embs /= np.maximum(np.linalg.norm(embs, axis=1, keepdims=True), 1e-12)
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
        self.doc_ids = doc_ids

    def retrieve(self, query, top_k=DEFAULT_TOP_K):
        t0 = time.perf_counter()
        q_emb = self.model.encode([query], convert_to_numpy=True).astype("float32")
        q_emb /= np.maximum(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12)
        _, I = self.index.search(q_emb, top_k)
        ids = [self.doc_ids[i] for i in I[0] if i >= 0]
        return ids, (time.perf_counter() - t0) * 1000


class _ZeroShotTask:
    """Zero-shot baseline: no retrieval, empty context."""
    def build(self, docs, doc_ids):
        pass

    def retrieve(self, query, top_k=DEFAULT_TOP_K):
        return [], 0.0


# ─────────────────────────────────────────────────────────
# Oracle scorer
# ─────────────────────────────────────────────────────────

def oracle_rank(retrieved_ids, gt_ids):
    """
    Return rank of first ground-truth hit (1-indexed).
    Return top_k+1 if not found (represents 'never found' = max iterations).
    """
    gt_set = set(gt_ids)
    for rank, rid in enumerate(retrieved_ids, start=1):
        if rid in gt_set:
            return rank
    return len(retrieved_ids) + 1


# ─────────────────────────────────────────────────────────
# Main evaluation
# ─────────────────────────────────────────────────────────

def run_agent_task_evaluation(top_k: int = DEFAULT_TOP_K):
    print("=" * 60)
    print(" CogniSync End-to-End Agent Task Evaluation")
    print("=" * 60)

    docs, doc_ids, tasks_by_type = load_tasks()
    model = SentenceTransformer(EMBEDDING_MODEL)

    SYSTEMS = {
        "CogniSync (Hybrid)": _CogniSyncTask,
        "Vanilla RAG":        _VanillaRAGTask,
        "Zero-Shot (No Mem)": _ZeroShotTask,
    }

    all_results = {}   # system_name → {task_type → list of per-trial metric dicts}

    for sys_name, SysCls in SYSTEMS.items():
        print(f"\n[{sys_name}]")
        all_results[sys_name] = {}
        trial_task_successes = []   # per-trial, all tasks combined

        for seed in SEEDS:
            random.seed(seed)
            sys = SysCls(model) if SysCls != _ZeroShotTask else _ZeroShotTask()
            if SysCls == _ZeroShotTask:
                sys.build(docs, doc_ids)
            else:
                sys.build(docs, doc_ids)

            per_type_results = {}
            trial_hits = []

            for task_type in TASK_TYPES:
                tasks = tasks_by_type[task_type]
                successes, ranks, latencies, token_usages = [], [], [], []

                for task in tasks:
                    retrieved, lat = sys.retrieve(task["query"], top_k)
                    hit = int(bool(set(retrieved) & set(task["gt_ids"])))
                    rank = oracle_rank(retrieved, task["gt_ids"])

                    successes.append(hit)
                    ranks.append(rank)
                    latencies.append(lat)
                    token_usages.append(len(retrieved) * AVG_TOKENS_PER_CHUNK)
                    trial_hits.append(hit)

                per_type_results[task_type] = {
                    "success_rate": float(np.mean(successes)),
                    "mean_rank":    float(np.mean(ranks)),
                    "latency_ms":   float(np.mean(latencies)),
                    "tokens_per_task": float(np.mean(token_usages)),
                    "n_tasks":      len(tasks),
                }
                print(f"  Seed={seed} | {task_type:20s} success={np.mean(successes):.2%}  "
                      f"rank={np.mean(ranks):.2f}  lat={np.mean(latencies):.2f}ms")

            trial_task_successes.append(trial_hits)

        # Aggregate across seeds per task type
        all_results[sys_name]["_trial_hits"] = trial_task_successes

        # Aggregate per-trial success rates across task types
        overall_success = {
            task_type: aggregate_trials(
                [[t[task_type]["success_rate"]] for t in [per_type_results]]
            )
            for task_type in TASK_TYPES
        }
        all_results[sys_name]["aggregated"] = overall_success

    # Statistical tests: CogniSync vs others
    cs_hits = [h for trial in all_results["CogniSync (Hybrid)"]["_trial_hits"] for h in trial]
    stat_results = {}
    for sys_name in ["Vanilla RAG", "Zero-Shot (No Mem)"]:
        other_hits = [h for trial in all_results[sys_name]["_trial_hits"] for h in trial]
        stat_results[sys_name] = run_all_tests(
            cs_hits, other_hits,
            label_a="CogniSync", label_b=sys_name,
        )

    # Build clean output (remove private _trial_hits)
    clean_results = {
        k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
        for k, v in all_results.items()
    }

    output = {
        "experiment":       "agent_task_eval",
        "top_k":            top_k,
        "seeds":            SEEDS,
        "task_types":       TASK_TYPES,
        "n_tasks_per_type": N_TASKS_PER_TYPE,
        "systems":          clean_results,
        "statistical_tests": stat_results,
    }

    out_json = RESULTS_DIR / "agent_task_eval.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\n✅ Agent task results → {out_json}")

    # CSV summary
    out_csv = RESULTS_DIR / "agent_task_eval.csv"
    rows = []
    # Flatten to system × task_type rows using the last trial's per_type_results
    for sys_name in SYSTEMS:
        for task_type in TASK_TYPES:
            rows.append({
                "System":        sys_name,
                "Task Type":     task_type,
                "Success Rate":  round(clean_results[sys_name].get("aggregated", {}).get(task_type, {}).get("mean", 0), 4),
            })
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["System", "Task Type", "Success Rate"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Agent task CSV   → {out_csv}")
    return output


if __name__ == "__main__":
    run_agent_task_evaluation()
