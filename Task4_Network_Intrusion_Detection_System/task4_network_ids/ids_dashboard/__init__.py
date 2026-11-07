from pathlib import Path
from .core import load_alerts, mark_reviewed

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config["ALERTS_FILE"] = Path(__file__).resolve().parents[1] / "data" / "alerts.jsonl"

    @app.get("/")
    def index():
        from flask import render_template
        alerts = load_alerts(app.config["ALERTS_FILE"])
        total = len(alerts)
        high = sum(1 for a in alerts if a.get("severity") == "High")
        medium = sum(1 for a in alerts if a.get("severity") == "Medium")
        low = sum(1 for a in alerts if a.get("severity") == "Low")
        return render_template(
            "index.html", alerts=alerts, total=total, high=high, medium=medium, low=low
        )

    @app.post("/review/<alert_id>")
    def review(alert_id):
        from flask import redirect, url_for
        mark_reviewed(app.config["ALERTS_FILE"], alert_id)
        return redirect(url_for("index"))

    return app
