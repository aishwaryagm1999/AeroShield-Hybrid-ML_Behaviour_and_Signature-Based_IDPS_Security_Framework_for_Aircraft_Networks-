"""
src/zta/alerting.py

Alert object + simple console "sink". In a real deployment this would send
TCP messages to cockpit HMI and ATC backends.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Alert:
    timestamp: str
    zone: str
    category: str
    severity: Severity
    confidence: float
    description: str
    action: str
    metadata: Dict[str, Any]


def current_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def send_alert(alert: Alert) -> None:
    """
    Simple console logger; replace with TCP / syslog / SIEM integration.
    """
    print("=== IDS ALERT ===")
    for k, v in asdict(alert).items():
        print(f"{k.upper()}: {v}")
    print("=== END ALERT ===\n")
