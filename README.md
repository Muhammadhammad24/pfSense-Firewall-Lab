# pfSense Firewall Lab

A virtualised perimeter firewall built with pfSense CE on VirtualBox: a WAN/LAN
split, a DHCP-served LAN, stateful rules, and runbooks for each step so the
build can be reproduced from scratch.

![pfSense](https://img.shields.io/badge/pfSense-CE-212121?logo=pfsense&logoColor=white)
![VirtualBox](https://img.shields.io/badge/VirtualBox-7-183A61?logo=virtualbox&logoColor=white)
![FreeBSD](https://img.shields.io/badge/FreeBSD-based-AB2B28?logo=freebsd&logoColor=white)
[![CI](https://github.com/Muhammadhammad24/pfSense-Firewall-Lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Muhammadhammad24/pfSense-Firewall-Lab/actions/workflows/ci.yml)

## Topology

```mermaid
flowchart LR
    I((Internet)) --- N[VirtualBox NAT]
    N -- em0 · WAN · DHCP --- F{{pfSense}}
    F -- em1 · LAN · 192.168.1.1/24 --- H[Host-only network]
    H --- C1[Client VM]
    H --- C2[Admin workstation<br/>web GUI on :443]
```

| Interface | Adapter      | Addressing                     | Role                        |
| --------- | ------------ | ------------------------------ | --------------------------- |
| `em0`     | NAT          | DHCP from VirtualBox           | WAN, upstream to internet   |
| `em1`     | Host-only    | `192.168.1.1/24`, DHCP server  | LAN, protected client side  |

## What the lab covers

| Area | Implementation | Runbook |
| --- | --- | --- |
| Install | pfSense CE on FreeBSD 64-bit, 2 GB RAM, 10 GB disk, UFS | [Installation](docs/pfSense-Installation.md) |
| Interfaces | WAN on `em0`, LAN on `em1`, default admin credentials rotated at first login | [Installation](docs/pfSense-Installation.md) |
| DHCP and DNS | ISC DHCP on the LAN scope, DNS Resolver for clients | [Screenshots](#screenshots) |
| Firewall policy | Anti-lockout rule for the GUI, LAN egress rules for IPv4 and IPv6, WAN default-deny | [Firewall rules](docs/Firewall-Rules.md) · [export](config/Firewall-Rules-Backup.xml) |
| Remote access | OpenVPN via the pfSense wizard, per-user client export | [VPN setup](docs/VPN-Setup.md) |
| Verification | Reachability with `ping`, exposed ports with `nmap` from outside the LAN | [Troubleshooting](docs/Troubleshooting.md) |

## Reproduce it

1. Create a VM: type **BSD**, version **FreeBSD (64-bit)**, 2 GB RAM, 10 GB disk.
2. Adapter 1 **NAT** (WAN), adapter 2 **Host-only** (LAN). Attach the pfSense ISO.
3. Install with **Auto (UFS)**, reboot, assign `em0` → WAN and `em1` → LAN.
4. Browse to `https://192.168.1.1` from a host-only client, sign in with the
   factory credentials, and **change the admin password immediately**.
5. Apply the rule set from [`config/Firewall-Rules-Backup.xml`](config/Firewall-Rules-Backup.xml)
   under _Diagnostics → Backup & Restore_, area **Firewall Rules**.

Step-by-step detail is in [`docs/`](docs).

## Rule-set audit

[`tools/audit_rules.py`](tools/audit_rules.py) parses an exported rule set and
flags policy mistakes before they reach the firewall:

| Severity | Check |
| --- | --- |
| high | WAN pass rules from any source to any destination |
| high | WAN rules that expose management ports (22, 80, 443, 3389, 8080, 8443), including inside port ranges |
| medium | Any-to-any pass rules on internal interfaces, meaning no egress filtering |
| low | Rules without a description, and disabled rules left in place |
| info | IPv6 pass rules, to confirm IPv6 is intended |

```console
$ python tools/audit_rules.py config/Firewall-Rules-Backup.xml
2 rules, 3 findings
  MEDIUM #1 [lan] Default allow LAN to any rule: lan may reach any destination on any port; consider egress filtering
  MEDIUM #2 [lan] Default allow LAN IPv6 to any rule: lan may reach any destination on any port; consider egress filtering
  INFO   #2 [lan] Default allow LAN IPv6 to any rule: IPv6 traffic is permitted; confirm IPv6 is in use
```

CI runs the unit tests and audits the committed export on every push, and
fails on any high-severity finding (`--fail-on` sets the threshold, and
`--format json` gives machine-readable output). The medium findings above are
the next hardening step on the roadmap.

## Screenshots

| Installer | Interface assignment |
| --- | --- |
| ![Installer](screenshots/pfSense_installation_2.png) | ![Assigning WAN and LAN](screenshots/assign_interfaces.png) |

| DHCP server on LAN | LAN rule set |
| --- | --- |
| ![DHCP server](screenshots/dhcp_setup_1.png) | ![Firewall rules](screenshots/firewall_rules.png) |

<details>
<summary>Full installation sequence</summary>

![Step 1](screenshots/pfSense_installation_1.webp)
![Step 2](screenshots/pfSense_installation_2.png)
![Step 3](screenshots/pfSense_installation_3.png)
![Step 4](screenshots/pfSense_installation_4.png)
![DHCP range](screenshots/dhcp_setup_2.png)

</details>

## Security notes

- Only the firewall-rule section is exported. Full `config.xml` backups contain
  the admin password hash and the web GUI's TLS private key, so they are kept
  out of version control.
- The anti-lockout rule keeps the GUI reachable from the LAN. In production, restrict it to a
  management VLAN or disable it once an explicit admin rule exists.

## Roadmap

- [x] Automated audit of the exported rule set in CI
- [ ] Replace LAN any-to-any with explicit egress rules (DNS, HTTP/S, NTP)
- [ ] Segment the LAN with VLANs (users, servers, management) and inter-VLAN rules
- [ ] Suricata IDS on WAN with the ET Open ruleset, alerts to syslog
- [ ] pfBlockerNG IP and DNS blocklists
- [ ] Remote syslog and a Grafana dashboard for rule hits

## Repository layout

```
config/        exported firewall rules (sanitised)
docs/          runbooks: install, rules, VPN, troubleshooting
tools/         rule-set audit script
tests/         audit tests, run in CI
screenshots/   evidence for each stage of the build
```

## License

[MIT](LICENSE)
