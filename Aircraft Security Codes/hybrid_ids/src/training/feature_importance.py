"""
src/training/feature_importance.py

Extracts and visualizes feature importances for all Random Forest models.
"""

import joblib
import matplotlib.pyplot as plt
from pathlib import Path


MODEL_DIR = Path("models")


def plot_feature_importance(model_name, feature_names):
    path = MODEL_DIR / f"{model_name}.joblib"
    bundle = joblib.load(path)
    model = bundle["model"]

    importances = model.feature_importances_

    fig, ax = plt.subplots(figsize=(6,4))
    ax.barh(feature_names, importances)
    ax.set_title(f"Feature Importance: {model_name}")
    plt.tight_layout()
    return fig
