"""
src/simulation/simulate_attacks.py

Simple high-level simulation of:

- Reconnaissance in ENTERTAINMENT (UNSW-based features)
- SYN-like DoS in COMMUNICATIONS
- Ghost aircraft ADS-B / ADS-C anomalies
- Malware drop in ENTERTAINMENT zone

This does not run real pcaps or VirtualBox, but mimics the detections described
in the manuscript so reviewers can see how the components interact.
"""

from __future__ import annotations

import random
from typing import Dict

import numpy as np

from src.core.feature_engineering import DATASET_LOADERS
from src.zta.tee import TrustEvaluationEngine
from src.zta.zones import ZoneEvent, ZoneName, zone_predict


def _sample_feature(loader_name: str, anomaly: bool = False) -> np.ndarray:
    data = DATASET_LOADERS[loader_name]()
    X = data["X_test"]
    y = data["y_test"]
    indices = np.where(y == (1 if anomaly else 0))[0]
    if len(indices) == 0:
        indices = np.arange(len(X))
    idx = random.choice(indices.tolist())
    return X[idx]


def run_simulation() -> None:
    tee = TrustEvaluationEngine()
    for z in ZoneName:
        tee.register_zone(z.value)

    # 1. Reconnaissance in ENTERTAINMENT (UNSW-NB15)
    print("[SIM] Reconnaissance attack in ENTERTAINMENT zone")
    feat = _sample_feature("unsw_nb15", anomaly=True)
    event = ZoneEvent(
        zone=ZoneName.ENTERTAINMENT,
        features=feat,
        meta={"src_ip": "10.0.3.42", "dst_port": 80, "attack": "Recon"},
    )
    pred = zone_predict(event)
    if pred == 1:
        tee.handle_detection(
            zone=event.zone.value,
            category="Reconnaissance",
            confidence=0.95,
            meta=event.meta,
        )

    # 2. DoS in COMMUNICATIONS (UNSW-NB15 or ADS-C)
    print("[SIM] DoS/SYN-like flood in COMMUNICATIONS zone")
    feat = _sample_feature("unsw_nb15", anomaly=True)
    event = ZoneEvent(
        zone=ZoneName.COMMUNICATIONS,
        features=feat,
        meta={"src_ip": "10.0.1.66", "dst_port": 443, "attack": "DoS"},
    )
    pred = zone_predict(event)
    if pred == 1:
        tee.handle_detection(
            zone=event.zone.value,
            category="DoS",
            confidence=0.92,
            meta=event.meta,
        )

    # 3. Ghost aircraft injection in ATC/COMMUNICATIONS (ADS-C)
    print("[SIM] Ghost aircraft / ADS-C anomaly")
    feat = _sample_feature("adsc", anomaly=True)
    event = ZoneEvent(
        zone=ZoneName.COMMUNICATIONS,
        features=feat,
        meta={"src_ip": "adsb-gateway", "flow_id": "adsb_stream_1", "attack": "Ghost"},
    )
    pred = zone_predict(event)
    if pred == 1:
        tee.handle_detection(
            zone=event.zone.value,
            category="GhostAircraft",
            confidence=0.973,
            meta=event.meta,
        )

    # 4. Malware infiltration in ENTERTAINMENT
    print("[SIM] Malware dropped into ENTERTAINMENT Downloads")
    event = ZoneEvent(
        zone=ZoneName.ENTERTAINMENT,
        features=_sample_feature("unsw_nb15", anomaly=True),
        meta={"file_path": "/home/entertainment/Downloads/malware.exe", "attack": "Malware"},
    )
    pred = zone_predict(event)
    if pred == 1:
        tee.handle_detection(
            zone=event.zone.value,
            category="Malware",
            confidence=0.94,
            meta=event.meta,
        )


if __name__ == "__main__":
    run_simulation()
