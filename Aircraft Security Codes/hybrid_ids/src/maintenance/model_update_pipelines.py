"""
src/maintenance/model_update_pipeline.py

Full retraining pipeline combining:
- Quarantine log ingestion
- Offline corpus update
- Optional re-generation of RF/IF models
"""

from pathlib import Path
from src.maintenance.post_flight_learning import main as build_corpus
from src.training.train_rf_if import main as retrain_models


def run_full_update():
    print("[Update] Building offline learning corpus...")
    build_corpus()

    print("[Update] Retraining RF/IF models from updated dataset...")
    retrain_models()

    print("[Update] Model update pipeline completed.")
