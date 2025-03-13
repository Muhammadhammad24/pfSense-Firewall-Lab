# 📌 pfSense Installation Guide

This guide explains how to install pfSense in VirtualBox step-by-step.

## 1️⃣ Download & Setup Virtual Machine
1. Download the pfSense ISO from [pfSense Official Site](https://www.pfsense.org/download/).
2. Open **VirtualBox**, click **New**, and configure:
   - **Name**: pfSense
   - **Type**: BSD
   - **Version**: FreeBSD (64-bit)
   - **Memory**: 2GB RAM
   - **Hard Disk**: 10GB (Dynamically allocated)
3. Attach the pfSense ISO in **Settings > Storage**.

## 2️⃣ Virtual Network Configuration
- **Adapter 1 (WAN)**: Set to **NAT**
- **Adapter 2 (LAN)**: Set to **Host-Only Adapter**

## 3️⃣ Start Installation
1. Boot pfSense from the ISO.
2. Select **Install pfSense** and choose **Auto (UFS)** for disk partitioning.
3. Let the installation complete and **reboot**.
4. Assign **WAN** to `em0` and **LAN** to `em1`.

## 4️⃣ Access pfSense Web UI
1. Open a browser and go to: `https://192.168.1.1`
2. Login with:
   - **Username**: `admin`
   - **Password**: `pfsense`
3. Change default password and set timezone.

---
