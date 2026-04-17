# ARP Spoof Detector 🛡️

A lightweight, real-time Python network utility designed to detect ARP Spoofing (ARP Poisoning) attacks on your local network. It monitors ARP traffic, maintains a local cache of IP-to-MAC pairings, and alerts you instantly if a mismatch is detected, signaling a potential Man-in-the-Middle (MitM) attack.

## 🚀 Features

- **Real-Time Detection:** Live packet sniffing using `scapy` with minimal overhead.
- **Dynamic MAC Tracking:** Learns IP-to-MAC associations dynamically and alerts on changes.
- **Static Whitelist:** Pre-define known, trusted devices (like routers or NAS) to prevent false positives.
- **Persistent Logging:** Writes all spoofing alerts to `arp_alerts.log` for auditing.
- **Colorized Alerts:** Immediate, highly visible console warnings using `colorama`.
- **Self-Aware:** Automatically excludes its own interface's MAC to prevent self-triggering alerts.

## 🛠️ Prerequisites

- **Python 3.x**
- **Root/Administrator Privileges:** Required for sniffing network packets (`sudo`).
- External Libraries: `scapy`, `colorama`

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/arp-spoof-detector.git
   cd arp-spoof-detector
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install scapy colorama
   ```

## 💻 Usage

> **Note:** Since this script captures raw packets, you must run it with elevated privileges (i.e., `sudo` on Linux/Ubuntu).

1. **List available network interfaces:**
   ```bash
   sudo python3 main.py --list-interfaces
   ```

2. **Start monitoring an interface** (e.g., `eth0` or `en0`):
   ```bash
   sudo python3 main.py -i eth0
   ```

3. **Stop monitoring:**
   Press `Ctrl+C`. A session summary will be automatically generated, displaying packets analyzed, alerts triggered, and the final IP-to-MAC table.

### Configuring the Whitelist
To prevent false alarms for known, safe static IP assignments on your network, edit `whitelist.py`:
```python
STATIC_WHITELIST = {
    "192.168.1.1":   "aa:bb:cc:dd:ee:ff",  # Router
}
```

## 📸 Screenshots & Attack Flow

*(Waiting for screenshots. The standard flow usually involves a victim and an attacker machine using tools like `arpspoof` or `ettercap` on Ubuntu/VirtualBox. The detector script will flash a red alert when the MAC address for a known IP abruptly changes.)*

1. **Normal Network State:** The detector safely tracks ARP requests.
   <!-- INSERT NORMAL STATE SCREENSHOT HERE -->

2. **Attack Initiated:** An attacker (e.g., from an Ubuntu VM) sends forged ARP replies.
   <!-- INSERT ATTACK GENERATION SCREENSHOT HERE -->

3. **Detection & Logging:** The detector catches the new conflicting MAC address and alerts the user.
   <!-- INSERT ALERT SCREENSHOT HERE -->

## 📝 Logging

Alerts are saved in `arp_alerts.log` in the following format:
```
2026-04-17 10:30:15  WARNING  SPOOF ip=192.168.1.5 known_mac=aa:bb:cc:dd:ee:11 claimed_mac=ff:ee:dd:cc:bb:22
```

## ⚠️ Disclaimer

This tool is strictly for educational and defensive purposes. Always ensure you have explicit permission to monitor traffic on the network you are on.

## 🤝 Contributing
Pull requests are welcome! Feel free to open an issue if you encounter any bugs or want to suggest new features.
