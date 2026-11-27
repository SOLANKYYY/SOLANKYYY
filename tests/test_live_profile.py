import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "api"))
import activity


class PublicProfileTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads(activity.SNAPSHOT.read_text())

    def test_both_chart_layouts_keep_data_date_visible(self):
        for view in ("activity", "totals"):
            for mobile in (True, False):
                with self.subTest(view=view, mobile=mobile):
                    content_type, payload = activity.respond(view, mobile, self.snapshot)
                    svg = ElementTree.fromstring(payload)
                    self.assertIn("image/svg+xml", content_type)
                    self.assertIn("Last verified " + self.snapshot["through"] + " UTC", payload)
                    self.assertEqual(svg.get("height"), svg.get("viewBox").split()[-1])

    def test_failure_serves_dated_snapshot_and_recovers(self):
        cutoff = activity.date.fromisoformat(self.snapshot["through"])
        fresh = {**self.snapshot, "source": "github"}
        with (patch.object(activity, "last_good", None),
              patch.object(activity, "retry_at", 0),
              patch.object(activity, "monotonic", side_effect=[3, 4, 5, 300]),
              patch.object(activity, "live_data", side_effect=[OSError("unavailable"), fresh]) as fetch):
            self.assertEqual(activity.stored_data(cutoff)["source"], "snapshot")
            self.assertEqual(activity.stored_data(cutoff)["source"], "snapshot")
            self.assertEqual(activity.stored_data(cutoff)["source"], "github")
            self.assertEqual(activity.stored_data(cutoff)["source"], "github")
            self.assertEqual(fetch.call_count, 2)
