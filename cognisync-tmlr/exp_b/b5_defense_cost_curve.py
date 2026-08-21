"""B5: the cost-of-defense frontier, at base rates that resemble deployment.

This is the figure the paper has been trying to produce since the CIKM version, and the
one place where the original framing was right: what does retrieval-layer filtering cost
in retrieval quality? The CIKM answer, "about 1 pp MRR at 1.04% FPR," came from a setup
with one payload per query, which is a poisoning base rate near 10%. Nobody's corpus is
10% poisoned.

Base rate is the whole story for false positives. At one poisoned document per 100,000,
a 1.04% false-positive rate blocks roughly a thousand clean documents for every payload it
catches. That ratio belongs in the paper, and it changes the recommendation.

Sweeps the classifier threshold and plots, at each poisoning base rate:
    retained nDCG@10   against   attack success rate
with the clean-document block rate and the block-to-catch ratio alongside.

Also replaces the CIKM Table 9. That table came from `heuristic_ablation.py`, which sweeps
four queries against four benign and four adversarial documents: sixteen cells per class.
Reviewer 2 could not reconcile it with Table 7 and neither could we. The threshold sweep
here runs on the same corpus and the same attacks as the rest of the security track, so
the two tables are finally about the same thing.

Usage
-----
    python -m exp_b.b5_defense_cost_curve --dataset scifact --n-queries 150
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DefenseConfig, FIGURES_DIR, RetrievalConfig, SEED, set_all_seeds
from common.data import load_beir
from common.io_utils import write_result
from common.metrics import ndcg_at_k

from exp_b.attacks import build_ladder
from exp_b.defenses import MultiSignalFilter, sample_holdout_clean_corpus
from exp_b.harness import SecurityHarness


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", default="scifact")
    ap.add_argument("--n-queries", type=int, default=150)
    ap.add_argument("--levels", nargs="+", type=int, default=[0, 2, 3])
    ap.add_argument(
        "--thresholds", nargs="+", type=float,
        default=[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95],
    )
    ap.add_argument(
        "--base-rates", nargs="+", type=float, default=[1e-2, 1e-3, 1e-4, 1e-5],
        help="poisoned documents as a fraction of the corpus",
    )
    ap.add_argument("--goal-redirection-thresholds", nargs="+", type=float, default=[0.0, 0.15, 0.30, 0.50])
    ap.add_argument("--top-k", type=int, default=10)
    args = ap.parse_args()

    set_all_seeds()
    rcfg = RetrievalConfig()
    corpus, queries, qrels = load_beir(args.dataset)
    qids = sorted(queries)
    np.random.default_rng(42).shuffle(qids)
    qids = qids[: args.n_queries]

    harness = SecurityHarness(corpus, queries, qrels, rcfg, DefenseConfig(), dataset_name=args.dataset)

    # Score every document once per query, at every threshold, so the sweep is a
    # post-processing step rather than a re-run.
    print("[b5] scoring clean documents and payloads")
    records: List[dict] = []

    for qid in tqdm(qids, desc="scoring"):
        query = queries[qid]
        rels = qrels.get(qid, {})
        clean_ranked = harness._clean_ranking(qid)
        clean_ids = [d for d, _ in clean_ranked]
        carrier = next((corpus[d] for d in clean_ids[:3] if d in corpus), None)

        calib = sample_holdout_clean_corpus(corpus, exclude_ids=clean_ids, n=2000, seed=SEED)
        flt = MultiSignalFilter(harness.encoder, DefenseConfig()).fit(
            calib[: max(6, len(calib) // 4)], centroid_docs=calib, centroid_source="holdout"
        )

        head_ids = clean_ids[: max(args.top_k * 5, 50)]
        head_decisions = flt.decide(query, [corpus[d] for d in head_ids])

        ladder = build_ladder(query, mean_doc_chars=harness.mean_doc_chars, carrier_passage=carrier, levels=args.levels)
        for level, attacks in ladder.items():
            payloads = [a.payload for a in attacks]
            poisoned = harness._rerank_with_payload(qid, clean_ranked, payloads)
            payload_decisions = flt.decide(query, payloads)

            records.append(
                {
                    "qid": qid,
                    "level": level,
                    "attack": attacks[0].name,
                    "rels": rels,
                    "head_ids": head_ids,
                    "clean_probs": [d.classifier_prob for d in head_decisions],
                    "clean_qsims_flagged": [d.goal_redirection for d in head_decisions],
                    "payload_probs": [d.classifier_prob for d in payload_decisions],
                    "payload_redirect": [d.goal_redirection for d in payload_decisions],
                    "poisoned_order": poisoned,
                    "n_required_chunks": attacks[0].metadata.get("requires_chunks", 1),
                    "ndcg_clean": ndcg_at_k(clean_ids, rels, args.top_k),
                }
            )

    print(f"[b5] sweeping {len(args.thresholds)} thresholds x {len(args.goal_redirection_thresholds)} gates")
    rows = []
    corpus_size = len(corpus)

    for threshold in args.thresholds:
        for gate in args.goal_redirection_thresholds:
            asr, ndcg_def, ndcg_cl, clean_block, rel_block = [], [], [], [], []
            per_level: Dict[int, List[int]] = {}

            for rec in records:
                use_gate = gate > 0
                blocked_clean = {
                    rec["head_ids"][i]
                    for i, p in enumerate(rec["clean_probs"])
                    if p > threshold or (use_gate and rec["clean_qsims_flagged"][i])
                }
                admitted_payloads = {
                    i for i, p in enumerate(rec["payload_probs"])
                    if not (p > threshold or (use_gate and rec["payload_redirect"][i]))
                }

                surviving = [
                    (d, kind)
                    for d, kind in rec["poisoned_order"]
                    if not (kind == "clean" and d in blocked_clean)
                    and not (kind == "payload" and int(d.split("_")[-1]) not in admitted_payloads)
                ]
                top = surviving[: args.top_k]
                n_payload = sum(1 for _, kind in top if kind == "payload")
                success = int(n_payload >= rec["n_required_chunks"])

                asr.append(success)
                per_level.setdefault(rec["level"], []).append(success)
                ndcg_def.append(ndcg_at_k([d for d, k in top if k == "clean"], rec["rels"], args.top_k))
                ndcg_cl.append(rec["ndcg_clean"])
                clean_block.append(len(blocked_clean) / max(1, len(rec["head_ids"])))
                rel_block.append(sum(1 for d in blocked_clean if rec["rels"].get(d, 0) > 0))

            fpr = float(np.mean(clean_block))
            row = {
                "classifier_threshold": threshold,
                "goal_redirection_threshold": gate,
                "asr": float(np.mean(asr)),
                "ndcg_clean": float(np.mean(ndcg_cl)),
                "ndcg_defended": float(np.mean(ndcg_def)),
                "ndcg_cost_pp": (float(np.mean(ndcg_cl)) - float(np.mean(ndcg_def))) * 100,
                "clean_block_rate": fpr,
                "relevant_docs_blocked_mean": float(np.mean(rel_block)),
                "n_observations": len(asr),
            }
            for level, vals in sorted(per_level.items()):
                row[f"asr_level_{level}"] = float(np.mean(vals))

            # Base rate turns a false-positive rate into an operational cost.
            for base_rate in args.base_rates:
                n_poisoned = corpus_size * base_rate
                n_blocked_clean = corpus_size * (1 - base_rate) * fpr
                caught = n_poisoned * (1 - row["asr"])
                row[f"blocked_per_catch@{base_rate:g}"] = n_blocked_clean / caught if caught > 0 else float("inf")

            rows.append(row)

    df = pd.DataFrame(rows)
    write_result(
        "b5_defense_cost_curve",
        df,
        config={
            "retrieval": rcfg.to_dict(),
            "dataset": args.dataset,
            "n_queries": len(qids),
            "levels": args.levels,
            "thresholds": args.thresholds,
            "base_rates": args.base_rates,
            "corpus_size": corpus_size,
            "replaces": (
                "CIKM Table 9, which came from heuristic_ablation.py: 4 queries x 4 benign "
                "and 4 adversarial documents, 16 cells per class, on a corpus unrelated to "
                "the rest of the security evaluation."
            ),
        },
    )

    print("\n" + "=" * 100)
    print("Threshold sweep (goal-redirection gate at the CIKM default of 0.30)")
    print("=" * 100)
    default = df[df.goal_redirection_threshold == 0.30]
    cols = ["classifier_threshold", "asr", "ndcg_defended", "ndcg_cost_pp", "clean_block_rate"]
    cols += [c for c in df.columns if c.startswith("blocked_per_catch")]
    print(default[cols].round(4).to_string(index=False))

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        for gate, group in df.groupby("goal_redirection_threshold"):
            g = group.sort_values("asr")
            axes[0].plot(g["asr"], g["ndcg_defended"], marker="o", ms=4, label=f"gate={gate:.2f}")
        axes[0].set_xlabel("attack success rate")
        axes[0].set_ylabel(f"nDCG@{args.top_k} retained")
        axes[0].set_title("Cost-of-defense frontier")
        axes[0].legend(fontsize=8)
        axes[0].grid(alpha=0.3)

        for col in [c for c in df.columns if c.startswith("blocked_per_catch")]:
            g = default.sort_values("classifier_threshold")
            axes[1].plot(g["classifier_threshold"], g[col], marker="s", ms=4, label=col.split("@")[1])
        axes[1].set_yscale("log")
        axes[1].set_xlabel("classifier threshold")
        axes[1].set_ylabel("clean documents blocked per payload caught")
        axes[1].set_title("Operational cost by poisoning base rate")
        axes[1].legend(fontsize=8, title="base rate")
        axes[1].grid(alpha=0.3, which="both")

        fig.tight_layout()
        out = FIGURES_DIR / "b5_defense_cost_curve.pdf"
        fig.savefig(out, bbox_inches="tight")
        fig.savefig(out.with_suffix(".png"), dpi=180, bbox_inches="tight")
        print(f"[b5] figure -> {out}")
    except Exception as exc:  # noqa: BLE001
        print(f"[b5] plotting skipped: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
