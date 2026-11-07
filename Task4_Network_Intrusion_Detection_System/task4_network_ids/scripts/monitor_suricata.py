#!/usr/bin/env python3
"""Follow Suricata eve.json and copy alert events into the dashboard JSONL file."""
import argparse
import json
import time
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "alerts.jsonl"

def normalize(event):
    alert = event.get("alert", {})
    severity_number = alert.get("severity", 3)
    severity = {1: "High", 2: "Medium", 3: "Low"}.get(severity_number, "Low")
    return {
        "id": f"suricata-{event.get('flow_id', '')}-{event.get('timestamp', '')}",
        "timestamp": event.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "severity": severity,
        "signature": alert.get("signature", "Suricata alert"),
        "category": alert.get("category", "Network activity"),
        "src_ip": event.get("src_ip", "-"),
        "dest_ip": event.get("dest_ip", "-"),
        "protocol": event.get("proto", "-"),
        "status": "New",
        "source": "Suricata"
    }

def follow(input_path, output_path=OUTPUT):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"[+] Watching {input_path} for Suricata alert events")
    print(f"[+] Dashboard data: {output_path}")
    # Start at end so old events are not re-imported every run.
    with input_path.open("r", encoding="utf-8", errors="replace") as source:
        source.seek(0, 2)
        while True:
            line = source.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("event_type") != "alert":
                continue
            record = normalize(event)
            with output_path.open("a", encoding="utf-8") as dest:
                dest.write(json.dumps(record) + "\n")
            print(f"[ALERT] {record['severity']} | {record['signature']} | {record['src_ip']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect Suricata EVE alert events")
    parser.add_argument("--input", default="logs/eve.json", help="Path to Suricata eve.json")
    args = parser.parse_args()
    follow(args.input)
