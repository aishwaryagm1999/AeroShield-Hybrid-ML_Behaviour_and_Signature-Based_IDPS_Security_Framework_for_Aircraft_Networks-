"""
src/zta/tee.py

Trust Evaluation Engine (TEE) implementing risk scoring, IPS decisions,
and coordination across zones under a Zero-Trust model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any

from .alerting import Alert, Severity, current_timestamp, send_alert
from .pep import PEP


@dataclass
class TEERiskState:
    scores: Dict[str, float] = field(default_factory=dict)


class TrustEvaluationEngine:
    def __init__(self) -> None:
        self.risk = TEERiskState()
        self.peps: Dict[str, PEP] = {}

    def register_zone(self, zone: str) -> None:
        self.peps[zone] = PEP(zone)

    def _update_zone_risk(self, zone: str, delta: float) -> float:
        cur = self.risk.scores.get(zone, 0.0)
        new = max(0.0, cur + delta)
        self.risk.scores[zone] = new
        return new

    def handle_detection(
        self,
        zone: str,
        category: str,
        confidence: float,
        meta: Dict[str, Any],
    ) -> None:
        """
        Called when a zone-local detector flags an anomaly.
        """
        # Update risk and derive severity
        risk_delta = confidence
        risk_score = self._update_zone_risk(zone, risk_delta)

        if risk_score > 2.5 or confidence > 0.95:
            severity = Severity.CRITICAL
        elif risk_score > 1.5:
            severity = Severity.HIGH
        elif risk_score > 0.8:
            severity = Severity.WARNING
        else:
            severity = Severity.INFO

        action = self._decide_action(zone, category, severity, meta)

        alert = Alert(
            timestamp=current_timestamp(),
            zone=zone,
            category=category,
            severity=severity,
            confidence=confidence,
            description=f"Anomalous activity detected in zone={zone}, category={category}",
            action=action,
            metadata=meta,
        )
        send_alert(alert)

    def _decide_action(
        self,
        zone: str,
        category: str,
        severity: Severity,
        meta: Dict[str, Any],
    ) -> str:
        pep = self.peps.get(zone)
        if pep is None:
            return "NO_PEP_CONFIGURED"

        ip = meta.get("src_ip")
        port = meta.get("dst_port")

        if severity in {Severity.CRITICAL, Severity.HIGH}:
            if category in {"DoS", "Reconnaissance"} and ip:
                pep.block_ip(ip)
                if port:
                    pep.block_port(port)
                return "IP_BLOCKED_PORT_BLOCKED"

            if category in {"GhostAircraft", "Spoofing"}:
                flow_id = meta.get("flow_id", "adsb_stream")
                pep.drop_flow(flow_id)
                return "STREAM_DROPPED"

            if category == "Malware" and meta.get("file_path"):
                pep.quarantine_file(meta["file_path"])
                return "FILE_QUARANTINED"

        if severity == Severity.WARNING and ip:
            pep.throttle_bandwidth(ip, kbps=50)
            return "BANDWIDTH_THROTTLED"

        return "MONITOR_ONLY"
