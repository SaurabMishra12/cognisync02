"""NB1 - Full-corpus BEIR retrieval with compute-matched baselines."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import md, code, write_notebook, ENV_BLOCK, BOOTSTRAP_BLOCK

C = []

C.append(md(r'''
# NB1 — Full-corpus retrieval on BEIR with compute-matched baselines

**What this replaces.** The CIKM version evaluated retrieval by reranking the
handful of passages each dataset ships alongside its query ("custom candidate
pools"). Reviewers correctly noted that this makes MRR@5 = 0.887 uninterpretable
and incomparable to anything published. This notebook throws that protocol away
and does **full-corpus retrieval over the complete BEIR corpora**, scored with
`pytrec_eval` so the numbers sit next to published BEIR results directly.

**What it measures.**

1. `nDCG@10`, `Recall@100`, `MRR@10` for every first-stage retriever over the
   whole corpus — no candidate pools anywhere.
2. A **compute-matched grid**: every first stage is evaluated with the *same*
   cross-encoder budget (none / top-50 / top-100). The CIKM submission compared
   CogniSync-with-a-reranker against baselines-without-one; that comparison is
   removed and replaced with this grid, so the reader can read off exactly what
   the fusion contributes at a fixed reranking budget.
3. **Retriever generality**: the same grid across 4 encoders (MiniLM, BGE-small,
   GTE-small, E5-small), so no conclusion rests on one backbone.
4. **Zero-shot transfer of the learned fusion weight**: α is fit once on MS MARCO
   and applied unchanged to every BEIR dataset.

**Artifacts written** (all under `ART/results/`):
`nb1_per_query.parquet`, `nb1_summary.csv`, `nb1_pairwise.csv`, `nb1_config.json`.

---

### Runtime and hardware

| Tier | Corpora | Docs | Free Colab T4 | Kaggle 2×T4 |
|---|---|---|---|---|
| `smoke` | nfcorpus, scifact | 9K | ~6 min | ~5 min |
| `standard` *(default)* | + arguana, scidocs, fiqa, trec-covid | 272K | **~55 min** (1 encoder) / ~3.2 h (4 encoders) | ~40 min / ~2.3 h |
| `extended` | + quora, touche2020 | 1.18M | ~2.5 h (1 encoder) | ~1.8 h |
| `msmarco` | MS MARCO dev-small, full 8.84M corpus | 8.84M | ✗ RAM | **~2.5 h**, Kaggle only |

Peak VRAM stays under **6 GB** in every tier (the corpus matrix is held in fp16
and the cross-encoder runs at batch 256), so a free T4 is never the binding
constraint — **host RAM is**. `standard` peaks around 5 GB RAM, `extended`
around 9 GB, and `msmarco` around 22 GB, which is why the last one needs Kaggle.

Embeddings are cached to `ART/cache/`, so re-running a tier after a disconnect
skips encoding entirely.
'''))

C.append(code(r'''
# One-time install. On Kaggle add `--no-index` problems are avoided by plain pip.
!pip install -q "sentence-transformers>=3.0" "bm25s[full]" PyStemmer pytrec_eval-terrier datasets pyarrow 2>&1 | tail -2
'''))

C.append(code(ENV_BLOCK + r'''

# --------------------------------------------------------------------------
# CONFIG - edit this cell only.
# --------------------------------------------------------------------------
TIER = "standard"       # smoke | standard | extended | msmarco
ENCODERS = ["minilm"]   # add "bge", "gte", "e5" for the generality grid
RERANK_BUDGETS = [0, 50, 100]   # 0 = no cross-encoder
FIRST_STAGE_DEPTH = 1000        # candidates carried out of stage 1
CACHE_EMBEDDINGS = True

DATASET_TIERS = {
    "smoke":    ["nfcorpus", "scifact"],
    "standard": ["nfcorpus", "scifact", "arguana", "scidocs", "fiqa", "trec-covid"],
    "extended": ["nfcorpus", "scifact", "arguana", "scidocs", "fiqa", "trec-covid",
                 "quora", "webis-touche2020"],
    "msmarco":  ["msmarco"],
}
DATASETS = DATASET_TIERS[TIER]

ENCODER_IDS = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "bge":    "BAAI/bge-small-en-v1.5",
    "gte":    "thenlper/gte-small",
    "e5":     "intfloat/e5-small-v2",
}
# Some encoders require an instruction prefix; getting this wrong silently costs
# several nDCG points, so it is spelled out rather than left implicit.
ENCODER_PREFIX = {
    "minilm": ("", ""),
    "bge":    ("Represent this sentence for searching relevant passages: ", ""),
    "gte":    ("", ""),
    "e5":     ("query: ", "passage: "),
}
CE_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

CONFIG = dict(tier=TIER, encoders=ENCODERS, rerank_budgets=RERANK_BUDGETS,
              first_stage_depth=FIRST_STAGE_DEPTH, datasets=DATASETS,
              ce_model=CE_MODEL, seed=SEED)
print(json.dumps(CONFIG, indent=2))
'''))

C.append(md(r'''
## 1. Data

BEIR is loaded straight from the Hugging Face mirrors (`BeIR/<name>` for corpus
and queries, `BeIR/<name>-qrels` for judgements), so no zip downloads and no
`beir` package pin. Everything is keyed by the dataset's own string ids — we
never renumber documents, which is what made the original candidate-pool code
hard to audit.
'''))

C.append(code(r'''
from datasets import load_dataset

# BEIR qrels live in different splits per dataset. Anything not listed uses
# "test"; the second entry is the split we are allowed to fit hyper-parameters
# on (None = no in-domain fitting is possible, so only zero-shot alpha applies).
BEIR_SPLITS = {
    "nfcorpus":          ("test", "dev"),
    "scifact":           ("test", "train"),
    "arguana":           ("test", None),
    "scidocs":           ("test", None),
    "fiqa":              ("test", "dev"),
    "trec-covid":        ("test", None),
    "quora":             ("test", "dev"),
    "webis-touche2020":  ("test", None),
}
# Query subsampling keeps the cross-encoder grid tractable. Sampling is seeded
# and reported; it is applied to the query side only, never to the corpus.
MAX_QUERIES = {"quora": 2000, "arguana": 1406, "scidocs": 1000}


def load_beir(name):
    """Return (corpus_ids, corpus_texts, query_ids, query_texts, qrels)."""
    cache = ART / "cache" / f"beir_{name}.parquet"
    qcache = ART / "cache" / f"beirq_{name}.json"
    if cache.exists() and qcache.exists():
        cdf = pd.read_parquet(cache)
        blob = json.load(open(qcache))
        return (cdf["_id"].tolist(), cdf["text"].tolist(),
                blob["qids"], blob["qtexts"], blob["qrels"])

    corpus = load_dataset(f"BeIR/{name}", "corpus", split="corpus")
    queries = load_dataset(f"BeIR/{name}", "queries", split="queries")
    test_split, _ = BEIR_SPLITS[name]
    qrels_ds = load_dataset(f"BeIR/{name}-qrels", split=test_split)

    qrels = {}
    for r in qrels_ds:
        if int(r["score"]) <= 0:
            continue
        qrels.setdefault(str(r["query-id"]), {})[str(r["corpus-id"])] = int(r["score"])

    qid2text = {str(q["_id"]): q["text"] for q in queries}
    qids = [q for q in qrels if q in qid2text]
    qids.sort()
    if name in MAX_QUERIES and len(qids) > MAX_QUERIES[name]:
        rng = np.random.default_rng(SEED)
        qids = sorted(rng.choice(qids, size=MAX_QUERIES[name], replace=False).tolist())
        qrels = {q: qrels[q] for q in qids}
    qtexts = [qid2text[q] for q in qids]

    cids, ctexts = [], []
    for d in corpus:
        title = (d.get("title") or "").strip()
        body = (d.get("text") or "").strip()
        cids.append(str(d["_id"]))
        ctexts.append((title + " " + body).strip() if title else body)

    if CACHE_EMBEDDINGS:
        pd.DataFrame({"_id": cids, "text": ctexts}).to_parquet(cache)
        json.dump({"qids": qids, "qtexts": qtexts, "qrels": qrels}, open(qcache, "w"))
    return cids, ctexts, qids, qtexts, qrels


def load_msmarco_full():
    """MS MARCO passage v2 corpus (8.84M) + dev-small queries. Kaggle-only tier."""
    corpus = load_dataset("BeIR/msmarco", "corpus", split="corpus")
    queries = load_dataset("BeIR/msmarco", "queries", split="queries")
    qrels_ds = load_dataset("BeIR/msmarco-qrels", split="validation")
    qrels = {}
    for r in qrels_ds:
        if int(r["score"]) > 0:
            qrels.setdefault(str(r["query-id"]), {})[str(r["corpus-id"])] = int(r["score"])
    qid2text = {str(q["_id"]): q["text"] for q in queries}
    qids = sorted([q for q in qrels if q in qid2text])
    qtexts = [qid2text[q] for q in qids]
    cids = [str(x) for x in corpus["_id"]]
    ctexts = corpus["text"]
    return cids, ctexts, qids, qtexts, qrels
'''))

C.append(md(r'''
## 2. First-stage retrievers

Dense retrieval is a plain normalised inner product done as a chunked `matmul`
on the GPU, with the corpus matrix held in fp16. This is exact (no ANN
approximation), so nothing in the results depends on FAISS index parameters —
one fewer confound than the original code, which mixed `IndexFlatIP` with an
occasional GPU clone.

Lexical retrieval uses `bm25s` rather than `rank_bm25`. `rank_bm25` scores every
document in pure Python on every query; at 500K documents × 2,000 queries that
is hours. `bm25s` is a sparse scipy implementation and does the same work in
seconds, with the same Lucene-style BM25 (k1=0.9, b=0.4 — BEIR's setting).
'''))

C.append(code(r'''
from sentence_transformers import SentenceTransformer, CrossEncoder
import bm25s, Stemmer


class DenseIndex:
    """Exact normalised-inner-product index held in fp16 on the GPU."""

    def __init__(self, encoder_key, batch_size=256):
        self.key = encoder_key
        self.model = SentenceTransformer(ENCODER_IDS[encoder_key], device=DEVICE)
        self.model.max_seq_length = 256
        self.qpre, self.dpre = ENCODER_PREFIX[encoder_key]
        self.bs = batch_size
        self.mat = None

    def _encode(self, texts, prefix, desc):
        if prefix:
            texts = [prefix + t for t in texts]
        emb = self.model.encode(texts, batch_size=self.bs, convert_to_numpy=True,
                                normalize_embeddings=True, show_progress_bar=True)
        return emb.astype(np.float16)

    def build(self, ds_name, texts):
        cpath = ART / "cache" / f"emb_{ds_name}_{self.key}.npy"
        if CACHE_EMBEDDINGS and cpath.exists():
            emb = np.load(cpath)
            print(f"  loaded cached embeddings {emb.shape}")
        else:
            t0 = time.time()
            emb = self._encode(texts, self.dpre, "corpus")
            print(f"  encoded {len(texts):,} docs in {time.time()-t0:.0f}s")
            if CACHE_EMBEDDINGS:
                np.save(cpath, emb)
        self.mat = torch.from_numpy(emb).to(DEVICE)
        return self

    def search(self, qtexts, k):
        qemb = self._encode(qtexts, self.qpre, "queries")
        q = torch.from_numpy(qemb).to(DEVICE)
        n = self.mat.shape[0]
        # Chunk over the corpus so peak activation memory stays bounded even at
        # 8.8M documents.
        chunk = max(1, int(2.0e8 // max(1, q.shape[0])))
        best_s, best_i = None, None
        for start in range(0, n, chunk):
            block = self.mat[start:start + chunk]
            s = q @ block.T                                  # [Q, chunk]
            kk = min(k, s.shape[1])
            sc, ix = torch.topk(s.float(), kk, dim=1)
            ix = ix + start
            if best_s is None:
                best_s, best_i = sc, ix
            else:
                best_s = torch.cat([best_s, sc], dim=1)
                best_i = torch.cat([best_i, ix], dim=1)
                kk = min(k, best_s.shape[1])
                sc, sel = torch.topk(best_s, kk, dim=1)
                best_s, best_i = sc, torch.gather(best_i, 1, sel)
            del s
        return best_s.cpu().numpy(), best_i.cpu().numpy()

    def free(self):
        self.mat = None
        gc.collect(); torch.cuda.empty_cache()


class BM25Index:
    """Lucene-parameterised BM25 (k1=0.9, b=0.4), the BEIR convention."""

    def __init__(self):
        self.stemmer = Stemmer.Stemmer("english")
        self.r = None

    def build(self, texts):
        t0 = time.time()
        tok = bm25s.tokenize(texts, stopwords="en", stemmer=self.stemmer, show_progress=False)
        self.r = bm25s.BM25(k1=0.9, b=0.4)
        self.r.index(tok, show_progress=False)
        print(f"  BM25 indexed {len(texts):,} docs in {time.time()-t0:.0f}s")
        return self

    def search(self, qtexts, k):
        tok = bm25s.tokenize(qtexts, stopwords="en", stemmer=self.stemmer, show_progress=False)
        idx, sc = self.r.retrieve(tok, k=k, show_progress=False)
        return sc.astype(np.float32), idx.astype(np.int64)
'''))

C.append(md(r'''
## 3. Fusion

Every fusion variant here operates on the union of the two top-`FIRST_STAGE_DEPTH`
lists. Scores are min-max normalised **within the retrieved list**, and a document
retrieved by only one channel gets 0 from the other. This is the same convention
the CIKM code used, but it was never written down — it is one of the
reproducibility gaps the reviewers listed, so it is stated explicitly here and
implemented in one place.

Four fusion policies are compared:

- `rrf` — reciprocal rank fusion, k=60 (the fixed-weight baseline).
- `alpha_fixed` — a single global α, chosen on the MS MARCO fitting set. This is
  the baseline the CIKM paper was missing: a *tuned* fixed weight, not just RRF.
- `alpha_learned` — the CogniSync mechanism: a random forest predicts α per query
  from six query and score-distribution features.
- `alpha_oracle` — the per-query α that maximises nDCG@10 in hindsight. Not a
  system; an **upper bound on any per-query fusion policy whatsoever**, which is
  what makes the learned-α result interpretable.

One detail worth flagging: the CIKM implementation contained a hard override,
`if max_dense_score > 0.85 or bm25_cv < 0.1: alpha = 1.0`, which discards the
regressor's prediction and falls back to pure dense retrieval. That override is
kept here as an explicit, separately-ablatable variant (`alpha_learned_override`)
rather than buried inside the predictor, because a large part of what the paper
attributed to "learned α" was in fact this rule.
'''))

C.append(code(r'''
from sklearn.ensemble import RandomForestRegressor

RRF_K = 60


def minmax(x):
    x = np.asarray(x, dtype=np.float64)
    lo, hi = float(x.min()), float(x.max())
    if hi - lo < 1e-12:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


def build_candidate_scores(d_idx, d_sc, b_idx, b_sc):
    """Union the two channels and return aligned normalised score vectors."""
    nd, nb = minmax(d_sc), minmax(b_sc)
    dmap = {int(i): float(s) for i, s in zip(d_idx, nd)}
    bmap = {int(i): float(s) for i, s in zip(b_idx, nb)}
    cands = np.array(sorted(set(dmap) | set(bmap)), dtype=np.int64)
    dv = np.array([dmap.get(int(c), 0.0) for c in cands])
    bv = np.array([bmap.get(int(c), 0.0) for c in cands])
    dr = {int(i): r for r, i in enumerate(d_idx)}
    br = {int(i): r for r, i in enumerate(b_idx)}
    BIG = len(cands) + RRF_K
    drank = np.array([dr.get(int(c), BIG) for c in cands])
    brank = np.array([br.get(int(c), BIG) for c in cands])
    return cands, dv, bv, drank, brank


def alpha_features(query, dv, bv, d_sc_raw):
    """The six features from the CIKM paper, defined unambiguously.

    Feature 6 fires on identifier-shaped queries: an explicit id/uuid/hash/key
    token, a hex literal, a dotted version string, or a long alphanumeric run.
    """
    dstd, bstd = float(dv.std()), float(bv.std())
    dmean, bmean = float(dv.mean()), float(bv.mean())
    dcv = dstd / dmean if dmean > 1e-9 else 0.0
    bcv = bstd / bmean if bmean > 1e-9 else 0.0
    has_id = float(bool(
        re.search(r"\b(id|uuid|hash|key|sha\d*|md5)\b", query, re.I) or
        re.search(r"0x[0-9a-fA-F]{4,}", query) or
        re.search(r"\bv?\d+\.\d+(\.\d+)?\b", query) or
        re.search(r"\b[0-9a-fA-F]{16,}\b", query)))
    return [float(len(query.split())), dstd, bstd, dcv, bcv, has_id]


def fuse(dv, bv, drank, brank, mode, alpha=None):
    if mode == "dense":
        return dv
    if mode == "bm25":
        return bv
    if mode == "rrf":
        return 1.0 / (RRF_K + drank + 1) + 1.0 / (RRF_K + brank + 1)
    return alpha * dv + (1.0 - alpha) * bv


def apply_dense_override(alpha, d_sc_raw, bcv):
    """The CIKM fallback rule, isolated so its contribution can be measured."""
    if float(np.max(d_sc_raw)) > 0.85 or bcv < 0.1:
        return 1.0
    return alpha
'''))

C.append(md(r'''
## 4. Reranking under a fixed budget

The cross-encoder reranks the top-`B` of whatever the first stage produced, for
`B` in `RERANK_BUDGETS`. Every system gets the same `B`, and pairs are scored
once per (query, document) and cached across systems within a dataset, so the
grid costs roughly one rerank pass rather than `len(systems) × len(budgets)`.
'''))

C.append(code(r'''
class RerankCache:
    """Scores (query, doc) pairs once per dataset and reuses them everywhere."""

    def __init__(self, model_name=CE_MODEL, batch_size=256):
        self.ce = CrossEncoder(model_name, max_length=320, device=DEVICE)
        self.bs = batch_size
        self.store = {}
        self.n_scored = 0

    def reset(self):
        self.store = {}; self.n_scored = 0

    def score(self, qi, qtext, doc_idx, doc_texts):
        need = [int(d) for d in doc_idx if (qi, int(d)) not in self.store]
        if need:
            pairs = [[qtext, doc_texts[d]] for d in need]
            out = self.ce.predict(pairs, batch_size=self.bs, show_progress_bar=False)
            for d, s in zip(need, out):
                self.store[(qi, d)] = float(s)
            self.n_scored += len(need)
        return np.array([self.store[(qi, int(d))] for d in doc_idx], dtype=np.float64)


def rerank(order, ce_scores, budget):
    """Reorder the head of `order` by cross-encoder score, keep the tail."""
    if budget <= 0 or len(order) <= 1:
        return order
    b = min(budget, len(order))
    head = order[:b]
    new_head = head[np.argsort(-ce_scores[:b], kind="stable")]
    return np.concatenate([new_head, order[b:]])
'''))

C.append(md(r'''
## 5. Metrics

`pytrec_eval` is the reference implementation TREC and BEIR use, so nDCG@10 here
is byte-for-byte the number other BEIR papers report. A pure-Python fallback
replicating `trec_eval`'s `ndcg_cut` (linear gain, `log2(rank+1)` discount) is
included for environments where the wheel will not build.
'''))

C.append(code(r'''
try:
    import pytrec_eval
    HAVE_PTE = True
except Exception:
    HAVE_PTE = False
print("pytrec_eval available:", HAVE_PTE)

METRICS = {"ndcg_cut.10", "recall.100", "recip_rank"}


def _py_eval(qrels, run, k_ndcg=10, k_recall=100):
    out = {}
    for qid, rel in qrels.items():
        ranked = sorted(run.get(qid, {}).items(), key=lambda kv: -kv[1])
        docs = [d for d, _ in ranked]
        gains = [rel.get(d, 0) for d in docs[:k_ndcg]]
        dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains))
        ideal = sorted(rel.values(), reverse=True)[:k_ndcg]
        idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
        rr = 0.0
        for i, d in enumerate(docs):
            if rel.get(d, 0) > 0:
                rr = 1.0 / (i + 1); break
        hit = sum(1 for d in docs[:k_recall] if rel.get(d, 0) > 0)
        out[qid] = {
            "ndcg_cut_10": dcg / idcg if idcg > 0 else 0.0,
            "recall_100": hit / max(1, len(rel)),
            "recip_rank": rr,
        }
    return out


def evaluate(qrels, run):
    """run: {qid: {docid: score}} -> {qid: {metric: value}}"""
    if HAVE_PTE:
        ev = pytrec_eval.RelevanceEvaluator(qrels, METRICS)
        return ev.evaluate(run)
    return _py_eval(qrels, run)
''' + BOOTSTRAP_BLOCK))

C.append(md(r'''
## 6. Main evaluation loop

For each dataset and encoder we run the two first stages once, build every
fusion order, then apply every rerank budget. Per-query metrics are kept so the
paired bootstrap in section 7 has something to work with — aggregate-only
reporting was another thing reviewers could not audit.
'''))

C.append(code(r'''
FUSION_SYSTEMS = ["dense", "bm25", "rrf", "alpha_fixed", "alpha_learned",
                  "alpha_learned_override", "alpha_oracle"]

ALPHA_GRID = np.round(np.linspace(0.0, 1.0, 21), 2)


def ndcg_at_k_single(order_ids, rel, k=10):
    gains = [rel.get(d, 0) for d in order_ids[:k]]
    dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains))
    ideal = sorted(rel.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0


def run_dataset(ds_name, enc_key, alpha_model, alpha_fixed_value, ce_cache):
    print(f"\n=== {ds_name} | {enc_key} ===")
    if ds_name == "msmarco":
        cids, ctexts, qids, qtexts, qrels = load_msmarco_full()
    else:
        cids, ctexts, qids, qtexts, qrels = load_beir(ds_name)
    print(f"  corpus={len(cids):,} queries={len(qids):,}")
    CORPUS_STATS.append({"dataset": ds_name, "n_docs": len(cids), "n_queries": len(qids)})

    dense = DenseIndex(enc_key).build(ds_name, ctexts)
    d_sc, d_ix = dense.search(qtexts, FIRST_STAGE_DEPTH)
    dense.free()
    bm = BM25Index().build(ctexts)
    b_sc, b_ix = bm.search(qtexts, FIRST_STAGE_DEPTH)

    ce_cache.reset()
    rows = []
    max_budget = max(RERANK_BUDGETS)

    for qi, qid in enumerate(tqdm(qids, desc="  scoring")):
        rel = qrels[qid]
        cands, dv, bv, drank, brank = build_candidate_scores(
            d_ix[qi], d_sc[qi], b_ix[qi], b_sc[qi])
        feats = alpha_features(qtexts[qi], dv, bv, d_sc[qi])
        a_learn = float(np.clip(alpha_model.predict([feats])[0], 0.0, 1.0))
        a_over = apply_dense_override(a_learn, d_sc[qi], feats[4])

        orders = {}
        oracle_alpha = float('nan')
        for sysname in FUSION_SYSTEMS:
            if sysname == "alpha_oracle":
                best, best_n, best_a = None, -1.0, None
                for a in ALPHA_GRID:
                    o = cands[np.argsort(-fuse(dv, bv, drank, brank, "alpha", a), kind="stable")]
                    n = ndcg_at_k_single([cids[i] for i in o[:10]], rel, 10)
                    if n > best_n:
                        best, best_n, best_a = o, n, float(a)
                orders[sysname] = best
                oracle_alpha = best_a
            else:
                a = {"alpha_fixed": alpha_fixed_value,
                     "alpha_learned": a_learn,
                     "alpha_learned_override": a_over}.get(sysname)
                mode = sysname if sysname in ("dense", "bm25", "rrf") else "alpha"
                sc = fuse(dv, bv, drank, brank, mode, a)
                orders[sysname] = cands[np.argsort(-sc, kind="stable")]

        # One cross-encoder pass over the union of every system's head.
        union_head = sorted({int(d) for o in orders.values() for d in o[:max_budget]})
        ce_all = ce_cache.score(qi, qtexts[qi], union_head, ctexts)
        ce_lookup = {d: s for d, s in zip(union_head, ce_all)}

        for sysname, order in orders.items():
            for budget in RERANK_BUDGETS:
                if budget == 0:
                    final = order
                else:
                    head = order[:budget]
                    cs = np.array([ce_lookup[int(d)] for d in head])
                    final = rerank(order, cs, budget)
                top = [cids[i] for i in final[:100]]
                rows.append({
                    "dataset": ds_name, "encoder": enc_key, "system": sysname,
                    "budget": budget, "qid": qid,
                    "ndcg10": ndcg_at_k_single(top, rel, 10),
                    "recall100": sum(1 for d in top if rel.get(d, 0) > 0) / max(1, len(rel)),
                    "mrr10": next((1.0 / (i + 1) for i, d in enumerate(top[:10])
                                   if rel.get(d, 0) > 0), 0.0),
                    "alpha_learned": a_learn, "alpha_override": a_over,
                    "alpha_oracle": oracle_alpha,
                })

    print(f"  cross-encoder pairs scored: {ce_cache.n_scored:,}")
    del d_sc, d_ix, b_sc, b_ix, bm
    gc.collect(); torch.cuda.empty_cache()
    return pd.DataFrame(rows)
'''))

C.append(md(r'''
### Fitting α once, on MS MARCO

α is fit on 3,000 MS MARCO training queries against a 200K-passage corpus and
then applied **unchanged** to every BEIR dataset. This is a deliberate protocol
choice: the CIKM version fit α on 300 held-out queries whose provenance the
reviewers could not determine, and applied it in-domain. Fitting once and
transferring zero-shot is both harder and easier to audit.

The oracle target is the α that maximises nDCG@10 for that query. We also record
how *flat* each query's α→nDCG curve is, which NB2 uses to explain the result.
'''))

C.append(code(r'''
N_ALPHA_FIT_QUERIES = 3000
ALPHA_FIT_CORPUS = 200_000


def fit_alpha_model(enc_key):
    cpath = ART / "cache" / f"alphafit_{enc_key}.json"
    mpath = ART / "cache" / f"alphamodel_{enc_key}.joblib"
    import joblib
    if mpath.exists() and cpath.exists():
        blob = json.load(open(cpath))
        print(f"  reusing fitted alpha model (fixed={blob['alpha_fixed']:.2f})")
        return joblib.load(mpath), blob["alpha_fixed"], pd.DataFrame(blob["rows"])

    print("Fitting alpha on MS MARCO train (once, then frozen)...")
    corpus = load_dataset("BeIR/msmarco", "corpus", split="corpus",
                          streaming=True)
    ctexts, cids = [], []
    for d in corpus:
        t = ((d.get("title") or "") + " " + (d.get("text") or "")).strip()
        if t:
            cids.append(str(d["_id"])); ctexts.append(t)
        if len(ctexts) >= ALPHA_FIT_CORPUS:
            break

    qrels_ds = load_dataset("BeIR/msmarco-qrels", split="train", streaming=True)
    queries = load_dataset("BeIR/msmarco", "queries", split="queries")
    qid2text = {str(q["_id"]): q["text"] for q in queries}
    cid_pos = {c: i for i, c in enumerate(cids)}

    fit_q, fit_rel = [], []
    for r in qrels_ds:
        qid, did = str(r["query-id"]), str(r["corpus-id"])
        if int(r["score"]) > 0 and qid in qid2text and did in cid_pos:
            fit_q.append(qid2text[qid]); fit_rel.append({did: 1})
        if len(fit_q) >= N_ALPHA_FIT_QUERIES:
            break
    print(f"  fitting on {len(fit_q)} queries / {len(ctexts):,} passages")

    dense = DenseIndex(enc_key).build("msmarco_alphafit", ctexts)
    d_sc, d_ix = dense.search(fit_q, FIRST_STAGE_DEPTH)
    dense.free()
    bm = BM25Index().build(ctexts)
    b_sc, b_ix = bm.search(fit_q, FIRST_STAGE_DEPTH)

    X, y, rows = [], [], []
    per_alpha = np.zeros(len(ALPHA_GRID))
    for i in tqdm(range(len(fit_q)), desc="  oracle alpha"):
        cands, dv, bv, drank, brank = build_candidate_scores(
            d_ix[i], d_sc[i], b_ix[i], b_sc[i])
        rel = fit_rel[i]
        curve = []
        for j, a in enumerate(ALPHA_GRID):
            o = cands[np.argsort(-fuse(dv, bv, drank, brank, "alpha", a), kind="stable")]
            n = ndcg_at_k_single([cids[k] for k in o[:10]], rel, 10)
            curve.append(n)
        curve = np.array(curve)
        per_alpha += curve
        X.append(alpha_features(fit_q[i], dv, bv, d_sc[i]))
        y.append(float(ALPHA_GRID[int(np.argmax(curve))]))
        rows.append({"query": fit_q[i], "oracle_alpha": y[-1],
                     "best_ndcg": float(curve.max()),
                     "ndcg_at_alpha1": float(curve[-1]),
                     "curve_range": float(curve.max() - curve.min()),
                     "n_argmax_ties": int((curve == curve.max()).sum()),
                     "features": X[-1]})

    alpha_fixed = float(ALPHA_GRID[int(np.argmax(per_alpha))])
    model = RandomForestRegressor(n_estimators=200, max_depth=8,
                                  min_samples_leaf=5, random_state=SEED, n_jobs=-1)
    model.fit(X, y)
    print(f"  best global alpha = {alpha_fixed:.2f}")
    print(f"  oracle alpha distribution: mean={np.mean(y):.3f} std={np.std(y):.3f}")

    joblib.dump(model, mpath)
    json.dump({"alpha_fixed": alpha_fixed, "rows": rows}, open(cpath, "w"), default=float)
    del d_sc, d_ix, b_sc, b_ix, bm, ctexts
    gc.collect(); torch.cuda.empty_cache()
    return model, alpha_fixed, pd.DataFrame(rows)
'''))

C.append(code(r'''
all_rows = []
CORPUS_STATS = []
ce_cache = RerankCache()

for enc_key in ENCODERS:
    alpha_model, alpha_fixed_value, alpha_fit_df = fit_alpha_model(enc_key)
    save_csv(alpha_fit_df.drop(columns=["features"]), f"nb1_alphafit_{enc_key}.csv")
    for ds in DATASETS:
        try:
            all_rows.append(run_dataset(ds, enc_key, alpha_model, alpha_fixed_value, ce_cache))
        except Exception as e:
            print(f"!! {ds}/{enc_key} failed: {type(e).__name__}: {e}")

per_query = pd.concat(all_rows, ignore_index=True)
per_query.to_parquet(ART / "results" / "nb1_per_query.parquet")
print("\nper-query rows:", len(per_query))
CONFIG["alpha_fixed"] = alpha_fixed_value
save_json(CONFIG, "nb1_config.json")
save_csv(pd.DataFrame(CORPUS_STATS).drop_duplicates("dataset"), "nb1_corpus_stats.csv")
'''))

C.append(md(r'''
## 7. Results

Three tables come out of this:

- **`nb1_summary.csv`** — nDCG@10 per dataset × system × rerank budget.
- **`nb1_pairwise.csv`** — every system against `dense` at the *same* rerank
  budget, with paired-bootstrap mean differences and 95% CIs.
- The headline grid printed below, which is what replaces Table 1 of the CIKM
  version.
'''))

C.append(code(r'''
summary = (per_query.groupby(["encoder", "dataset", "system", "budget"])
           [["ndcg10", "recall100", "mrr10"]].mean().reset_index())
save_csv(summary, "nb1_summary.csv")

# BEIR convention: the headline number is the unweighted mean of per-dataset
# nDCG@10, so a 171K-document corpus does not drown out a 3.6K one.
grid = (summary.groupby(["encoder", "system", "budget"])["ndcg10"].mean()
        .unstack("budget").round(4))
print("\nMean nDCG@10 across datasets (rows = system, cols = rerank budget)\n")
print(grid.to_string())

pairs = []
for (enc, ds, budget), g in per_query.groupby(["encoder", "dataset", "budget"]):
    piv = g.pivot_table(index="qid", columns="system", values="ndcg10")
    if "dense" not in piv:
        continue
    for sysname in piv.columns:
        if sysname == "dense":
            continue
        sub = piv[[sysname, "dense"]].dropna()
        if len(sub) < 10:
            continue
        st = paired_bootstrap(sub[sysname].values, sub["dense"].values)
        st.update(encoder=enc, dataset=ds, budget=budget, system=sysname)
        pairs.append(st)
pairwise = pd.DataFrame(pairs)
save_csv(pairwise, "nb1_pairwise.csv")

print("\nPooled vs Dense at matched rerank budget (mean nDCG@10 delta, 95% CI)\n")
pool = (pairwise.groupby(["encoder", "system", "budget"])
        [["mean_diff", "ci_low", "ci_high"]].mean().round(4))
print(pool.to_string())
'''))

C.append(code(r'''
# LaTeX for the paper's main retrieval table.
def latex_main_table(enc="minilm"):
    s = summary[summary.encoder == enc]
    order = ["bm25", "dense", "rrf", "alpha_fixed", "alpha_learned",
             "alpha_learned_override", "alpha_oracle"]
    pretty = {"bm25": "BM25", "dense": "Dense", "rrf": "RRF ($k$=60)",
              "alpha_fixed": "Fixed $\\alpha^\\star$", "alpha_learned": "Learned $\\alpha$",
              "alpha_learned_override": "Learned $\\alpha$ + dense override",
              "alpha_oracle": "\\emph{Oracle} $\\alpha$ (upper bound)"}
    ds_list = sorted(s.dataset.unique())
    lines = [r"\begin{tabular}{l" + "c" * (len(ds_list) + 1) + "}", r"\toprule",
             "First stage & " + " & ".join(d.replace("webis-", "") for d in ds_list) + r" & Mean \\"]
    for budget in RERANK_BUDGETS:
        lines.append(r"\midrule")
        tag = "no reranking" if budget == 0 else f"cross-encoder top-{budget}"
        lines.append(r"\multicolumn{%d}{l}{\emph{%s}} \\" % (len(ds_list) + 2, tag))
        for sysname in order:
            r = s[(s.system == sysname) & (s.budget == budget)]
            if r.empty:
                continue
            vals = [r[r.dataset == d]["ndcg10"] for d in ds_list]
            cells = [f"{float(v.iloc[0]):.3f}" if len(v) else "--" for v in vals]
            mean = r["ndcg10"].mean()
            lines.append(f"{pretty[sysname]} & " + " & ".join(cells) + f" & {mean:.3f} " + r"\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines)

tex = latex_main_table(ENCODERS[0])
(ART / "results" / "nb1_main_table.tex").write_text(tex)
print(tex)
'''))

C.append(md(r'''
## 8. How to read this

The result to look for is whether any row beats `Dense` **at the same rerank
budget**. In the CIKM submission the +2.80 pp headline came from comparing a
reranked system against unreranked baselines; once the budget is matched, that
gap is expected to largely close. If it does, that is the paper's finding, and
it should be stated as such rather than worked around.

The `alpha_oracle` row is the load-bearing one. It says how much *any*
per-query fusion policy could win if it predicted α perfectly. If oracle-α is
well above dense while learned-α sits on top of dense, the honest conclusion is
that the headroom exists but the six features do not capture it — and NB2
characterises why. If oracle-α is *also* close to dense, then per-query fusion
weighting has nothing to offer on these corpora, which is a cleaner and more
useful negative result.
'''))

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "notebooks", "NB1_full_corpus_beir.ipynb")
write_notebook(OUT_PATH, C, "full-corpus BEIR + compute-matched grid")
