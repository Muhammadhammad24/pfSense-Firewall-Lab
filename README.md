# pfSense Firewall Lab Setup (VirtualBox) 

## 📌 Overview
This project is a **hands-on implementation** of **pfSense**, a powerful open-source firewall, in a **VirtualBox lab environment**. It covers **firewall security, networking, VPN configuration, automation, and security monitoring**—key skills highly valued in **IT, cybersecurity, and network engineering**.

This project demonstrates expertise in **network security, system administration, and automation**, making it a valuable portfolio piece for job applications in **IT support, system administration, cybersecurity, and cloud security roles**.

---

## 📂 Project Structure
```
📂 pfSense-Firewall-Lab  
 ├── 📁 docs/                  # Step-by-step installation guide  
 ├── 📁 screenshots/           # Screenshots of the setup  
 ├── 📁 config/                # pfSense backup configuration files  
 ├── 🔹 README.md              # Project description & instructions  
 └── 🔹 pfSense-Setup-Guide.md  # Detailed setup guide  
```

---

## 🛠️ Key Features & Skills Demonstrated
✔ **Firewall Security:** Implemented firewall rules to allow/block network traffic  
✔ **Network Administration:** Configured WAN & LAN interfaces, VLANs for segmentation  
✔ **VPN & Secure Access:** Set up OpenVPN/IPSec for secure remote access  
✔ **DHCP & DNS Management:** Enabled DHCP Server & DNS Resolver  
✔ **Intrusion Detection & Prevention (IDS/IPS):** Configured Suricata/Snort for security monitoring  
✔ **Network Troubleshooting:** Used Wireshark & Nmap for analysis  
✔ **Automation & Scripting:** Automated firewall rule updates using PowerShell/Bash  
✔ **Security Analysis:** Simulated attack scenarios to test defense mechanisms  

---

## 🔧 Installation & Configuration Guide

### 1️⃣ Setting Up VirtualBox for pfSense
- Download pfSense ISO from the **[Official Site](https://www.pfsense.org/download/)**
- Create a New Virtual Machine in VirtualBox:
  - **Type:** BSD  
  - **Version:** FreeBSD (64-bit)  
  - **Memory:** 2GB RAM  
  - **Hard Disk:** 10GB (Dynamically allocated)  
- Attach the pfSense ISO & Start Installation
- Configure Virtual Network Adapters:
  - **Adapter 1 (WAN):** NAT
  - **Adapter 2 (LAN):** Host-Only Adapter

### 2️⃣ pfSense Installation Steps
- Boot pfSense from the ISO and start the installation.
- Choose **Auto (UFS)** as the partition scheme.
- Confirm disk formatting and installation.
- Once installed, remove the ISO and reboot.
- Assign **WAN to em0** and **LAN to em1**.
- Access the pfSense Web GUI at: **https://192.168.1.1**
- **Login Credentials (default):**
  - **Username:** admin  
  - **Password:** pfsense

### 3️⃣ Configuring pfSense Network
✔ Change admin password & set timezone  
✔ Configure WAN Interface (DHCP for internet access)  
✔ Set LAN Interface with a static IP (e.g., 192.168.1.1/24)  
✔ Enable DHCP Server to assign IPs to LAN clients  
✔ Configure DNS Resolver for name resolution  
✔ **Create VLANs for better network segmentation**  
✔ **Set up site-to-site VPN (OpenVPN/IPSec)**  

### 4️⃣ Firewall & Security Enhancements
✔ Create firewall rules to allow/block specific traffic  
✔ Restrict port access to prevent unauthorized usage  
✔ **Enable intrusion detection system (Suricata/Snort) for security monitoring**  
✔ **Automate firewall rule updates using PowerShell or Bash scripting**  
✔ Enable VPN for secure remote access  
✔ **Monitor security logs and generate alerts for suspicious activity**  

### 5️⃣ Troubleshooting & Monitoring
✔ Use **Diagnostics > Ping** in pfSense to test connectivity  
✔ Run **Wireshark** to analyze network packets  
✔ Use **Nmap** to scan open ports and verify firewall rules  
✔ **Analyze security logs for unusual activity**  
✔ **Set up email alerts for firewall events**  

---

## 📷 Screenshots

### ✅ pfSense Installation Screens
![pfSense Installation - Step 1](screenshots/pfSense_installation_1.png)  
![pfSense Installation - Step 2](screenshots/pfSense_installation_2.png)  
![pfSense Installation - Step 3](screenshots/pfSense_installation_3.png)  
![pfSense Installation - Step 4](screenshots/pfSense_installation_4.png)  

### ✅ Assigning WAN & LAN Interfaces
![Assigning Interfaces](screenshots/assign_interfaces.png)  

### ✅ pfSense Web Dashboard
![pfSense Dashboard](screenshots/dhcp_setup_1.png)  
![pfSense Dashboard - More Config](screenshots/dhcp_setup_2.png)  

### ✅ Firewall Rules Configuration
![Firewall Rules](screenshots/firewall_rules.png)  

### ✅ Wireshark Packet Analysis
![Wireshark Analysis](screenshots/wireshark_analysis.png)  

---

## 📝 Notes & Troubleshooting

### ❌ Can't Access 192.168.1.1?
- Ensure VirtualBox network settings are configured properly.
- Restart the pfSense VM and check interface assignments.
- Run `ping 8.8.8.8` inside pfSense to test external internet access.

### ❌ Firewall Rules Not Working?
- Check the rules under **Firewall > Rules > LAN/WAN**.
- Ensure the correct **allow/block settings** are applied.

---

## 🎯 Why This Project Stands Out
- **Real-world firewall and security implementation experience**, aligning with industry expectations.
- **Demonstrates expertise in enterprise networking, cybersecurity, and automation**.
- **Enhances job applications for IT support, system administration, and security roles**.
- **Practical use of VPNs, VLANs, IDS/IPS, and automated firewall rule management**.
- **Complements cybersecurity certifications like CompTIA Security+, CISSP, or CEH**.
- **Strong addition to GitHub for showcasing practical hands-on skills**.

---

## 👨‍💻 About the Author
🚀 **Muhammad Hammad**  
🔗 **LinkedIn:** [mhammad24](https://linkedin.com/in/mhammad24)  
🔗 **GitHub:** [Muhammadhammad24](https://github.com/Muhammadhammad24)  

---

📢 **Want to contribute?** Feel free to **fork & improve this project!** 🚀
