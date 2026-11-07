import json
from pathlib import Path

def load_alerts(path):
    path = Path(path)
    if not path.exists():
        return []
    alerts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            alerts.append(item)
        except json.JSONDecodeError:
            # Ignore a partially-written or malformed line rather than crashing the UI.
            continue
    alerts.sort(key=lambda item: item.get("timestamp", ""), reverse=True)
    return alerts

def mark_reviewed(path, alert_id):
    path = Path(path)
    alerts = load_alerts(path)
    changed = False
    for alert in alerts:
        if str(alert.get("id")) == str(alert_id):
            alert["status"] = "Reviewed"
            changed = True
    if changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "".join(json.dumps(a, ensure_ascii=False) + "\n" for a in alerts),
            encoding="utf-8"
        )
    return changed
