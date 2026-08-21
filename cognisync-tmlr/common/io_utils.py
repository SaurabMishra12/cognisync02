"""Result writing, config logging, and resumable checkpoints.

Reviewer 2 listed six details as underspecified in the CIKM PDF. The point of this module
is that they cannot be underspecified again: every run writes its full resolved config
next to its results, so the log file *is* the reproducibility appendix.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import time
from dataclasses import is_dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from .config import LOGS_DIR, RESULTS_DIR, CACHE_DIR


def _jsonable(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, Path):
        return str(obj)
    return obj


def environment_fingerprint() -> Dict[str, Any]:
    """Package versions, hardware, git commit. Cheap, and it settles arguments later."""
    info: Dict[str, Any] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    for pkg in (
        "numpy", "pandas", "scipy", "sklearn", "torch", "transformers",
        "sentence_transformers", "faiss", "datasets", "rank_bm25", "bm25s", "beir",
    ):
        try:
            mod = __import__(pkg)
            info[f"version.{pkg}"] = getattr(mod, "__version__", "unknown")
        except Exception:
            info[f"version.{pkg}"] = None
    try:
        import torch

        info["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["gpu"] = torch.cuda.get_device_name(0)
            info["gpu_mem_gb"] = round(
                torch.cuda.get_device_properties(0).total_memory / 1e9, 1
            )
    except Exception:
        info["cuda_available"] = None
    try:
        info["git_commit"] = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        info["git_commit"] = None
    return info


def write_result(
    name: str,
    frame: pd.DataFrame,
    config: Optional[Dict[str, Any]] = None,
    per_query: Optional[pd.DataFrame] = None,
) -> Dict[str, Path]:
    """Write aggregate CSV, optional per-query CSV, and the config log.

    Per-query output is not optional in spirit. Every significance claim in the paper
    should be recomputable from the raw per-query file without re-running retrieval.
    """
    paths: Dict[str, Path] = {}

    agg_path = RESULTS_DIR / f"{name}.csv"
    frame.to_csv(agg_path, index=False)
    paths["aggregate"] = agg_path

    if per_query is not None and len(per_query):
        pq_path = RESULTS_DIR / f"{name}__per_query.csv"
        per_query.to_csv(pq_path, index=False)
        paths["per_query"] = pq_path

    log = {"experiment": name, "environment": environment_fingerprint()}
    if config:
        log["config"] = _jsonable(config)
    log_path = LOGS_DIR / f"{name}.json"
    log_path.write_text(json.dumps(log, indent=2))
    paths["log"] = log_path

    print(f"[write_result] {name}: " + ", ".join(f"{k}={v}" for k, v in paths.items()))
    return paths


class Checkpoint:
    """Resume support for long sweeps.

    Kaggle sessions die. A sweep over 7 BEIR datasets x 6 first stages x 3 rerankers is
    126 cells; losing all of them to a timeout at cell 120 is avoidable. Each completed
    cell is appended to a JSONL file keyed by a config hash.
    """

    def __init__(self, name: str):
        self.path = CACHE_DIR / f"{name}.checkpoint.jsonl"
        self._done: Dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                    self._done[rec["_key"]] = rec
                except json.JSONDecodeError:
                    continue
            print(f"[checkpoint] {name}: resuming with {len(self._done)} completed cells")

    @staticmethod
    def key(**parts: Any) -> str:
        blob = json.dumps(_jsonable(parts), sort_keys=True)
        return hashlib.sha1(blob.encode()).hexdigest()[:16]

    def has(self, key: str) -> bool:
        return key in self._done

    def get(self, key: str) -> Optional[dict]:
        return self._done.get(key)

    def put(self, key: str, record: dict) -> None:
        record = dict(record)
        record["_key"] = key
        self._done[key] = record
        with self.path.open("a") as fh:
            fh.write(json.dumps(_jsonable(record)) + "\n")

    def all_records(self) -> pd.DataFrame:
        rows = [{k: v for k, v in r.items() if k != "_key"} for r in self._done.values()]
        return pd.DataFrame(rows)


def cache_path(*parts: str, suffix: str = ".npy") -> Path:
    """Deterministic cache path from a tuple of identifiers."""
    stem = "__".join(str(p).replace("/", "_") for p in parts)
    if len(stem) > 120:
        stem = stem[:100] + "_" + hashlib.sha1(stem.encode()).hexdigest()[:12]
    return CACHE_DIR / f"{stem}{suffix}"
