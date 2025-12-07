"""
src/zta/zones.py

Definitions for aircraft network zones and simple "zone-local" IDS wrappers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

import numpy as np

from src.core.anomaly_detection import hybrid_predict


class ZoneName(str, Enum):
    COCKPIT = "cockpit"
    COMMUNICATIONS = "communications"
    CABIN_CREW = "cabin_crew"
    ENTERTAINMENT = "entertainment"


@dataclass
class ZoneConfig:
    name: ZoneName
    dataset: str  # which RF/IF model to use
    threshold: float = 0.85


ZONE_CONFIGS: Dict[ZoneName, ZoneConfig] = {
    ZoneName.COCKPIT: ZoneConfig(ZoneName.COCKPIT, "milstd1553", 0.85),
    ZoneName.COMMUNICATIONS: ZoneConfig(ZoneName.COMMUNICATIONS, "adsc", 0.85),
    ZoneName.CABIN_CREW: ZoneConfig(ZoneName.CABIN_CREW, "acars", 0.85),
    ZoneName.ENTERTAINMENT: ZoneConfig(ZoneName.ENTERTAINMENT, "unsw_nb15", 0.85),
}


@dataclass
class ZoneEvent:
    zone: ZoneName
    features: np.ndarray  # single-sample feature vector
    meta: Dict  # additional info (IP, port, protocol, etc.)


def zone_predict(event: ZoneEvent) -> int:
    """Run the zone-local detector and return 0 (normal) / 1 (anomaly)."""
    cfg = ZONE_CONFIGS[event.zone]
    X = event.features.reshape(1, -1)
    preds = hybrid_predict(cfg.dataset, X, threshold=cfg.threshold)
    return int(preds[0])
