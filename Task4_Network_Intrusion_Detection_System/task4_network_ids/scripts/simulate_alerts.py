#!/usr/bin/env python3
"""Create clearly labelled synthetic alerts for a safe project demonstration."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
import uuid

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "alerts.jsonl"

DEMO = [
    ("High", "Possible TCP SYN port scan", "Attempted reconnaissance", "192.0.2.25", "192.0.2.10", "TCP"),
    ("Medium", "Repeated SSH connection attempts", "Possible attempted administration", "198.51.100.44", "192.0.2.10", "TCP"),
    ("Low", "ICMP echo request burst", "Possible denial-of-service indicator", "203.0.113.18", "192.0.2.10", "ICMP"),
]

def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    with OUT.open("a", encoding="utf-8") as f:
        for index, (severity, signature, category, src, dst, proto) in enumerate(DEMO):
            item = {
                "id": str(uuid.uuid4()),
                "timestamp": (now - timedelta(minutes=index * 3)).isoformat(timespec="seconds"),
                "severity": severity,
                "signature": signature,
                "category": category,
                "src_ip": src,
                "dest_ip": dst,
                "protocol": proto,
                "status": "New",
                "source": "SIMULATION — not real traffic"
            }
            f.write(json.dumps(item) + "\n")
    print(f"[+] Added {len(DEMO)} synthetic demo alerts to {OUT}")
    print("[!] These are simulated examples, not evidence of real attacks.")

if __name__ == "__main__":
    main()
