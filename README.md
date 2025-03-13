🚀 pfSense Firewall Lab Setup (VirtualBox)

## 📌 Overview
This project documents the **installation and configuration** of **pfSense** in a **VirtualBox environment**, covering **firewall security, networking, VPN setup, and troubleshooting**. This hands-on setup is ideal for learning **network security** and **system administration**.

---

## 📁 Project Structure
📂 pfSense-Firewall-Lab  
 ├── 📁 docs/  _(Step-by-step installation guide)_  
 ├── 📁 screenshots/  _(Screenshots of the setup)_  
 ├── 📁 config/  _(pfSense backup configuration files)_  
 ├── 🔹 README.md  _(Project description & instructions)_  
 └── 🔹 pfSense-Setup-Guide.md _(Detailed setup guide)_


---

## 🛠️ Features & Configurations
- ✅ Installed **pfSense 2.7.2** in **VirtualBox**  
- ✅ Configured **WAN & LAN interfaces**  
- ✅ Set up **firewall rules** (allow/block traffic)  
- ✅ Enabled **DHCP Server & DNS Resolver**  
- ✅ Created a **VPN tunnel (OpenVPN)**  
- ✅ Used **Wireshark & Nmap for troubleshooting**  

---

## 🔧 Installation & Configuration Guide

### 1️⃣ **Setting up VirtualBox for pfSense**
1. **Download pfSense ISO** from [pfSense Official Site](https://www.pfsense.org/download/)
2. **Create a New Virtual Machine** in VirtualBox:
   - **Type**: BSD  
   - **Version**: FreeBSD (64-bit)  
   - **Memory**: 2GB RAM  
   - **Hard Disk**: 10GB (Dynamically allocated)  
3. **Attach the pfSense ISO** & Start Installation
4. **Configure Virtual Network Adapters:**
   - **Adapter 1 (WAN)** → NAT  
   - **Adapter 2 (LAN)** → Host-Only Adapter  

### 2️⃣ **pfSense Installation Steps**
1. **Boot pfSense from the ISO** and start the installation.
2. Choose **Auto (UFS)** as the partition scheme.
3. Confirm disk formatting and installation.
4. Once installed, **remove the ISO and reboot**.
5. After rebooting, assign **WAN** to em0 and **LAN** to em1.
6. **Access pfSense Web GUI**: Open a browser and go to https://192.168.1.1.
7. Login (default credentials):
   - **Username**: admin
   - **Password**: pfsense

### 3️⃣ **Configuring pfSense Network**
- Change **admin password & set timezone**.
- Configure **WAN Interface** to use DHCP (for internet access).
- Set up **LAN Interface** with static IP (e.g., 192.168.1.1/24).
- Configure **DHCP Server** to assign IPs to LAN clients.
- Enable **DNS Resolver** for name resolution.

### 4️⃣ **Firewall & Security Settings**
- **Create firewall rules** to allow/block specific traffic.
- **Limit access to specific ports** to prevent unauthorized use.
- **Enable VPN for remote secure access** (Optional: OpenVPN).

### 5️⃣ **Troubleshooting & Monitoring**
- Use **Diagnostics > Ping** in pfSense to test connectivity.
- Run **Wireshark** to analyze network packets.
- Use **Nmap** to scan open ports and verify firewall rules.

---

## 📷 Screenshots (Placeholder)
💡 Below are **recommended images** you should include for a complete professional setup:

- ✅ **pfSense Installation Screen** (pfSense_installer.png)
- ✅ **Assigning WAN & LAN Interfaces** (assign_interfaces.png)
- ✅ **pfSense Web Dashboard** (dashboard.png)
- ✅ **Firewall Rules Configuration** (firewall_rules.png)
- ✅ **DHCP Server Setup** (dhcp_setup.png)
- ✅ **VPN Configuration (Optional)** (vpn_config.png)
- ✅ **Wireshark Packet Analysis** (wireshark_analysis.png)

📸 You can either **capture these screenshots** from your setup or find **open-source images** to document the process.

---

## 📝 Notes & Troubleshooting
- **Can't access 192.168.1.1?**
  - Ensure VirtualBox network settings are configured properly.
  - Restart the pfSense VM and check interface assignments.
  - Run ping 8.8.8.8 inside pfSense to test external internet access.

- **Firewall Rules Not Working?**
  - Check the rules under **Firewall > Rules > LAN/WAN**.
  - Ensure the correct **allow/block settings** are applied.

---

## 📌 Why This Project Matters
✅ **Real-world networking experience** with pfSense and firewall security.  
✅ **Demonstrates IT support skills** (troubleshooting, network monitoring).  
✅ **Showcases expertise in virtualization & security**.  
✅ **Great portfolio project for IT Support, Networking, or System Admin roles**.  

---

## 👨‍💻 Author
**[Muhammad Hammad]**  
🔗 LinkedIn: [Your LinkedIn](https://linkedin.com/in/mhammad24)  
🔗 GitHub: [Your GitHub](https://github.com/Muhammadhammad24)  

---

📢 **Want to improve this project?** Feel free to **fork & contribute!** 🚀
