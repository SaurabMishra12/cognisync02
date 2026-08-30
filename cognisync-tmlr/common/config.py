"""Global configuration: seeds, pinned model revisions, paths.

Every experiment script imports from here so that a single edit changes the whole
suite, and so that `logs/*.json` always records what was actually used.
"""
from __future__ import annotations

import os
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List

SEED = 42

# --------------------------------------------------------------------------------------
# Models. Revisions are pinned so a silent upstream update cannot change a published
# number. Look a revision up with `huggingface_hub.HfApi().model_info(name).sha`.
# --------------------------------------------------------------------------------------

DENSE_ENCODERS: Dict[str, Dict[str, str]] = {
    # The paper's encoder. Trained on MS MARCO (9,144,553 triplets), Code Search
    # (1,151,414 pairs) and SQuAD2.0 (87,599 pairs), among 27 sources. That membership is
    # the subject of exp_a/a2_contamination.py.
    "minilm": {
        "name": "sentence-transformers/all-MiniLM-L6-v2",
        "revision": "c9745ed1d9f207416be6d2e6f8de32d1f16199bf",
        "dim": "384",
    },
    # Capacity control: same training mixture, larger model. Isolates capacity from
    # contamination.
    "mpnet": {
        "name": "sentence-transformers/all-mpnet-base-v2",
        "revision": "main",
        "dim": "768",
    },
    # Different training mixture. If a gain survives here it is less likely to be a
    # membership artifact.
    "bge": {
        "name": "BAAI/bge-small-en-v1.5",
        "revision": "main",
        "dim": "384",
    },
}

CROSS_ENCODERS: Dict[str, Dict[str, str]] = {
    # The paper's reranker. Trained on MS MARCO by construction, which is why evaluating
    # it on MS MARCO is an in-domain measurement rather than a zero-shot one.
    "ms-marco": {
        "name": "cross-encoder/ms-marco-MiniLM-L-6-v2",
        "revision": "main",
        "kind": "cross-encoder",
    },
    # Provenance control for a2/a1. Different training data, comparable cost.
    "bge-reranker": {
        "name": "BAAI/bge-reranker-base",
        "revision": "main",
        "kind": "cross-encoder",
    },
}

GENERATORS: Dict[str, Dict[str, str]] = {
    # Matches the paper's local-first claim (Gemma-2B class, runs in 8-24 GB).
    "gemma2-2b": {"name": "google/gemma-2-2b-it", "load": "fp16"},
    "qwen2.5-3b": {"name": "Qwen/Qwen2.5-3B-Instruct", "load": "fp16"},
    "qwen2.5-7b": {"name": "Qwen/Qwen2.5-7B-Instruct", "load": "4bit"},
}

INJECTION_DETECTORS: Dict[str, Dict[str, str]] = {
    "deberta-pi-v2": {
        "name": "protectai/deberta-v3-base-prompt-injection-v2",
        "params_m": "184",
    },
    "prompt-guard": {
        "name": "meta-llama/Prompt-Guard-86M",
        "params_m": "86",
    },
}

# --------------------------------------------------------------------------------------
# Datasets
# --------------------------------------------------------------------------------------

# BEIR sets chosen for (a) zero-shot status relative to the encoders above and
# (b) fitting a single T4 session. Corpus/query counts are the published BEIR figures and
# are re-checked at load time; a mismatch means the download changed and is worth knowing.
BEIR_DATASETS: Dict[str, Dict[str, int]] = {
    "scifact": {"corpus": 5183, "queries": 300},
    "nfcorpus": {"corpus": 3633, "queries": 323},
    "arguana": {"corpus": 8674, "queries": 1406},
    "scidocs": {"corpus": 25657, "queries": 1000},
    "fiqa": {"corpus": 57638, "queries": 648},
    "trec-covid": {"corpus": 171332, "queries": 50},
    "webis-touche2020": {"corpus": 382545, "queries": 49},
}

# Datasets that appear in all-MiniLM-L6-v2's published training mixture. Used by
# exp_a/a2_contamination.py to split results into in-mixture and out-of-mixture groups.
# Source: the model card's "Training Data" table.
ENCODER_TRAINING_MEMBERSHIP: Dict[str, Dict[str, object]] = {
    "msmarco": {"in_mixture": True, "pairs": 9_144_553, "entry": "MS MARCO triplets"},
    "codesearchnet": {"in_mixture": True, "pairs": 1_151_414, "entry": "Code Search"},
    "squad": {"in_mixture": True, "pairs": 87_599, "entry": "SQuAD2.0"},
    "nq": {"in_mixture": True, "pairs": 100_231, "entry": "Natural Questions"},
    "quora": {"in_mixture": True, "pairs": 103_663, "entry": "Quora Question Triplets"},
    "sciq": {"in_mixture": False, "pairs": 0, "entry": None},
    "scifact": {"in_mixture": False, "pairs": 0, "entry": None},
    "nfcorpus": {"in_mixture": False, "pairs": 0, "entry": None},
    "arguana": {"in_mixture": False, "pairs": 0, "entry": None},
    "scidocs": {"in_mixture": False, "pairs": 0, "entry": None},
    "fiqa": {"in_mixture": False, "pairs": 0, "entry": None},
    "trec-covid": {"in_mixture": False, "pairs": 0, "entry": None},
    "webis-touche2020": {"in_mixture": False, "pairs": 0, "entry": None},
}

DATASET_REVISIONS: Dict[str, str] = {
    "microsoft/ms_marco": "a47ee7aae8d7d466ba15f9f0bfac3b3681087b3a",
    "code-search-net/code_search_net": "bd0cf265c1ad74dcbcedbabb9e6ebc98a1a7fbe4",
    "allenai/sciq": "2c94ad3e1aafab77146f384e23536f97a4849815",
    "rajpurkar/squad": "7b6d24c440a36b6815f21b70d25016731768db1f",
    "deepset/prompt-injections": "main",
}

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------

ROOT = Path(os.environ.get("COGNISYNC_ROOT", "./cognisync_out")).resolve()
RESULTS_DIR = ROOT / "results"
LOGS_DIR = ROOT / "logs"
CACHE_DIR = Path(os.environ.get("COGNISYNC_CACHE", ROOT / "cache")).resolve()
FIGURES_DIR = ROOT / "figures"
DATA_DIR = Path(os.environ.get("COGNISYNC_DATA", ROOT / "data")).resolve()

for _d in (RESULTS_DIR, LOGS_DIR, CACHE_DIR, FIGURES_DIR, DATA_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------------------
# Retrieval defaults
# --------------------------------------------------------------------------------------

@dataclass
class RetrievalConfig:
    """Every knob the paper needs to report, in one place."""

    first_stage_depth: int = 100          # candidates carried out of the first stage
    rerank_depth: int = 10                # <-- the number reviewer 2 asked for and the
                                          #     CIKM code hardcoded without reporting
    eval_k: int = 10
    recall_ks: tuple = (1, 5, 10, 100)
    rrf_k: int = 60
    fixed_alpha: float = 0.5

    # The undisclosed override found in CogniSync_v3_strong.ipynb cell 6. Off by default
    # here; a3_alpha_decomposition.py toggles it explicitly so its effect is measurable
    # rather than baked in.
    use_dense_fallback: bool = False
    fallback_dmax_threshold: float = 0.85
    fallback_bm25_cv_threshold: float = 0.10

    alpha_model_trees: int = 50
    alpha_model_depth: int = 5
    alpha_grid_steps: int = 11
    alpha_tuning_queries: int = 300

    encoder_key: str = "minilm"
    reranker_key: str = "ms-marco"
    batch_size: int = 256

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DefenseConfig:
    """Filter configuration. `centroid_source` is the fix for audit finding 1.4."""

    # "oracle" reproduces the CIKM setup (centroid fit on the query's own clean pool).
    # "holdout" is the deployable one. b1 compares them.
    centroid_source: str = "holdout"
    holdout_clean_docs: int = 2000
    classifier_threshold: float = 0.5
    goal_redirection_threshold: float = 0.30
    imperative_terms: List[str] = field(
        default_factory=lambda: ["ignore", "reveal", "execute", "forget", "bypass", "output"]
    )
    # The CIKM filter trained on 6 clean + 6 poison strings. Kept as a condition so the
    # effect of training-set size is measurable rather than assumed.
    train_regime: str = "public"   # "six_templates" | "public" | "public_plus_templates"
    poison_base_rate: float = 1e-3

    def to_dict(self) -> dict:
        return asdict(self)


def set_all_seeds(seed: int = SEED) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
