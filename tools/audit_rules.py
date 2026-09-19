#!/usr/bin/env python3
"""Audit an exported pfSense rule set for common policy mistakes.

Reads the <filter> section exported from Diagnostics > Backup & Restore
(area "Firewall Rules") and reports findings by severity:

  high    pass rules on WAN from any source to any destination
  high    pass rules on WAN that expose management ports (22, 80, 443, 3389)
  medium  any-to-any pass rules on internal interfaces
  low     rules without a description
  low     disabled rules left in the rule set
  info    IPv6 pass rules (check they are intended)

Exit status is 1 if any finding reaches --fail-on (default: high), so the
script can gate CI.

    python tools/audit_rules.py config/Firewall-Rules-Backup.xml
    python tools/audit_rules.py rules.xml --fail-on medium --format json
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass

SEVERITIES = ["info", "low", "medium", "high"]
MANAGEMENT_PORTS = {"22", "80", "443", "3389", "8080", "8443"}
EXTERNAL_INTERFACES = {"wan"}


@dataclass
class Rule:
    index: int
    type: str
    interface: str
    ipprotocol: str
    protocol: str
    source: str
    destination: str
    dest_port: str
    description: str
    disabled: bool

    @property
    def label(self) -> str:
        return f"#{self.index} [{self.interface}] {self.description or '(no description)'}"


@dataclass
class Finding:
    severity: str
    rule: str
    message: str


def _endpoint(node: ET.Element | None) -> tuple[str, str]:
    """Return (address, port) for a <source> or <destination> element."""
    if node is None:
        return "any", ""
    port = (node.findtext("port") or "").strip()
    if node.find("any") is not None:
        return "any", port
    for tag in ("network", "address"):
        value = node.findtext(tag)
        if value:
            prefix = "!" if node.find("not") is not None else ""
            return prefix + value.strip(), port
    return "any", port


def parse_rules(xml_text: str) -> list[Rule]:
    root = ET.fromstring(xml_text)
    filter_node = root if root.tag == "filter" else root.find(".//filter")
    if filter_node is None:
        raise ValueError("no <filter> section found")
    rules = []
    for i, node in enumerate(filter_node.findall("rule"), start=1):
        source, _ = _endpoint(node.find("source"))
        destination, port = _endpoint(node.find("destination"))
        rules.append(
            Rule(
                index=i,
                type=(node.findtext("type") or "pass").strip(),
                interface=(node.findtext("interface") or "").strip().lower(),
                ipprotocol=(node.findtext("ipprotocol") or "inet").strip(),
                protocol=(node.findtext("protocol") or "any").strip(),
                source=source,
                destination=destination,
                dest_port=port,
                description=(node.findtext("descr") or "").strip(),
                disabled=node.find("disabled") is not None,
            )
        )
    return rules


def _ports(spec: str) -> set[str]:
    if not spec:
        return set()
    if "-" in spec:
        lo, hi = (int(p) for p in spec.split("-", 1))
        return {p for p in MANAGEMENT_PORTS if lo <= int(p) <= hi}
    return {spec}


def audit(rules: list[Rule]) -> list[Finding]:
    findings: list[Finding] = []
    for r in rules:
        if r.disabled:
            findings.append(Finding("low", r.label, "disabled rule left in the rule set"))
            continue
        if not r.description:
            findings.append(Finding("low", r.label, "rule has no description"))
        if r.type != "pass":
            continue
        external = r.interface in EXTERNAL_INTERFACES
        wide_open = r.source == "any" and r.destination == "any" and not r.dest_port
        if external and wide_open:
            findings.append(Finding("high", r.label, "WAN allows any source to any destination"))
        elif external and r.source == "any":
            exposed = _ports(r.dest_port) & MANAGEMENT_PORTS
            if exposed or not r.dest_port:
                what = f"port(s) {', '.join(sorted(exposed))}" if exposed else "all ports"
                findings.append(Finding("high", r.label, f"WAN exposes {what} to the internet"))
        elif not external and r.destination == "any" and not r.dest_port and r.protocol == "any":
            message = f"{r.source} may reach any destination on any port; consider egress filtering"
            findings.append(Finding("medium", r.label, message))
        if r.ipprotocol in ("inet6", "inet46"):
            findings.append(Finding("info", r.label, "IPv6 traffic is permitted; confirm IPv6 is in use"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="exported rules XML")
    parser.add_argument("--fail-on", choices=SEVERITIES, default="high")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    with open(args.path, encoding="utf-8") as f:
        rules = parse_rules(f.read())
    findings = audit(rules)

    if args.format == "json":
        print(json.dumps({"rules": len(rules), "findings": [asdict(x) for x in findings]}, indent=2))
    else:
        print(f"{len(rules)} rules, {len(findings)} findings")
        for x in sorted(findings, key=lambda x: -SEVERITIES.index(x.severity)):
            print(f"  {x.severity.upper():<6} {x.rule}: {x.message}")

    threshold = SEVERITIES.index(args.fail_on)
    return 1 if any(SEVERITIES.index(x.severity) >= threshold for x in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
