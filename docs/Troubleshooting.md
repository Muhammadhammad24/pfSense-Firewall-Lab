# Troubleshooting Common pfSense Issues

## 1. Can't access `192.168.1.1`?
- Ensure VirtualBox **network settings** are correct.
- Restart pfSense VM and check **interface assignments**.
- Run `ping 8.8.8.8` inside pfSense to test internet access.

## 2. Firewall rules not working?
- Check **Firewall > Rules > LAN/WAN**.
- Ensure **rules are applied correctly** and ports are not blocked.
