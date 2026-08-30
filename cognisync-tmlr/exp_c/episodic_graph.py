"""A persistent episodic memory graph, implemented.

The CIKM submission described this design and evaluated none of it. Reviewer 4: "the
unimplemented episodic-memory section diminishes the contribution." Reviewer 1: "this part
feels more like a future-work idea than a contribution of the current paper." They were
right, so here it is.

The design claim from the CIKM paper, restated so it can be tested:

    Similarity-only memory answers "what do I know about X". It cannot answer "what
    happened just before X failed", because the passage that caused a failure is often
    topically unlike the failure itself. Directed temporal and precondition edges retrieve
    the sequence rather than the topic.

That claim makes a prediction: an episodic graph should help on temporal-reasoning and
knowledge-update questions and do nothing on single-session factual recall. LongMemEval
has exactly those categories, so the prediction is falsifiable, and c2 includes a
timestamp-shuffling control that will expose the structure as decorative if it is.

Three edge types:

    TEMPORAL   v_i -> v_j when v_j immediately follows v_i in the same session, and
               across the session boundary, giving a spine through the whole history.
    ENTITY     v_i -- v_j when they share a salient entity, which is what carries a
               referent forward across sessions.
    PRECEDES   v_i -> v_j when v_i is earlier, shares an entity with v_j, and sits within
               a bounded window. This is the "structural precondition" edge, approximated
               without an LLM. `link_with_llm` upgrades it when a generator is available.

Retrieval is seed-and-expand: dense similarity picks seeds, then a budgeted walk collects
neighbours scored by edge weight and recency, so a node adjacent to a strong seed can be
retrieved even when its own similarity to the query is low. That is the entire point.
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import numpy as np

TEMPORAL, ENTITY, PRECEDES = "temporal", "entity", "precedes"

_STOPWORDS = set(
    """a an and are as at be but by for from has have he her his i in is it its me my of on or our she
    that the their them they this to was we were what when where which who will with you your do does
    did not no so if then than there here about into over under can could would should may might must
    just very really also too more most some any all both each other same how why""".split()
)

_ENTITY_PATTERNS = [
    re.compile(r"\b[A-Z][a-zA-Z0-9]*(?:[-_][A-Za-z0-9]+)+\b"),   # Foo-Bar, snake_case ids
    re.compile(r"\b[A-Z]{2,}\b"),                                 # acronyms
    re.compile(r"\b\d{1,4}(?:\.\d+)+\b"),                         # version strings
    re.compile(r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b"),
    re.compile(r"\$\d[\d,]*(?:\.\d+)?"),                          # amounts
    re.compile(r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b"),              # dates
]


def extract_entities(text: str, max_entities: int = 12) -> Set[str]:
    """Cheap salient-token extraction.

    Deliberately not a full NER pipeline. LongMemEval turns are conversational, and the
    referents that matter across sessions are mostly proper nouns, identifiers and
    numbers. If a heavier extractor changes the conclusions that is worth knowing, and
    c2 has a switch for it.
    """
    found: Set[str] = set()
    for pattern in _ENTITY_PATTERNS:
        found.update(m.group(0).lower() for m in pattern.finditer(text))

    # Mid-sentence capitalised words, which the patterns above miss.
    tokens = re.findall(r"\b[A-Za-z][A-Za-z'-]+\b", text)
    for i, tok in enumerate(tokens):
        if i > 0 and tok[0].isupper() and tok.lower() not in _STOPWORDS:
            found.add(tok.lower())

    # Rare content words as a fallback, so entity-free turns still link somewhere.
    if len(found) < 3:
        content = [t.lower() for t in tokens if t.lower() not in _STOPWORDS and len(t) > 4]
        found.update(w for w, _ in Counter(content).most_common(3))

    return set(sorted(found)[:max_entities])


def parse_timestamp(value: object) -> float:
    """LongMemEval dates arrive in a few shapes. Fall back to 0 rather than crash."""
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str) or not value.strip():
        return 0.0
    for fmt in ("%Y/%m/%d (%a) %H:%M", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.strip(), fmt).timestamp()
        except ValueError:
            continue
    digits = re.findall(r"\d+", value)
    return float("".join(digits[:3])) if digits else 0.0


@dataclass
class EventNode:
    node_id: str
    text: str
    timestamp: float
    session_id: str
    turn_index: int
    role: str = "user"
    entities: Set[str] = field(default_factory=set)
    tools: List[str] = field(default_factory=list)
    is_evidence: bool = False          # LongMemEval's has_answer flag, for scoring only
    embedding: Optional[np.ndarray] = None


@dataclass
class Edge:
    source: str
    target: str
    kind: str
    weight: float = 1.0


class EpisodicGraph:
    """Event nodes with temporal, entity and precondition edges, plus a semantic store."""

    def __init__(
        self,
        encoder,
        entity_window_seconds: float = 60 * 60 * 24 * 30,
        max_entity_degree: int = 24,
        time_decay_halflife_days: float = 30.0,
        edge_weights: Optional[Dict[str, float]] = None,
        use_time_decay: bool = True,
        consolidate: bool = True,
    ):
        self.encoder = encoder
        self.entity_window = entity_window_seconds
        self.max_entity_degree = max_entity_degree
        self.halflife = time_decay_halflife_days * 86400
        self.edge_weights = edge_weights or {TEMPORAL: 0.6, ENTITY: 0.8, PRECEDES: 1.0}
        self.use_time_decay = use_time_decay
        self.do_consolidate = consolidate

        self.nodes: Dict[str, EventNode] = {}
        self.adjacency: Dict[str, List[Edge]] = defaultdict(list)
        self.entity_index: Dict[str, List[str]] = defaultdict(list)
        self._matrix: Optional[np.ndarray] = None
        self._order: List[str] = []
        self.semantic_store: List[dict] = []

    # -- construction -------------------------------------------------------------------

    def add_event(
        self,
        text: str,
        timestamp: float,
        session_id: str,
        turn_index: int,
        role: str = "user",
        tools: Optional[List[str]] = None,
        is_evidence: bool = False,
        node_id: Optional[str] = None,
    ) -> EventNode:
        nid = node_id or f"{session_id}::{turn_index}"
        node = EventNode(
            node_id=nid,
            text=text,
            timestamp=timestamp,
            session_id=session_id,
            turn_index=turn_index,
            role=role,
            entities=extract_entities(text),
            tools=tools or [],
            is_evidence=is_evidence,
        )
        self.nodes[nid] = node
        for ent in node.entities:
            self.entity_index[ent].append(nid)
        return node

    def build_edges(self, enable: Sequence[str] = (TEMPORAL, ENTITY, PRECEDES)) -> "EpisodicGraph":
        self.adjacency.clear()
        ordered = sorted(self.nodes.values(), key=lambda n: (n.timestamp, n.session_id, n.turn_index))

        if TEMPORAL in enable:
            for prev, curr in zip(ordered, ordered[1:]):
                # Within-session succession is a strong signal; the cross-session hop is
                # weaker but keeps the spine connected.
                w = 1.0 if prev.session_id == curr.session_id else 0.4
                self._add_edge(prev.node_id, curr.node_id, TEMPORAL, w)

        if ENTITY in enable or PRECEDES in enable:
            for ent, node_ids in self.entity_index.items():
                if len(node_ids) < 2 or len(node_ids) > self.max_entity_degree:
                    # A term shared by half the history carries no information and turns
                    # the graph into a clique. Skipping it is what keeps expansion useful.
                    continue
                members = sorted(node_ids, key=lambda n: self.nodes[n].timestamp)
                for i, a in enumerate(members):
                    for b in members[i + 1 :]:
                        na, nb = self.nodes[a], self.nodes[b]
                        gap = abs(nb.timestamp - na.timestamp)
                        if ENTITY in enable:
                            self._add_edge(a, b, ENTITY, 1.0, bidirectional=True)
                        if PRECEDES in enable and 0 < gap <= self.entity_window and na.session_id != nb.session_id:
                            # Earlier event in a different session sharing a referent: the
                            # candidate precondition. Directed, unlike the entity edge.
                            self._add_edge(a, b, PRECEDES, 1.0)

        if self.do_consolidate:
            self._consolidate()
        return self

    def _add_edge(self, source: str, target: str, kind: str, weight: float, bidirectional: bool = False) -> None:
        self.adjacency[source].append(Edge(source, target, kind, weight))
        if bidirectional:
            self.adjacency[target].append(Edge(target, source, kind, weight))

    def link_with_llm(self, generator, candidate_pairs: Sequence[Tuple[str, str]], max_pairs: int = 200) -> int:
        """Upgrade heuristic PRECEDES edges with an LLM precondition judgement.

        Optional. The heuristic version is what c1 runs by default, because an LLM in the
        graph-construction loop makes the ablation harder to interpret and the cost harder
        to report. This exists so the paper can state what the heuristic gives up.
        """
        upgraded = 0
        for src, tgt in list(candidate_pairs)[:max_pairs]:
            a, b = self.nodes.get(src), self.nodes.get(tgt)
            if a is None or b is None:
                continue
            prompt = (
                "Two events from a user's history are given in time order.\n\n"
                f"Earlier: {a.text[:400]}\n\nLater: {b.text[:400]}\n\n"
                "Was the earlier event a precondition for the later one, meaning the later "
                "one would not have happened or would have been different without it? "
                "Answer with one word, yes or no."
            )
            answer = generator.generate("You judge causal preconditions between events.", prompt)
            if answer.strip().lower().startswith("y"):
                self._add_edge(src, tgt, PRECEDES, 1.5)
                upgraded += 1
        return upgraded

    def _consolidate(self, min_support: int = 3) -> None:
        """Fold repeated entity mentions into a semantic store.

        Tulving's distinction, made operational: facts that recur across sessions stop
        being episodes and become background knowledge. Cheap, and it gives the retriever
        a place to look for stable facts without walking the graph.
        """
        self.semantic_store = []
        for ent, node_ids in self.entity_index.items():
            sessions = {self.nodes[n].session_id for n in node_ids}
            if len(sessions) >= min_support:
                latest = max(node_ids, key=lambda n: self.nodes[n].timestamp)
                self.semantic_store.append(
                    {
                        "entity": ent,
                        "support_sessions": len(sessions),
                        "latest_node": latest,
                        "summary": self.nodes[latest].text[:300],
                        "timestamp": self.nodes[latest].timestamp,
                    }
                )
        self.semantic_store.sort(key=lambda r: -r["support_sessions"])

    # -- indexing -----------------------------------------------------------------------

    def index(self, batch_size: int = 256) -> "EpisodicGraph":
        self._order = list(self.nodes)
        texts = [self.nodes[n].text for n in self._order]
        embs = self.encoder.encode(texts, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False)
        embs = np.asarray(embs, dtype=np.float32)
        embs /= np.linalg.norm(embs, axis=1, keepdims=True) + 1e-10
        self._matrix = embs
        for nid, emb in zip(self._order, embs):
            self.nodes[nid].embedding = emb
        return self

    # -- retrieval ----------------------------------------------------------------------

    def _decay(self, node: EventNode, query_time: float) -> float:
        if not self.use_time_decay or query_time <= 0 or node.timestamp <= 0:
            return 1.0
        age = max(0.0, query_time - node.timestamp)
        return float(0.5 ** (age / self.halflife))

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        n_seeds: int = 10,
        hops: int = 1,
        expansion_budget: int = 40,
        query_time: float = 0.0,
        neighbour_discount: float = 0.55,
    ) -> List[Tuple[str, float]]:
        """Seed by similarity, then expand along edges.

        A neighbour's score is the seed's similarity times the edge weight times a
        per-hop discount, so a node topically unlike the query can still surface when it
        sits next to something that is. That is the mechanism the CIKM design argued for
        and never tested.
        """
        if self._matrix is None:
            raise RuntimeError("call index() before retrieve()")

        q = self.encoder.encode([query], convert_to_numpy=True).astype(np.float32)[0]
        q /= np.linalg.norm(q) + 1e-10
        sims = self._matrix @ q

        seed_idx = np.argsort(-sims)[:n_seeds]
        scores: Dict[str, float] = {}
        frontier: List[Tuple[str, float]] = []

        for i in seed_idx:
            nid = self._order[int(i)]
            score = float(sims[int(i)]) * self._decay(self.nodes[nid], query_time)
            scores[nid] = max(scores.get(nid, 0.0), score)
            frontier.append((nid, score))

        visited = set(scores)
        for _ in range(hops):
            next_frontier: List[Tuple[str, float]] = []
            for nid, parent_score in frontier:
                for edge in sorted(self.adjacency.get(nid, []), key=lambda e: -e.weight):
                    if len(visited) >= expansion_budget + n_seeds:
                        break
                    kind_weight = self.edge_weights.get(edge.kind, 0.5) * edge.weight
                    candidate = parent_score * neighbour_discount * kind_weight
                    candidate *= self._decay(self.nodes[edge.target], query_time)
                    if candidate > scores.get(edge.target, 0.0):
                        scores[edge.target] = candidate
                        next_frontier.append((edge.target, candidate))
                    visited.add(edge.target)
            frontier = next_frontier
            if not frontier:
                break

        ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:top_k]
        return ranked

    # -- statistics ---------------------------------------------------------------------

    def stats(self) -> Dict[str, float]:
        by_kind = Counter(e.kind for edges in self.adjacency.values() for e in edges)
        # Count every node, including isolated ones. Averaging over `adjacency` alone
        # would silently drop nodes with no edges and inflate the mean.
        degrees = [len(self.adjacency.get(nid, [])) for nid in self.nodes] or [0]
        return {
            "n_nodes": len(self.nodes),
            "n_edges": sum(by_kind.values()),
            "n_temporal": by_kind[TEMPORAL],
            "n_entity": by_kind[ENTITY],
            "n_precedes": by_kind[PRECEDES],
            "mean_degree": float(np.mean(degrees)),
            "max_degree": int(np.max(degrees)),
            "n_entities": len(self.entity_index),
            "semantic_store_size": len(self.semantic_store),
        }


# --------------------------------------------------------------------------------------
# Baselines
# --------------------------------------------------------------------------------------

class FlatDenseMemory:
    """Similarity over turns or sessions. The standard RAG-over-history baseline."""

    def __init__(self, encoder, granularity: str = "turn"):
        self.encoder, self.granularity = encoder, granularity
        self.ids: List[str] = []
        self.texts: List[str] = []
        self.matrix: Optional[np.ndarray] = None

    def build(self, units: Sequence[Tuple[str, str]], batch_size: int = 256) -> "FlatDenseMemory":
        self.ids = [u[0] for u in units]
        self.texts = [u[1] for u in units]
        embs = np.asarray(
            self.encoder.encode(self.texts, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=False),
            dtype=np.float32,
        )
        self.matrix = embs / (np.linalg.norm(embs, axis=1, keepdims=True) + 1e-10)
        return self

    def retrieve(self, query: str, top_k: int = 10, **_) -> List[Tuple[str, float]]:
        q = self.encoder.encode([query], convert_to_numpy=True).astype(np.float32)[0]
        q /= np.linalg.norm(q) + 1e-10
        sims = self.matrix @ q
        idx = np.argsort(-sims)[:top_k]
        return [(self.ids[int(i)], float(sims[int(i)])) for i in idx]


class BM25Memory:
    def __init__(self):
        self.ids: List[str] = []
        self.index = None

    def build(self, units: Sequence[Tuple[str, str]]) -> "BM25Memory":
        from common.retrieval import BM25Index

        self.ids = [u[0] for u in units]
        self.index = BM25Index().build(self.ids, [u[1] for u in units])
        return self

    def retrieve(self, query: str, top_k: int = 10, **_) -> List[Tuple[str, float]]:
        idx, scores = self.index.search(query, top_k)
        return [(self.ids[int(i)], float(s)) for i, s in zip(idx, scores)]


class SimilarityGraphMemory(FlatDenseMemory):
    """A-MEM-style memory: nodes linked by cosine similarity, retrieved by seed-and-expand.

    The comparison that matters for the design claim. Same seed-and-expand retrieval as
    the episodic graph, same budget, but the edges encode topical similarity instead of
    time and precondition. Any difference between the two is attributable to edge
    semantics rather than to the retrieval procedure.
    """

    def __init__(self, encoder, link_threshold: float = 0.5, max_links: int = 8):
        super().__init__(encoder, granularity="turn")
        self.link_threshold, self.max_links = link_threshold, max_links
        self.adjacency: Dict[str, List[Tuple[str, float]]] = defaultdict(list)

    def build(self, units, batch_size: int = 256) -> "SimilarityGraphMemory":
        super().build(units, batch_size)
        sims = self.matrix @ self.matrix.T
        np.fill_diagonal(sims, -1.0)
        for i, nid in enumerate(self.ids):
            top = np.argsort(-sims[i])[: self.max_links]
            for j in top:
                if sims[i][j] >= self.link_threshold:
                    self.adjacency[nid].append((self.ids[int(j)], float(sims[i][j])))
        return self

    def retrieve(self, query: str, top_k: int = 10, n_seeds: int = 10, expansion_budget: int = 40, **_):
        q = self.encoder.encode([query], convert_to_numpy=True).astype(np.float32)[0]
        q /= np.linalg.norm(q) + 1e-10
        sims = self.matrix @ q
        scores: Dict[str, float] = {}
        for i in np.argsort(-sims)[:n_seeds]:
            nid = self.ids[int(i)]
            scores[nid] = float(sims[int(i)])
        for nid, base in list(scores.items()):
            for neighbour, w in self.adjacency.get(nid, [])[: max(1, expansion_budget // max(1, n_seeds))]:
                scores[neighbour] = max(scores.get(neighbour, 0.0), base * 0.55 * w)
        return sorted(scores.items(), key=lambda kv: -kv[1])[:top_k]


class DecayMemory(FlatDenseMemory):
    """MemoryBank-style forgetting curve applied to similarity scores."""

    def __init__(self, encoder, halflife_days: float = 30.0):
        super().__init__(encoder, granularity="turn")
        self.halflife = halflife_days * 86400
        self.timestamps: Dict[str, float] = {}

    def build(self, units, timestamps: Optional[Dict[str, float]] = None, batch_size: int = 256):
        super().build(units, batch_size)
        self.timestamps = timestamps or {}
        return self

    def retrieve(self, query: str, top_k: int = 10, query_time: float = 0.0, **_):
        q = self.encoder.encode([query], convert_to_numpy=True).astype(np.float32)[0]
        q /= np.linalg.norm(q) + 1e-10
        sims = self.matrix @ q
        scored = []
        for i, nid in enumerate(self.ids):
            ts = self.timestamps.get(nid, 0.0)
            decay = 1.0
            if query_time > 0 and ts > 0:
                decay = float(0.5 ** (max(0.0, query_time - ts) / self.halflife))
            scored.append((nid, float(sims[i]) * decay))
        return sorted(scored, key=lambda kv: -kv[1])[:top_k]
