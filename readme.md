# 📱 FROGSEC SENTINEL v0.2

**Low-Level Android Monitor for Termux**  
*Powered by Nucleus Binding & Entropy Vectors*

![Android](https://img.shields.io/badge/Android-Termux-green)  
![Python](https://img.shields.io/badge/Python-3.x-blue)

---

FrogSec Sentinel v0.2 quietly scans your Android device in Termux to calculate an **Affinity Score** — a real-time indicator of how "clean" or "exposed" your phone appears.

- 🟢 **GREEN = CLEAN** → Device looks secure  
- 🔴 **RED = WARNING** → Potential anomalies detected  

Think of it as a lightweight security check-up running directly on your device.

## 🚀 One-Click Install (Recommended)

Tap the link below in your Termux session:

[termux://x-exec?url=pkg%20update%20%26%26%20pkg%20upgrade%20-y%20%26%26%20pkg%20install%20python%20git%20-y%20%26%26%20git%20clone%20https%3A%2F%2Fgithub.com%2FBoxfrog1%2FFROGSEC-SENTINEL-v0.2.git%20%26%26%20cd%20FROGSEC-SENTINEL-v0.2%20%26%26%20python%20sentinel.py](termux://x-exec?url=pkg%20update%20%26%26%20pkg%20upgrade%20-y%20%26%26%20pkg%20install%20python%20git%20-y%20%26%26%20git%20clone%20https%3A%2F%2Fgithub.com%2FBoxfrog1%2FFROGSEC-SENTINEL-v0.2.git%20%26%26%20cd%20FROGSEC-SENTINEL-v0.2%20%26%26%20python%20sentinel.py)

## 📋 Manual Installation

**Important:** Use Termux from [F-Droid](https://f-droid.org) — **not** the Play Store version.

Open Termux and run:

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/Boxfrog1/FROGSEC-SENTINEL-v0.2.git
cd FROGSEC-SENTINEL-v0.2
python sentinel.py
```

### Termux:API (Recommended for --real mode)

For full RSSI and network signal data in real mode:

```bash
pkg install termux-api
```

Grant the permission prompt in Android Settings when it appears.

## ▶️ Usage & Modes

```bash
python sentinel.py --mode demo   # Safe mode (no risky system calls)
python sentinel.py --mode real   # Full checks (default, may log warnings)
```

**Default:** real mode

The sentinel launches immediately and displays a live dashboard (updates every 8 seconds). Press **Ctrl + C** to exit.

Logs are saved to `sentinel.log` in the current directory.

## 🔍 How It Works

FrogSec Sentinel samples low-level system signals (seccomp, SELinux, entropy patterns, network indicators) and combines them using proprietary Nucleus Binding logic to produce your Affinity Score.

No data leaves your device. Purely local analysis.

## ⚠️ Notes

- Requires Termux with basic permissions  
- --real mode performs best with Termux:API installed  
- This is **beta software** — results are indicative, not definitive security audits

---

**We watch from the gray. We shield in silence.**

*© 2026 Boxfrog Systems*