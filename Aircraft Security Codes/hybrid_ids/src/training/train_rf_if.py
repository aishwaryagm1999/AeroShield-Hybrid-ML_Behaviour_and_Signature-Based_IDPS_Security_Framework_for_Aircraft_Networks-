"""
src/training/train_rf_if.py

Entry point to train RF + IF models on all six datasets and print metrics.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.core.anomaly_detection import train_all_datasets


def main() -> None:
    results = train_all_datasets()
    out_path = Path("models") / "training_metrics.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"[+] Saved metrics to {out_path}")


if __name__ == "__main__":
    main()
