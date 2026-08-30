"""B4: where does a three-feature filter sit on the cost-quality frontier?

The CIKM paper reports 86.36% accuracy on `deepset/prompt-injections` with no baseline, so
the number floats free. A keyword regex sets the floor and a 184M-parameter DeBERTa
detector sets a realistic ceiling. Between them, the interesting question is whether the
cheap filter is close enough to be worth a thousand-fold latency saving on a local-first
deployment, which is the paper's whole premise.

Also runs the transfer matrix. Train on distribution A, test on B, both ways. Reviewers 1
and 2 both doubted that six poison templates generalise; this measures it instead of
asserting it, and includes the six-template regime as a condition so the effect of
training-set size is visible.

Usage
-----
    python -m exp_b.b4_detector_comparison
    python -m exp_b.b4_detector_comparison --skip-transformers   # if the Hub is unreachable
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DefenseConfig, DENSE_ENCODERS, INJECTION_DETECTORS, SEED, set_all_seeds
from common.data import load_prompt_injection_corpus
from common.io_utils import write_result

from exp_b.defenses import (
    CIKM_POISON_TEMPLATES,
    KeywordRegexFilter,
    MultiSignalFilter,
    TransformerDetector,
    measure_throughput,
)


def classification_report_row(y_true: Sequence[int], y_prob: Sequence[float], threshold: float = 0.5) -> Dict[str, float]:
    from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score

    y_true = np.asarray(y_true)
    y_pred = (np.asarray(y_prob) >= threshold).astype(int)

    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())

    try:
        auc = float(roc_auc_score(y_true, y_prob))
    except ValueError:
        auc = float("nan")

    return {
        "accuracy": float((y_pred == y_true).mean()),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "f1_benign": float(f1_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "f1_injection": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "precision_injection": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall_injection": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "roc_auc": auc,
        # The two rates the paper actually needs: what fraction of attacks get through,
        # and what fraction of clean documents get blocked.
        "attack_success_rate": fn / max(1, fn + tp),
        "false_positive_rate": fp / max(1, fp + tn),
        "n_test": int(len(y_true)),
    }


def build_three_feature_filter(
    encoder, train_texts: Sequence[str], train_labels: Sequence[int], regime: str
) -> MultiSignalFilter:
    """Fit the CIKM filter under one of three training regimes.

    `six_templates` reproduces the CIKM classifier exactly: six clean documents from the
    corpus plus the six synthetic poison strings. `public` uses the real training split.
    The gap between them is the answer to "does six examples generalise?".
    """
    cfg = DefenseConfig(train_regime=regime, centroid_source="holdout")
    flt = MultiSignalFilter(encoder, cfg)

    clean = [t for t, y in zip(train_texts, train_labels) if y == 0]
    poison = [t for t, y in zip(train_texts, train_labels) if y == 1]

    if regime == "six_templates":
        return flt.fit(clean[:6], poison_docs=list(CIKM_POISON_TEMPLATES), centroid_docs=clean, centroid_source="holdout")
    if regime == "public_plus_templates":
        return flt.fit(clean, poison_docs=poison + list(CIKM_POISON_TEMPLATES), centroid_docs=clean, centroid_source="holdout")
    return flt.fit(clean, poison_docs=poison, centroid_docs=clean, centroid_source="holdout")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpora", nargs="+", default=["deepset", "jailbreak"])
    ap.add_argument("--regimes", nargs="+", default=["six_templates", "public"])
    ap.add_argument("--encoder", default="minilm")
    ap.add_argument("--skip-transformers", action="store_true")
    ap.add_argument("--test-size", type=float, default=0.2)
    args = ap.parse_args()

    set_all_seeds()

    from sentence_transformers import SentenceTransformer
    from sklearn.model_selection import train_test_split

    spec = DENSE_ENCODERS[args.encoder]
    encoder = SentenceTransformer(spec["name"], **({"revision": spec["revision"]} if spec["revision"] != "main" else {}))

    splits: Dict[str, Tuple[List[str], List[int], List[str], List[int]]] = {}
    for name in args.corpora:
        try:
            texts, labels = load_prompt_injection_corpus(name)
        except Exception as exc:  # noqa: BLE001
            print(f"[b4] could not load {name}: {type(exc).__name__}: {exc}")
            continue
        tr_x, te_x, tr_y, te_y = train_test_split(
            texts, labels, test_size=args.test_size, random_state=SEED, stratify=labels
        )
        splits[name] = (tr_x, tr_y, te_x, te_y)
        print(f"[b4] {name}: {len(texts)} examples ({sum(labels)} injections), test n={len(te_x)}")

    if not splits:
        print("[b4] no corpora loaded")
        return

    rows, cost_rows = [], []

    # Zero-shot detectors: no training, so they are evaluated on every test split.
    detectors = {"keyword-regex": KeywordRegexFilter()}
    if not args.skip_transformers:
        for key in INJECTION_DETECTORS:
            try:
                detectors[key] = TransformerDetector(key)
            except Exception as exc:  # noqa: BLE001
                print(f"[b4] skipping {key}: {type(exc).__name__}: {exc}")

    for name, det in detectors.items():
        for test_corpus, (_, _, te_x, te_y) in splits.items():
            probs = det.block_probability(te_x)
            row = classification_report_row(te_y, probs)
            row.update(
                {
                    "detector": name,
                    "train_corpus": "zero-shot",
                    "test_corpus": test_corpus,
                    "regime": "zero-shot",
                    "params_m": getattr(det, "params_m", 0.0),
                }
            )
            rows.append(row)
            print(f"  {name:22s} -> {test_corpus:10s} macro-F1={row['macro_f1']:.4f}  FPR={row['false_positive_rate']:.4f}")

        sample = next(iter(splits.values()))[2][:256]
        cost = measure_throughput(det, sample)
        cost.update({"detector": name, "params_m": getattr(det, "params_m", 0.0), "n_docs": len(sample)})
        cost_rows.append(cost)

    # The three-feature filter, trained on each corpus under each regime, tested on both.
    for regime in args.regimes:
        for train_corpus, (tr_x, tr_y, _, _) in splits.items():
            flt = build_three_feature_filter(encoder, tr_x, tr_y, regime)
            for test_corpus, (_, _, te_x, te_y) in splits.items():
                probs = flt.block_probability(te_x)
                row = classification_report_row(te_y, probs)
                row.update(
                    {
                        "detector": f"three-feature ({regime})",
                        "train_corpus": train_corpus,
                        "test_corpus": test_corpus,
                        "regime": regime,
                        "params_m": 0.0,
                        "transfer": train_corpus != test_corpus,
                    }
                )
                rows.append(row)
                marker = "transfer" if train_corpus != test_corpus else "in-domain"
                print(
                    f"  3-feat/{regime:22s} {train_corpus}->{test_corpus:10s} "
                    f"macro-F1={row['macro_f1']:.4f} ({marker})"
                )

            if regime == "public" and train_corpus == args.corpora[0]:
                sample = next(iter(splits.values()))[2][:256]
                cost = measure_throughput(flt, sample)
                cost.update({"detector": "three-feature", "params_m": 0.0, "n_docs": len(sample)})
                cost_rows.append(cost)

    df = pd.DataFrame(rows)
    cost_df = pd.DataFrame(cost_rows)

    write_result(
        "b4_detector_comparison",
        df,
        config={
            "encoder": spec,
            "detectors": INJECTION_DETECTORS,
            "corpora": args.corpora,
            "regimes": args.regimes,
            "cikm_reference": (
                "CIKM reported 86.36% accuracy, F1 0.89 benign / 0.81 injection on deepset. "
                "That corresponds to detector='three-feature (public)', train=test=deepset here. "
                "The CIKM run refit the centroid and length normaliser on deepset's own train "
                "split, so it measures a retrained filter rather than a transferred one."
            ),
        },
    )
    write_result("b4_detector_cost", cost_df)

    print("\n" + "=" * 92)
    print("In-domain performance and cost")
    print("=" * 92)
    in_domain = df[(df.train_corpus == "zero-shot") | (df.train_corpus == df.test_corpus)]
    print(
        in_domain[["detector", "test_corpus", "macro_f1", "attack_success_rate", "false_positive_rate", "params_m"]]
        .round(4)
        .to_string(index=False)
    )

    transfer = df[df.get("transfer", False) == True]  # noqa: E712
    if len(transfer):
        print("\nCross-distribution transfer:")
        print(transfer[["detector", "train_corpus", "test_corpus", "macro_f1", "attack_success_rate"]].round(4).to_string(index=False))

    if len(cost_df):
        print("\nCost per document:")
        print(cost_df[["detector", "ms_per_doc", "docs_per_sec", "params_m"]].round(4).to_string(index=False))

        # The frontier claim, as a sentence the paper can use verbatim.
        cheap = cost_df[cost_df.detector == "three-feature"]
        heavy = cost_df[cost_df.params_m > 50]
        if len(cheap) and len(heavy):
            speedup = float(heavy["ms_per_doc"].min() / cheap["ms_per_doc"].iloc[0])
            f1_cheap = in_domain[in_domain.detector.str.startswith("three-feature")]["macro_f1"].max()
            f1_heavy = in_domain[in_domain.params_m > 50]["macro_f1"].max()
            print(
                f"\nFrontier: the three-feature filter is {speedup:.0f}x faster per document "
                f"and {(f1_heavy - f1_cheap) * 100:.1f} macro-F1 points behind the best "
                f"transformer detector."
            )


if __name__ == "__main__":
    main()
