# pfSense Firewall Lab

A virtualised perimeter firewall built with pfSense CE on VirtualBox: a WAN/LAN
split, a DHCP-served LAN, stateful rules, and runbooks for each step so the
build can be reproduced from scratch.

![pfSense](https://img.shields.io/badge/pfSense-CE-212121?logo=pfsense&logoColor=white)
![VirtualBox](https://img.shields.io/badge/VirtualBox-7-183A61?logo=virtualbox&logoColor=white)
![FreeBSD](https://img.shields.io/badge/FreeBSD-based-AB2B28?logo=freebsd&logoColor=white)

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

- [ ] Segment the LAN with VLANs (users, servers, management) and inter-VLAN rules
- [ ] Suricata IDS on WAN with the ET Open ruleset, alerts to syslog
- [ ] pfBlockerNG IP and DNS blocklists
- [ ] Remote syslog and a Grafana dashboard for rule hits

## Repository layout

```
config/        exported firewall rules (sanitised)
docs/          runbooks: install, rules, VPN, troubleshooting
screenshots/   evidence for each stage of the build
```

## License

[MIT](LICENSE)
