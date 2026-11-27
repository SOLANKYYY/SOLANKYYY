"""Serve Om's public GitHub activity. Fetch once per completed UTC day."""
from datetime import date, datetime, timezone
from http.server import BaseHTTPRequestHandler
import json
from pathlib import Path
import re
import sys
from threading import Lock
from time import monotonic
from urllib.parse import parse_qs, urlsplit
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from activity_chart import render
from github_activity import Activity, DAY, public_calendar, public_commits, summarize_activity
from update_github_stats import accessible_summary, activity_snapshot, public_repositories, request, stat_card

OWNER = "SOLANKYYY"
SNAPSHOT = ROOT / "assets" / "mixtape" / "activity-snapshot.json"
CANONICAL_DATA = "https://solankyyy-profile-mixtape.vercel.app/api/activity?view=data"
lock = Lock()
last_good = None
retry_at = 0.0


def live_data(cutoff):
    repos = public_repositories(OWNER, None)
    calendar = public_calendar(OWNER, cutoff, request)
    commits = public_commits(OWNER, repos, cutoff, request)
    activity = summarize_activity(cutoff, calendar, commits, len(repos))
    return activity_snapshot(activity, repos, "github")


def stored_data(cutoff):
    global last_good, retry_at
    with lock:
        if last_good and last_good["through"] == cutoff.isoformat():
            return last_good
        if monotonic() >= retry_at:
            try:
                data = live_data(cutoff)
            except (OSError, URLError, ValueError, KeyError, TypeError) as error:
                print(f"Public GitHub fetch failed: {type(error).__name__} {error}", flush=True)
                retry_at = monotonic() + 180
            else:
                last_good = data
                retry_at = 0.0
                return data
        fallback = last_good or json.loads(SNAPSHOT.read_text())
        return {**fallback, "source": "snapshot"}


def activity_from(fields):
    values = dict(fields)
    for key in ("as_of", "first_monday", "record_end"):
        if values[key]:
            values[key] = date.fromisoformat(values[key])
    return Activity(**values)


def with_dateline(svg, data):
    """Add a legible caption to either existing chart without overlapping it."""
    root, _, rest = svg.partition(">")
    w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', root).groups())
    root = root.replace(f'0 0 {w} {h}"', f'0 0 {w} {h+30}"')
    svg = root.replace(f'height="{h}"', f'height="{h+30}"') + ">" + rest
    status = "Last verified" if data["source"] == "snapshot" else "Through"
    caption = (f'<rect x="0" y="{h+4}" width="{w}" height="26" rx="7" fill="#181a35"/>'
               f'<text x="13" y="{h+22}" fill="#e8e5ff" font-size="13" '
               f'font-family="Arial,sans-serif">{status} {data["through"]} UTC</text>')
    return svg.replace("</svg>", caption + "</svg>")


def respond(view, mobile, data):
    if view == "data":
        return "application/json; charset=utf-8", json.dumps(data, separators=(",", ":"))
    if view == "text":
        return "text/plain; charset=utf-8", (data["summary"] + "\n" +
                accessible_summary(data["overview"]) + "\nData source: " + data["source"] + "\n")
    if view == "totals":
        svg = stat_card(data["overview"], mobile)
    else:
        svg = render(activity_from(data["activity"]), mobile)
    return "image/svg+xml; charset=utf-8", with_dateline(svg, data)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlsplit(self.path).query)
        view = query.get("view", ["activity"])[0]
        mobile = query.get("layout", ["wide"])[0] == "mobile"
        if view not in {"activity", "data", "text", "totals"}:
            self.send_error(404)
            return
        now = datetime.now(timezone.utc)
        cutoff = now.date() - DAY
        if view == "data":
            data = stored_data(cutoff)
        else:
            # Both charts, both layouts and text share one CDN-cached upstream fetch.
            try:
                data = json.loads(request(CANONICAL_DATA, accept="application/json"))
            except (OSError, URLError, ValueError):
                data = stored_data(cutoff)
        mimetype, content = respond(view, mobile, data)
        until_midnight = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
        ttl = min(until_midnight, 21600) if data["through"] == cutoff.isoformat() and data["source"] == "github" else 180
        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", mimetype)
        self.send_header("Cache-Control", f"public, max-age={min(ttl,300)}")
        self.send_header("Vercel-CDN-Cache-Control", f"public, s-maxage={ttl}, stale-while-revalidate=60")
        self.send_header("X-Data-Through", data["through"])
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
