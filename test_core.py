import json
import tempfile
import unittest
from pathlib import Path
from ids_dashboard.core import load_alerts, mark_reviewed

class DashboardCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "alerts.jsonl"
        self.path.write_text(
            json.dumps({"id": "a1", "timestamp": "2026-01-01", "severity": "High", "status": "New"}) + "\n",
            encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_load_alerts(self):
        self.assertEqual(len(load_alerts(self.path)), 1)

    def test_mark_reviewed(self):
        self.assertTrue(mark_reviewed(self.path, "a1"))
        self.assertEqual(load_alerts(self.path)[0]["status"], "Reviewed")

    def test_unknown_id(self):
        self.assertFalse(mark_reviewed(self.path, "missing"))

if __name__ == "__main__":
    unittest.main()
