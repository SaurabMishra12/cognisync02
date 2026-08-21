"""C2: which part of the graph is doing the work, and is the temporal structure real?

Edge types, decay, consolidation and hop budget, each toggled. Plus the control that makes
the whole section credible:

    shuffle the timestamps

If accuracy holds up when temporal order is destroyed, the temporal edges are decorative
and the graph is a similarity graph with extra steps. Reporting that plainly is a fine
outcome for a TMLR paper and a much better one than quietly not running the check. Two
shuffle modes are included, because they fail differently:

    within-session   session order preserved, turn order scrambled inside each session
    global           every timestamp reassigned at random, destroying all order

Usage
-----
    python -m exp_c.c2_graph_ablation --n-instances 100
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DENSE_ENCODERS, SEED, set_all_seeds
from common.data import load_longmemeval
from common.io_utils import write_result
from common.metrics import paired_bootstrap

from exp_c.c1_longmemeval import PREDICTED_TO_HELP, flatten_instance, score_retrieval
from exp_c.episodic_graph import ENTITY, PRECEDES, TEMPORAL, EpisodicGraph

EDGE_SETS = [
    ((TEMPORAL,), "temporal only"),
    ((ENTITY,), "entity only"),
    ((PRECEDES,), "precondition only"),
    ((TEMPORAL, ENTITY), "temporal + entity"),
    ((TEMPORAL, PRECEDES), "temporal + precondition"),
    ((ENTITY, PRECEDES), "entity + precondition"),
    ((TEMPORAL, ENTITY, PRECEDES), "all three"),
]


def shuffle_timestamps(turns: List[dict], mode: str, rng: np.random.Generator) -> List[dict]:
    """Destroy temporal order while leaving text and session membership untouched."""
    out = [dict(t) for t in turns]
    if mode == "none":
        return out
    if mode == "within-session":
        by_session: Dict[str, List[int]] = {}
        for i, t in enumerate(out):
            by_session.setdefault(t["session_id"], []).append(i)
        for indices in by_session.values():
            stamps = [out[i]["timestamp"] for i in indices]
            rng.shuffle(stamps)
            for i, ts in zip(indices, stamps):
                out[i]["timestamp"] = ts
        return out
    if mode == "global":
        stamps = [t["timestamp"] for t in out]
        rng.shuffle(stamps)
        for t, ts in zip(out, stamps):
            t["timestamp"] = ts
        return out
    raise ValueError(f"unknown shuffle mode {mode!r}")


def build_graph(encoder, turns: Sequence[dict], edges, use_decay: bool, consolidate: bool) -> EpisodicGraph:
    g = EpisodicGraph(encoder, use_time_decay=use_decay, consolidate=consolidate)
    for t in turns:
        g.add_event(
            text=t["text"], timestamp=t["timestamp"], session_id=t["session_id"],
            turn_index=t["turn_index"], role=t["role"], is_evidence=t["is_evidence"], node_id=t["node_id"],
        )
    return g.build_edges(enable=edges).index()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variant", default="s")
    ap.add_argument("--n-instances", type=int, default=100)
    ap.add_argument("--encoder", default="minilm")
    ap.add_argument("--top-k", type=int, default=20)
    ap.add_argument("--ks", nargs="+", type=int, default=[1, 3, 5, 10])
    ap.add_argument("--hops", nargs="+", type=int, default=[1, 2])
    ap.add_argument("--decay", nargs="+", type=int, default=[0, 1])
    ap.add_argument("--consolidate", nargs="+", type=int, default=[1])
    ap.add_argument("--shuffle-modes", nargs="+", default=["none", "within-session", "global"])
    ap.add_argument("--tag", default="c2_graph_ablation")
    args = ap.parse_args()

    set_all_seeds()

    from sentence_transformers import SentenceTransformer

    spec = DENSE_ENCODERS[args.encoder]
    encoder = SentenceTransformer(spec["name"], **({"revision": spec["revision"]} if spec["revision"] != "main" else {}))

    instances = load_longmemeval(args.variant)
    instances = [i for i in instances if not str(i.get("question_id", "")).endswith("_abs")]
    instances = instances[: args.n_instances]
    print(f"[c2] {len(instances)} instances")

    configurations = list(
        itertools.product(EDGE_SETS, args.hops, args.decay, args.consolidate, args.shuffle_modes)
    )
    print(f"[c2] {len(configurations)} configurations x {len(instances)} instances")

    rows, stat_rows = [], []
    rng_master = np.random.default_rng(SEED)

    for inst in tqdm(instances, desc="instances"):
        turns, question_time = flatten_instance(inst)
        if not turns:
            continue
        evidence_nodes = [t["node_id"] for t in turns if t["is_evidence"]]
        evidence_sessions = [str(s) for s in inst.get("answer_session_ids", [])] or sorted(
            {n.split("::")[0] for n in evidence_nodes}
        )

        for (edges, edge_label), hops, decay, consolidate, shuffle_mode in configurations:
            shuffled = shuffle_timestamps(turns, shuffle_mode, np.random.default_rng(rng_master.integers(1 << 31)))
            graph = build_graph(encoder, shuffled, edges, bool(decay), bool(consolidate))
            retrieved = graph.retrieve(
                inst["question"], top_k=args.top_k, hops=hops, expansion_budget=40, query_time=question_time
            )
            scores = score_retrieval(retrieved, evidence_nodes, evidence_sessions, args.ks, "turn")

            rows.append(
                {
                    "question_id": inst.get("question_id"),
                    "question_type": inst.get("question_type", "unknown"),
                    "predicted_to_help": inst.get("question_type") in PREDICTED_TO_HELP,
                    "edges": edge_label,
                    "hops": hops,
                    "time_decay": bool(decay),
                    "consolidation": bool(consolidate),
                    "shuffle": shuffle_mode,
                    **scores,
                }
            )
            if edge_label == "all three" and shuffle_mode == "none" and hops == args.hops[0]:
                stat_rows.append({"question_id": inst.get("question_id"), **graph.stats()})

    df = pd.DataFrame(rows)
    if df.empty:
        print("[c2] no results")
        return

    metric = f"session_hit@{args.ks[min(2, len(args.ks) - 1)]}"
    group_cols = ["edges", "hops", "time_decay", "consolidation", "shuffle"]
    metric_cols = [c for c in df.columns if c.startswith(("turn_", "session_"))]
    agg = df.groupby(group_cols)[metric_cols].mean(numeric_only=True).reset_index()

    write_result(
        args.tag,
        agg,
        per_query=df,
        config={
            "variant": args.variant,
            "n_instances": len(instances),
            "encoder": spec,
            "edge_sets": [label for _, label in EDGE_SETS],
            "shuffle_modes": args.shuffle_modes,
            "note": (
                "The shuffle modes are negative controls. If performance under 'global' "
                "matches 'none', the temporal and precondition edges carry no information "
                "and the graph reduces to a similarity graph."
            ),
        },
    )
    if stat_rows:
        write_result(f"{args.tag}__graph_stats", pd.DataFrame(stat_rows))

    print("\n" + "=" * 92)
    print(f"Edge ablation ({metric}, unshuffled, decay on)")
    print("=" * 92)
    view = agg[(agg.shuffle == "none") & (agg.time_decay)]
    print(view[group_cols + [metric]].round(4).to_string(index=False))

    print("\nNegative control: what happens when timestamps are shuffled")
    control = agg[(agg.edges == "all three") & (agg.time_decay)]
    print(control[["shuffle", "hops", metric]].round(4).to_string(index=False))

    # Paired test on the control, because this is the claim that decides the section.
    base = df[(df.edges == "all three") & (df.shuffle == "none") & (df.time_decay)].set_index("question_id")
    rows_sig = []
    for mode in [m for m in args.shuffle_modes if m != "none"]:
        shuf = df[(df.edges == "all three") & (df.shuffle == mode) & (df.time_decay)].set_index("question_id")
        shared = sorted(set(base.index) & set(shuf.index))
        if not shared:
            continue
        for slice_name, subset in (
            ("all", shared),
            ("predicted", [q for q in shared if base.loc[q, "predicted_to_help"]]),
            ("control", [q for q in shared if not base.loc[q, "predicted_to_help"]]),
        ):
            if not subset:
                continue
            boot = paired_bootstrap(base.loc[subset, metric].tolist(), shuf.loc[subset, metric].tolist())
            rows_sig.append({"shuffle": mode, "slice": slice_name, "metric": metric, **boot})

    if rows_sig:
        sig_df = pd.DataFrame(rows_sig)
        print("\nUnshuffled minus shuffled (positive means temporal order carries information):")
        print(sig_df.round(4).to_string(index=False))
        write_result(f"{args.tag}__shuffle_control", sig_df)


if __name__ == "__main__":
    main()
