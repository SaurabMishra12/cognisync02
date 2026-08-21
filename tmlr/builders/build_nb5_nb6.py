"""NB5 - honest cost accounting; NB6 - assemble every table and figure."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import md, code, write_notebook, ENV_BLOCK, BOOTSTRAP_BLOCK

# ===========================================================================
# NB5
# ===========================================================================
C = []

C.append(md(r'''
# NB5 — Cost accounting: what each component actually costs

The CIKM version reported 275.6 ms average latency on a "persistent 100K-passage
index" and claimed the retrieval and filtering stack is practical. Two problems
with that number as evidence:

1. **The measured corpus was synthetic.** The latency script generates documents
   by sampling from a 12-word vocabulary. BM25 over a 12-word vocabulary has
   nothing like the posting-list structure of a real corpus, and the encoder sees
   trivially short, repetitive inputs.
2. **The claim it supports is about the whole pipeline**, but the numbers were
   collected under a configuration that differs from the one used for the quality
   results (a different candidate count, a different reranking depth). Two of the
   repository's own artifacts disagree with the paper by an order of magnitude
   (`latency_results.txt` records a 3,325 ms median).

This notebook measures cost on **real corpora, in the exact configuration the
quality results were produced under**, and reports it as a cost/quality curve
rather than a single number. Both halves of the tradeoff come from the same runs.

Reported per configuration:

- wall-clock p50/p95/p99 per query, split by stage (encode / dense / BM25 / fuse /
  rerank / filter);
- index build time and resident memory;
- **cross-encoder forward passes per query**, which is the hardware-independent
  cost measure and the one that actually transfers to another machine;
- the quality obtained at that cost, so the table is a frontier and not a boast.

**Runtime** ~20 min on a free T4. Peak VRAM ~3 GB.
'''))

C.append(code(r'''
!pip install -q "sentence-transformers>=3.0" "bm25s[full]" PyStemmer datasets pyarrow psutil 2>&1 | tail -1
'''))

C.append(code(ENV_BLOCK + r'''
import psutil

BENCH_DATASETS = ["scifact", "fiqa"]     # real corpora, 5K and 58K
N_BENCH_QUERIES = 200
DEPTHS = [100, 1000]                     # first-stage depth
RERANK_BUDGETS = [0, 10, 50, 100]
WARMUP = 10

CONFIG = dict(datasets=BENCH_DATASETS, n_queries=N_BENCH_QUERIES,
              depths=DEPTHS, rerank_budgets=RERANK_BUDGETS, seed=SEED,
              device=DEVICE, gpu=(torch.cuda.get_device_name(0) if DEVICE == "cuda" else "cpu"))
print(json.dumps(CONFIG, indent=2))


def rss_gb():
    return psutil.Process().memory_info().rss / 1e9
''' + BOOTSTRAP_BLOCK))

C.append(code(r'''
from datasets import load_dataset
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.linear_model import LogisticRegression
import bm25s, Stemmer

ENC_ID = "sentence-transformers/all-MiniLM-L6-v2"
CE_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"
IMPERATIVE_RE = re.compile(r"(?i)\b(ignore|reveal|execute|forget|bypass|output)\b")


def load_beir(name):
    cache = ART / "cache" / f"beir_{name}.parquet"
    qcache = ART / "cache" / f"beirq_{name}.json"
    if cache.exists() and qcache.exists():
        cdf = pd.read_parquet(cache); blob = json.load(open(qcache))
        return cdf["_id"].tolist(), cdf["text"].tolist(), blob["qids"], blob["qtexts"], blob["qrels"]
    corpus = load_dataset(f"BeIR/{name}", "corpus", split="corpus")
    queries = load_dataset(f"BeIR/{name}", "queries", split="queries")
    qrels_ds = load_dataset(f"BeIR/{name}-qrels", split="test")
    qrels = {}
    for r in qrels_ds:
        if int(r["score"]) > 0:
            qrels.setdefault(str(r["query-id"]), {})[str(r["corpus-id"])] = int(r["score"])
    qid2text = {str(q["_id"]): q["text"] for q in queries}
    qids = sorted([q for q in qrels if q in qid2text]); qtexts = [qid2text[q] for q in qids]
    cids, ctexts = [], []
    for d in corpus:
        t = (d.get("title") or "").strip(); b = (d.get("text") or "").strip()
        cids.append(str(d["_id"])); ctexts.append((t + " " + b).strip() if t else b)
    pd.DataFrame({"_id": cids, "text": ctexts}).to_parquet(cache)
    json.dump({"qids": qids, "qtexts": qtexts, "qrels": qrels}, open(qcache, "w"))
    return cids, ctexts, qids, qtexts, qrels


def ndcg_at_k(order_ids, rel, k=10):
    gains = [rel.get(d, 0) for d in order_ids[:k]]
    dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains))
    ideal = sorted(rel.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0


def minmax(x):
    x = np.asarray(x, dtype=np.float64); lo, hi = float(x.min()), float(x.max())
    return np.zeros_like(x) if hi - lo < 1e-12 else (x - lo) / (hi - lo)


class Timer:
    def __init__(self): self.t = {}
    def __call__(self, k):
        self.k = k; return self
    def __enter__(self):
        if DEVICE == "cuda": torch.cuda.synchronize()
        self.t0 = time.perf_counter(); return self
    def __exit__(self, *a):
        if DEVICE == "cuda": torch.cuda.synchronize()
        self.t[self.k] = self.t.get(self.k, 0.0) + (time.perf_counter() - self.t0) * 1000
'''))

C.append(md(r'''
## Benchmark loop

Indices are built once per corpus and kept resident, exactly as a deployed system
would — the CIKM candidate-pool code rebuilt a FAISS index and a BM25 index
*inside the per-query loop*, which is why its own timing artifacts vary by an
order of magnitude depending on which script produced them. Timings below exclude
index construction, which is reported separately.
'''))

C.append(code(r'''
encoder = SentenceTransformer(ENC_ID, device=DEVICE); encoder.max_seq_length = 256
cross_encoder = CrossEncoder(CE_ID, max_length=320, device=DEVICE)

# A minimal three-feature filter so the filtering stage is timed as configured.
_f_clean = ["placeholder"] * 6
_filter_clf = LogisticRegression().fit(np.array([[0.9, 0, 1.0], [0.2, 1, 0.2]] * 3),
                                       [0, 1] * 3)

rows, build_rows = [], []

for ds in BENCH_DATASETS:
    cids, ctexts, qids, qtexts, qrels = load_beir(ds)
    rng = np.random.default_rng(SEED)
    pick = rng.choice(len(qids), size=min(N_BENCH_QUERIES, len(qids)), replace=False)
    bq = [qtexts[i] for i in sorted(pick)]; bqid = [qids[i] for i in sorted(pick)]

    m0 = rss_gb()
    t0 = time.perf_counter()
    cpath = ART / "cache" / f"emb_{ds}_minilm.npy"
    if cpath.exists():
        emb = np.load(cpath); enc_time = float("nan")
    else:
        emb = encoder.encode(ctexts, batch_size=256, convert_to_numpy=True,
                             normalize_embeddings=True, show_progress_bar=True).astype(np.float16)
        np.save(cpath, emb); enc_time = time.perf_counter() - t0
    mat = torch.from_numpy(emb).to(DEVICE)
    t1 = time.perf_counter()
    stem = Stemmer.Stemmer("english")
    bm = bm25s.BM25(k1=0.9, b=0.4)
    bm.index(bm25s.tokenize(ctexts, stopwords="en", stemmer=stem, show_progress=False),
             show_progress=False)
    bm25_build = time.perf_counter() - t1
    mu = torch.from_numpy(emb[:2000].astype(np.float32)).mean(0)
    mu = (mu / mu.norm()).to(DEVICE)
    clean_mean_len = float(np.mean([len(t) for t in ctexts]))

    build_rows.append({"dataset": ds, "n_docs": len(ctexts),
                       "corpus_encode_s": enc_time, "bm25_build_s": bm25_build,
                       "embedding_mb": emb.nbytes / 1e6,
                       "rss_after_build_gb": rss_gb(), "rss_delta_gb": rss_gb() - m0})

    for depth in DEPTHS:
        for budget in RERANK_BUDGETS:
            if budget > depth:
                continue
            per_q, ndcgs, ce_calls = [], [], []
            for i, q in enumerate(tqdm(bq, desc=f"{ds} d={depth} b={budget}", leave=False)):
                T = Timer()
                with T("encode_query"):
                    qe = encoder.encode([q], convert_to_numpy=True,
                                        normalize_embeddings=True).astype(np.float16)
                with T("dense_search"):
                    qt = torch.from_numpy(qe).to(DEVICE)
                    sc, ix = torch.topk((qt @ mat.T).float(), min(depth, mat.shape[0]), dim=1)
                    d_sc, d_ix = sc[0].cpu().numpy(), ix[0].cpu().numpy()
                with T("bm25_search"):
                    tk = bm25s.tokenize([q], stopwords="en", stemmer=stem, show_progress=False)
                    b_ix, b_sc = bm.retrieve(tk, k=min(depth, len(ctexts)), show_progress=False)
                    b_ix, b_sc = b_ix[0], b_sc[0]
                with T("fuse"):
                    nd, nb = minmax(d_sc), minmax(b_sc)
                    dmap = {int(a): float(b) for a, b in zip(d_ix, nd)}
                    bmap = {int(a): float(b) for a, b in zip(b_ix, nb)}
                    cand = np.array(sorted(set(dmap) | set(bmap)))
                    fs = np.array([0.6 * dmap.get(int(c), 0.) + 0.4 * bmap.get(int(c), 0.)
                                   for c in cand])
                    order = cand[np.argsort(-fs, kind="stable")]
                with T("rerank"):
                    n_ce = 0
                    if budget > 0:
                        head = order[:budget]; n_ce = len(head)
                        cs = cross_encoder.predict([[q, ctexts[j]] for j in head],
                                                   batch_size=128, show_progress_bar=False)
                        order = np.concatenate([head[np.argsort(-cs, kind="stable")],
                                                order[budget:]])
                with T("filter"):
                    top = order[:10]
                    te = encoder.encode([ctexts[j] for j in top], convert_to_numpy=True,
                                        normalize_embeddings=True)
                    feats = np.stack([
                        te @ mu.cpu().numpy(),
                        np.array([1.0 if IMPERATIVE_RE.search(ctexts[j]) else 0.0 for j in top]),
                        np.array([len(ctexts[j]) / clean_mean_len for j in top])], axis=1)
                    _ = _filter_clf.predict_proba(feats)[:, 1]
                if i >= WARMUP:
                    per_q.append(dict(T.t, total=sum(T.t.values())))
                    ce_calls.append(n_ce)
                    ndcgs.append(ndcg_at_k([cids[j] for j in order[:10]], qrels[bqid[i]], 10))
            d = pd.DataFrame(per_q)
            rows.append({
                "dataset": ds, "n_docs": len(ctexts), "depth": depth, "rerank_budget": budget,
                "ndcg10": float(np.mean(ndcgs)),
                "ce_forward_passes_per_query": float(np.mean(ce_calls)),
                "p50_ms": float(d.total.quantile(.50)), "p95_ms": float(d.total.quantile(.95)),
                "p99_ms": float(d.total.quantile(.99)), "mean_ms": float(d.total.mean()),
                **{f"stage_{c}_ms": float(d[c].mean()) for c in d.columns if c != "total"},
            })
    del mat; gc.collect(); torch.cuda.empty_cache()

cost = pd.DataFrame(rows).round(3)
save_csv(cost, "nb5_cost_quality.csv")
save_csv(pd.DataFrame(build_rows).round(3), "nb5_index_build.csv")
save_json(CONFIG, "nb5_config.json")
print(cost[["dataset", "n_docs", "depth", "rerank_budget", "ndcg10",
            "ce_forward_passes_per_query", "p50_ms", "p95_ms", "p99_ms"]].to_string(index=False))
'''))

C.append(code(r'''
print("\n=== Stage breakdown (mean ms/query, depth=1000, rerank=100) ===")
sub = cost[(cost.depth == 1000) & (cost.rerank_budget == 100)]
stage_cols = [c for c in cost.columns if c.startswith("stage_")]
print(sub.set_index("dataset")[stage_cols].round(2).to_string())

print("\n=== What the reranker costs per nDCG point ===")
for ds, g in cost[cost.depth == 1000].groupby("dataset"):
    base = g[g.rerank_budget == 0]
    if base.empty:
        continue
    b_ndcg, b_ms = float(base.ndcg10.iloc[0]), float(base.mean_ms.iloc[0])
    for _, r in g[g.rerank_budget > 0].iterrows():
        dn, dm = r.ndcg10 - b_ndcg, r.mean_ms - b_ms
        print(f"  {ds:9s} top-{int(r.rerank_budget):3d}: "
              f"{dn:+.4f} nDCG for {dm:+7.1f} ms  "
              f"({dm/max(dn,1e-9):8.0f} ms per nDCG point)")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for ds, g in cost[cost.depth == 1000].groupby("dataset"):
    g = g.sort_values("mean_ms")
    ax.plot(g.mean_ms, g.ndcg10, marker="o", label=f"{ds} ({int(g.n_docs.iloc[0]):,} docs)")
    for _, r in g.iterrows():
        ax.annotate(f"CE@{int(r.rerank_budget)}", (r.mean_ms, r.ndcg10),
                    fontsize=7, xytext=(4, -8), textcoords="offset points")
ax.set_xlabel("mean latency per query (ms, persistent index)")
ax.set_ylabel("nDCG@10"); ax.set_xscale("log")
ax.set_title("Cost/quality frontier of cross-encoder reranking")
ax.legend(fontsize=8); ax.grid(alpha=.3)
plt.tight_layout()
for ext in ("pdf", "png"):
    plt.savefig(ART / "results" / f"fig_cost_quality.{ext}", dpi=180, bbox_inches="tight")
print("\nsaved fig_cost_quality.{pdf,png}")
plt.close()
'''))

C.append(md(r'''
## Reading this

Report `ce_forward_passes_per_query` next to every latency figure. Wall-clock on
a T4 tells a reader nothing about their own hardware; forward passes tell them
everything, and the two together let anyone re-derive the first from the second.

The "ms per nDCG point" line is the honest version of the CIKM latency claim. If
reranking the top-100 costs 200 ms for +0.05 nDCG on a 58K corpus, that is a
defensible engineering trade and should be stated as such — not as "sub-300 ms,
therefore practical", which was a claim about a synthetic 12-word vocabulary.
'''))

C.append(md(r'''
## 4. Archive and Download Outputs

Packages all latency profiling results into `cognisync_tmlr_results.zip` and initiates automatic download.
'''))

C.append(code(r'''
import shutil
from IPython.display import FileLink, display, Javascript

out_dir = str(ART)
zip_name = "cognisync_tmlr_results"
zip_base = f"/kaggle/working/{zip_name}" if Path("/kaggle/working").exists() else f"./{zip_name}"

shutil.make_archive(zip_base, "zip", out_dir)
zip_file = f"{zip_base}.zip"
size_mb = os.path.getsize(zip_file) / (1024 * 1024)

print("\n" + "="*60)
print(f">>> ARCHIVE CREATED: {zip_file} ({size_mb:.2f} MB)")
print("="*60)

display(FileLink(os.path.basename(zip_file)))

try:
    from google.colab import files
    files.download(zip_file)
except Exception:
    try:
        js_code = f"""
            const a = document.createElement("a");
            a.href = "{os.path.basename(zip_file)}";
            a.download = "{os.path.basename(zip_file)}";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        """
        display(Javascript(js_code))
        print(">>> Automatic download triggered in browser.")
    except Exception:
        print(">>> Click the link above to download your results archive.")
'''))

OUT_PATH_NB5 = os.path.join(os.path.dirname(__file__), "..", "notebooks", "NB5_cost_accounting.ipynb")
write_notebook(OUT_PATH_NB5, C, "cost/quality frontier")

# ===========================================================================
# NB6
# ===========================================================================
C = []

C.append(md(r'''
# NB6 — Assemble every table and figure for the paper

Reads the artifacts written by NB1–NB5 and emits the LaTeX the paper `\input`s,
so no number is ever retyped by hand. Every table carries the `n` it was computed
over and the operating point it was measured at.

Run this last. It needs no GPU and finishes in under a minute.

**Emits** into `ART/paper/`: `tab_*.tex`, `fig_*.pdf`, and `claims.json` — a
machine-checkable list of every numeric claim the paper makes, with the artifact
each one came from. Section 4 verifies that the paper's `.tex` contains no number
that `claims.json` cannot account for.
'''))

C.append(code(ENV_BLOCK + r'''
# Robust resolution for PAPER directory
PAPER = ART / "paper"
for cand in [Path("tmlr/paper"), Path("../paper"), Path("../../tmlr/paper")]:
    if cand.exists():
        PAPER = cand.resolve()
        break
PAPER.mkdir(parents=True, exist_ok=True)

R = ART / "results"

# Discover and unpack artifacts from /kaggle/input, /kaggle/working, or /content
discover_artifacts()

def have(name):
    p = R / name
    return p if p.exists() else None

print("\n" + "="*60)
print("NB6 INPUT ARTIFACT AUDIT:")
print("="*60)
for n in ["nb1_summary.csv", "nb1_pairwise.csv", "nb2_headroom.csv",
          "nb2_policy_comparison.csv", "nb2_alpha_predictability.csv",
          "nb3_attack_defense_matrix.csv", "nb3_roc_auc.csv", "nb3_calibration.csv",
          "nb4_behavioural_summary.csv", "nb4_retrieval_vs_behavioural.csv",
          "nb4_tool_selection_summary.csv", "nb5_cost_quality.csv"]:
    print(f"  [{'✓' if have(n) else '✗'}] {n}")
print("="*60 + "\n")

CLAIMS = {}
def claim(key, value, source, note=""):
    CLAIMS[key] = {"value": value, "source": source, "note": note}
    return value
'''))

C.append(code(r'''
def tex_escape(s):
    return str(s).replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def validate_tabular(body, name):
    """Fail loudly on the two LaTeX errors that are easy to generate and painful
    to debug: a row whose cell count disagrees with the column spec, and a stray
    unescaped percent sign (which silently comments out the rest of a line)."""
    key = "begin{tabular}{"
    i = body.find(key)
    assert i >= 0, f"{name}: no tabular spec found"
    j = body.index("}", i + len(key))
    ncol = sum(1 for ch in body[i + len(key):j] if ch in "lcr")
    problems = []
    for i, line in enumerate(body.splitlines()):
        st = line.strip()
        if not st.endswith("\\\\") or st.startswith("%"):
            continue
        if "multicolumn" in st:
            continue
        cells = st[:-2].split("&")
        if len(cells) != ncol:
            problems.append(f"    line {i}: {len(cells)} cells, spec says {ncol}: {st[:78]}")
    for i, line in enumerate(body.splitlines()):
        for k, ch in enumerate(line):
            if ch == "%" and (k == 0 or line[k - 1] != chr(92)):
                problems.append(f"    line {i}: unescaped % -> {line[:78]}")
    assert not problems, f"{name} is malformed:\n" + "\n".join(problems)
    return ncol


def write_tex(name, body, caption, label):
    ncol = validate_tabular(body, name)
    for m in re.finditer(r"%", caption):
        assert m.start() > 0 and caption[m.start() - 1] == chr(92), \
            f"{name}: unescaped % in caption -> {caption[:90]}"
    doc = ("\\begin{table}[t]\n\\centering\n\\small\n"
           f"\\caption{{{caption}}}\n\\label{{{label}}}\n{body}\n\\end{{table}}\n")
    (PAPER / name).write_text(doc)
    print(f"wrote {PAPER / name}  ({ncol} columns, validated)")


# ---------------------------------------------------------------- Table 1
if have("nb1_summary.csv"):
    s = pd.read_csv(R / "nb1_summary.csv")
    enc = s.encoder.iloc[0]
    s = s[s.encoder == enc]
    order = ["bm25", "dense", "rrf", "alpha_fixed", "alpha_learned",
             "alpha_learned_override", "alpha_oracle"]
    pretty = {"bm25": "BM25", "dense": "Dense", "rrf": "RRF ($k{=}60$)",
              "alpha_fixed": "Fixed $\\alpha^\\star$", "alpha_learned": "Learned $\\alpha$",
              "alpha_learned_override": "Learned $\\alpha$ + dense override",
              "alpha_oracle": "\\textit{Oracle} $\\alpha$"}
    ds_list = sorted(s.dataset.unique())
    budgets = sorted(s.budget.unique())
    L = ["\\begin{tabular}{l" + "c" * (len(ds_list) + 1) + "}", "\\toprule",
         "First stage & " + " & ".join(tex_escape(d) for d in ds_list) + " & Mean \\\\"]
    for b in budgets:
        L += ["\\midrule",
              "\\multicolumn{%d}{l}{\\textit{%s}} \\\\" %
              (len(ds_list) + 2, "no reranking" if b == 0 else f"cross-encoder top-{b}")]
        for sysname in order:
            r = s[(s.system == sysname) & (s.budget == b)]
            if r.empty:
                continue
            cells = []
            for d in ds_list:
                v = r[r.dataset == d]["ndcg10"]
                cells.append(f"{float(v.iloc[0]):.3f}" if len(v) else "--")
            L.append(f"{pretty[sysname]} & " + " & ".join(cells) +
                     f" & {r.ndcg10.mean():.3f} \\\\")
            claim(f"ndcg10.{sysname}.budget{b}", round(float(r.ndcg10.mean()), 4),
                  "nb1_summary.csv", f"mean over {len(ds_list)} BEIR corpora, encoder={enc}")
    L += ["\\bottomrule", "\\end{tabular}"]
    write_tex("tab_main_retrieval.tex", "\n".join(L),
              "Full-corpus nDCG@10 on BEIR under a matched cross-encoder budget. "
              "Every first stage is scored at the same reranking depth, so the "
              "fusion mechanism is compared against dense retrieval on equal "
              "compute. Oracle $\\alpha$ is an upper bound, not a system.",
              "tab:main_retrieval")

# ---------------------------------------------------------------- Table 2
if have("nb2_headroom.csv") and have("nb2_policy_comparison.csv"):
    h = pd.read_csv(R / "nb2_headroom.csv")
    p = pd.read_csv(R / "nb2_policy_comparison.csv")
    L = ["\\begin{tabular}{lcccc}", "\\toprule",
         "Policy & nDCG@10 & $\\Delta$ vs.\\ Dense & 95\\% CI & \\% headroom \\\\",
         "\\midrule"]
    fixed = p[p.policy.str.startswith("Fixed")]["ndcg10"]
    orac = p[p.policy.str.startswith("Oracle")]["ndcg10"]
    span = (float(orac.iloc[0]) - float(fixed.iloc[0])) if len(fixed) and len(orac) else np.nan
    for _, r in p.iterrows():
        pct = ((r.ndcg10 - float(fixed.iloc[0])) / span * 100) if span and span > 1e-9 else np.nan
        L.append(f"{tex_escape(r.policy)} & {r.ndcg10:.4f} & {r.delta_vs_dense:+.4f} & "
                 f"[{r.ci_low:+.4f}, {r.ci_high:+.4f}] & "
                 + (f"{pct:.0f}\\%" if np.isfinite(pct) else "--") + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    write_tex("tab_alpha_policies.tex", "\n".join(L),
              "Per-query fusion policies against the oracle ceiling. "
              "``\\% headroom'' is the share of the oracle-minus-fixed gap a policy "
              "captures. Intervals are paired bootstrap over per-query nDCG@10.",
              "tab:alpha_policies")
    claim("headroom.oracle_minus_fixed", round(float(span), 4) if span == span else None,
          "nb2_policy_comparison.csv")
    claim("headroom.pct_queries_alpha_irrelevant",
          round(float(h.pct_queries_alpha_irrelevant.mean()), 4), "nb2_headroom.csv",
          "fraction of queries where the entire alpha grid moves nDCG@10 by <0.01")

if have("nb2_alpha_predictability.csv"):
    pr = pd.read_csv(R / "nb2_alpha_predictability.csv")
    L = ["\\begin{tabular}{lccc}", "\\toprule",
         "Model & CV $R^2$ & Spearman $\\rho$ & MAE \\\\", "\\midrule"]
    for _, r in pr.iterrows():
        L.append(f"{tex_escape(r.model)} & {r.cv_r2:.3f} & {r.spearman_rho:.3f} & {r.mae:.3f} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    write_tex("tab_alpha_predictability.tex", "\n".join(L),
              "How predictable the oracle fusion weight is from the six query and "
              "score-distribution features, under 5-fold cross-validation.",
              "tab:alpha_predictability")
'''))

C.append(code(r'''
# ---------------------------------------------------------------- Table 3
if have("nb3_attack_defense_matrix.csv"):
    m = pd.read_csv(R / "nb3_attack_defense_matrix.csv")
    f_main = 0.01 if (m.target_fpr == 0.01).any() else float(m.target_fpr.min())
    mm = m[m.target_fpr == f_main]
    piv = mm.pivot(index="attack", columns="defense", values="asr")
    cols = [c for c in ["D0_none", "D1_3feat_tiny", "D1b_3feat_trained", "D2_embed_probe",
                        "D3_distilbert", "D4_guard_zeroshot", "D5_perplexity", "D6_ensemble"]
            if c in piv.columns]
    piv = piv[cols]
    short = {"D0_none": "none", "D1_3feat_tiny": "D1", "D1b_3feat_trained": "D1b",
             "D2_embed_probe": "D2", "D3_distilbert": "D3", "D4_guard_zeroshot": "D4",
             "D5_perplexity": "D5", "D6_ensemble": "D6"}
    L = ["\\begin{tabular}{l" + "c" * len(cols) + "}", "\\toprule",
         "Attacker & " + " & ".join(short[c] for c in cols) + " \\\\", "\\midrule"]
    for a in piv.index:
        L.append(tex_escape(a) + " & " +
                 " & ".join(f"{piv.loc[a, c]:.2f}" for c in cols) + " \\\\")
        for c in cols:
            claim(f"asr.{a}.{c}.fpr{f_main}", round(float(piv.loc[a, c]), 4),
                  "nb3_attack_defense_matrix.csv", f"n={int(mm[mm.attack==a].n.iloc[0])}")
    L += ["\\bottomrule", "\\end{tabular}"]
    # The "none" column already is the undefended entry rate, so it is named in
    # the caption rather than repeated as a row.
    write_tex("tab_attack_defense.tex", "\n".join(L),
              f"Retrieval-level attack success rate at a matched false-positive "
              f"budget of {f_main*100:g}\\%. Rows are attackers ordered by capability; "
              f"columns are defenses ordered by cost. The \\textit{{none}} column is "
              f"the undefended payload-entry rate. Every defended cell is measured "
              f"at the same operating point, calibrated on held-out clean documents.",
              "tab:attack_defense")

    ucost = (m[m.attack == "A0_static_templates"]
             .pivot(index="defense", columns="target_fpr", values="utility_cost_ndcg"))
    L = ["\\begin{tabular}{l" + "c" * len(ucost.columns) + "}", "\\toprule",
         "Defense & " + " & ".join(f"FPR {c*100:g}\\%" for c in ucost.columns) +
         " \\\\", "\\midrule"]
    for d in ucost.index:
        L.append(tex_escape(d) + " & " +
                 " & ".join(f"{ucost.loc[d, c]:.4f}" for c in ucost.columns) + " \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    write_tex("tab_utility_cost.tex", "\n".join(L),
              "Utility cost of filtering: nDCG@10 lost on clean full-corpus "
              "retrieval, with no attack present, at each operating point.",
              "tab:utility_cost")

# ---------------------------------------------------------------- Table 4
if have("nb4_retrieval_vs_behavioural.csv"):
    g = pd.read_csv(R / "nb4_retrieval_vs_behavioural.csv")
    L = ["\\begin{tabular}{llccc}", "\\toprule",
         "Model & Attacker & ASR$_\\text{retr}$ & ASR$_\\text{behav}$ & "
         "$P(\\text{comply}\\mid\\text{entry})$ \\\\", "\\midrule"]
    for _, r in g.iterrows():
        L.append(f"{tex_escape(r.model.split('/')[-1])} & {tex_escape(r.attack)} & "
                 f"{r.asr_retrieval_undefended:.2f} & {r.asr_behavioural_undefended:.2f} & "
                 f"{r.compliance_given_entry:.2f} \\\\")
        claim(f"compliance.{r.model.split('/')[-1]}.{r.attack}",
              round(float(r.compliance_given_entry), 4),
              "nb4_retrieval_vs_behavioural.csv")
    L += ["\\bottomrule", "\\end{tabular}"]
    write_tex("tab_behavioural_gap.tex", "\n".join(L),
              "Retrieval-level payload entry versus downstream compliance, on the "
              "same episodes with no defense. The last column is the factor by "
              "which a retrieval-level metric must be discounted to estimate "
              "real exposure.",
              "tab:behavioural_gap")

# ---------------------------------------------------------------- Table 5
if have("nb5_cost_quality.csv"):
    c = pd.read_csv(R / "nb5_cost_quality.csv")
    c = c[c.depth == c.depth.max()]
    L = ["\\begin{tabular}{lrrrrrr}", "\\toprule",
         "Corpus & $|D|$ & CE/query & nDCG@10 & p50 & p95 & p99 \\\\", "\\midrule"]
    for _, r in c.iterrows():
        L.append(f"{tex_escape(r.dataset)} & {int(r.n_docs):,} & "
                 f"{int(r.ce_forward_passes_per_query)} & {r.ndcg10:.3f} & "
                 f"{r.p50_ms:.0f} & {r.p95_ms:.0f} & {r.p99_ms:.0f} \\\\")
    L += ["\\bottomrule", "\\end{tabular}"]
    write_tex("tab_cost.tex", "\n".join(L),
              "Cost and quality from the same runs, on real corpora with a "
              "persistent index. Cross-encoder forward passes per query is the "
              "hardware-independent cost; latencies are on a single T4.",
              "tab:cost")
'''))

C.append(md(r'''
## Result macros for the manuscript

The paper's prose contains no hand-typed numbers. Every inline figure is a LaTeX
macro defined in `results_macros.tex`, generated here from the artifacts. Until
this notebook has run, each macro renders as a red placeholder in the compiled
PDF, so an unfilled slot is impossible to miss and impossible to mistake for a
measurement.
'''))

C.append(code(r'''
def pct(x, d=1):
    return f"{100*float(x):.{d}f}\\%"


def num(x, d=3):
    return f"{float(x):.{d}f}"


M = {}

# ---- retrieval (NB1) -------------------------------------------------------
if have("nb1_summary.csv"):
    s1 = pd.read_csv(R / "nb1_summary.csv")
    s1 = s1[s1.encoder == s1.encoder.iloc[0]]
    top_budget = int(s1.budget.max())
    def mean_ndcg(system, budget):
        v = s1[(s1.system == system) & (s1.budget == budget)]["ndcg10"]
        return float(v.mean()) if len(v) else float("nan")
    M["ndcgDenseCE"] = num(mean_ndcg("dense", top_budget))
    M["ndcgLearnedCE"] = num(mean_ndcg("alpha_learned", top_budget))
    claim("macro.ndcgDenseCE", mean_ndcg("dense", top_budget), "nb1_summary.csv",
          f"mean nDCG@10, cross-encoder top-{top_budget}")
    claim("macro.ndcgLearnedCE", mean_ndcg("alpha_learned", top_budget),
          "nb1_summary.csv", f"mean nDCG@10, cross-encoder top-{top_budget}")

if have("nb1_corpus_stats.csv"):
    cs = pd.read_csv(R / "nb1_corpus_stats.csv")
    M["nBeirCorpora"] = str(len(cs))
    M["nBeirDocs"] = f"{int(cs.n_docs.sum()):,}"
    M["nBeirQueries"] = f"{int(cs.n_queries.sum()):,}"

# ---- fusion headroom (NB2) -------------------------------------------------
if have("nb2_policy_comparison.csv"):
    p2 = pd.read_csv(R / "nb2_policy_comparison.csv")
    orac = p2[p2.policy.str.startswith("Oracle")]["ndcg10"]
    fixed = p2[p2.policy.str.startswith("Fixed")]["ndcg10"]
    learned = p2[p2.policy.str.startswith("Learned")]["ndcg10"]
    if len(orac) and len(fixed):
        M["ndcgOracle"] = num(orac.iloc[0]); M["ndcgFixed"] = num(fixed.iloc[0])
        span = float(orac.iloc[0]) - float(fixed.iloc[0])
        if len(learned) and abs(span) > 1e-9:
            frac = (float(learned.max()) - float(fixed.iloc[0])) / span
            M["headroomPct"] = pct(max(0.0, frac), 0)
            claim("macro.headroomPct", round(frac, 4), "nb2_policy_comparison.csv",
                  "share of oracle-minus-fixed gap captured by the best learned policy")

if have("nb2_headroom.csv"):
    h2 = pd.read_csv(R / "nb2_headroom.csv")
    M["flatFrac"] = pct(h2.pct_queries_alpha_irrelevant.mean(), 0)

if have("nb2_alpha_predictability.csv"):
    a2 = pd.read_csv(R / "nb2_alpha_predictability.csv")
    M["alphaRtwo"] = num(a2.cv_r2.max(), 3)
    claim("macro.alphaRtwo", float(a2.cv_r2.max()), "nb2_alpha_predictability.csv",
          "best cross-validated R^2 over all predictors tried")

# ---- security (NB3) --------------------------------------------------------
if have("nb3_attack_defense_matrix.csv"):
    m3 = pd.read_csv(R / "nb3_attack_defense_matrix.csv")
    f_main = 0.01 if (m3.target_fpr == 0.01).any() else float(m3.target_fpr.min())
    mm = m3[m3.target_fpr == f_main]
    def asr(attack, defense):
        v = mm[(mm.attack == attack) & (mm.defense == defense)]["asr"]
        return float(v.iloc[0]) if len(v) else float("nan")
    for key, (a, d) in {"asrDoneStatic": ("A0_static_templates", "D1_3feat_tiny"),
                        "asrDoneAdaptive": ("A5_score_guided", "D1_3feat_tiny"),
                        "asrDthreeAdaptive": ("A5_score_guided", "D3_distilbert")}.items():
        v = asr(a, d)
        if v == v:
            M[key] = pct(v, 1)
            claim(f"macro.{key}", round(v, 4), "nb3_attack_defense_matrix.csv",
                  f"{a} vs {d} at FPR {f_main:.1%}")
    uc = mm[(mm.attack == "A0_static_templates") &
            (mm.defense == "D3_distilbert")]["utility_cost_ndcg"]
    if len(uc):
        M["utilityCost"] = num(uc.iloc[0], 4)

# ---- behaviour (NB4) -------------------------------------------------------
if have("nb4_retrieval_vs_behavioural.csv"):
    g4 = pd.read_csv(R / "nb4_retrieval_vs_behavioural.csv")
    g4 = g4[np.isfinite(g4.compliance_given_entry)]
    if len(g4):
        M["complianceRate"] = pct(g4.compliance_given_entry.mean(), 0)
        fin = g4[np.isfinite(g4.overstatement_factor)]
        if len(fin):
            M["overstatement"] = f"{fin.overstatement_factor.mean():.1f}"
        claim("macro.complianceRate", round(float(g4.compliance_given_entry.mean()), 4),
              "nb4_retrieval_vs_behavioural.csv", "mean over models and attacks")

if have("nb4_behavioural_summary.csv"):
    b4 = pd.read_csv(R / "nb4_behavioural_summary.csv")
    hd = b4[(b4.system == "hardened") & (b4.attack != "clean") & (b4.position == 0)]
    if len(hd):
        M["promptHardenASR"] = pct(hd.asr_behavioural.mean(), 1)
        claim("macro.promptHardenASR", round(float(hd.asr_behavioural.mean()), 4),
              "nb4_behavioural_summary.csv", "hardened system prompt, poison at rank 0")

lines = ["%% Auto-generated by NB6. Do not edit by hand.",
         "%% Regenerate by re-running NB6 after the experiment notebooks."]
for k, v in sorted(M.items()):
    lines.append("\\newcommand{\\%s}{%s}" % (k, v))
(PAPER / "results_macros.tex").write_text("\n".join(lines) + "\n")
print(f"wrote {PAPER/'results_macros.tex'} with {len(M)} macros\n")
print("\n".join(lines[2:]))

missing = [k for k in ["ndcgDenseCE", "ndcgLearnedCE", "ndcgOracle", "ndcgFixed",
                       "headroomPct", "flatFrac", "alphaRtwo", "asrDoneStatic",
                       "asrDoneAdaptive", "asrDthreeAdaptive", "complianceRate",
                       "overstatement", "utilityCost", "promptHardenASR",
                       "nBeirCorpora", "nBeirDocs", "nBeirQueries"] if k not in M]
if missing:
    print("\nSTILL PLACEHOLDERS (run the notebook that produces each):")
    for k in missing:
        print("   \\" + k)
else:
    print("\nEvery macro the manuscript uses is filled.")
'''))

C.append(code(r'''
import shutil
for f in R.glob("fig_*.pdf"):
    shutil.copy(f, PAPER / f.name)
for f in R.glob("fig_*.png"):
    shutil.copy(f, PAPER / f.name)

with open(PAPER / "claims.json", "w") as fh:
    json.dump(CLAIMS, fh, indent=2, default=float)
print(f"\n{len(CLAIMS)} numeric claims recorded in {PAPER/'claims.json'}")
for k, v in sorted(CLAIMS.items())[:25]:
    print(f"  {k:52s} = {v['value']}   <- {v['source']}")
print("\nFiles for the paper:")
for f in sorted(PAPER.iterdir()):
    print("  ", f.name)
'''))

C.append(md(r'''
## Claim audit

`claims.json` is the artifact that makes the paper checkable. Every number in the
manuscript should be traceable to a key in it, and the check below flags any
number in the `.tex` that is not — the direct answer to the reviewer complaint
that the CIKM version's tables disagreed with each other (Table 7 reporting FPR
1.04% while Table 9 reported 0.0% for the same system, and the repository's own
`latency_results.txt` recording a 3,325 ms median against the paper's 275.6 ms).

Point `PAPER_TEX` at the manuscript and run it before every submission.
'''))

C.append(code(r'''
PAPER_TEX = None
for cand in [Path("cognisync_tmlr.tex"), Path("tmlr/paper/cognisync_tmlr.tex"),
             Path("../paper/cognisync_tmlr.tex"), Path("../../tmlr/paper/cognisync_tmlr.tex"),
             PAPER / "cognisync_tmlr.tex"]:
    if cand.exists():
        PAPER_TEX = cand
        break

if PAPER_TEX and PAPER_TEX.exists():
    src = PAPER_TEX.read_text()
    src = re.sub(r"%.*", "", src)
    nums = set(re.findall(r"(?<![\w.])(\d+\.\d{2,4})(?![\w])", src))
    known = set()
    for v in CLAIMS.values():
        if isinstance(v["value"], (int, float)):
            for d in (2, 3, 4):
                known.add(f"{v['value']:.{d}f}")
                known.add(f"{v['value']*100:.{d}f}")
    unaccounted = sorted(n for n in nums if n not in known)
    print(f"{len(nums)} numeric literals in the manuscript; "
          f"{len(nums)-len(unaccounted)} match a recorded claim.")
    if unaccounted:
        print("\nNot traceable to claims.json (check each is a citation year, a "
              "hyperparameter, or a typo):")
        for n in unaccounted[:60]:
            print("   ", n)
else:
    print(f"{PAPER_TEX} not found - upload the manuscript next to this notebook "
          f"to run the audit.")
'''))

C.append(md(r'''
## 5. Archive and Download Outputs

Packages all results, LaTeX tables, figures, and macros into `cognisync_tmlr_results.zip` and initiates automatic download.
'''))

C.append(code(r'''
import shutil
from IPython.display import FileLink, display, Javascript

out_dir = str(ART)
zip_name = "cognisync_tmlr_results"
zip_base = f"/kaggle/working/{zip_name}" if Path("/kaggle/working").exists() else f"./{zip_name}"

shutil.make_archive(zip_base, "zip", out_dir)
zip_file = f"{zip_base}.zip"
size_mb = os.path.getsize(zip_file) / (1024 * 1024)

print("\n" + "="*60)
print(f">>> ARCHIVE CREATED: {zip_file} ({size_mb:.2f} MB)")
print("="*60)

display(FileLink(os.path.basename(zip_file)))

try:
    from google.colab import files
    files.download(zip_file)
except Exception:
    try:
        js_code = f"""
            const a = document.createElement("a");
            a.href = "{os.path.basename(zip_file)}";
            a.download = "{os.path.basename(zip_file)}";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        """
        display(Javascript(js_code))
        print(">>> Automatic download triggered in browser.")
    except Exception:
        print(">>> Click the link above to download your results archive.")
'''))

OUT_PATH_NB6 = os.path.join(os.path.dirname(__file__), "..", "notebooks", "NB6_tables_figures.ipynb")
write_notebook(OUT_PATH_NB6, C, "assemble tables/figures + claim audit")
