"""NB2 - Why per-query fusion weighting does not pay: oracle headroom + identifiability."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import md, code, write_notebook, ENV_BLOCK, BOOTSTRAP_BLOCK

C = []

C.append(md(r'''
# NB2 — Oracle headroom and the identifiability of per-query fusion weights

Reviewers of the CIKM version all converged on the same observation: learned-α
fusion does not beat dense retrieval, so the mechanism in the title is not what
produces the numbers. That observation is correct. This notebook stops treating
it as a defect to be explained away and turns it into the paper's main
retrieval result, by answering a question the CIKM version never asked:

> **Is per-query fusion weighting hard because the predictor is weak, or because
> the target is not there to be predicted?**

Those two possibilities call for completely different follow-up work, and
telling them apart is a genuinely useful thing to publish.

### The three quantities

For each query we sweep α over a grid and record the whole α → nDCG@10 curve.
That gives:

| Quantity | Meaning |
|---|---|
| `ndcg(α_fixed)` | best single global weight — what a tuned static hybrid gets |
| `ndcg(α_oracle)` | best per-query weight in hindsight — **ceiling for any per-query policy** |
| `ndcg(α_learned)` | what the six-feature random forest actually achieves |

`oracle − fixed` is the **total headroom** available to per-query weighting.
`learned − fixed` is the fraction of it that gets captured. The CIKM paper
reported neither.

### The identifiability diagnostics

1. **Curve flatness.** For most queries, does α matter at all? We report the
   per-query range `max(curve) − min(curve)` and the fraction of the grid within
   ε of the optimum. If curves are flat, α* is nearly arbitrary and the
   regression target is noise — no feature set can fix that.
2. **Argmax multiplicity.** How many grid points tie for the optimum.
3. **Target predictability.** Spearman ρ and R² between predicted and oracle α,
   plus a permutation test. Also: an upper bound obtained by fitting a *much*
   larger model (gradient boosting, 500 trees) on the same features, which
   separates "features are uninformative" from "random forest is underpowered".
4. **Feature ablation and mutual information** between each feature and α*.

### Three formulations beyond regression

Because "predict a real number" may simply be the wrong framing, we also
evaluate:

- **Router (classification).** Pick one of {dense-only, RRF, bm25-heavy} per query.
- **Selective / risk–coverage.** Deviate from dense only when a confidence score
  exceeds a threshold; sweep the threshold to get a risk–coverage curve. If any
  per-query policy is worth deploying, it shows up here as a region where
  selective deviation beats always-dense.
- **Best-of-both oracle-lite.** Rank by dense, but let BM25 promote a document
  only when its normalised lexical score is extreme (a cheap, interpretable rule).

**Inputs.** Reads `nb1_per_query.parquet` and `nb1_alphafit_*.csv` if NB1 has
been run; otherwise it regenerates the α sweep itself on two BEIR datasets.

**Runtime.** ~15 min on a free T4 if NB1 artifacts exist; ~35 min standalone.
Peak VRAM ~2 GB. This notebook is cheap — it is analysis, not a sweep.
'''))

C.append(code(r'''
!pip install -q "sentence-transformers>=3.0" "bm25s[full]" PyStemmer datasets pyarrow scikit-learn 2>&1 | tail -1
'''))

C.append(code(ENV_BLOCK + r'''

ALPHA_GRID = np.round(np.linspace(0.0, 1.0, 21), 2)
FLATNESS_EPS = 0.01     # nDCG within this of the max counts as "as good as optimal"
STANDALONE_DATASETS = ["scifact", "fiqa"]   # used only if NB1 artifacts are absent
FIRST_STAGE_DEPTH = 1000
RRF_K = 60

nb1_path = ART / "results" / "nb1_per_query.parquet"
HAVE_NB1 = nb1_path.exists()
print("NB1 artifacts present:", HAVE_NB1)
''' + BOOTSTRAP_BLOCK))

C.append(md(r'''
## 1. Building the α → nDCG curves

If NB1 has run we still need the *full curve* per query (NB1 only stored the
argmax), so this cell recomputes the sweep. The retrieval machinery is copied
verbatim from NB1 rather than imported, so this notebook runs standalone.
'''))

C.append(code(r'''
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import bm25s, Stemmer

ENC_ID = "sentence-transformers/all-MiniLM-L6-v2"


def minmax(x):
    x = np.asarray(x, dtype=np.float64)
    lo, hi = float(x.min()), float(x.max())
    return np.zeros_like(x) if hi - lo < 1e-12 else (x - lo) / (hi - lo)


def build_candidate_scores(d_idx, d_sc, b_idx, b_sc):
    nd, nb = minmax(d_sc), minmax(b_sc)
    dmap = {int(i): float(s) for i, s in zip(d_idx, nd)}
    bmap = {int(i): float(s) for i, s in zip(b_idx, nb)}
    cands = np.array(sorted(set(dmap) | set(bmap)), dtype=np.int64)
    dv = np.array([dmap.get(int(c), 0.0) for c in cands])
    bv = np.array([bmap.get(int(c), 0.0) for c in cands])
    dr = {int(i): r for r, i in enumerate(d_idx)}
    br = {int(i): r for r, i in enumerate(b_idx)}
    BIG = len(cands) + RRF_K
    return (cands, dv, bv,
            np.array([dr.get(int(c), BIG) for c in cands]),
            np.array([br.get(int(c), BIG) for c in cands]))


def alpha_features(query, dv, bv):
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


FEATURE_NAMES = ["query_len", "dense_std", "bm25_std", "dense_cv", "bm25_cv", "has_identifier"]


def ndcg_at_k(order_ids, rel, k=10):
    gains = [rel.get(d, 0) for d in order_ids[:k]]
    dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains))
    ideal = sorted(rel.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0


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
    qids = sorted([q for q in qrels if q in qid2text])
    qtexts = [qid2text[q] for q in qids]
    cids, ctexts = [], []
    for d in corpus:
        t = (d.get("title") or "").strip(); b = (d.get("text") or "").strip()
        cids.append(str(d["_id"])); ctexts.append((t + " " + b).strip() if t else b)
    pd.DataFrame({"_id": cids, "text": ctexts}).to_parquet(cache)
    json.dump({"qids": qids, "qtexts": qtexts, "qrels": qrels}, open(qcache, "w"))
    return cids, ctexts, qids, qtexts, qrels


def sweep_dataset(name):
    """Return a DataFrame with one row per query holding the full alpha curve."""
    cache = ART / "results" / f"nb2_curves_{name}.parquet"
    if cache.exists():
        print(f"  reusing {cache.name}")
        return pd.read_parquet(cache)
    cids, ctexts, qids, qtexts, qrels = load_beir(name)
    print(f"{name}: corpus={len(cids):,} queries={len(qids):,}")

    model = SentenceTransformer(ENC_ID, device=DEVICE); model.max_seq_length = 256
    cpath = ART / "cache" / f"emb_{name}_minilm.npy"
    if cpath.exists():
        emb = np.load(cpath)
    else:
        emb = model.encode(ctexts, batch_size=256, convert_to_numpy=True,
                           normalize_embeddings=True, show_progress_bar=True).astype(np.float16)
        np.save(cpath, emb)
    mat = torch.from_numpy(emb).to(DEVICE)
    q = torch.from_numpy(model.encode(qtexts, batch_size=256, convert_to_numpy=True,
                                      normalize_embeddings=True,
                                      show_progress_bar=False).astype(np.float16)).to(DEVICE)
    d_sc, d_ix = torch.topk((q @ mat.T).float(), min(FIRST_STAGE_DEPTH, mat.shape[0]), dim=1)
    d_sc, d_ix = d_sc.cpu().numpy(), d_ix.cpu().numpy()
    del mat, q; gc.collect(); torch.cuda.empty_cache()

    stem = Stemmer.Stemmer("english")
    r = bm25s.BM25(k1=0.9, b=0.4)
    r.index(bm25s.tokenize(ctexts, stopwords="en", stemmer=stem, show_progress=False),
            show_progress=False)
    b_ix, b_sc = r.retrieve(bm25s.tokenize(qtexts, stopwords="en", stemmer=stem,
                                           show_progress=False),
                            k=min(FIRST_STAGE_DEPTH, len(ctexts)), show_progress=False)

    rows = []
    for i, qid in enumerate(tqdm(qids, desc=f"  sweep {name}")):
        rel = qrels[qid]
        cands, dv, bv, drank, brank = build_candidate_scores(d_ix[i], d_sc[i], b_ix[i], b_sc[i])
        curve = []
        for a in ALPHA_GRID:
            o = cands[np.argsort(-(a * dv + (1 - a) * bv), kind="stable")]
            curve.append(ndcg_at_k([cids[k] for k in o[:10]], rel, 10))
        curve = np.array(curve)
        rrf_o = cands[np.argsort(-(1.0 / (RRF_K + drank + 1) + 1.0 / (RRF_K + brank + 1)),
                                 kind="stable")]
        rows.append({
            "dataset": name, "qid": qid, "query": qtexts[i],
            "curve": curve.tolist(),
            "features": alpha_features(qtexts[i], dv, bv),
            "ndcg_rrf": ndcg_at_k([cids[k] for k in rrf_o[:10]], rel, 10),
            "n_rel": len(rel),
        })
    df = pd.DataFrame(rows)
    df.to_parquet(cache)
    return df


datasets_to_sweep = (sorted(pd.read_parquet(nb1_path)["dataset"].unique())
                     if HAVE_NB1 else STANDALONE_DATASETS)
datasets_to_sweep = [d for d in datasets_to_sweep if d != "msmarco"]
print("sweeping:", datasets_to_sweep)
curves = pd.concat([sweep_dataset(d) for d in datasets_to_sweep], ignore_index=True)
print(len(curves), "queries with full alpha curves")
'''))

C.append(md(r'''
## 2. Headroom: how much is per-query weighting worth *at best*?

`α_fixed` is chosen per dataset by maximising the mean nDCG@10 over the grid —
i.e. the strongest possible static hybrid, tuned on the very queries it is
scored on. That deliberately over-credits the baseline: if per-query weighting
cannot beat a baseline this generous, the negative result is airtight.
'''))

C.append(code(r'''
curve_mat = np.vstack(curves["curve"].apply(np.asarray).values)   # [Q, |grid|]
curves["oracle_ndcg"] = curve_mat.max(axis=1)
curves["oracle_alpha"] = ALPHA_GRID[curve_mat.argmax(axis=1)]
curves["dense_ndcg"] = curve_mat[:, -1]      # alpha = 1.0
curves["bm25_ndcg"] = curve_mat[:, 0]        # alpha = 0.0
curves["curve_range"] = curve_mat.max(axis=1) - curve_mat.min(axis=1)
curves["n_within_eps"] = (curve_mat >= (curve_mat.max(axis=1, keepdims=True) - FLATNESS_EPS)).sum(axis=1)
curves["n_argmax_ties"] = (curve_mat == curve_mat.max(axis=1, keepdims=True)).sum(axis=1)

head = []
for ds, g in curves.groupby("dataset"):
    m = np.vstack(g["curve"].apply(np.asarray).values)
    a_fixed = float(ALPHA_GRID[m.mean(axis=0).argmax()])
    fixed_ndcg = m[:, int(np.where(ALPHA_GRID == a_fixed)[0][0])]
    head.append({
        "dataset": ds, "n_queries": len(g),
        "alpha_fixed": a_fixed,
        "ndcg_dense": g["dense_ndcg"].mean(),
        "ndcg_bm25": g["bm25_ndcg"].mean(),
        "ndcg_rrf": g["ndcg_rrf"].mean(),
        "ndcg_fixed": fixed_ndcg.mean(),
        "ndcg_oracle": g["oracle_ndcg"].mean(),
        "headroom_oracle_minus_fixed": g["oracle_ndcg"].mean() - fixed_ndcg.mean(),
        "headroom_oracle_minus_dense": g["oracle_ndcg"].mean() - g["dense_ndcg"].mean(),
        "pct_queries_alpha_irrelevant": float((g["curve_range"] < FLATNESS_EPS).mean()),
        "median_grid_points_within_eps": float(g["n_within_eps"].median()),
        "median_argmax_ties": float(g["n_argmax_ties"].median()),
    })
headroom = pd.DataFrame(head).round(4)
save_csv(headroom, "nb2_headroom.csv")
print(headroom.to_string(index=False))
print("\nPooled (unweighted over datasets):")
print(headroom[["ndcg_dense", "ndcg_rrf", "ndcg_fixed", "ndcg_oracle",
                "headroom_oracle_minus_fixed", "pct_queries_alpha_irrelevant"]].mean().round(4).to_string())
'''))

C.append(md(r'''
## 3. Identifiability: is α\* even a learnable target?

Three diagnostics, in increasing order of how damning they are if they come back
negative:

1. **Flatness.** The fraction of queries where the entire α grid moves nDCG@10 by
   less than ε. For those queries, α\* is whichever grid point won a coin flip;
   any regressor trained on them is fitting noise.
2. **Ceiling on predictability.** We fit a deliberately overpowered model
   (gradient boosting, 500 estimators) with 5-fold cross-validation on the same
   six features. If *that* cannot predict α\*, the features are the problem, not
   the random forest.
3. **Permutation test.** Shuffle α\* against the features and re-fit. If the real
   R² sits inside the shuffled distribution, the features carry no signal at all.
'''))

C.append(code(r'''
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.feature_selection import mutual_info_regression
from scipy.stats import spearmanr

X = np.vstack(curves["features"].apply(np.asarray).values)
y = curves["oracle_alpha"].values
kf = KFold(n_splits=5, shuffle=True, random_state=SEED)

def r2(y_true, y_pred):
    ss_res = float(((y_true - y_pred) ** 2).sum())
    ss_tot = float(((y_true - y_true.mean()) ** 2).sum())
    return 1 - ss_res / (ss_tot + 1e-12)

models = {
    "RandomForest(50,d5) [CIKM config]": RandomForestRegressor(
        n_estimators=50, max_depth=5, random_state=SEED, n_jobs=-1),
    "RandomForest(500,d16)": RandomForestRegressor(
        n_estimators=500, max_depth=16, min_samples_leaf=2, random_state=SEED, n_jobs=-1),
    "GradientBoosting(500)": GradientBoostingRegressor(
        n_estimators=500, max_depth=4, random_state=SEED),
}
pred_rows, preds_store = [], {}
for name, m in models.items():
    p = cross_val_predict(m, X, y, cv=kf, n_jobs=1)
    preds_store[name] = p
    rho, _ = spearmanr(p, y)
    pred_rows.append({"model": name, "cv_r2": r2(y, p), "spearman_rho": float(rho),
                      "mae": float(np.abs(p - y).mean()),
                      "mae_predict_mean": float(np.abs(y.mean() - y).mean())})

# Permutation baseline for the strongest model.
rng = np.random.default_rng(SEED)
perm_r2 = []
for _ in range(50):
    yp = rng.permutation(y)
    p = cross_val_predict(models["GradientBoosting(500)"], X, yp, cv=kf, n_jobs=1)
    perm_r2.append(r2(yp, p))
pred_df = pd.DataFrame(pred_rows).round(4)
save_csv(pred_df, "nb2_alpha_predictability.csv")
print(pred_df.to_string(index=False))
print(f"\nPermuted-label CV R^2: mean={np.mean(perm_r2):.4f} "
      f"95th pct={np.percentile(perm_r2, 95):.4f}")
print(f"Real GB CV R^2: {pred_df.loc[pred_df.model.str.startswith('Gradient'), 'cv_r2'].iloc[0]:.4f}")

mi = mutual_info_regression(X, y, random_state=SEED)
mi_df = pd.DataFrame({"feature": FEATURE_NAMES, "mutual_info_with_alpha_star": mi}).round(4)
save_csv(mi_df, "nb2_feature_mi.csv")
print("\n" + mi_df.to_string(index=False))
'''))

C.append(md(r'''
## 4. What the predictions are actually worth

Predicting α\* well and *retrieving* well are not the same thing: a small error
on a flat curve costs nothing, a small error on a peaked one costs a lot. So we
score each predictor the way it will be used — read the achieved nDCG@10 straight
off each query's curve at the predicted α — and compare against fixed-α, dense,
RRF, and the oracle.
'''))

C.append(code(r'''
def ndcg_at_alpha(curve_row, alpha):
    """Curve is on a grid; snap to the nearest grid point (grid step 0.05)."""
    j = int(np.abs(ALPHA_GRID - alpha).argmin())
    return float(curve_row[j])

alpha_fixed_global = float(ALPHA_GRID[curve_mat.mean(axis=0).argmax()])
achieved = {
    "BM25 (alpha=0)": curve_mat[:, 0],
    "Dense (alpha=1)": curve_mat[:, -1],
    "RRF (k=60)": curves["ndcg_rrf"].values,
    f"Fixed alpha*={alpha_fixed_global:.2f}": curve_mat[:, int(np.abs(ALPHA_GRID - alpha_fixed_global).argmin())],
    "Oracle alpha (ceiling)": curve_mat.max(axis=1),
}
for name, p in preds_store.items():
    achieved[f"Learned: {name}"] = np.array(
        [ndcg_at_alpha(curve_mat[i], p[i]) for i in range(len(p))])

rows = []
dense_scores = curve_mat[:, -1]
for name, sc in achieved.items():
    st = paired_bootstrap(sc, dense_scores)
    rows.append({"policy": name, "ndcg10": float(np.mean(sc)),
                 "delta_vs_dense": st["mean_diff"],
                 "ci_low": st["ci_low"], "ci_high": st["ci_high"],
                 "boot_p": st["boot_p"]})
policy_df = pd.DataFrame(rows).round(4)
save_csv(policy_df, "nb2_policy_comparison.csv")
print(policy_df.to_string(index=False))

captured = ((policy_df.set_index("policy").loc[[c for c in policy_df.policy if c.startswith("Learned")], "ndcg10"].max()
             - policy_df.set_index("policy").loc[f"Fixed alpha*={alpha_fixed_global:.2f}", "ndcg10"])
            / max(1e-9, (policy_df.set_index("policy").loc["Oracle alpha (ceiling)", "ndcg10"]
                         - policy_df.set_index("policy").loc[f"Fixed alpha*={alpha_fixed_global:.2f}", "ndcg10"])))
print(f"\nFraction of oracle headroom captured by the best learned policy: {captured*100:.1f}%")
'''))

C.append(md(r'''
## 5. Formulations other than regression

Regression onto a flat, tie-ridden target may simply be the wrong learning
problem. Three alternatives, all fit on the same six features:

- **Router.** Three-way classification over {dense, RRF, bm25-lean (α=0.3)}, with
  the label being whichever wins on that query.
- **Selective deviation.** Rank by dense unless the router is confident; sweep the
  confidence threshold to trace a risk–coverage curve. This is the formulation
  most likely to work, because it only has to be right about *when to act*.
- **Extreme-lexical promotion.** No learning at all: rank by dense, but move a
  document up if its normalised BM25 score exceeds τ while its dense score is
  mediocre. A one-parameter interpretable rule as a sanity check on whether
  learning is needed for the cases that matter.
'''))

C.append(code(r'''
from sklearn.ensemble import RandomForestClassifier

ROUTE_ALPHAS = {"dense": 1.0, "rrf_like": 0.5, "bm25_lean": 0.3}
route_cols = {k: curve_mat[:, int(np.abs(ALPHA_GRID - v).argmin())] for k, v in ROUTE_ALPHAS.items()}
route_stack = np.vstack([route_cols[k] for k in ROUTE_ALPHAS]).T
route_label = np.array(list(ROUTE_ALPHAS))[route_stack.argmax(axis=1)]

clf = RandomForestClassifier(n_estimators=300, max_depth=10, min_samples_leaf=5,
                             class_weight="balanced", random_state=SEED, n_jobs=-1)
proba = cross_val_predict(clf, X, route_label, cv=kf, method="predict_proba", n_jobs=1)
classes = np.array(sorted(set(route_label)))
pred_route = classes[proba.argmax(axis=1)]
conf = proba.max(axis=1)

router_ndcg = np.array([route_cols[pred_route[i]][i] for i in range(len(pred_route))])
print("Router accuracy: %.3f   (majority-class baseline %.3f)"
      % ((pred_route == route_label).mean(),
         pd.Series(route_label).value_counts(normalize=True).max()))

rows = []
for thr in np.round(np.arange(0.34, 1.001, 0.02), 3):
    act = conf >= thr
    sc = np.where(act & (pred_route != "dense"), router_ndcg, dense_scores)
    st = paired_bootstrap(sc, dense_scores)
    rows.append({"confidence_threshold": thr,
                 "coverage_deviated_from_dense": float((act & (pred_route != "dense")).mean()),
                 "ndcg10": float(sc.mean()),
                 "delta_vs_dense": st["mean_diff"],
                 "ci_low": st["ci_low"], "ci_high": st["ci_high"]})
risk_cov = pd.DataFrame(rows).round(4)
save_csv(risk_cov, "nb2_risk_coverage.csv")
best = risk_cov.loc[risk_cov["delta_vs_dense"].idxmax()]
print("\nBest point on the risk-coverage curve:")
print(best.to_string())
print("\n(If ci_low <= 0 at every threshold, selective deviation never reliably "
      "beats always-dense on these corpora.)")
'''))

C.append(code(r'''
# Figures for the paper.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 4.0))

# (a) mean alpha curve per dataset
for ds, g in curves.groupby("dataset"):
    m = np.vstack(g["curve"].apply(np.asarray).values).mean(axis=0)
    axes[0].plot(ALPHA_GRID, m, marker="o", ms=3, label=ds)
axes[0].set_xlabel(r"fusion weight $\alpha$ (1 = dense only)")
axes[0].set_ylabel("mean nDCG@10")
axes[0].set_title("(a) nDCG is nearly flat in " + r"$\alpha$" + " near the optimum")
axes[0].legend(fontsize=7); axes[0].grid(alpha=.3)

# (b) distribution of per-query curve range
axes[1].hist(curves["curve_range"], bins=40, color="#4C72B0")
axes[1].axvline(FLATNESS_EPS, color="crimson", ls="--",
                label=f"$\\epsilon$={FLATNESS_EPS}")
frac = float((curves["curve_range"] < FLATNESS_EPS).mean())
axes[1].set_xlabel(r"per-query $\max_\alpha$nDCG $-\ \min_\alpha$nDCG")
axes[1].set_ylabel("queries")
axes[1].set_title(f"(b) {frac*100:.0f}% of queries: " + r"$\alpha$" + " changes nothing")
axes[1].legend(fontsize=8)

# (c) headroom bars
lab = ["BM25", "RRF", "Dense", r"Fixed $\alpha^\star$", "Learned", "Oracle"]
learned_best = policy_df[policy_df.policy.str.startswith("Learned")]["ndcg10"].max()
val = [policy_df.set_index("policy").loc["BM25 (alpha=0)", "ndcg10"],
       policy_df.set_index("policy").loc["RRF (k=60)", "ndcg10"],
       policy_df.set_index("policy").loc["Dense (alpha=1)", "ndcg10"],
       policy_df.set_index("policy").loc[f"Fixed alpha*={alpha_fixed_global:.2f}", "ndcg10"],
       learned_best,
       policy_df.set_index("policy").loc["Oracle alpha (ceiling)", "ndcg10"]]
cols = ["#999", "#999", "#4C72B0", "#4C72B0", "#DD8452", "#55A868"]
axes[2].bar(lab, val, color=cols)
axes[2].set_ylabel("mean nDCG@10")
axes[2].set_ylim(min(val) * 0.9, max(val) * 1.03)
axes[2].set_title("(c) headroom exists, learning does not reach it")
axes[2].tick_params(axis="x", rotation=25, labelsize=8)

plt.tight_layout()
for ext in ("pdf", "png"):
    plt.savefig(ART / "results" / f"fig_alpha_headroom.{ext}", dpi=180, bbox_inches="tight")
print("saved fig_alpha_headroom.{pdf,png}")
plt.close()
'''))

C.append(md(r'''
## 6. Reading the output

The paper's retrieval claim should be written directly from `nb2_headroom.csv`
and `nb2_policy_comparison.csv`, in whichever of these forms the numbers support:

- **If oracle ≫ fixed but learned ≈ fixed:** per-query fusion weighting has real
  headroom that six cheap features cannot reach. Report the headroom, report the
  permutation test showing the features carry little signal about α\*, and frame
  the contribution as *quantifying an open problem* rather than solving it.
- **If oracle ≈ fixed:** per-query weighting is worth nothing on modern dense
  retrievers, full stop. That is a stronger and more useful result, because it
  tells the community to stop building this particular mechanism. The flatness
  histogram is then the central figure of the paper.

Either way the claim is now bounded by evidence, which is the thing TMLR asks
for and the thing the CIKM version did not have.
'''))

write_notebook("/home/user/cognisync02/tmlr/notebooks/NB2_alpha_headroom.ipynb", C,
               "oracle headroom + identifiability")
