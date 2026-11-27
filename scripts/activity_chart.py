"""Render the same GitHub activity data as wide and stacked SVG cards."""
from html import escape
from math import floor

from github_activity import DAY

HEIGHT = 282
GAP = 12
FONT = "Inter, Arial, Helvetica, sans-serif"
NUMBERS = "Inter, Arial, Helvetica, sans-serif"


def label(x, y, value, size, color, *, weight=400, anchor="start", family=FONT):
    return (f'<text x="{x:g}" y="{y:g}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')


def rect(x, y, width, height, fill, radius=0):
    return f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" rx="{radius:g}" fill="{fill}"/>'


def short_date(day):
    return f"{day:%b} {day.day}"


def span(start, end):
    if start.year != end.year:
        return f"{short_date(start)}, {start.year} – {short_date(end)}, {end.year}"
    if start.month == end.month:
        return f"{short_date(start)}–{end.day}, {end.year}" if start != end else f"{short_date(end)}, {end.year}"
    return f"{short_date(start)} – {short_date(end)}, {end.year}"


def heading(width, title, sub, bg, border, accent, highlight):
    return [
        f'<rect x=".5" y=".5" width="{width-1}" height="{HEIGHT-1}" rx="17" fill="{bg}" stroke="{border}"/>',
        rect(1, 19, 4, 38, highlight, 2),
        label(21, 37, title, 23, "#f5f4ff", weight=700),
        label(22, 59, sub, 14, accent),
    ]


def streak_panel(stats, w):
    pale, hot_pink, lilac = "#fae3f3", "#ff86c2", "#cdaaff"
    out = heading(w, "Contribution streaks", "Consecutive days on GitHub", "#291733", "#814774", pale, hot_pink)
    second = w / 2 + 1
    for x, value, desc, color in [(22, stats.current, "Current streak", hot_pink), (second, stats.longest, "Longest streak", lilac)]:
        out += [label(x, 121, value, 57, color, weight=700, family=NUMBERS), label(x, 143, desc, 16, pale)]
    out += [label(22, 175, "Last 14 days", 14, pale, weight=700),
            label(w-22, 175, "Active day", 12, pale, anchor="end"),
            rect(w-91, 166, 8, 8, hot_pink, 3)]
    step = (w - 44) / 14
    for i, count in enumerate(stats.recent_days):
        day = stats.as_of - (13-i) * DAY
        out.append(f'<g><title>{day} · {count} contributions</title>' +
                   rect(22+i*step, 187, step-3, 13, hot_pink if count else "#573553", 4) + "</g>")
    out += [label(22, 221, short_date(stats.as_of-13*DAY), 12, pale),
            label(w-22, 221, short_date(stats.as_of), 12, pale, anchor="end"),
            rect(22, 239, w-44, 1, "#654060")]
    best = span(stats.record_end-(stats.longest-1)*DAY, stats.record_end) if stats.record_end else "No active days yet"
    out.append(label(22, 262, f"Best run · {best}", 14, lilac))
    return out


def commits_panel(stats, w):
    pale, blue = "#e2eaff", "#83dfff"
    out = heading(w, "Daily commits", "Authored on public default branches", "#141d49", "#515fc5", pale, blue)
    values = stats.commits
    peak = max(values)
    out += [label(22, 121, sum(values), 57, blue, weight=700, family=NUMBERS),
            label(22, 143, "Commits in 30 days", 16, pale),
            label(w-21, 136, f"Peak day · {peak}", 13, "#d5b4ff", anchor="end")]
    axis_max = max(1, peak)
    left, right, top, bottom = 43, w-22, 164, 215
    for y, tick in [(top, axis_max), (bottom, 0)]:
        out += [label(left-6, y+4, tick, 11, pale, anchor="end"), rect(left, y, right-left, 1, "#59679f")]
    step = (right-left) / len(values)
    start = stats.as_of - (len(values)-1)*DAY
    for i, count in enumerate(values):
        bar = (bottom-top) * count / axis_max
        color = "#e2b5ff" if count == peak and peak else "url(#commit-ink)"
        if count == 0:
            color = "#4b5585"
        out.append(f'<g><title>{start+i*DAY} · {count} authored commits</title>' +
                   rect(left+i*step+1, bottom-max(bar, 2), max(1, step-2), max(bar, 2), color, 1.5) + "</g>")
    out += [label(left, 232, short_date(start), 12, pale),
            label(right, 232, short_date(stats.as_of), 12, pale, anchor="end"),
            rect(22, 239, w-44, 1, "#46538c"),
            label(22, 262, f"Across {stats.repo_count} public repositories · UTC", 14, blue)]
    return out


def consistency_panel(stats, w):
    pale, lime = "#eeeaff", "#d8ee8e"
    out = heading(w, "Weekly consistency", "Last 12 complete weeks", "#221e40", "#6459a7", pale, lime)
    out += [label(22, 121, f"{stats.active_weeks} / {len(stats.weeks)}", 51, lime, weight=700, family=NUMBERS),
            label(22, 143, "Weeks with a contribution", 16, pale)]
    left, right, top, step_y = 53, w-22, 157, 9
    step_x = (right-left) / len(stats.weeks)
    for i, weekday in [(0, "Mon"), (3, "Thu"), (6, "Sun")]:
        out.append(label(left-7, top+i*step_y+7, weekday, 10, pale, anchor="end"))
    colors = ("#3c3757", "#7162ab", "#aa9eea", "#d8ee8e")
    for i, week in enumerate(stats.weeks):
        for d, count in enumerate(week):
            day = stats.first_monday + (i*7+d)*DAY
            color = colors[0 if count == 0 else 1 if count < 4 else 2 if count < 8 else 3]
            out.append(f'<g><title>{day} · {count} contributions</title>' +
                       rect(left+i*step_x, top+d*step_y, floor(step_x)-3, 7, color, 2) + "</g>")
    end = stats.first_monday + (7*len(stats.weeks)-1)*DAY
    out += [label(left, 232, short_date(stats.first_monday), 12, pale), label(right, 232, short_date(end), 12, pale, anchor="end"),
            rect(22, 239, w-44, 1, "#534b76"),
            label(22, 262, f"{stats.active_days} of {7*len(stats.weeks)} days active", 14, lime)]
    out.append(label(w-100, 261, "Less", 10, pale, anchor="end"))
    for i, color in enumerate(colors):
        out.append(rect(w-96+i*11, 253, 9, 9, color, 2))
    out.append(label(w-49, 261, "More", 10, pale))
    return out


def day_unit(n):
    return "day" if n == 1 else "days"


def description(stats):
    return (f"Through {stats.as_of} UTC. Current streak {stats.current} {day_unit(stats.current)}, "
            f"longest streak {stats.longest} {day_unit(stats.longest)}. "
            f"{sum(stats.commits)} authored commits in 30 days across {stats.repo_count} public repositories. "
            f"Activity in {stats.active_weeks} of the last {len(stats.weeks)} complete weeks, "
            f"on {stats.active_days} of {7*len(stats.weeks)} days.")


def render(stats, mobile):
    w = 390 if mobile else 334
    width, height = (w, 3*HEIGHT+2*GAP) if mobile else (3*w+2*GAP, HEIGHT)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
           "<title id=\"title\">Om Solanki’s GitHub activity</title>",
           f'<desc id="desc">{escape(description(stats))}</desc>',
           '<defs><linearGradient id="commit-ink" x1="0%" y1="100%" x2="0%" y2="0%"><stop stop-color="#737bff"/><stop offset="1" stop-color="#91e6ff"/></linearGradient></defs>']
    for i, panel in enumerate((streak_panel, commits_panel, consistency_panel)):
        x, y = (0, i*(HEIGHT+GAP)) if mobile else (i*(w+GAP), 0)
        out += [f'<g transform="translate({x} {y})">', *panel(stats, w), "</g>"]
    return "\n".join([*out, "</svg>", ""])
