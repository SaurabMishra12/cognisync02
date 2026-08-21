"""Shared evaluation loop for the security track.

The CIKM protocol inserted exactly one payload into each query's candidate pool and asked
whether it landed in the top 5. Two things go wrong with that.

First, one payload per query is a base rate of roughly 1 in 10, which is nothing like a
poisoned corpus. Base rate drives the false-positive cost: at one poisoned document per
100k, a 1.04% false-positive rate blocks about a thousand clean documents for every real
catch. The paper's "1 pp MRR cost" is a statement about the wrong base rate.

Second, measuring "did the payload enter the top k" and calling it attack success counts a
retrieved-but-ignored document as a win for the attacker. b3 measures what the model
actually does; this module measures entry, and reports both so the gap is visible.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.config import DefenseConfig, RetrievalConfig, SEED
from common.metrics import ndcg_at_k
from common.retrieval import BM25Index, DenseIndex, HybridRetriever

from exp_b.attacks import Attack, build_ladder
from exp_b.defenses import MultiSignalFilter, sample_holdout_clean_corpus


@dataclass
class AttackOutcome:
    query_id: str
    level: int
    attack_name: str
    knowledge: str
    centroid_source: str

    entered_topk_undefended: bool
    entered_topk_defended: bool
    payload_blocked: bool
    n_payload_chunks: int
    n_payload_chunks_admitted: int

    ndcg_clean: float
    ndcg_defended: float
    clean_docs_blocked: int
    clean_docs_total: int
    relevant_docs_blocked: int

    block_prob: float = 0.0
    goal_redirection_fired: bool = False
    attacker_queries_used: int = 0
    payload_text: str = ""
    metadata: Dict[str, object] = field(default_factory=dict)


class SecurityHarness:
    """Poison a real corpus, retrieve, filter, and score entry plus quality cost."""

    def __init__(
        self,
        corpus: Dict[str, str],
        queries: Dict[str, str],
        qrels: Dict[str, Dict[str, int]],
        retrieval_cfg: RetrievalConfig,
        defense_cfg: DefenseConfig,
        dataset_name: str = "corpus",
    ):
        self.corpus, self.queries, self.qrels = corpus, queries, qrels
        self.rcfg, self.dcfg = retrieval_cfg, defense_cfg
        self.dataset_name = dataset_name

        self.doc_ids = list(corpus)
        self.doc_texts = [corpus[d] for d in self.doc_ids]
        self.mean_doc_chars = int(np.mean([len(t) for t in self.doc_texts]))

        print(f"[harness] indexing {len(self.doc_ids)} docs (mean {self.mean_doc_chars} chars)")
        self.dense = DenseIndex(retrieval_cfg.encoder_key, batch_size=retrieval_cfg.batch_size).build(
            self.doc_ids, self.doc_texts, cache_tag=dataset_name
        )
        self.lexical = BM25Index().build(self.doc_ids, self.doc_texts)
        self.retriever = HybridRetriever(retrieval_cfg, self.dense, self.lexical)
        self.encoder = self.dense.model

    # ----------------------------------------------------------------------------------

    def _clean_ranking(self, qid: str) -> List[Tuple[str, float]]:
        return self.retriever.retrieve(
            self.queries[qid], strategy="learned+fallback", depth=self.rcfg.first_stage_depth, record=False
        )

    def _rerank_with_payload(
        self, qid: str, clean_ranked: List[Tuple[str, float]], payloads: List[str]
    ) -> List[Tuple[str, str]]:
        """Insert payloads into the ranking by scoring them against the query directly.

        Re-indexing the whole corpus per attack would cost hours. Scoring the payload with
        the same encoder and splicing it in by score is equivalent for entry measurement
        and orders of magnitude cheaper. The BM25 channel is approximated by the dense
        score, which is conservative in the attacker's favour for camouflaged payloads
        (they are written to score well semantically) and slightly against it for
        keyword-stuffed ones.
        """
        import faiss

        q_emb = self.encoder.encode([self.queries[qid]], convert_to_numpy=True).astype("float32")
        p_emb = self.encoder.encode(payloads, convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(q_emb)
        faiss.normalize_L2(p_emb)
        payload_scores = (p_emb @ q_emb[0]).tolist()

        merged: List[Tuple[str, str, float]] = [(d, "clean", s) for d, s in clean_ranked]
        for i, s in enumerate(payload_scores):
            merged.append((f"__payload_{i}", "payload", float(s)))

        # Clean scores come from fused min-max values in [0, 1]; payload scores are raw
        # cosines, also in [0, 1] for a normalised encoder, so the scales are comparable.
        merged.sort(key=lambda x: -x[2])
        return [(d, kind) for d, kind, _ in merged]

    # ----------------------------------------------------------------------------------

    def evaluate_query(
        self,
        qid: str,
        levels: Sequence[int],
        centroid_source: str,
        filter_obj: Optional[MultiSignalFilter] = None,
        attacker_budget: int = 200,
        top_k: int = 10,
    ) -> List[AttackOutcome]:
        query = self.queries[qid]
        rels = self.qrels.get(qid, {})
        clean_ranked = self._clean_ranking(qid)
        clean_ids = [d for d, _ in clean_ranked]
        ndcg_clean = ndcg_at_k(clean_ids, rels, top_k)

        # Filter calibration. "oracle" reproduces the CIKM setup, fitting the centroid on
        # the query's own retrieved documents; "holdout" fits on a disjoint sample.
        if centroid_source == "oracle":
            calib_docs = [self.corpus[d] for d in clean_ids[: self.rcfg.first_stage_depth]]
        else:
            calib_docs = sample_holdout_clean_corpus(
                self.corpus, exclude_ids=clean_ids, n=self.dcfg.holdout_clean_docs, seed=SEED
            )

        flt = filter_obj or MultiSignalFilter(self.encoder, self.dcfg)
        flt.fit(calib_docs[: max(6, len(calib_docs) // 4)], centroid_docs=calib_docs, centroid_source=centroid_source)

        # A real relevant passage as the L3/L5 carrier: the attacker scrapes the corpus.
        carrier = next((self.corpus[d] for d in clean_ids[:3] if d in self.corpus), None)

        ladder = build_ladder(
            query,
            seed=SEED,
            mean_doc_chars=self.mean_doc_chars,
            carrier_passage=carrier,
            score_fn=flt.score_fn(query) if 5 in levels else None,
            levels=levels,
            budget=attacker_budget,
        )

        outcomes: List[AttackOutcome] = []
        for level, attacks in ladder.items():
            payloads = [a.payload for a in attacks]
            poisoned = self._rerank_with_payload(qid, clean_ranked, payloads)

            entered_undefended = any(kind == "payload" for _, kind in poisoned[:top_k])

            decisions = flt.decide(query, payloads)
            admitted = [i for i, d in enumerate(decisions) if not d.blocked]

            # Clean-side false positives, on the documents the query actually retrieved.
            head_ids = clean_ids[:top_k]
            head_decisions = flt.decide(query, [self.corpus[d] for d in head_ids])
            blocked_clean = {head_ids[i] for i, d in enumerate(head_decisions) if d.blocked}
            relevant_blocked = sum(1 for d in blocked_clean if rels.get(d, 0) > 0)

            surviving = [
                (d, kind)
                for d, kind in poisoned
                if not (kind == "clean" and d in blocked_clean)
                and not (kind == "payload" and int(d.split("_")[-1]) not in admitted)
            ]
            top = surviving[:top_k]
            n_payload_in_top = sum(1 for _, kind in top if kind == "payload")

            # A split payload only succeeds if enough chunks land together.
            required = attacks[0].metadata.get("requires_chunks", 1) if attacks else 1
            entered_defended = n_payload_in_top >= required

            defended_ids = [d for d, kind in top if kind == "clean"]
            ndcg_defended = ndcg_at_k(defended_ids, rels, top_k)

            outcomes.append(
                AttackOutcome(
                    query_id=qid,
                    level=level,
                    attack_name=attacks[0].name,
                    knowledge=attacks[0].knowledge,
                    centroid_source=centroid_source,
                    entered_topk_undefended=entered_undefended,
                    entered_topk_defended=entered_defended,
                    payload_blocked=len(admitted) < len(payloads),
                    n_payload_chunks=len(payloads),
                    n_payload_chunks_admitted=len(admitted),
                    ndcg_clean=ndcg_clean,
                    ndcg_defended=ndcg_defended,
                    clean_docs_blocked=len(blocked_clean),
                    clean_docs_total=len(head_ids),
                    relevant_docs_blocked=relevant_blocked,
                    block_prob=float(np.mean([d.classifier_prob for d in decisions])),
                    goal_redirection_fired=any(d.goal_redirection for d in decisions),
                    attacker_queries_used=int(attacks[0].metadata.get("queries_used", 0)),
                    payload_text=payloads[0][:400],
                    metadata=dict(attacks[0].metadata),
                )
            )
        return outcomes

    def run(
        self,
        qids: Sequence[str],
        levels: Sequence[int] = (0, 1, 2, 3, 4, 5),
        centroid_sources: Sequence[str] = ("holdout",),
        attacker_budget: int = 200,
        top_k: int = 10,
    ) -> List[AttackOutcome]:
        out: List[AttackOutcome] = []
        for source in centroid_sources:
            for qid in tqdm(qids, desc=f"centroid={source}"):
                try:
                    out.extend(
                        self.evaluate_query(qid, levels, source, attacker_budget=attacker_budget, top_k=top_k)
                    )
                except Exception as exc:  # noqa: BLE001
                    print(f"[harness] query {qid} failed: {type(exc).__name__}: {exc}")
        return out


def summarise(outcomes: Sequence[AttackOutcome]) -> "pd.DataFrame":
    import pandas as pd

    rows = [
        {
            "query_id": o.query_id,
            "level": o.level,
            "attack": o.attack_name,
            "knowledge": o.knowledge,
            "centroid_source": o.centroid_source,
            "asr_undefended": int(o.entered_topk_undefended),
            "asr_defended": int(o.entered_topk_defended),
            "payload_blocked": int(o.payload_blocked),
            "chunks_admitted_frac": o.n_payload_chunks_admitted / max(1, o.n_payload_chunks),
            "ndcg_clean": o.ndcg_clean,
            "ndcg_defended": o.ndcg_defended,
            "ndcg_cost_pp": (o.ndcg_clean - o.ndcg_defended) * 100,
            "clean_block_rate": o.clean_docs_blocked / max(1, o.clean_docs_total),
            "relevant_blocked": o.relevant_docs_blocked,
            "block_prob": o.block_prob,
            "goal_redirection_fired": int(o.goal_redirection_fired),
            "attacker_queries_used": o.attacker_queries_used,
        }
        for o in outcomes
    ]
    return pd.DataFrame(rows)
