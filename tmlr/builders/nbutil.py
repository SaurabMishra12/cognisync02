"""Shared helpers for building the TMLR experiment notebooks."""
import json
import os


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.strip("\n").splitlines(keepends=True),
    }


def write_notebook(path, cells, title=""):
    nb = {
        "cells": cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": [], "gpuType": "T4", "toc_visible": True, "name": os.path.basename(path)},
            "kernelspec": {"display_name": "Python 3", "name": "python3", "language": "python"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(nb, f, indent=1)
    n_code = sum(1 for c in cells if c["cell_type"] == "code")
    print(f"wrote {path}  ({len(cells)} cells, {n_code} code)  {title}")


# ---------------------------------------------------------------------------
# Reusable source blocks shared across notebooks (kept as strings so each
# notebook stays fully self-contained and independently runnable in Colab).
# ---------------------------------------------------------------------------

ENV_BLOCK = '''
import os, sys, json, math, time, random, hashlib, re, gc, warnings, shutil, glob, zipfile, io
from pathlib import Path
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

SEED = 42
random.seed(SEED); np.random.seed(SEED)

# torch is required by the experiment notebooks but not by the reporting one,
# so a missing install degrades to a clear message rather than a traceback.
try:
    import torch
    torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    if DEVICE == "cuda":
        props = torch.cuda.get_device_properties(0)
        print(f"GPU: {props.name} | {props.total_memory/1e9:.1f} GB | "
              f"n_gpus={torch.cuda.device_count()}")
    else:
        print("WARNING: no GPU detected. Everything will run but ~10-20x slower.")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("torch not installed (fine for the reporting notebook, required for the rest).")

# Artifact directory. On Kaggle write to /kaggle/working so results persist in
# the version output; on Colab mount Drive if you want results to survive a
# disconnect.
if Path("/kaggle/working").exists():
    ART = Path("/kaggle/working/cognisync_tmlr")
elif Path("/content/drive/MyDrive/cognisync_tmlr").exists():
    ART = Path("/content/drive/MyDrive/cognisync_tmlr")
elif Path("/content/drive/MyDrive").exists():
    ART = Path("/content/drive/MyDrive/cognisync_tmlr")
else:
    ART = Path("./cognisync_tmlr").resolve()

(ART / "results").mkdir(parents=True, exist_ok=True)
(ART / "cache").mkdir(parents=True, exist_ok=True)


def discover_artifacts():
    """Universal artifact finder: searches /kaggle/input, /kaggle/working, /content,
    parent folders, and all subdirectories for uploaded .zip archives or raw result files,
    extracting/copying them directly into ART / 'results'."""
    res_dir = ART / "results"
    res_dir.mkdir(parents=True, exist_ok=True)
    
    search_dirs = [
        Path("/kaggle/input"), Path("/kaggle/working"),
        Path("/content"), Path("/content/drive/MyDrive"),
        Path("."), Path(".."), Path("../.."),
        Path("tmlr"), Path("../tmlr"), Path("../../tmlr"),
        Path("cognisync_tmlr"), Path("../cognisync_tmlr"), Path("../../cognisync_tmlr"),
        Path("results"), Path("../results"), Path("../../results"),
        Path("tmlr/results"), Path("../tmlr/results"), Path("../../tmlr/results"),
    ]

    seen = set()
    for sdir in search_dirs:
        try:
            if not sdir.exists():
                continue
            resolved = sdir.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
        except Exception:
            continue

        # 1. Search for any .zip files
        for zpath in sdir.glob("*.zip"):
            try:
                with zipfile.ZipFile(zpath, "r") as zf:
                    extracted = 0
                    for info in zf.infolist():
                        if info.is_dir():
                            continue
                        fname = Path(info.filename).name
                        if (fname.startswith(("nb", "fig_", "beir")) or fname.endswith((".parquet", ".csv", ".json", ".tex", ".pdf", ".png"))):
                            target_path = res_dir / fname
                            if not target_path.exists():
                                with zf.open(info) as source, open(target_path, "wb") as target:
                                    shutil.copyfileobj(source, target)
                                extracted += 1
                    if extracted > 0:
                        print(f">>> Unpacked {extracted} artifacts from {zpath.name} -> {res_dir}")
            except Exception:
                pass

        # 2. Search for any raw files in input datasets / working dirs
        for p in sdir.rglob("nb*.*"):
            if p.is_file() and p.suffix in [".parquet", ".csv", ".json", ".tex", ".pdf", ".png"]:
                dest = res_dir / p.name
                if not dest.exists():
                    try:
                        shutil.copy(p, dest)
                        print(f">>> Found & copied artifact: {p.name} -> {dest}")
                    except Exception:
                        pass

        for p in sdir.rglob("fig_*.*"):
            if p.is_file() and p.suffix in [".pdf", ".png"]:
                dest = res_dir / p.name
                if not dest.exists():
                    try:
                        shutil.copy(p, dest)
                        print(f">>> Found & copied figure: {p.name} -> {dest}")
                    except Exception:
                        pass


discover_artifacts()
print("Artifacts directory ->", ART)


def save_json(obj, name):
    p = ART / "results" / name
    with open(p, "w") as f:
        json.dump(obj, f, indent=2, default=float)
    print("saved", p)
    return p


def save_csv(df, name):
    p = ART / "results" / name
    df.to_csv(p, index=False)
    print("saved", p, df.shape)
    return p
'''

BOOTSTRAP_BLOCK = '''
def paired_bootstrap(a, b, n_boot=10000, seed=SEED):
    """Paired bootstrap over per-query scores.

    Returns mean difference (a - b), a 95% percentile CI, and a two-sided
    bootstrap p-value for H0: mean difference == 0. We report effect sizes and
    intervals rather than leaning on p-values, because at n in the thousands a
    Wilcoxon test declares almost any difference "significant" while the effect
    itself may be far below what a practitioner would notice.
    """
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    assert len(a) == len(b) and len(a) > 1
    d = a - b
    obs = float(d.mean())
    # A degenerate difference (every query tied) has no bootstrap variance, so
    # the percentile test below would report p = 0 for two systems that are in
    # fact identical. Return the correct answer instead.
    if float(d.std(ddof=0)) < 1e-12:
        return {"mean_diff": obs, "ci_low": obs, "ci_high": obs, "boot_p": 1.0,
                "n": int(len(d)), "cohen_dz": 0.0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(d), size=(n_boot, len(d)))
    boot = d[idx].mean(axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    # two-sided p: fraction of centred bootstrap means at least as extreme
    centred = boot - obs
    p = float((np.abs(centred) >= abs(obs)).mean())
    return {
        "mean_diff": obs,
        "ci_low": float(lo),
        "ci_high": float(hi),
        "boot_p": p,
        "n": int(len(d)),
        "cohen_dz": float(obs / (d.std(ddof=1) + 1e-12)),
    }
'''
