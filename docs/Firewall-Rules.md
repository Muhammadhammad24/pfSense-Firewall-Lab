# 📌 pfSense Firewall Rules Configuration

This guide explains how to configure firewall rules to **allow or block traffic**.

## 1️⃣ Create Basic Rules
1. Navigate to **Firewall > Rules**.
2. Choose **LAN** tab and click **Add** to create a rule.
3. Configure:
   - **Action**: Pass
   - **Protocol**: TCP/UDP
   - **Source**: Any
   - **Destination**: Any
   - **Description**: Allow all outbound traffic
4. Click **Save** and **Apply Changes**.

## 2️⃣ Block Unwanted Traffic
- Block access to **specific ports or IPs** by adding **Deny Rules**.
- Example: **Deny traffic to port 22 (SSH) from external sources**.

## 3️⃣ Verify Rules
1. Use `ping` from a client PC to test connectivity.
2. Use **Nmap** to scan for open ports.
