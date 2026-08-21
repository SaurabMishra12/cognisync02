"""B1 + B2: the honest security numbers.

Two changes to the CIKM protocol, run as a grid so each one's effect is separable.

B1, the oracle. The CIKM evaluation fitted the filter's clean centroid on the query's own
retrieved documents at attack time. `--centroid-sources oracle holdout` runs both, so the
paper can report what the oracle was worth.

B2, the adversary. The CIKM evaluation used one payload containing two of the six words
the filter matches on. `--levels 0 1 2 3 4 5` walks up from that payload to an attacker
with decision access, adding one piece of knowledge per level.

Expect attack success to climb back toward the undefended rate somewhere around level 3.
That is the result. A defense that stops a payload carrying its own trigger word, and
stops nothing else, is worth reporting accurately.

Usage
-----
    python -m exp_b.b1_b2_attack_ladder --dataset scifact --n-queries 200
    python -m exp_b.b1_b2_attack_ladder --dataset fiqa --centroid-sources oracle holdout --levels 0 1 2 3 4 5
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DefenseConfig, RetrievalConfig, set_all_seeds
from common.data import load_beir
from common.io_utils import write_result
from common.metrics import paired_bootstrap

from exp_b.harness import SecurityHarness, summarise


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", default="scifact")
    ap.add_argument("--n-queries", type=int, default=200)
    ap.add_argument("--levels", nargs="+", type=int, default=[0, 1, 2, 3, 4, 5])
    ap.add_argument("--centroid-sources", nargs="+", default=["oracle", "holdout"])
    ap.add_argument("--attacker-budget", type=int, default=200)
    ap.add_argument("--top-k", type=int, default=10)
    ap.add_argument("--classifier-threshold", type=float, default=0.5)
    ap.add_argument("--tag", default="b1_b2_attack_ladder")
    args = ap.parse_args()

    set_all_seeds()
    rcfg = RetrievalConfig()
    dcfg = DefenseConfig(classifier_threshold=args.classifier_threshold)

    corpus, queries, qrels = load_beir(args.dataset)
    qids = sorted(queries)
    rng = np.random.default_rng(42)
    rng.shuffle(qids)
    qids = qids[: args.n_queries]
    print(f"[b1b2] {args.dataset}: {len(corpus)} docs, evaluating {len(qids)} queries")

    harness = SecurityHarness(corpus, queries, qrels, rcfg, dcfg, dataset_name=args.dataset)
    outcomes = harness.run(
        qids,
        levels=args.levels,
        centroid_sources=args.centroid_sources,
        attacker_budget=args.attacker_budget,
        top_k=args.top_k,
    )
    if not outcomes:
        print("[b1b2] no outcomes")
        return

    raw = summarise(outcomes)
    raw["dataset"] = args.dataset

    agg = (
        raw.groupby(["centroid_source", "level", "attack", "knowledge"])
        .agg(
            n=("query_id", "count"),
            asr_undefended=("asr_undefended", "mean"),
            asr_defended=("asr_defended", "mean"),
            payload_block_rate=("payload_blocked", "mean"),
            chunks_admitted=("chunks_admitted_frac", "mean"),
            ndcg_clean=("ndcg_clean", "mean"),
            ndcg_defended=("ndcg_defended", "mean"),
            ndcg_cost_pp=("ndcg_cost_pp", "mean"),
            clean_block_rate=("clean_block_rate", "mean"),
            mean_block_prob=("block_prob", "mean"),
            goal_redirection_rate=("goal_redirection_fired", "mean"),
            attacker_queries=("attacker_queries_used", "mean"),
        )
        .reset_index()
        .sort_values(["centroid_source", "level"])
    )
    agg["asr_reduction_pp"] = (agg["asr_undefended"] - agg["asr_defended"]) * 100
    agg["dataset"] = args.dataset

    write_result(
        args.tag,
        agg,
        per_query=raw,
        config={
            "retrieval": rcfg.to_dict(),
            "defense": dcfg.to_dict(),
            "dataset": args.dataset,
            "n_queries": len(qids),
            "levels": args.levels,
            "centroid_sources": args.centroid_sources,
            "cikm_baseline_note": (
                "CIKM Table 7 reported adaptive-injection ASR 99.30% -> 0.12% at FPR 1.04%. "
                "That configuration corresponds to centroid_source='oracle' and level=0 here."
            ),
        },
    )

    print("\n" + "=" * 92)
    print("Attack success by adversary knowledge and filter calibration")
    print("=" * 92)
    cols = [
        "centroid_source", "level", "attack", "n",
        "asr_undefended", "asr_defended", "payload_block_rate", "clean_block_rate", "ndcg_cost_pp",
    ]
    print(agg[cols].round(4).to_string(index=False))

    # B1's headline: what was the oracle worth?
    if {"oracle", "holdout"}.issubset(set(raw["centroid_source"])):
        print("\nOracle centroid minus held-out centroid, per level (paired by query):")
        rows = []
        for level in sorted(raw["level"].unique()):
            o = raw[(raw.centroid_source == "oracle") & (raw.level == level)].set_index("query_id")
            h = raw[(raw.centroid_source == "holdout") & (raw.level == level)].set_index("query_id")
            shared = sorted(set(o.index) & set(h.index))
            if not shared:
                continue
            boot = paired_bootstrap(
                h.loc[shared, "asr_defended"].tolist(), o.loc[shared, "asr_defended"].tolist()
            )
            rows.append(
                {
                    "level": level,
                    "asr_oracle": float(o.loc[shared, "asr_defended"].mean()),
                    "asr_holdout": float(h.loc[shared, "asr_defended"].mean()),
                    "delta_pp": boot["delta"] * 100,
                    "ci_low_pp": boot["ci_low"] * 100,
                    "ci_high_pp": boot["ci_high"] * 100,
                    "p": boot["p_value"],
                }
            )
        oracle_df = pd.DataFrame(rows)
        print(oracle_df.round(4).to_string(index=False))
        write_result(f"{args.tag}__oracle_effect", oracle_df)

    # B2's headline: how far up the ladder does the defense survive?
    hold = agg[agg.centroid_source == "holdout"]
    if len(hold):
        base = hold[hold.level == 0]["asr_defended"]
        base_val = float(base.iloc[0]) if len(base) else float("nan")
        worst = hold.loc[hold["asr_defended"].idxmax()]
        print(
            f"\nUnder a held-out centroid: ASR at level 0 is {base_val:.3f}; "
            f"the strongest level is {int(worst['level'])} ({worst['attack']}) at {worst['asr_defended']:.3f}, "
            f"against an undefended rate of {worst['asr_undefended']:.3f}."
        )


if __name__ == "__main__":
    main()
