import json
from pathlib import Path

import pytest

from tools.audit_rules import audit, main, parse_rules

EXPORT = Path(__file__).resolve().parents[1] / "config" / "Firewall-Rules-Backup.xml"


def rule(interface="lan", descr="Test", source="<network>lan</network>", dest="<any></any>", extra=""):
    return f"""
    <rule>
      <type>pass</type><interface>{interface}</interface><ipprotocol>inet</ipprotocol>
      <descr><![CDATA[{descr}]]></descr>
      <source>{source}</source><destination>{dest}</destination>{extra}
    </rule>"""


def findings(*rules):
    return [(f.severity, f.message) for f in audit(parse_rules("<filter>" + "".join(rules) + "</filter>"))]


def test_parses_the_committed_export():
    rules = parse_rules(EXPORT.read_text(encoding="utf-8"))
    assert [(r.interface, r.ipprotocol, r.source, r.destination) for r in rules] == [
        ("lan", "inet", "lan", "any"),
        ("lan", "inet6", "lan", "any"),
    ]


def test_committed_export_has_no_high_severity_findings():
    assert main([str(EXPORT)]) == 0


def test_wan_any_to_any_is_high():
    assert ("high", "WAN allows any source to any destination") in findings(
        rule(interface="wan", source="<any></any>")
    )


def test_wan_ssh_exposure_is_high():
    result = findings(rule(interface="wan", source="<any></any>", dest="<address>10.0.0.5</address><port>22</port>"))
    assert ("high", "WAN exposes port(s) 22 to the internet") in result


def test_wan_port_range_covering_rdp_is_high():
    result = findings(
        rule(interface="wan", source="<any></any>", dest="<address>10.0.0.5</address><port>3000-4000</port>")
    )
    assert ("high", "WAN exposes port(s) 3389 to the internet") in result


def test_wan_rule_from_trusted_source_is_not_flagged_high():
    result = findings(rule(interface="wan", source="<address>203.0.113.10</address>", dest="<any></any>"))
    assert not [s for s, _ in result if s == "high"]


def test_missing_description_is_low():
    assert ("low", "rule has no description") in findings(rule(descr=""))


def test_disabled_rule_is_low_and_not_otherwise_audited():
    result = findings(rule(interface="wan", source="<any></any>", extra="<disabled></disabled>"))
    assert result == [("low", "disabled rule left in the rule set")]


def test_fail_on_threshold_controls_exit_code(tmp_path):
    path = tmp_path / "rules.xml"
    path.write_text("<filter>" + rule(descr="") + "</filter>", encoding="utf-8")
    assert main([str(path)]) == 0
    assert main([str(path), "--fail-on", "low"]) == 1


def test_json_output(tmp_path, capsys):
    path = tmp_path / "rules.xml"
    path.write_text("<pfsense><filter>" + rule(interface="wan", source="<any></any>") + "</filter></pfsense>")
    assert main([str(path), "--format", "json"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["rules"] == 1
    assert report["findings"][0]["severity"] == "high"


def test_missing_filter_section_is_an_error():
    with pytest.raises(ValueError):
        parse_rules("<pfsense></pfsense>")
