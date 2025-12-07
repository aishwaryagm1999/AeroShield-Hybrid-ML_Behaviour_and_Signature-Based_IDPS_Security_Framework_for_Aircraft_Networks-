"""
src/zta/pep.py

Policy Enforcement Point abstraction.

In the VirtualBox testbed this corresponded to UFW/iptables and tc rules. Here
we simulate the actions and print them; in a real deployment these would call
system commands or firewall APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PEP:
    zone: str

    def block_ip(self, ip: str) -> None:
        print(f"[PEP::{self.zone}] Blocking IP {ip}")

    def block_port(self, port: int, proto: str = "tcp") -> None:
        print(f"[PEP::{self.zone}] Blocking {proto.upper()} port {port}")

    def throttle_bandwidth(self, ip: str, kbps: int) -> None:
        print(f"[PEP::{self.zone}] Throttling {ip} to {kbps} kbps")

    def quarantine_file(self, path: str) -> None:
        print(f"[PEP::{self.zone}] Quarantining file {path}")

    def drop_flow(self, flow_id: str) -> None:
        print(f"[PEP::{self.zone}] Dropping flow {flow_id}")
