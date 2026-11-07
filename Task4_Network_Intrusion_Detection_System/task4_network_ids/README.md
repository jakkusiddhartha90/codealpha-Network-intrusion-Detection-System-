# Task 3 — Network Intrusion Detection System (NIDS)

A beginner-friendly defensive network monitoring project for the cybersecurity internship task.
It combines **Suricata** (network IDS engine), custom detection rules, a Python log collector,
and a small web dashboard. It also includes a safe simulation mode so the dashboard can be
demonstrated without capturing real network traffic.

## What this project does

1. **Monitors network events:** Suricata inspects traffic on a selected network interface.
2. **Detects suspicious activity:** local rules flag examples such as TCP SYN port scans,
   repeated SSH connection attempts, and ICMP echo bursts.
3. **Creates alerts:** Suricata writes JSON events; `scripts/monitor_suricata.py` converts alert
   events into the dashboard's `data/alerts.jsonl` format.
4. **Shows a dashboard:** the Flask app displays alert counts, severity, source/destination IPs,
   signatures, protocols, and timestamps.
5. **Supports response workflow:** alerts can be marked reviewed and the dashboard provides
   recommended containment steps. This project does **not** automatically block traffic;
   response is deliberately human-approved and safe for a student lab.
6. **Includes tests and demo data:** use simulation mode to demonstrate the complete workflow.

## Architecture

```text
Network interface
      |
      v
  Suricata IDS  <--- suricata/rules/local.rules
      |
      v
  eve.json (Suricata JSON event log)
      |
      v
scripts/monitor_suricata.py
      |
      v
data/alerts.jsonl
      |
      v
Flask dashboard (localhost:5000)
```

## Requirements

- Python 3.10 or newer
- Windows 10/11, Kali Linux, or Ubuntu for dashboard/simulation
- Suricata is required only for real network monitoring (best supported on Kali/Ubuntu)
- Use only on networks and devices you own or have permission to monitor.

## A. Run the dashboard in demo mode (Windows or Linux)

### 1. Extract the ZIP
Extract the project folder somewhere easy to find, for example `Desktop/task4_network_ids`.

### 2. Open a terminal in the project folder
In VS Code: **File → Open Folder** → select `task4_network_ids`, then **Terminal → New Terminal**.

### 3. Create a Python virtual environment

Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, run this once in that terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Kali/Ubuntu:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 5. Start the dashboard
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

### 6. Generate demo alerts
Open a second terminal in the same project folder, activate the same virtual environment,
then run:
```bash
python scripts/simulate_alerts.py
```
Refresh the dashboard. You should see sample port-scan, SSH-attempt, and ICMP-burst alerts.
These are synthetic records, not real attacks.

## B. Run with real Suricata alerts (Kali/Ubuntu)

> Only monitor your own lab network or a network for which you have explicit authorization.
> On a shared/public network, do not capture traffic without permission.

### 1. Install Suricata
```bash
sudo apt update
sudo apt install suricata -y
suricata --build-info
```

### 2. Identify your network interface
```bash
ip -br link
```
Common names include `eth0`, `ens33`, or `wlan0`. Use the interface actually connected to
your authorized lab network.

### 3. Validate the included rules
From the project directory:
```bash
sudo suricata -T -c /etc/suricata/suricata.yaml -S suricata/rules/local.rules
```
If your distribution uses a different Suricata config path, locate it with:
```bash
sudo find /etc -name suricata.yaml 2>/dev/null
```

### 4. Start Suricata
Replace `eth0` with your interface:
```bash
sudo suricata -c /etc/suricata/suricata.yaml -S "$PWD/suricata/rules/local.rules" -i eth0 -l "$PWD/logs"
```
Keep this terminal running. Suricata writes `logs/eve.json`.

### 5. Start the collector
In another terminal, activate your Python environment and run:
```bash
python scripts/monitor_suricata.py --input logs/eve.json
```
The collector watches the file and appends Suricata `alert` events to `data/alerts.jsonl`.

### 6. Start the dashboard
In another terminal:
```bash
python app.py
```
Open http://127.0.0.1:5000.

## C. Windows note

The dashboard and demo mode work on Windows. For actual packet inspection, use Suricata on a
supported Linux environment (for example, Kali/Ubuntu in a VM) or install a compatible native
Suricata build and configure its capture driver/interface correctly. A Windows dashboard by
itself does not capture packets.

## Project structure

```text
task4_network_ids/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── ids_dashboard/
│   ├── __init__.py
│   ├── core.py
│   ├── templates/index.html
│   └── static/style.css
├── suricata/rules/local.rules
├── scripts/
│   ├── monitor_suricata.py
│   └── simulate_alerts.py
├── tests/test_core.py
└── data/alerts.jsonl
```

## Detection rule overview

| Rule | Example behavior | Severity |
|---|---|---|
| TCP SYN scan | Many SYN packets to different destination ports | High |
| SSH connection burst | Repeated SSH connection attempts to port 22 | Medium |
| ICMP echo burst | Many ICMP echo requests in a short period | Low |

Rules are heuristic indicators, not proof that a host is compromised. Tune thresholds for your lab.

## Response procedure

1. Review the source and destination IP, signature, timestamp, and protocol.
2. Confirm whether the source is a known scanner, administrator, or approved test system.
3. Preserve the Suricata `eve.json` and dashboard alert record.
4. If suspicious, notify the network owner and isolate the affected lab host using approved controls.
5. Block an IP only after authorization and validation; document who approved the action.
6. Mark the alert reviewed in the dashboard.



