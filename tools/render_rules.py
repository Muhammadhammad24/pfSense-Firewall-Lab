#!/usr/bin/env python3
"""Render a TOML firewall policy into a pfSense <filter> rule set.

The output can be imported under Diagnostics > Backup & Restore, restore
area "Firewall Rules". Rules are emitted in policy order, with one rule per
destination port so each shows as its own line in the GUI. Tracker IDs are
derived from the rule content, so re-rendering an unchanged policy produces
byte-identical XML, which CI checks.

    python tools/render_rules.py policy/lab.toml -o config/hardened-rules.xml
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

ACTIONS = {"pass", "block", "reject"}
PROTOCOLS = {"any", "tcp", "udp", "tcp/udp", "icmp"}


class PolicyError(ValueError):
    pass


def _ports(rule: dict) -> list[str]:
    ports = rule.get("ports", [])
    ports = [ports] if isinstance(ports, str) else list(ports)
    for p in ports:
        lo, _, hi = p.partition("-")
        if not lo.isdigit() or (hi and not hi.isdigit()) or not 0 < int(lo) <= 65535:
            raise PolicyError(f"invalid port {p!r}")
    return ports or [""]


def validate(policy: dict) -> list[dict]:
    interfaces = policy.get("interfaces", {})
    rules = policy.get("rule", [])
    if not rules:
        raise PolicyError("policy has no [[rule]] entries")
    for i, r in enumerate(rules, start=1):
        where = f"rule {i} ({r.get('description', 'no description')})"
        if r.get("interface") not in interfaces:
            raise PolicyError(f"{where}: unknown interface {r.get('interface')!r}")
        if r.get("action") not in ACTIONS:
            raise PolicyError(f"{where}: action must be one of {sorted(ACTIONS)}")
        if r.get("protocol", "any") not in PROTOCOLS:
            raise PolicyError(f"{where}: protocol must be one of {sorted(PROTOCOLS)}")
        if not r.get("description"):
            raise PolicyError(f"{where}: every rule needs a description")
        if r.get("ports") and r.get("protocol") not in ("tcp", "udp", "tcp/udp"):
            raise PolicyError(f"{where}: ports need protocol tcp, udp or tcp/udp")
        _ports(r)
    return rules


def _endpoint(parent: ET.Element, tag: str, target: str, subnet: str, port: str = "") -> None:
    node = ET.SubElement(parent, tag)
    if target == "any":
        ET.SubElement(node, "any")
    elif target == "self":
        ET.SubElement(node, "network").text = "(self)"
    elif target == "subnet":
        ET.SubElement(node, "network").text = subnet
    else:
        ET.SubElement(node, "address").text = target
    if port:
        ET.SubElement(node, "port").text = port


def _tracker(*parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return str(int(digest[:8], 16) + 1_000_000_000)


def render(policy: dict) -> str:
    rules = validate(policy)
    interfaces = policy["interfaces"]
    root = ET.Element("filter")
    for r in rules:
        subnet = interfaces[r["interface"]]["subnet"]
        protocol = r.get("protocol", "any")
        ports = _ports(r)
        for port in ports:
            descr = r["description"] + (f" ({port})" if port and len(ports) > 1 else "")
            node = ET.SubElement(root, "rule")
            tracker = _tracker(r["interface"], r["action"], protocol, r["destination"], port)
            ET.SubElement(node, "tracker").text = tracker
            ET.SubElement(node, "type").text = r["action"]
            ET.SubElement(node, "interface").text = r["interface"]
            ET.SubElement(node, "ipprotocol").text = "inet"
            if protocol != "any":
                ET.SubElement(node, "protocol").text = protocol
            if protocol == "icmp":
                ET.SubElement(node, "icmptype").text = "any"
            _endpoint(node, "source", r.get("source", "subnet"), subnet)
            _endpoint(node, "destination", r["destination"], subnet, port)
            if r.get("log"):
                ET.SubElement(node, "log")
            ET.SubElement(node, "descr").text = descr
    ET.indent(root, space="\t")
    return ET.tostring(root, encoding="unicode") + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("policy", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="write here instead of stdout")
    args = parser.parse_args(argv)

    try:
        xml = render(tomllib.loads(args.policy.read_text(encoding="utf-8")))
    except (PolicyError, tomllib.TOMLDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.output:
        args.output.write_text(xml, encoding="utf-8", newline="\n")
        print(f"wrote {xml.count('<rule>')} rules to {args.output}")
    else:
        sys.stdout.write(xml)
    return 0


if __name__ == "__main__":
    sys.exit(main())
