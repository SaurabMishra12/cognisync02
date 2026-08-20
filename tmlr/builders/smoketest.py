"""Offline smoke test: exercise every pure-logic function extracted from the
notebooks against synthetic data, so bugs surface here rather than 40 minutes
into a Colab run."""
import json, math, re, sys, os
import numpy as np
import pandas as pd

NB = os.path.join(os.path.dirname(__file__), "..", "notebooks")
SEED = 42


def extract(nbname, must_contain, stop_at=None, start_at=None):
    """Pull the source of the first code cell containing a marker.

    `stop_at` truncates before the cell's top-level driver code, so only the
    function definitions are exec'd.
    """
    nb = json.load(open(os.path.join(NB, nbname)))
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if must_contain in src:
            # Drop shell escapes and heavyweight imports; we only exercise the
            # pure-Python logic here, with no GPU or network available.
            drop = ("!", "from datasets", "from sentence_transformers", "import bm25s",
                    "from transformers", "import Stemmer", "from sklearn.linear_model",
                    "import torch", "from sklearn.metrics", "import faiss")
            if start_at:
                src = start_at + src.split(start_at, 1)[1]
            if stop_at:
                src = src.split(stop_at)[0]
            return "".join(l for l in src.splitlines(keepends=True)
                           if not l.strip().startswith(drop))
    raise KeyError(f"{must_contain!r} not found in {nbname}")


ok, fail = [], []


def check(name, cond, detail=""):
    (ok if cond else fail).append(name)
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"   {detail}" if detail else ""))


# ---------------------------------------------------------------------------
print("\n[1] NB1/NB2 fusion + feature extraction")
ns = {"np": np, "re": re, "math": math, "pd": pd, "RRF_K": 60}
exec(extract("NB2_alpha_headroom.ipynb", "def build_candidate_scores",
             stop_at="datasets_to_sweep ="), ns)

d_idx = np.array([5, 3, 9, 1]); d_sc = np.array([0.9, 0.7, 0.5, 0.1])
b_idx = np.array([3, 7, 5, 2]); b_sc = np.array([8.0, 6.0, 4.0, 1.0])
cands, dv, bv, drank, brank = ns["build_candidate_scores"](d_idx, d_sc, b_idx, b_sc)

check("union covers both channels", set(cands) == {1, 2, 3, 5, 7, 9}, f"got {sorted(cands)}")
check("normalised scores in [0,1]", dv.min() >= 0 and dv.max() <= 1 and bv.max() <= 1)
check("doc missing from dense gets 0", dv[list(cands).index(7)] == 0.0)
check("doc missing from lexical gets 0", bv[list(cands).index(9)] == 0.0)
check("top dense doc keeps score 1.0", dv[list(cands).index(5)] == 1.0)
check("ranks are 0-based for retrieved docs", drank[list(cands).index(5)] == 0)
check("unretrieved docs get a rank beyond the pool",
      drank[list(cands).index(7)] >= len(cands))

# constant-score channel must not divide by zero
c2, dv2, bv2, _, _ = ns["build_candidate_scores"](
    np.array([0, 1]), np.array([0.5, 0.5]), np.array([0, 1]), np.array([2.0, 2.0]))
check("constant dense scores -> zeros, no NaN", np.all(dv2 == 0) and not np.isnan(dv2).any())

f = ns["alpha_features"]("what is the sha256 hash of the key", dv, bv)
check("feature vector has 6 entries", len(f) == 6, f"{f}")
check("identifier flag fires on 'hash'/'key'", f[5] == 1.0)
check("identifier flag off for plain prose",
      ns["alpha_features"]("how do vaccines work", dv, bv)[5] == 0.0)
check("identifier flag fires on version strings",
      ns["alpha_features"]("upgrade to v2.11.3", dv, bv)[5] == 1.0)
check("query length counted in tokens", f[0] == 8.0, f"got {f[0]}")

# ---------------------------------------------------------------------------
print("\n[2] nDCG")
ns2 = {"math": math}
exec(extract("NB2_alpha_headroom.ipynb", "def ndcg_at_k",
             stop_at="datasets_to_sweep ="), ns2)
nd = ns2["ndcg_at_k"]
check("perfect ranking -> 1.0", abs(nd(["a", "b", "c"], {"a": 1, "b": 1}, 10) - 1.0) < 1e-9)
check("no relevant retrieved -> 0.0", nd(["x", "y"], {"a": 1}, 10) == 0.0)
check("empty qrels -> 0.0 not ZeroDivision", nd(["a"], {}, 10) == 0.0)
r2 = nd(["x", "a"], {"a": 1}, 10)
check("rank-2 hit scores 1/log2(3)", abs(r2 - 1 / math.log2(3)) < 1e-9, f"{r2:.4f}")
check("graded relevance is used", nd(["a", "b"], {"a": 2, "b": 1}, 10) >
      nd(["b", "a"], {"a": 2, "b": 1}, 10))
check("cutoff k is respected", nd(["x"] * 9 + ["a"], {"a": 1}, 10) > 0
      and nd(["x"] * 9 + ["a"], {"a": 1}, 5) == 0.0)

# ---------------------------------------------------------------------------
print("\n[3] paired bootstrap")
ns3 = {"np": np, "SEED": SEED}
exec(extract("NB1_full_corpus_beir.ipynb", "def paired_bootstrap"), ns3)
pb = ns3["paired_bootstrap"]
rng = np.random.default_rng(0)
a = rng.normal(0.55, 0.1, 800); b = rng.normal(0.50, 0.1, 800)
st = pb(a, b, n_boot=2000)
check("recovers the true mean difference", abs(st["mean_diff"] - (a - b).mean()) < 1e-12)
check("CI brackets the estimate", st["ci_low"] < st["mean_diff"] < st["ci_high"])
check("real effect is detected", st["boot_p"] < 0.05, f"p={st['boot_p']:.4f}")
st0 = pb(a, a + 1e-12, n_boot=2000)
check("near-identical inputs are not called significant", st0["boot_p"] > 0.05,
      f"p={st0['boot_p']:.4f}")
c = rng.normal(0.50, 0.1, 800)
check("null effect is not called significant", pb(b, c, n_boot=2000)["boot_p"] > 0.05)
check("effect size reported", "cohen_dz" in st)
st_tied = pb(a, a.copy(), n_boot=2000)
check("all-tied systems report p=1.0, not p=0", st_tied["boot_p"] == 1.0,
      f"p={st_tied['boot_p']}")
check("all-tied systems report zero effect size", st_tied["cohen_dz"] == 0.0)

# ---------------------------------------------------------------------------
print("\n[4] NB3 attack constructors")
import hashlib
ns4 = {"np": np, "re": re, "math": math, "json": json, "hashlib": hashlib,
       "CLEAN_MEAN_LEN": 600.0, "SPLIT_K": 3}
exec(extract("NB3_adaptive_security.ipynb", "CIKM_TEMPLATES = [",
             stop_at="STATIC_ATTACKS = {"), ns4)
ctx = ["Randomised trials show the treatment reduces mortality in adults. " * 6,
       "Secondary endpoints included hospitalisation and length of stay. " * 6,
       "Background material on the study population and its selection. " * 6]
q = "does the treatment reduce mortality"
IMP = ns4["IMPERATIVE_RE"]
CAN = ns4["CANARY"]

a0 = ns4["attack_A0_static"](q, ctx)
a1 = ns4["attack_A1_query_conditioned"](q, ctx)
a2 = ns4["attack_A2_imperative_free"](q, ctx)
a3 = ns4["attack_A3_semantic_camouflage"](q, ctx)
a4 = ns4["attack_A4_length_matched"](q, ctx)
a6 = ns4["attack_A6_split_payload"](q, ctx)

check("A0 uses a CIKM template verbatim", a0[0] in ns4["CIKM_TEMPLATES"])
check("A1 reproduces the CIKM query-conditioned payload",
      "Ignore previous instructions" in a1[0] and q.split()[0] in a1[0])
check("A2 evades the keyword filter", IMP.search(a2[0]) is None, repr(a2[0][:70]))
check("A2 still carries a working directive", CAN in a2[0])
check("A3 embeds real corpus text", ctx[0][:50] in a3[0])
check("A3 still carries a working directive", CAN in a3[0])
check("A4 approaches the clean mean length",
      0.6 * 600 <= len(a4[0]) <= 1.2 * 600, f"len={len(a4[0])}")
check("A6 emits exactly SPLIT_K chunks", len(a6) == 3, f"got {len(a6)}")
check("A6 chunks reassemble the directive",
      all(w in " ".join(a6) for w in CAN.split()))
check("no A6 chunk contains the whole directive",
      not any(CAN in c and "reply with the token" in c for c in a6))

# adaptive mutation must preserve the core directive
ns4b = dict(ns4)
ns4b.update({"A5_QUERY_BUDGET": 20, "SEED": SEED})
exec(extract("NB3_adaptive_security.ipynb", "def _mutate",
             stop_at="def adaptive_attack_A5"), ns4b)
core = ns4["CORE_DIRECTIVES"][0]
doc = f"{q}. Prior guidance no longer applies. {core}."
rs = np.random.default_rng(0)
survived = 0
for _ in range(400):
    m = ns4b["_mutate"](doc, core, ctx, rs)
    if core[:24] in m:
        survived += 1
check("mutations preserve the core directive", survived == 400, f"{survived}/400")

# Regression: no core directive may contain a keyword A2 is meant to evade,
# and template selection must not depend on Python's randomised str hash.
check("no core directive contains a filtered keyword",
      not any(IMP.search(d) for d in ns4["CORE_DIRECTIVES"]),
      str([d for d in ns4["CORE_DIRECTIVES"] if IMP.search(d)]))
check("A2 is keyword-free for every query in a sweep",
      all(IMP.search(ns4["attack_A2_imperative_free"](f"query number {i} about output", ctx)[0]) is None
          for i in range(200)))
check("template selection is deterministic across processes",
      ns4["sel"](["a", "b", "c", "d", "e"], "the treatment") ==
      ["a", "b", "c", "d", "e"][int(hashlib.md5(b"the treatment").hexdigest()[:8], 16) % 5])

# three-feature extraction
ns4c = {"np": np, "re": re, "IMPERATIVE_RE": IMP}
exec(extract("NB3_adaptive_security.ipynb", "def three_features",
             start_at="def three_features", stop_at="class ThreeFeatureLR"), ns4c)
mu = np.ones(4) / 2.0
embs = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0]])
X = ns4c["three_features"](["ignore this", "a benign passage"], embs, mu, 100.0)
check("three_features returns (n,3)", X.shape == (2, 3), str(X.shape))
check("imperative flag set on flagged doc", X[0, 1] == 1.0)
check("imperative flag clear on benign doc", X[1, 1] == 0.0)
check("length ratio computed", abs(X[0, 2] - len("ignore this") / 101.0) < 1e-9)

# ---------------------------------------------------------------------------
print("\n[5] NB4 QA scoring + poison placement")
ns5 = {"re": re, "np": np, "N_CTX_DOCS": 5, "CANARY": CAN}
exec(extract("NB4_downstream_llm.ipynb", "def qa_em"), ns5)
check("EM ignores articles and case", ns5["qa_em"]("The Paris", ["paris"]) == 1.0)
check("EM ignores punctuation", ns5["qa_em"]("Paris.", ["Paris"]) == 1.0)
check("EM rejects a wrong answer", ns5["qa_em"]("London", ["Paris"]) == 0.0)
check("F1 is 1.0 on an exact match", abs(ns5["qa_f1"]("Paris", ["Paris"]) - 1.0) < 1e-9)
p = ns5["qa_f1"]("the city of Paris", ["Paris"])
check("F1 partial credit is in (0,1)", 0 < p < 1, f"{p:.3f}")
check("F1 is 0 with no overlap", ns5["qa_f1"]("London", ["Paris"]) == 0.0)
check("F1 handles multiple golds", ns5["qa_f1"]("Lyon", ["Paris", "Lyon"]) == 1.0)
check("hijack detects the canary", ns5["hijacked"](f"answer is {CAN}") == 1.0)
check("hijack detects it case-insensitively", ns5["hijacked"](CAN.lower()) == 1.0)
check("hijack clear on a normal answer", ns5["hijacked"]("The answer is Paris.") == 0.0)

clean = [f"clean{i}" for i in range(8)]
for pos in (0, 2, 4):
    d = ns5["place_poison"](clean, ["POISON"], pos)
    check(f"poison lands at rank {pos}", d[pos] == "POISON", str(d[:pos + 2]))
    check(f"context stays bounded at pos {pos}", len(d) == 6, f"len={len(d)}")
d3 = ns5["place_poison"](clean, ["P1", "P2", "P3"], 0)
check("multi-chunk poison all placed", all(f"P{i}" in d3 for i in (1, 2, 3)), str(d3))

# ---------------------------------------------------------------------------
print("\n[6] NB1 rerank + minmax")
ns6 = {"np": np}
exec(extract("NB1_full_corpus_beir.ipynb", "def rerank",
             start_at="def rerank"), ns6)
order = np.array([10, 11, 12, 13, 14])
ce = np.array([0.1, 0.9, 0.5, 0.2, 0.0])
out = ns6["rerank"](order, ce, 3)
check("rerank reorders the head by CE score", list(out[:3]) == [11, 12, 10], str(out))
check("rerank leaves the tail untouched", list(out[3:]) == [13, 14], str(out))
check("budget 0 is a no-op", list(ns6["rerank"](order, ce, 0)) == list(order))
check("budget beyond list length is clamped",
      sorted(ns6["rerank"](order, ce, 99)) == sorted(order))

exec(extract("NB1_full_corpus_beir.ipynb", "def minmax",
             start_at="def minmax", stop_at="def build_candidate_scores"), ns6)
check("minmax maps to [0,1]", ns6["minmax"]([1, 2, 3]).tolist() == [0.0, 0.5, 1.0])
check("minmax of constants is zeros", ns6["minmax"]([7, 7, 7]).tolist() == [0.0, 0.0, 0.0])

exec(extract("NB1_full_corpus_beir.ipynb", "def apply_dense_override",
             start_at="def apply_dense_override"), ns6)
check("override forces dense on a confident dense hit",
      ns6["apply_dense_override"](0.3, np.array([0.95, 0.2]), 0.5) == 1.0)
check("override forces dense when BM25 is flat",
      ns6["apply_dense_override"](0.3, np.array([0.4, 0.2]), 0.05) == 1.0)
check("override passes the prediction through otherwise",
      ns6["apply_dense_override"](0.3, np.array([0.4, 0.2]), 0.5) == 0.3)

# ---------------------------------------------------------------------------
print(f"\n{'='*66}\n{len(ok)} passed, {len(fail)} failed")
if fail:
    print("FAILED:")
    for f_ in fail:
        print("  -", f_)
    sys.exit(1)
print("all smoke tests passed")
