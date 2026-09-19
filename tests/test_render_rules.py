from pathlib import Path

import pytest

from tools.audit_rules import audit, parse_rules
from tools.render_rules import PolicyError, main, render, tomllib

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "policy" / "lab.toml"
RENDERED = ROOT / "config" / "hardened-rules.xml"


def load(text: str) -> dict:
    return tomllib.loads(text)


BASE = """
[interfaces]
lan = { subnet = "lan" }
"""


def test_committed_rules_match_the_policy():
    assert render(load(POLICY.read_text(encoding="utf-8"))) == RENDERED.read_text(encoding="utf-8")


def test_rendering_is_deterministic():
    policy = load(POLICY.read_text(encoding="utf-8"))
    assert render(policy) == render(policy)


def test_hardened_rules_pass_the_audit_cleanly():
    assert audit(parse_rules(RENDERED.read_text(encoding="utf-8"))) == []


def test_policy_ends_in_a_logged_default_deny():
    last = parse_rules(RENDERED.read_text(encoding="utf-8"))[-1]
    assert (last.type, last.destination) == ("block", "any")
    assert "<log />" in RENDERED.read_text(encoding="utf-8")


def test_multi_port_rules_expand_to_one_rule_per_port():
    xml = render(load(BASE + """
[[rule]]
interface = "lan"
action = "pass"
protocol = "tcp"
destination = "any"
ports = ["80", "443"]
description = "Web"
"""))
    rules = parse_rules(xml)
    assert [(r.dest_port, r.description) for r in rules] == [("80", "Web (80)"), ("443", "Web (443)")]


@pytest.mark.parametrize(
    "rule, message",
    [
        ('interface = "dmz"\naction = "pass"\ndestination = "any"\ndescription = "x"', "unknown interface"),
        ('interface = "lan"\naction = "allow"\ndestination = "any"\ndescription = "x"', "action must be"),
        ('interface = "lan"\naction = "pass"\ndestination = "any"', "needs a description"),
        (
            'interface = "lan"\naction = "pass"\nprotocol = "icmp"\ndestination = "any"\nports = "80"\n'
            'description = "x"',
            "ports need protocol",
        ),
        (
            'interface = "lan"\naction = "pass"\nprotocol = "tcp"\ndestination = "any"\nports = "70000"\n'
            'description = "x"',
            "invalid port",
        ),
    ],
)
def test_invalid_policies_are_rejected(rule, message):
    with pytest.raises(PolicyError, match=message):
        render(load(BASE + "\n[[rule]]\n" + rule))


def test_cli_reports_policy_errors(tmp_path, capsys):
    bad = tmp_path / "bad.toml"
    bad.write_text(BASE, encoding="utf-8")
    assert main([str(bad)]) == 2
    assert "no [[rule]] entries" in capsys.readouterr().err
