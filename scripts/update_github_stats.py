"""Refresh the profile's GitHub metrics and the accessible text in ReadMe.md."""
from collections import Counter
from datetime import date
from html import escape, unescape
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / "assets" / "studio"
START = "<!-- github-stats:start -->"
END = "<!-- github-stats:end -->"
LANG_COLORS = {
    "HTML": "#ff9c81", "Python": "#86c9ff", "JavaScript": "#f5d76b",
    "Jupyter Notebook": "#efb3ec", "TypeScript": "#77e1d1",
    "Java": "#c3afff", "MATLAB": "#ffbc79", "Other": "#c3c0ce",
}
PALETTE = ("#a5d99f", "#f6c0ce", "#b4c4ff", "#d5c991")


def request(url, token=None, body=None, accept="application/vnd.github+json"):
    headers = {"User-Agent": "profile-statistics", "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, headers=headers, data=json.dumps(body).encode() if body else None)
    with urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8")


def contribution_total(owner, token):
    if token:
        query = "query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions}}}}"
        try:
            data = json.loads(request("https://api.github.com/graphql", token, {"query": query, "variables": {"u": owner}}))
            total = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
            if isinstance(total, int) and total >= 0:
                return total
        except (HTTPError, URLError, ValueError, KeyError, TypeError):
            pass
    # GitHub also publishes this aggregate in the public profile calendar.
    fragment = request(f"https://github.com/users/{quote(owner)}/contributions", accept="text/html")
    plain = " ".join(unescape(re.sub(r"<[^>]+>", " ", fragment)).split())
    match = re.search(r"\b([\d,]+) contributions? in the last year\b", plain, re.I)
    if not match:
        raise ValueError("GitHub did not return a contribution total. Existing graphics have been preserved.")
    return int(match[1].replace(",", ""))


def collect(owner):
    token = os.environ.get("GH_TOKEN")
    repos = []
    page = 1
    while True:
        batch = json.loads(request(f"https://api.github.com/users/{quote(owner)}/repos?type=owner&sort=full_name&per_page=100&page={page}", token))
        repos.extend(r for r in batch if not r["private"] and r["owner"]["login"].casefold() == owner.casefold())
        if len(batch) < 100:
            break
        page += 1
    return summarize(repos, contribution_total(owner, token))


def summarize(repos, contributions):
    counts = Counter(r.get("language") or "Unclassified" for r in repos)
    ordered = sorted(counts.items(), key=lambda v: (-v[1], v[0]))
    return {
        "repos": len(repos), "stars": sum(r["stargazers_count"] for r in repos),
        "forks": sum(r["forks_count"] for r in repos), "contributions": contributions,
        "language_count": len(counts) - int("Unclassified" in counts), "languages": ordered,
    }


def labels(stats):
    values = [
        (stats["repos"], "Public repositories"),
        (stats["stars"], "Stars received"),
        (stats["forks"], "Forks received"),
    ]
    activity = stats["contributions"]
    return values + ([(activity, "Contributions · 12 mo")] if activity is not None else [(stats["language_count"], "Primary languages")])


def language_rows(stats):
    rows = stats["languages"]
    if len(rows) > 8:
        rows = rows[:7] + [("Other", sum(count for _, count in rows[7:]))]
    return [(name, count, LANG_COLORS.get(name, PALETTE[i % len(PALETTE)])) for i, (name, count) in enumerate(rows)]


def text(x, y, value, size, color, weight=400, family="Arial,sans-serif"):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>'


def accessible_summary(stats):
    total = stats["contributions"]
    fork_unit = "fork" if stats["forks"] == 1 else "forks"
    parts = [f'{stats["repos"]} public repositories', f'{stats["stars"]} stars received', f'{stats["forks"]} {fork_unit} received']
    if total is not None:
        parts.append(f"{total:,} contributions in the past 12 months")
    names = ", ".join(f"{name} {count}" for name, count in stats["languages"])
    return ". ".join([", ".join(parts), "Repositories by primary language — " + (names or "none")]) + "."


def stat_card(stats, mobile):
    cols = 2 if mobile else 4
    w, padding, step = (456, 23, 207) if mobile else (1000, 32, 240)
    values_y = 58 if mobile else 74
    lang_y = 230 if mobile else 151
    row_height = 27 if mobile else 26
    rows = language_rows(stats)
    legend_y = lang_y + 54
    height = legend_y + row_height * ((len(rows) + cols - 1) // cols) + 12
    if not rows:
        height = legend_y + 18
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" role="img" aria-labelledby="t d">',
             '<title id="t">GitHub stats for Om Solanki</title>',
             f'<desc id="d">{escape(accessible_summary(stats))}</desc>',
             f'<rect width="{w}" height="{height}" rx="17" fill="#211d35"/>']
    for index, ((value, label), color) in enumerate(zip(labels(stats), ("#ffcca8", "#c8b6ff", "#9debd5", "#ffc1e0"))):
        x = padding + index % cols * step
        y = values_y + index // cols * 91
        parts.append(text(x, y, f"{value:,}", 47 if mobile else 58, color, 700, "Georgia,serif"))
        parts.append(text(x, y + 26, label, 16 if mobile else 18, "#f5eefa"))
    parts.extend([f'<path d="M{padding} {lang_y-30}H{w-padding}" stroke="#4e4664"/>',
                  text(padding, lang_y, "Primary language by public repository", 18 if mobile else 20, "#f3edf9", 600)])
    bar_width = w - 2 * padding
    parts.append(f'<defs><clipPath id="bar"><rect x="{padding}" y="{lang_y+13}" width="{bar_width}" height="12" rx="6"/></clipPath></defs><g clip-path="url(#bar)">')
    x = float(padding)
    for _, count, color in rows:
        span = bar_width * count / stats["repos"]
        parts.append(f'<rect x="{x:.2f}" y="{lang_y+13}" width="{span+.05:.2f}" height="12" fill="{color}"/>')
        x += span
    parts.append("</g>")
    for i, (name, count, color) in enumerate(rows):
        x = padding + i % cols * step
        y = legend_y + i // cols * row_height
        parts.append(f'<rect x="{x}" y="{y-10}" width="9" height="9" rx="2" fill="{color}"/>')
        parts.append(text(x+17, y, f"{name} · {count}", 15 if mobile else 16, "#efe9f7"))
    if not rows:
        parts.append(text(padding, legend_y, "No public repositories", 16, "#efe9f7"))
    return "\n".join(parts + ["</svg>", ""])


def write_stats(stats, owner):
    readme = ROOT / "ReadMe.md"
    current = readme.read_text(encoding="utf-8")
    if current.count(START) != 1 or current.count(END) != 1:
        raise ValueError("ReadMe.md must contain one GitHub stats block.")
    before, _, after_start = current.partition(START)
    old_block, _, after = after_start.partition(END)
    alt = escape(accessible_summary(stats), quote=True)
    figures = {"github-stats.svg": stat_card(stats, False), "github-stats-mobile.svg": stat_card(stats, True)}
    # Date the snapshot only when the displayed information changes.
    stamp = re.search(r"Snapshot from GitHub on (\d{4}-\d{2}-\d{2})", old_block)
    unchanged = all((STUDIO / name).is_file() and (STUDIO / name).read_text(encoding="utf-8") == content for name, content in figures.items())
    snapshot_date = stamp[1] if stamp and unchanged else date.today().isoformat()
    base = f"https://raw.githubusercontent.com/{owner}/{owner}/main/assets/studio"
    block = f'''
<picture>
  <source media="(max-width: 760px)" srcset="{base}/github-stats-mobile.svg">
  <img src="{base}/github-stats.svg" width="100%" alt="{alt}">
</picture>

Snapshot from GitHub on {snapshot_date}. [Public repositories](https://github.com/{owner}?tab=repositories) · [Contribution calendar](https://github.com/{owner}#js-contribution-activity-description)
'''
    updated = before + START + "\n" + block + "\n" + END + after
    for name, content in figures.items():
        path = STUDIO / name
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
    if updated != current:
        readme.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    owner = os.environ.get("GITHUB_REPOSITORY_OWNER", "SOLANKYYY")
    write_stats(collect(owner), owner)
