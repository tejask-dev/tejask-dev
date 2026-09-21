#!/usr/bin/env python3
"""Render a GitHub profile calendar from unauthenticated public data (stdlib only)."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import tempfile
from urllib.error import URLError
from urllib.request import Request, urlopen

PROFILE = "tejask-dev"
CALENDAR_URL = f"https://github.com/users/{PROFILE}/contributions"
REPOSITORIES_URL = f"https://api.github.com/users/{PROFILE}/repos?type=owner&per_page=100&sort=full_name"
ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    "dark": {"bg": "#101719", "fg": "#f5f2eb", "muted": "#94a6a2", "line": "#2b3838", "levels": ["#202c2c", "#30574c", "#498c73", "#70bb9b", "#a8e5cd"]},
    "light": {"bg": "#f5f2eb", "fg": "#101719", "muted": "#526761", "line": "#d3ded7", "levels": ["#e3e7e0", "#bbdacb", "#85b9a3", "#4b9479", "#146953"]},
}


class ActivityError(ValueError):
    """A fetch or source validation failed; keep the last good snapshot."""


class CalendarParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.days: dict[date, int] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        # Legend swatches also have data-level, but are not calendar day cells.
        if tag not in ("td", "rect") or "ContributionCalendar-day" not in (attributes.get("class") or "").split():
            return
        if "data-date" not in attributes:
            return  # GitHub's future calendar placeholders have no date.
        try:
            raw_date = attributes["data-date"] or ""
            day = date.fromisoformat(raw_date)
            if day.isoformat() != raw_date:
                raise ValueError("noncanonical date")
            raw_level = attributes.get("data-level")
            if raw_level not in ("0", "1", "2", "3", "4"):
                raise ValueError("intensity must be in 0..4")
            level = int(raw_level)
        except (ValueError, TypeError) as exc:
            raise ActivityError(f"Malformed contribution calendar cell: {attributes.get('data-date')!r}") from exc
        if day in self.days:
            raise ActivityError(f"Duplicate contribution calendar day: {day}")
        self.days[day] = level


def sunday(day: date) -> date:
    return day - timedelta(days=(day.weekday() + 1) % 7)


def parse_calendar(html: str, today: date) -> list[dict[str, str | int]]:
    parser = CalendarParser()
    parser.feed(html)
    first = sunday(today) - timedelta(weeks=52)
    days = sorted((day, level) for day, level in parser.days.items() if first <= day <= today)
    if len(days) < 350 or not days or days[-1][0] != today:
        raise ActivityError("Calendar is incomplete or stale: expected at least 350 days through UTC today")
    expected = (today - days[0][0]).days + 1
    if len(days) != expected:
        raise ActivityError("Calendar contains a date gap; refusing to invent zero-activity days")
    return [{"date": day.isoformat(), "level": level} for day, level in days]


def fetch(url: str, accept: str) -> bytes:
    # Deliberately no token, cookies, gh CLI, or environment credentials.
    request = Request(url, headers={"User-Agent": f"{PROFILE}-profile-activity/1.0", "Accept": accept})
    with urlopen(request, timeout=30) as response:
        body = response.read(8_000_001)
        if len(body) > 8_000_000:
            raise ActivityError("Source response exceeded the size limit")
        return body


def fetch_repositories(fetcher=fetch) -> dict[str, int]:
    repositories = []
    ids: set[int] = set()
    for page in range(1, 101):
        payload = json.loads(fetcher(f"{REPOSITORIES_URL}&page={page}", "application/vnd.github+json"))
        if not isinstance(payload, list):
            raise ActivityError("Repository API did not return a list")
        for repo in payload:
            if not isinstance(repo, dict) or not isinstance(repo.get("id"), int):
                raise ActivityError("Repository API returned a malformed repository")
            if repo.get("private") is not False or repo.get("visibility") not in (None, "public"):
                raise ActivityError("Repository API included a nonpublic repository")
            if repo.get("owner", {}).get("login", "").casefold() != PROFILE.casefold():
                raise ActivityError("Repository API included an unexpected owner")
            if type(repo.get("fork")) is not bool or type(repo.get("archived")) is not bool:
                raise ActivityError("Repository API omitted fork/archive status")
            if repo["id"] in ids:
                raise ActivityError("Repository pagination returned a duplicate")
            ids.add(repo["id"])
            repositories.append(repo)
        if len(payload) < 100:
            break
    else:
        raise ActivityError("Repository pagination exceeded the page limit")
    originals = [repo for repo in repositories if not repo["fork"]]
    return {
        "public_total": len(repositories),
        "public_forks": sum(repo["fork"] for repo in repositories),
        "public_originals": len(originals),
        "archived_public_originals": sum(repo["archived"] for repo in originals),
        "active_public_originals": sum(not repo["archived"] for repo in originals),
    }


def collect_snapshot(today: date, now: datetime, fetcher=fetch) -> dict:
    calendar = parse_calendar(fetcher(CALENDAR_URL, "text/html").decode("utf-8"), today)
    repositories = fetch_repositories(fetcher)
    return {
        "schema_version": 1,
        "profile": PROFILE,
        "fetched_at": now.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "through": today.isoformat(),
        "sources": {
            "contributions": {
                "url": CALENDAR_URL,
                "access": "unauthenticated",
                "meaning": "Visible contribution activity, which may include anonymized private activity. Levels 0-4 are GitHub intensity categories, not exact contribution or commit counts.",
            },
            "repositories": {
                "url": REPOSITORIES_URL,
                "access": "unauthenticated; all pages",
                "meaning": "Public owner repositories. The card counts originals that are neither forks nor archived repositories.",
            },
        },
        "repositories": repositories,
        "days": calendar,
    }


def validate_snapshot(snapshot: dict) -> None:
    if snapshot.get("schema_version") != 1 or snapshot.get("profile") != PROFILE:
        raise ActivityError("Unexpected snapshot schema or profile")
    today = date.fromisoformat(snapshot["through"])
    fetched = datetime.fromisoformat(snapshot["fetched_at"].replace("Z", "+00:00"))
    if fetched.tzinfo is None:
        raise ActivityError("Snapshot timestamp must include a timezone")
    days = snapshot["days"]
    if not isinstance(days, list) or len(days) < 350:
        raise ActivityError("Snapshot calendar is incomplete")
    seen = []
    for entry in days:
        day = date.fromisoformat(entry["date"])
        if day.isoformat() != entry["date"] or type(entry["level"]) is not int or not 0 <= entry["level"] <= 4:
            raise ActivityError("Snapshot has an invalid calendar cell")
        seen.append(day)
    if seen != sorted(set(seen)) or seen[-1] != today or len(seen) != (today - seen[0]).days + 1:
        raise ActivityError("Snapshot dates must be unique, continuous, ordered, and end on its through date")
    if seen[0] < sunday(today) - timedelta(weeks=52):
        raise ActivityError("Snapshot exceeds 53 calendar weeks")
    counts = snapshot["repositories"]
    required = ("public_total", "public_forks", "public_originals", "archived_public_originals", "active_public_originals")
    if any(type(counts.get(key)) is not int or counts[key] < 0 for key in required):
        raise ActivityError("Invalid repository counts")
    if counts["public_total"] != counts["public_forks"] + counts["public_originals"] or counts["public_originals"] != counts["archived_public_originals"] + counts["active_public_originals"]:
        raise ActivityError("Repository counts do not reconcile")
    sources = snapshot["sources"]
    if sources["contributions"]["url"] != CALENDAR_URL or sources["repositories"]["url"] != REPOSITORIES_URL:
        raise ActivityError("Unexpected snapshot provenance")


def date_label(day: date) -> str:
    return f"{day.day} {day.strftime('%b %Y')}"


def render_svg(snapshot: dict, theme: str, mobile: bool = False) -> str:
    validate_snapshot(snapshot)
    palette = THEMES[theme]
    today = date.fromisoformat(snapshot["through"])
    weeks = 26 if mobile else 53
    start = sunday(today) - timedelta(weeks=weeks - 1)
    entries = [(date.fromisoformat(item["date"]), item["level"]) for item in snapshot["days"] if date.fromisoformat(item["date"]) >= start]
    active = sum(level > 0 for _, level in entries)
    first = entries[0][0]
    date_range = f"{date_label(first)} – {date_label(today)}"
    originals = snapshot["repositories"]["active_public_originals"]
    width, height = (640, 704) if mobile else (1200, 446)
    description = f"Visible contribution activity for {PROFILE}: {date_range}. {active} days with visible activity. {originals} public original repositories, excluding forks and archives. GitHub intensity levels are not exact contribution or commit counts. Visible activity may include anonymized private contributions."
    pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
              '<title id="title">The build rhythm.</title>', f'<desc id="description">{escape(description)}</desc>',
              f'<rect width="{width}" height="{height}" rx="18" fill="{palette["bg"]}"/>',
              '<g font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif">']

    def text(x, y, content, size=20, color=None, weight=400, anchor=None):
        anchor_attribute = f' text-anchor="{anchor}"' if anchor else ""
        pieces.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color or palette["fg"]}"{anchor_attribute}>{escape(str(content))}</text>')

    def line(x1, y1, x2, y2):
        pieces.append(f'<path d="M{x1} {y1}H{x2}" stroke="{palette["line"]}"/>')

    if mobile:
        text(32, 45, "VISIBLE CONTRIBUTION ACTIVITY", 21, palette["muted"], 600)
        text(32, 107, "The build rhythm.", 48, weight=600)
        text(32, 149, date_range, 22, palette["muted"])
        line(32, 180, 608, 180)
        text(32, 237, active, 42, palette["levels"][4], 600)
        text(32, 271, "days with activity", 23)
        text(336, 237, originals, 42, palette["levels"][4], 600)
        text(336, 271, "public originals", 23)
        text(336, 299, "excludes forks / archives", 18, palette["muted"])
        chart_x, chart_y, step, cell = 62, 366, 21, 16
        month_y, month_font, weekday_font = 342, 20, 18
    else:
        text(48, 43, "GITHUB / VISIBLE CONTRIBUTION ACTIVITY", 17, palette["muted"], 600)
        text(48, 105, "The build rhythm.", 46, weight=600)
        text(48, 141, date_range, 19, palette["muted"])
        text(750, 87, active, 40, palette["levels"][4], 600)
        text(750, 119, "days with activity", 19)
        text(955, 87, originals, 40, palette["levels"][4], 600)
        text(955, 119, "public originals", 19)
        text(955, 145, "excludes forks / archives", 15, palette["muted"])
        chart_x, chart_y, step, cell = 100, 221, 19, 15
        month_y, month_font, weekday_font = 200, 16, 15
    line(32 if mobile else 48, 558 if mobile else 376, 608 if mobile else 1152, 558 if mobile else 376)
    for row, label in ((1, "M" if mobile else "Mon"), (3, "W" if mobile else "Wed"), (5, "F" if mobile else "Fri")):
        text(chart_x - 14, chart_y + row * step + cell - 2, label, weekday_font, palette["muted"], anchor="end")
    last_month_label_x = -100
    for day, level in entries:
        column = (day - start).days // 7
        row = (day.weekday() + 1) % 7
        x, y = chart_x + column * step, chart_y + row * step
        if day.day == 1 or (day == first and day.day <= 15):
            if x - last_month_label_x >= (64 if mobile else 55) and x < width - 58:
                text(x, month_y, day.strftime("%b"), month_font, palette["muted"])
                last_month_label_x = x
        pieces.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{palette["levels"][level]}"><title>{day.isoformat()}: intensity {level} of 4</title></rect>')
    if mobile:
        text(32, 533, "Intensity", 19, palette["muted"])
        text(342, 533, "Less", 18, palette["muted"])
        legend_x, legend_y, legend_step = 390, 517, 27
        text(539, 533, "More", 18, palette["muted"])
        text(32, 597, "Public GitHub calendar · intensity levels", 20, palette["muted"])
        text(32, 631, "May include anonymized private activity.", 20, palette["muted"])
        text(32, 674, f"Snapshot through {date_label(today)} UTC", 20, palette["muted"])
    else:
        text(48, 411, "Public GitHub calendar · may include anonymized private activity", 17, palette["muted"])
        text(855, 411, "Less", 16, palette["muted"])
        legend_x, legend_y, legend_step = 900, 397, 24
        text(1033, 411, "More", 16, palette["muted"])
        text(1152, 411, "UTC", 15, palette["muted"], anchor="end")
    for level in range(5):
        pieces.append(f'<rect x="{legend_x + level * legend_step}" y="{legend_y}" width="16" height="16" rx="3" fill="{palette["levels"][level]}"/>')
    pieces.extend(["</g>", "</svg>", ""])
    return "\n".join(pieces)


def artifacts(snapshot: dict) -> dict[Path, str]:
    result = {Path("data/activity.json"): json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"}
    for theme in THEMES:
        for mobile in (False, True):
            suffix = "-mobile" if mobile else ""
            result[Path(f"assets/profile/activity-{theme}{suffix}.svg")] = render_svg(snapshot, theme, mobile)
    return result


def write_artifacts(root: Path, outputs: dict[Path, str]) -> list[str]:
    # Prepare every output first; network or validation failures never reach this point.
    pending = []
    try:
        for relative, content in outputs.items():
            target = root / relative
            if target.exists() and target.read_text(encoding="utf-8") == content:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, prefix=f".{target.name}.", delete=False) as handle:
                handle.write(content)
                temp = Path(handle.name)
            pending.append((temp, target))
        for temp, target in pending:
            temp.replace(target)
    finally:
        for temp, _ in pending:
            temp.unlink(missing_ok=True)
    return [str(target.relative_to(root)) for _, target in pending]


def refresh(root: Path = ROOT, now: datetime | None = None, fetcher=fetch) -> list[str]:
    now = now or datetime.now(timezone.utc)
    today = now.astimezone(timezone.utc).date()
    snapshot = collect_snapshot(today, now, fetcher)
    previous_path = root / "data/activity.json"
    if previous_path.exists():
        try:
            previous = json.loads(previous_path.read_text(encoding="utf-8"))
            # An unchanged fetch retains its honest last-change snapshot timestamp.
            if {k: v for k, v in previous.items() if k != "fetched_at"} == {k: v for k, v in snapshot.items() if k != "fetched_at"}:
                snapshot["fetched_at"] = previous["fetched_at"]
        except (OSError, ValueError, KeyError):
            pass
    return write_artifacts(root, artifacts(snapshot))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate committed snapshot and SVGs without network or writes")
    args = parser.parse_args()
    try:
        if args.check:
            snapshot = json.loads((ROOT / "data/activity.json").read_text(encoding="utf-8"))
            expected = artifacts(snapshot)
            mismatches = [str(path) for path, content in expected.items() if not (ROOT / path).exists() or (ROOT / path).read_text(encoding="utf-8") != content]
            if mismatches:
                raise ActivityError("Generated files differ: " + ", ".join(mismatches))
            print("Activity snapshot and four SVG variants are valid and reproducible.")
        else:
            changed = refresh()
            print("Updated: " + ", ".join(changed) if changed else "No public activity changes; files unchanged.")
        return 0
    except (ActivityError, OSError, URLError, ValueError, KeyError, TypeError) as exc:
        print(f"Activity refresh failed; existing snapshot/assets retained: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
