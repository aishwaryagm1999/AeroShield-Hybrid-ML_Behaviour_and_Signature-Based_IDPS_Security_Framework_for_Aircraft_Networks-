"""
src/training/cross_validation.py

Performs stratified K-fold cross-validation on each dataset.
"""

from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from src.core.feature_engineering import DATASET_LOADERS
from src.core.model_utils import compute_metrics


def run_cross_validation(k=5):
    results = {}

    for name, loader in DATASET_LOADERS.items():
        data = loader()
        X = data["X_train"]
        y = data["y_train"]
        skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)

        fold_metrics = []

        for train_idx, test_idx in skf.split(X, y):
            Xtr, Xte = X[train_idx], X[test_idx]
            ytr, yte = y[train_idx], y[test_idx]

            model = RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            )
            model.fit(Xtr, ytr)
            pred = model.predict(Xte)
            metrics = compute_metrics(yte, pred)
            fold_metrics.append(metrics)

        results[name] = fold_metrics
        print(f"[CV] Completed {k}-fold for {name}")

    return results
