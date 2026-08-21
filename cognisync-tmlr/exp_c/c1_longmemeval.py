"""C1: does the episodic graph help, on a benchmark someone else built?

LongMemEval (ICLR 2025) has 500 instances of timestamped multi-session chat history and a
question taxonomy with two categories the episodic design makes a prediction about:

    temporal-reasoning   "what happened before X" - the design's motivating case
    knowledge-update     a fact changes across sessions; the recent one wins

and four it makes no prediction about (single-session-user, single-session-assistant,
single-session-preference, multi-session). Reporting the slices separately is what makes
the result interpretable either way: a graph that helps everywhere is probably just a
better retriever, and a graph that helps nowhere is a negative result worth publishing.

Two levels of measurement:

    retrieval   recall@k of the turns LongMemEval marks `has_answer`, and session-level
                recall against `answer_session_ids`. No generation needed, so this runs
                fast and is the primary number.
    end-task    QA accuracy with a local judge, on the subset where retrieval succeeded
                and where it did not, so the reader can separate retrieval failure from
                reasoning failure.

The 30 abstention instances (question_id ending `_abs`) are skipped, following the
benchmark authors.

Usage
-----
    python -m exp_c.c1_longmemeval --variant s --n-instances 100
    python -m exp_c.c1_longmemeval --variant s --with-qa --judge qwen2.5-3b
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DENSE_ENCODERS, GENERATORS, set_all_seeds
from common.data import load_longmemeval
from common.io_utils import write_result

from exp_c.episodic_graph import (
    BM25Memory,
    DecayMemory,
    EpisodicGraph,
    FlatDenseMemory,
    SimilarityGraphMemory,
    parse_timestamp,
)

PREDICTED_TO_HELP = {"temporal-reasoning", "knowledge-update"}


def flatten_instance(instance: dict) -> Tuple[List[dict], float]:
    """Turn a LongMemEval instance into a flat list of turn records."""
    sessions = instance.get("haystack_sessions", [])
    session_ids = instance.get("haystack_session_ids", [f"s{i}" for i in range(len(sessions))])
    dates = instance.get("haystack_dates", [""] * len(sessions))

    turns: List[dict] = []
    for s_idx, session in enumerate(sessions):
        sid = str(session_ids[s_idx]) if s_idx < len(session_ids) else f"s{s_idx}"
        ts = parse_timestamp(dates[s_idx] if s_idx < len(dates) else "")
        for t_idx, turn in enumerate(session):
            content = (turn.get("content") or "").strip()
            if not content:
                continue
            turns.append(
                {
                    "node_id": f"{sid}::{t_idx}",
                    "session_id": sid,
                    "turn_index": t_idx,
                    "role": turn.get("role", "user"),
                    "text": content,
                    "timestamp": ts + t_idx,        # keep within-session order strict
                    "is_evidence": bool(turn.get("has_answer", False)),
                }
            )
    return turns, parse_timestamp(instance.get("question_date", ""))


def build_systems(encoder, turns: Sequence[dict], enable_edges, use_decay: bool, consolidate: bool) -> Dict[str, object]:
    units = [(t["node_id"], t["text"]) for t in turns]
    timestamps = {t["node_id"]: t["timestamp"] for t in turns}

    session_texts: Dict[str, List[str]] = defaultdict(list)
    for t in turns:
        session_texts[t["session_id"]].append(t["text"])
    session_units = [(sid, "\n".join(texts)) for sid, texts in session_texts.items()]

    graph = EpisodicGraph(encoder, use_time_decay=use_decay, consolidate=consolidate)
    for t in turns:
        graph.add_event(
            text=t["text"],
            timestamp=t["timestamp"],
            session_id=t["session_id"],
            turn_index=t["turn_index"],
            role=t["role"],
            is_evidence=t["is_evidence"],
            node_id=t["node_id"],
        )
    graph.build_edges(enable=enable_edges).index()

    return {
        "bm25": BM25Memory().build(units),
        "dense-turn": FlatDenseMemory(encoder, "turn").build(units),
        "dense-session": FlatDenseMemory(encoder, "session").build(session_units),
        "similarity-graph": SimilarityGraphMemory(encoder).build(units),
        "decay": DecayMemory(encoder).build(units, timestamps=timestamps),
        "episodic-graph": graph,
    }


def score_retrieval(
    retrieved: Sequence[Tuple[str, float]],
    evidence_nodes: Sequence[str],
    evidence_sessions: Sequence[str],
    ks: Sequence[int],
    granularity: str,
) -> Dict[str, float]:
    ids = [r[0] for r in retrieved]
    ev_nodes, ev_sessions = set(evidence_nodes), set(evidence_sessions)
    out: Dict[str, float] = {}

    for k in ks:
        head = ids[:k]
        if granularity == "session":
            hit_sessions = set(head)
        else:
            hit_sessions = {i.split("::")[0] for i in head}
            out[f"turn_recall@{k}"] = (
                len(set(head) & ev_nodes) / len(ev_nodes) if ev_nodes else float("nan")
            )
            out[f"turn_hit@{k}"] = float(bool(set(head) & ev_nodes))
        out[f"session_recall@{k}"] = (
            len(hit_sessions & ev_sessions) / len(ev_sessions) if ev_sessions else float("nan")
        )
        out[f"session_hit@{k}"] = float(bool(hit_sessions & ev_sessions))
    return out


def judge_answer(generator, question: str, gold: str, prediction: str) -> bool:
    """Binary correctness judgement with a fixed rubric, so it is reproducible."""
    prompt = (
        f"Question: {question}\n"
        f"Reference answer: {gold}\n"
        f"Candidate answer: {prediction}\n\n"
        "Does the candidate answer convey the same information as the reference answer? "
        "Ignore differences in wording, length and formatting. Answer with one word, yes or no."
    )
    verdict = generator.generate("You grade answers strictly against a reference.", prompt)
    return verdict.strip().lower().startswith("y")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variant", default="s", choices=["s", "m", "oracle"])
    ap.add_argument("--n-instances", type=int, default=100)
    ap.add_argument("--encoder", default="minilm")
    ap.add_argument("--ks", nargs="+", type=int, default=[1, 3, 5, 10, 20])
    ap.add_argument("--top-k", type=int, default=20)
    ap.add_argument("--hops", type=int, default=1)
    ap.add_argument("--expansion-budget", type=int, default=40)
    ap.add_argument("--with-qa", action="store_true", help="also run generation and judge the answers")
    ap.add_argument("--qa-model", default="qwen2.5-3b", choices=list(GENERATORS))
    ap.add_argument("--qa-context-k", type=int, default=10)
    ap.add_argument("--systems", nargs="+", default=None)
    ap.add_argument("--tag", default="c1_longmemeval")
    args = ap.parse_args()

    set_all_seeds()

    from sentence_transformers import SentenceTransformer

    spec = DENSE_ENCODERS[args.encoder]
    encoder = SentenceTransformer(spec["name"], **({"revision": spec["revision"]} if spec["revision"] != "main" else {}))

    instances = load_longmemeval(args.variant)
    instances = [i for i in instances if not str(i.get("question_id", "")).endswith("_abs")]
    instances = instances[: args.n_instances]
    print(f"[c1] {len(instances)} instances (abstention instances excluded)")

    generator = None
    if args.with_qa:
        from exp_b.b3_downstream_compliance import Generator

        generator = Generator(args.qa_model, max_new_tokens=96)

    rows, graph_stats = [], []

    for inst in tqdm(instances, desc="instances"):
        turns, question_time = flatten_instance(inst)
        if not turns:
            continue

        evidence_nodes = [t["node_id"] for t in turns if t["is_evidence"]]
        evidence_sessions = [str(s) for s in inst.get("answer_session_ids", [])]
        if not evidence_sessions:
            evidence_sessions = sorted({n.split("::")[0] for n in evidence_nodes})

        systems = build_systems(encoder, turns, ("temporal", "entity", "precedes"), True, True)
        if args.systems:
            systems = {k: v for k, v in systems.items() if k in args.systems}

        graph_stats.append({"question_id": inst.get("question_id"), **systems["episodic-graph"].stats()}
                          if "episodic-graph" in systems else {})

        for name, system in systems.items():
            kwargs = {"top_k": args.top_k}
            if name == "episodic-graph":
                kwargs.update(
                    {"hops": args.hops, "expansion_budget": args.expansion_budget, "query_time": question_time}
                )
            elif name == "decay":
                kwargs["query_time"] = question_time

            retrieved = system.retrieve(inst["question"], **kwargs)
            granularity = "session" if name == "dense-session" else "turn"
            scores = score_retrieval(retrieved, evidence_nodes, evidence_sessions, args.ks, granularity)

            row = {
                "question_id": inst.get("question_id"),
                "question_type": inst.get("question_type", "unknown"),
                "predicted_to_help": inst.get("question_type") in PREDICTED_TO_HELP,
                "system": name,
                "n_turns": len(turns),
                "n_sessions": len({t["session_id"] for t in turns}),
                "n_evidence_turns": len(evidence_nodes),
                **scores,
            }

            if generator is not None:
                node_text = {t["node_id"]: t["text"] for t in turns}
                session_text = defaultdict(list)
                for t in turns:
                    session_text[t["session_id"]].append(t["text"])
                context = []
                for rid, _ in retrieved[: args.qa_context_k]:
                    context.append("\n".join(session_text[rid]) if granularity == "session" else node_text.get(rid, ""))
                prompt = (
                    "Conversation history excerpts:\n\n"
                    + "\n\n---\n\n".join(c[:800] for c in context)
                    + f"\n\nToday's date: {inst.get('question_date', 'unknown')}\n"
                    + f"Question: {inst['question']}\n\nAnswer concisely."
                )
                prediction = generator.generate(
                    "You answer questions using the user's conversation history.", prompt
                )
                row["prediction"] = prediction[:300]
                row["qa_correct"] = int(judge_answer(generator, inst["question"], inst.get("answer", ""), prediction))

            rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        print("[c1] no results")
        return

    metric_cols = [c for c in df.columns if c.startswith(("turn_", "session_")) or c == "qa_correct"]
    overall = df.groupby("system")[metric_cols].mean(numeric_only=True).reset_index()
    by_type = df.groupby(["system", "question_type"])[metric_cols].mean(numeric_only=True).reset_index()
    by_prediction = df.groupby(["system", "predicted_to_help"])[metric_cols].mean(numeric_only=True).reset_index()

    write_result(
        args.tag,
        overall,
        per_query=df,
        config={
            "variant": args.variant,
            "n_instances": len(instances),
            "encoder": spec,
            "top_k": args.top_k,
            "hops": args.hops,
            "expansion_budget": args.expansion_budget,
            "qa_model": GENERATORS.get(args.qa_model) if args.with_qa else None,
            "note": (
                "Abstention instances excluded, following the LongMemEval authors. "
                "temporal-reasoning and knowledge-update are the categories the episodic "
                "design predicts an advantage on; the rest are controls."
            ),
        },
    )
    write_result(f"{args.tag}__by_question_type", by_type)
    write_result(f"{args.tag}__by_prediction", by_prediction)
    if graph_stats and any(graph_stats):
        write_result(f"{args.tag}__graph_stats", pd.DataFrame([g for g in graph_stats if g]))

    print("\n" + "=" * 92)
    print("Overall")
    print("=" * 92)
    show = [c for c in ["session_hit@5", "session_recall@5", "turn_hit@5", "turn_recall@10", "qa_correct"] if c in overall]
    print(overall[["system"] + show].round(4).to_string(index=False))

    print("\nThe categories the design makes a prediction about:")
    key = "session_hit@5" if "session_hit@5" in by_prediction else metric_cols[0]
    pivot = by_prediction.pivot(index="system", columns="predicted_to_help", values=key)
    pivot.columns = ["control categories", "temporal-reasoning + knowledge-update"]
    pivot["difference"] = pivot.iloc[:, 1] - pivot.iloc[:, 0]
    print(pivot.round(4).to_string())

    if "episodic-graph" in set(overall["system"]) and "similarity-graph" in set(overall["system"]):
        from common.metrics import paired_bootstrap

        e = df[df.system == "episodic-graph"].set_index("question_id")
        s = df[df.system == "similarity-graph"].set_index("question_id")
        shared = sorted(set(e.index) & set(s.index))
        sig_rows = []
        for slice_name, subset in (
            ("all", shared),
            ("predicted", [q for q in shared if e.loc[q, "predicted_to_help"]]),
            ("control", [q for q in shared if not e.loc[q, "predicted_to_help"]]),
        ):
            if not subset:
                continue
            boot = paired_bootstrap(e.loc[subset, key].tolist(), s.loc[subset, key].tolist())
            sig_rows.append({"slice": slice_name, "metric": key, **boot})
        sig_df = pd.DataFrame(sig_rows)
        print("\nEpisodic graph minus similarity graph (same retrieval procedure, different edges):")
        print(sig_df.round(4).to_string(index=False))
        write_result(f"{args.tag}__significance", sig_df)


if __name__ == "__main__":
    main()
