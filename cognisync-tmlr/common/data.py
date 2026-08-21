"""Dataset loading.

BEIR first, because the whole point of Track A is full-corpus evaluation against a
standard, publicly checkable protocol. Two loaders are provided: the `beir` package
(canonical qrels handling) and a Hugging Face fallback for when the Zenodo mirror is
unreachable, which happens often enough on Kaggle to be worth the extra code.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import BEIR_DATASETS, DATA_DIR, DATASET_REVISIONS, SEED

Corpus = Dict[str, str]                  # doc_id -> text
Queries = Dict[str, str]                 # query_id -> text
Qrels = Dict[str, Dict[str, int]]        # query_id -> doc_id -> grade


def _join_title_text(title: str, text: str) -> str:
    title = (title or "").strip()
    text = (text or "").strip()
    return f"{title} {text}".strip() if title else text


def load_beir(name: str, split: str = "test", data_dir: Optional[Path] = None) -> Tuple[Corpus, Queries, Qrels]:
    """Load a BEIR dataset, preferring the official package."""
    data_dir = Path(data_dir or DATA_DIR) / "beir"
    data_dir.mkdir(parents=True, exist_ok=True)

    try:
        from beir import util
        from beir.datasets.data_loader import GenericDataLoader

        url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{name}.zip"
        path = data_dir / name
        if not path.exists():
            path = Path(util.download_and_unzip(url, str(data_dir)))
        raw_corpus, queries, qrels = GenericDataLoader(data_folder=str(path)).load(split=split)
        corpus = {k: _join_title_text(v.get("title", ""), v.get("text", "")) for k, v in raw_corpus.items()}
        return corpus, queries, qrels
    except Exception as exc:  # noqa: BLE001
        print(f"[data] beir package path failed for {name} ({type(exc).__name__}: {exc}); trying Hugging Face")

    return _load_beir_hf(name, split)


def _load_beir_hf(name: str, split: str = "test") -> Tuple[Corpus, Queries, Qrels]:
    """Fallback loader using the BeIR/* mirrors on the Hugging Face Hub."""
    from datasets import load_dataset

    corpus_ds = load_dataset(f"BeIR/{name}", "corpus", split="corpus")
    queries_ds = load_dataset(f"BeIR/{name}", "queries", split="queries")
    qrels_ds = load_dataset(f"BeIR/{name}-qrels", split=split)

    corpus = {
        str(r["_id"]): _join_title_text(r.get("title", ""), r.get("text", "")) for r in corpus_ds
    }
    queries = {str(r["_id"]): r["text"] for r in queries_ds}

    qrels: Qrels = {}
    for r in qrels_ds:
        qid, did, score = str(r["query-id"]), str(r["corpus-id"]), int(r["score"])
        qrels.setdefault(qid, {})[did] = score

    queries = {qid: text for qid, text in queries.items() if qid in qrels}
    return corpus, queries, qrels


def check_expected_sizes(name: str, corpus: Corpus, queries: Queries) -> Dict[str, object]:
    """Compare against the published BEIR counts and report, rather than assert.

    A mismatch usually means the mirror changed, not that anything is wrong. It belongs
    in the log either way.
    """
    expected = BEIR_DATASETS.get(name, {})
    report = {
        "dataset": name,
        "corpus_actual": len(corpus),
        "corpus_expected": expected.get("corpus"),
        "queries_actual": len(queries),
        "queries_expected": expected.get("queries"),
    }
    for field in ("corpus", "queries"):
        exp, act = expected.get(field), report[f"{field}_actual"]
        if exp and abs(act - exp) / exp > 0.02:
            print(f"[data] {name}: {field} count {act} differs from published {exp} by >2%")
    return report


# --------------------------------------------------------------------------------------
# MS MARCO, for the contamination contrast
# --------------------------------------------------------------------------------------

def load_msmarco_passage_corpus(n_passages: int = 100_000, seed: int = SEED) -> Tuple[List[str], List[str]]:
    """Sample the Tevatron passage corpus. Returns (doc_ids, texts)."""
    from datasets import load_dataset

    ds = load_dataset("Tevatron/msmarco-passage-corpus", split="train")
    ds = ds.shuffle(seed=seed).select(range(min(n_passages, len(ds))))
    return [str(d) for d in ds["docid"]], list(ds["text"])


def load_msmarco_queries(split: str, n_queries: int = 500, seed: int = SEED) -> List[dict]:
    """Load MS MARCO queries with their positive passages.

    `split` is "train" or "dev". The contrast between them is the contamination
    measurement: all-MiniLM-L6-v2 was trained on 9.14M MS MARCO triplets drawn from the
    train split, so train-split queries are effectively seen data. The CIKM full-corpus
    experiment used `split="train"`, which is why its MRR@10 was 0.92.
    """
    from datasets import load_dataset

    hf_split = "train" if split == "train" else "dev"
    ds = load_dataset("Tevatron/msmarco-passage", split=hf_split)
    ds = ds.shuffle(seed=seed).select(range(min(n_queries * 3, len(ds))))

    out: List[dict] = []
    for row in ds:
        positives = row.get("positive_passages") or []
        if not positives:
            continue
        out.append(
            {
                "query_id": str(row.get("query_id", len(out))),
                "query": row["query"],
                "positive_docids": [str(p["docid"]) for p in positives],
                "positive_texts": [p["text"] for p in positives],
            }
        )
        if len(out) >= n_queries:
            break
    return out


def build_index_with_guaranteed_positives(
    base_ids: List[str], base_texts: List[str], query_records: List[dict]
) -> Tuple[List[str], List[str], Qrels]:
    """Append each query's positives to the corpus if absent, and build qrels.

    This mirrors the CIKM protocol so the contamination contrast is measured under the
    paper's own conditions. Note the guarantee itself inflates absolute numbers: a
    positive that is present by construction cannot be missing from the corpus, which is
    not true of real retrieval. Worth a sentence in the paper.
    """
    ids, texts = list(base_ids), list(base_texts)
    present = {d: i for i, d in enumerate(ids)}
    qrels: Qrels = {}

    for rec in query_records:
        judged: Dict[str, int] = {}
        for did, text in zip(rec["positive_docids"], rec["positive_texts"]):
            if did not in present:
                present[did] = len(ids)
                ids.append(did)
                texts.append(text)
            judged[did] = 1
        if judged:
            qrels[rec["query_id"]] = judged

    return ids, texts, qrels


# --------------------------------------------------------------------------------------
# The four CIKM benchmarks, kept so old and new protocols can be compared directly
# --------------------------------------------------------------------------------------

def load_cikm_candidate_pool_benchmark(dataset: str, limit: int = 5000, seed: int = SEED) -> List[dict]:
    """Reproduce the CIKM candidate-pool format: per-query pools with local indices.

    Kept because Track A's argument is a comparison between protocols, and the comparison
    needs the old protocol run under the same code as the new one.
    """
    from datasets import load_dataset

    def rev(key: str) -> Optional[str]:
        r = DATASET_REVISIONS.get(key)
        return None if r in (None, "main") else r

    out: List[dict] = []

    if dataset == "msmarco":
        ds = load_dataset("microsoft/ms_marco", "v1.1", split="validation", revision=rev("microsoft/ms_marco"))
        ds = ds.shuffle(seed=seed)
        for row in ds:
            passages = row["passages"]["passage_text"]
            selected = row["passages"]["is_selected"]
            docs, seen = [], set()
            for p in passages:
                if p and p not in seen:
                    seen.add(p)
                    docs.append(p)
            rel = [docs.index(passages[i]) for i, s in enumerate(selected) if s == 1 and passages[i] in docs]
            if row["query"] and docs and rel:
                out.append({"query": row["query"], "documents": docs, "relevant_indices": sorted(set(rel))})
            if len(out) >= limit:
                break

    elif dataset == "sciq":
        ds = load_dataset("allenai/sciq", split="train", revision=rev("allenai/sciq")).shuffle(seed=seed)
        supports = [r["support"] for r in ds if r.get("support")]
        for i, row in enumerate(ds):
            if not row.get("support"):
                continue
            distractors = [supports[(i + j + 1) % len(supports)] for j in range(9)]
            docs = [row["support"]] + distractors
            out.append({"query": row["question"], "documents": docs, "relevant_indices": [0]})
            if len(out) >= limit:
                break

    elif dataset == "squad":
        ds = load_dataset("rajpurkar/squad", split="validation", revision=rev("rajpurkar/squad")).shuffle(seed=seed)
        contexts = list({r["context"] for r in ds})
        for i, row in enumerate(ds):
            distractors = [contexts[(i + j + 1) % len(contexts)] for j in range(9)]
            docs = [row["context"]] + distractors
            out.append({"query": row["question"], "documents": docs, "relevant_indices": [0]})
            if len(out) >= limit:
                break

    elif dataset == "codesearchnet":
        ds = load_dataset(
            "code-search-net/code_search_net", "python", split="test",
            revision=rev("code-search-net/code_search_net"), trust_remote_code=True,
        ).shuffle(seed=seed)
        codes = [r["func_code_string"] for r in ds]
        for i, row in enumerate(ds):
            doc = row["func_documentation_string"]
            if not doc or not row["func_code_string"]:
                continue
            distractors = [codes[(i + j + 1) % len(codes)] for j in range(9)]
            docs = [row["func_code_string"]] + distractors
            out.append({"query": doc, "documents": docs, "relevant_indices": [0]})
            if len(out) >= limit:
                break

    else:
        raise ValueError(f"unknown dataset {dataset!r}")

    return out


def load_prompt_injection_corpus(name: str = "deepset") -> Tuple[List[str], List[int]]:
    """Return (texts, labels) with 1 = injection.

    `deepset` is the set the CIKM paper used. `jailbreak` is a second, larger and
    structurally different distribution, used for the transfer matrix in b4.
    """
    from datasets import load_dataset

    if name == "deepset":
        ds = load_dataset("deepset/prompt-injections", split="train")
        return list(ds["text"]), [int(x) for x in ds["label"]]

    if name == "jailbreak":
        ds = load_dataset("jackhhao/jailbreak-classification", split="train")
        texts = list(ds["prompt"])
        labels = [1 if str(t).strip().lower() == "jailbreak" else 0 for t in ds["type"]]
        return texts, labels

    raise ValueError(f"unknown injection corpus {name!r}")


def load_longmemeval(variant: str = "s", data_dir: Optional[Path] = None) -> List[dict]:
    """Load LongMemEval.

    `variant` is "s" (~40 sessions per instance), "m" (~500 sessions), or "oracle".
    Files come from the `xiaowu0162/longmemeval-cleaned` dataset repository. The 30
    abstention instances (question_id ending in `_abs`) are kept here and filtered at
    evaluation time, matching the benchmark authors' protocol.
    """
    data_dir = Path(data_dir or DATA_DIR) / "longmemeval"
    data_dir.mkdir(parents=True, exist_ok=True)
    fname = f"longmemeval_{variant}.json"
    local = data_dir / fname

    if not local.exists():
        from huggingface_hub import hf_hub_download

        downloaded = hf_hub_download(
            repo_id="xiaowu0162/longmemeval-cleaned",
            filename=fname,
            repo_type="dataset",
            local_dir=str(data_dir),
        )
        local = Path(downloaded)

    with local.open() as fh:
        return json.load(fh)
