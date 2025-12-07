from __future__ import annotations

"""
Training and inference wrappers for the Hybrid-IDS anomaly engine.

- Random Forest (supervised) for all 6 datasets
- Isolation Forest (unsupervised) for ADS-C, ACARS, ARINC 429
- Hybrid score fusion (RF + IF) for domains that enable it
"""

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from .feature_engineering import DATASET_LOADERS
from .model_utils import compute_metrics, save_artifacts, load_artifacts


@dataclass
class HybridScores:
    rf_proba: float
    if_score: Optional[float]
    fused_score: float


def train_all_datasets(
    random_state: int = 42,
    n_estimators: int = 300,
    max_depth: int | None = None,
) -> Dict[str, Dict]:
    """Train RF models (and IF for selected domains) on all datasets.

    For each dataset we:
    - Load preprocessed features (SMOTE + split)
    - Fit a StandardScaler on the training set
    - Train RF (and IF where applicable) on the scaled training data
    - Evaluate on the scaled test data and store metrics
    - Persist the model bundle (model + scaler)
    """
    results: Dict[str, Dict] = {}

    for name, loader in DATASET_LOADERS.items():
        data = loader()
        X_train = data["X_train"]
        X_test = data["X_test"]
        y_train = data["y_train"]
        y_test = data["y_test"]

        # Scale features
        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        # Train RF
        print(f"[+] Training RF for dataset: {name}")
        rf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            n_jobs=-1,
            random_state=random_state,
            class_weight="balanced_subsample",
        )
        rf.fit(X_train_s, y_train)
        y_pred = rf.predict(X_test_s)
        metrics = compute_metrics(y_test, y_pred)

        # Save RF + scaler
        save_artifacts(f"rf_{name}", rf, scaler=scaler)

        # Train IF for ADS-C, ACARS, ARINC 429
        if name in {"adsc", "acars", "arinc429"}:
            print(f"[+] Training Isolation Forest for dataset: {name}")
            if_model = IsolationForest(
                n_estimators=200,
                contamination="auto",
                random_state=random_state,
                n_jobs=-1,
            )
            if_model.fit(X_train_s)
            save_artifacts(f"if_{name}", if_model, scaler=scaler)

        results[name] = metrics
        print(f"[=] Metrics for {name}: {metrics}\n")

    return results


def hybrid_predict(
    dataset_name: str,
    X_raw: np.ndarray,
    threshold: float = 0.85,
) -> np.ndarray:
    """Hybrid prediction for a given dataset.

    Args:
        dataset_name: One of the keys of DATASET_LOADERS.
        X_raw: 2-D array of *unscaled* feature vectors.
        threshold: Decision threshold on the fused anomaly score.

    Returns:
        Binary predictions (0 = normal, 1 = anomaly).
    """
    rf_art = load_artifacts(f"rf_{dataset_name}")
    rf = rf_art.model
    scaler = rf_art.scaler
    if scaler is None:
        raise RuntimeError(f"No scaler stored for dataset '{dataset_name}'")

    X = scaler.transform(X_raw)

    # RF posterior probability for class "1" (anomaly)
    proba = rf.predict_proba(X)[:, 1]

    if dataset_name in {"adsc", "acars", "arinc429"}:
        if_art = load_artifacts(f"if_{dataset_name}")
        if_model = if_art.model
        raw_if_scores = if_model.decision_function(X)
        # Normalize IF scores to [0,1] (higher = more anomalous)
        if_min, if_max = raw_if_scores.min(), raw_if_scores.max()
        if_span = max(if_max - if_min, 1e-9)
        if_scores_norm = 1.0 - (raw_if_scores - if_min) / if_span
        fused = 0.5 * proba + 0.5 * if_scores_norm
    else:
        fused = proba

    preds = (fused >= threshold).astype(int)
    return preds
