"""Collect the public data for the activity charts. All chart dates are UTC."""
from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from html.parser import HTMLParser
import json
import re
from urllib.error import HTTPError
from urllib.parse import quote, urlencode

DAY = timedelta(days=1)
WINDOW_DAYS = 30
WEEK_COUNT = 12


class CalendarParser(HTMLParser):
    """Join GitHub's dated calendar cells to their exact accessible counts."""

    def __init__(self):
        super().__init__()
        self.cells = {}
        self.labels = {}
        self.tip_ids = ()
        self.tip_text = []

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag in ("td", "rect") and props.get("data-date"):
            day = date.fromisoformat(props["data-date"])
            self.cells[day] = (props.get("aria-label", ""), props.get("aria-labelledby"), props.get("id"))
        if tag == "tool-tip":
            self.tip_ids = (props.get("id"), props.get("for"))
            self.tip_text = []

    def handle_data(self, data):
        if self.tip_ids:
            self.tip_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            for key in filter(None, self.tip_ids):
                self.labels[key] = "".join(self.tip_text).strip()
            self.tip_ids = ()

    def counts(self, start, end):
        result = {}
        for offset in range((end - start).days + 1):
            day = start + offset * DAY
            label, tip, cell = self.cells.get(day, ("", None, None))
            label = label or self.labels.get(tip) or self.labels.get(cell) or ""
            match = re.match(r"^\s*(No|[\d,]+) contributions? on\b", label, re.I)
            if not match:
                raise ValueError(f"Missing contribution count for {day}")
            count = match[1]
            result[day] = 0 if count.lower() == "no" else int(count.replace(",", ""))
        return result


def public_calendar(owner, as_of, request):
    api = "https://api.github.com/users/" + quote(owner)
    created = date.fromisoformat(json.loads(request(api))["created_at"][:10])
    days = {}
    for year in range(created.year, as_of.year + 1):
        start = max(created, date(year, 1, 1))
        end = min(as_of, date(year, 12, 31))
        if end < start:
            continue
        params = urlencode({"from": date(year, 1, 1).isoformat(), "to": end.isoformat()})
        parser = CalendarParser()
        parser.feed(request(f"https://github.com/users/{quote(owner)}/contributions?{params}", accept="text/html"))
        parser.close()
        days.update(parser.counts(start, end))
    return days


def public_commits(owner, repos, as_of, request, token=None):
    """Count each authored SHA once across the owner's public default branches."""
    counts = Counter()
    seen = set()
    first = as_of - (WINDOW_DAYS - 1) * DAY
    for repo in repos:
        if repo["private"] or repo["owner"]["login"].casefold() != owner.casefold():
            continue
        # A repository last pushed before the window cannot have recent pushed commits.
        if repo.get("pushed_at") and repo["pushed_at"][:10] < first.isoformat():
            continue
        page = 1
        while True:
            params = urlencode({
                "author": owner, "sha": repo["default_branch"],
                "since": f"{first}T00:00:00Z", "until": f"{as_of}T23:59:59Z",
                "per_page": 100, "page": page,
            })
            try:
                batch = json.loads(request(f'https://api.github.com/repos/{repo["full_name"]}/commits?{params}', token))
            except HTTPError as exc:
                if exc.code == 409 and "Git Repository is empty" in exc.read().decode():
                    break
                raise
            for commit in batch:
                sha = commit["sha"]
                day = date.fromisoformat(commit["commit"]["committer"]["date"][:10])
                if sha not in seen and first <= day <= as_of:
                    seen.add(sha)
                    counts[day] += 1
            if len(batch) < 100:
                break
            page += 1
    return counts


@dataclass
class Activity:
    as_of: date
    repo_count: int
    current: int
    longest: int
    record_end: date | None
    recent_days: list[int]
    commits: list[int]
    first_monday: date
    weeks: list[list[int]]

    @property
    def active_weeks(self):
        return sum(any(week) for week in self.weeks)

    @property
    def active_days(self):
        return sum(value > 0 for week in self.weeks for value in week)


def summarize_activity(as_of, calendar, commit_counts, repo_count):
    current_run = longest = 0
    last = record_end = None
    for day in sorted(day for day, count in calendar.items() if count > 0 and day <= as_of):
        current_run = current_run + 1 if last == day - DAY else 1
        if current_run > longest:
            longest, record_end = current_run, day
        last = day
    current = current_run if last == as_of else 0
    first_monday = as_of - ((as_of.weekday() + 1) % 7 + WEEK_COUNT * 7 - 1) * DAY
    weeks = [[calendar.get(first_monday + (w * 7 + d) * DAY, 0) for d in range(7)] for w in range(WEEK_COUNT)]
    commits = [commit_counts.get(as_of - offset * DAY, 0) for offset in reversed(range(WINDOW_DAYS))]
    recent = [calendar.get(as_of - offset * DAY, 0) for offset in reversed(range(14))]
    return Activity(as_of, repo_count, current, longest, record_end, recent, commits, first_monday, weeks)
