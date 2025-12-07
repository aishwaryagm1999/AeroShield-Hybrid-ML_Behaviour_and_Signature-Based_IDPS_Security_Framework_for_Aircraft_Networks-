"""
src/maintenance/post_flight_learning.py

Post-flight learning pipeline (simplified):

- Ingest "quarantine log" (JSONL) with low-confidence events, IF outliers, etc.
- Aggregate into a feature corpus for offline retraining
- (Optionally) regenerate YARA rules and imphash index

This does NOT run live malware sandboxes, but defines clear hooks to do so.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
import pandas as pd


LOG_DIR = Path("logs")
QUARANTINE_LOG = LOG_DIR / "quarantine_log.jsonl"
OFFLINE_CORPUS = Path("data") / "offline_corpus.csv"


def load_quarantine_events() -> List[Dict[str, Any]]:
    if not QUARANTINE_LOG.exists():
        return []
    events: List[Dict[str, Any]] = []
    with open(QUARANTINE_LOG, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            events.append(json.loads(line))
    return events


def build_offline_corpus(events: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for ev in events:
        feat = ev.get("features", [])
        if not feat:
            continue
        row = {
            "zone": ev.get("zone"),
            "label": ev.get("label", 1),
        }
        for i, v in enumerate(feat):
            row[f"f{i}"] = v
        rows.append(row)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    events = load_quarantine_events()
    if not events:
        print("[post-flight] No quarantine events found.")
        return

    df = build_offline_corpus(events)
    if df.empty:
        print("[post-flight] No usable events in quarantine log.")
        return

    OFFLINE_CORPUS.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OFFLINE_CORPUS, index=False)
    print(f"[post-flight] Saved offline corpus to {OFFLINE_CORPUS}")
    print("[post-flight] Use this file as an additional dataset for retraining.")


if __name__ == "__main__":
    main()
