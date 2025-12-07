from __future__ import annotations

"""
src/core/model_utils.py

Utility functions for saving/loading models, scalers, and encoders with LZMA
compression, and for computing common evaluation metrics.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    matthews_corrcoef,
)

MODEL_DIR = Path("models")


@dataclass
class ModelArtifacts:
    model: Any
    scaler: Any | None = None
    label_encoder: Any | None = None


def ensure_model_dir() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)


def save_artifacts(
    name: str,
    model: Any,
    scaler: Any | None = None,
    label_encoder: Any | None = None,
) -> None:
    """Save model + optional scaler/encoder as a compressed joblib bundle."""
    ensure_model_dir()
    bundle = {
        "model": model,
        "scaler": scaler,
        "label_encoder": label_encoder,
    }
    path = MODEL_DIR / f"{name}.joblib"
    # "lzma" here refers to the compressor; joblib handles it internally
    joblib.dump(bundle, path, compress=("lzma", 3))


def load_artifacts(name: str) -> ModelArtifacts:
    """Load a bundle saved by save_artifacts()."""
    path = MODEL_DIR / f"{name}.joblib"
    bundle = joblib.load(path)
    return ModelArtifacts(
        model=bundle.get("model"),
        scaler=bundle.get("scaler"),
        label_encoder=bundle.get("label_encoder"),
    )


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute metrics used in the manuscript."""
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    mcc = matthews_corrcoef(y_true, y_pred) if len(np.unique(y_true)) == 2 else 0.0

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "specificity": spec,
        "fpr": fpr,
        "fnr": fnr,
        "mcc": mcc,
    }
