from datetime import date
import json
from pathlib import Path
import sys
import unittest
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from github_activity import CalendarParser, DAY, public_commits, summarize_activity


class ActivityTests(unittest.TestCase):
    def test_streak_crosses_year_but_unfinished_week_is_excluded(self):
        friday = date(2027, 1, 1)
        history = {friday - i * DAY: 1 for i in range(4)}
        activity = summarize_activity(friday, history, {}, 2)
        self.assertEqual((activity.current, activity.longest, activity.record_end), (4, 4, friday))
        self.assertEqual((activity.active_weeks, activity.active_days), (0, 0))
        sunday = summarize_activity(friday + 2 * DAY, history, {}, 2)
        self.assertEqual((sunday.current, sunday.longest), (0, 4))
        self.assertEqual((sunday.active_weeks, sunday.active_days), (1, 4))
        self.assertEqual(sunday.first_monday + 83 * DAY, friday + 2 * DAY)

    def test_calendar_requires_exact_counts_even_when_levels_match(self):
        day = date(2026, 11, 25)
        document = '''<td id="a" data-date="2026-11-25" data-level="1" aria-labelledby="ta"></td>
          <td id="b" data-date="2026-11-26" data-level="1"></td>
          <tool-tip id="ta" for="a">3 contributions on November 25th.</tool-tip>
          <tool-tip for="b">1 contribution on November 26th.</tool-tip>'''
        parser = CalendarParser()
        parser.feed(document)
        self.assertEqual(parser.counts(day, day + DAY), {day: 3, day + DAY: 1})
        with self.assertRaisesRegex(ValueError, "2026-11-27"):
            parser.counts(day, day + 2 * DAY)

    def test_commits_page_and_deduplicate_on_public_default_branches(self):
        owner, cutoff = "octocat", date(2026, 11, 25)
        def repo(name, private=False):
            return {"full_name": f"{owner}/{name}", "owner": {"login": owner},
                    "default_branch": "trunk", "private": private}
        def commit(sha, day="2026-11-25"):
            return {"sha": str(sha), "commit": {"committer": {"date": day + "T03:00:00Z"}}}
        def read(url, token):
            parts = urlsplit(url)
            self.assertNotIn("/secret/", parts.path)
            query = parse_qs(parts.query)
            self.assertEqual(query["sha"], ["trunk"])
            self.assertEqual(query["author"], [owner])
            if "/one/" in parts.path and query["page"] == ["1"]:
                return json.dumps([commit(i) for i in range(100)])
            if "/one/" in parts.path:
                return json.dumps([commit(100, "2026-10-27")])
            return json.dumps([commit(0), commit(101, "2026-10-26")])
        counts = public_commits(owner, [repo("one"), repo("fork"), repo("secret", True)], cutoff, read)
        self.assertEqual(counts, {cutoff: 100, date(2026, 10, 27): 1})


if __name__ == "__main__":
    unittest.main()
