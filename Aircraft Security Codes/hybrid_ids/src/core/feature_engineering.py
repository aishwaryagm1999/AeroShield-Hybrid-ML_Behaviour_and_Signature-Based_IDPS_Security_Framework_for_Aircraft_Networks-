from __future__ import annotations

"""
Feature loading + preprocessing for the six anomaly datasets.

This module only handles:
- CSV loading
- Optional feature selection (ExtraTrees)
- SMOTE
- Train/test split

**No scaling is done here**; scaling is handled in the training code so that
the same StandardScaler can be reused consistently at inference time.
"""

from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split


DATA_DIR = Path("data")


def _load_csv(dataset_dir: str, filename: str) -> pd.DataFrame:
    path = DATA_DIR / dataset_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Expected dataset file missing: {path}")
    return pd.read_csv(path)


def _split_smote(
    df: pd.DataFrame,
    feature_cols: List[str],
    label_col: str = "label",
    test_size: float = 0.3,
    random_state: int = 42,
    k_features: int | None = 10,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]:
    """Common pipeline: feature selection → SMOTE → train/test split.

    Returns:
        X_train, X_test, y_train, y_test, selected_feature_cols
    """
    X = df[feature_cols].values
    y = df[label_col].values

    # Optional feature ranking using ExtraTrees
    if k_features is not None and len(feature_cols) > k_features:
        etc = ExtraTreesClassifier(n_estimators=200, random_state=random_state, n_jobs=-1)
        etc.fit(X, y)
        importances = etc.feature_importances_
        ranked_idx = np.argsort(importances)[::-1][:k_features]
        feature_cols = [feature_cols[i] for i in ranked_idx]
        X = df[feature_cols].values

    # SMOTE for class imbalance (offline)
    smote = SMOTE(random_state=random_state)
    X_res, y_res = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_res,
        y_res,
        test_size=test_size,
        random_state=random_state,
        stratify=y_res,
    )

    return X_train, X_test, y_train, y_test, feature_cols


def load_unsw_nb15() -> Dict:
    df = _load_csv("unsw-nb15", "unsw_processed.csv")
    features = ["sttl", "dttl", "state", "dload", "rate"]
    X_train, X_test, y_train, y_test, selected_features = _split_smote(
        df, features, k_features=None
    )
    return {
        "name": "unsw_nb15",
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": selected_features,
    }


def load_adsb_injection() -> Dict:
    df = _load_csv("adsb_injection", "adsb_injection_processed.csv")
    features = ["rss", "lon", "geoaltitude", "baroaltitude", "lat"]
    X_train, X_test, y_train, y_test, selected = _split_smote(
        df, features, k_features=None
    )
    return {
        "name": "adsb_injection",
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": selected,
    }


def load_milstd1553() -> Dict:
    df = _load_csv("milstd1553", "milstd1553_processed.csv")
    features = ["sa", "gap", "da", "rxSts", "connType"]
    X_train, X_test, y_train, y_test, selected = _split_smote(
        df, features, k_features=None
    )
    return {
        "name": "milstd1553",
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": selected,
    }


def load_adsc() -> Dict:
    df = _load_csv("adsc", "adsc_features.csv")
    # RF uses reduced features; rule-based ADS-C logic uses the full raw file.
    features = [
        "time_diff",
        "wind_dir_deg",
        "wind_speed_kt",
        "temperature_C",
        "altitude_ft",
    ]
    X_train, X_test, y_train, y_test, selected = _split_smote(
        df, features, k_features=None
    )
    return {
        "name": "adsc",
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": selected,
    }


def load_acars() -> Dict:
    df = _load_csv("acars", "acars_features.csv")
    features = [
        "altitude_change_rate",
        "wind_speed_delta",
        "temp_gradient",
        "geodist_delta_km",
    ]
    X_train, X_test, y_train, y_test, selected = _split_smote(
        df, features, k_features=None
    )
    return {
        "name": "acars",
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": selected,
    }


def load_arinc429() -> Dict:
    df = _load_csv("arinc429", "arinc429_waveform_features.csv")
    features = [
        "std_v",
        "trans_ratio",
        "null_hi_ratio",
        "null_lo_ratio",
        "slope_std",
    ]
    X_train, X_test, y_train, y_test, selected = _split_smote(
        df, features, k_features=None
    )
    return {
        "name": "arinc429",
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": selected,
    }


DATASET_LOADERS = {
    "unsw_nb15": load_unsw_nb15,
    "adsb_injection": load_adsb_injection,
    "milstd1553": load_milstd1553,
    "adsc": load_adsc,
    "acars": load_acars,
    "arinc429": load_arinc429,
}
