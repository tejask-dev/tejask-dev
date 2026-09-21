#!/usr/bin/env python3
"""Regression checks for public provenance, date correctness, and last-good output."""
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import URLError
import xml.etree.ElementTree as ET

import update_activity as activity


def calendar_html(today, *, missing=None, malformed=None):
    first = today - timedelta(days=365)
    cells = ['<div data-level="4">legend</div>']
    for offset in range(366):
        day = first + timedelta(days=offset)
        if day == missing:
            continue
        level = "bad" if day == malformed else str(offset % 5)
        cells.append(f'<td class="ContributionCalendar-day" data-date="{day}" data-level="{level}"></td>')
    return "<table>" + "".join(cells) + "</table>"


def repository(identifier, *, fork=False, archived=False):
    return {"id": identifier, "private": False, "visibility": "public", "owner": {"login": activity.PROFILE}, "fork": fork, "archived": archived}


class ActivityTests(unittest.TestCase):
    today = date(2024, 3, 1)
    now = datetime(2024, 3, 1, 12, 0, tzinfo=timezone.utc)

    def fetcher(self, url, accept):
        if url == activity.CALENDAR_URL:
            return calendar_html(self.today).encode()
        return json.dumps([repository(1), repository(2, fork=True), repository(3, archived=True)]).encode()

    def snapshot(self):
        return activity.collect_snapshot(self.today, self.now, self.fetcher)

    def test_leap_day_and_sunday_layout_are_preserved(self):
        days = activity.parse_calendar(calendar_html(self.today), self.today)
        self.assertIn("2024-02-29", [day["date"] for day in days])
        self.assertEqual(days[-1]["date"], "2024-03-01")
        self.assertEqual(activity.sunday(date(2024, 3, 3)), date(2024, 3, 3))
        self.assertEqual(activity.sunday(date(2024, 3, 2)), date(2024, 2, 25))
        self.assertLessEqual((self.today - activity.sunday(date.fromisoformat(days[0]["date"]))).days // 7 + 1, 53)

    def test_gaps_and_bad_levels_fail_instead_of_becoming_zero(self):
        for html in (calendar_html(self.today, missing=self.today - timedelta(days=20)), calendar_html(self.today, malformed=self.today - timedelta(days=10))):
            with self.assertRaises(activity.ActivityError):
                activity.parse_calendar(html, self.today)

    def test_duplicate_days_stale_and_noncalendar_responses_fail(self):
        duplicate = f'<td class="ContributionCalendar-day" data-date="{self.today}" data-level="1"></td>'
        for html in (calendar_html(self.today) + duplicate, calendar_html(self.today - timedelta(days=1)), '<html>Rate limit reached</html>'):
            with self.assertRaises(activity.ActivityError):
                activity.parse_calendar(html, self.today)

    def test_calendar_ignores_legend_and_future_cells(self):
        html = calendar_html(self.today) + '<td class="ContributionCalendar-day"></td>'
        html += f'<td class="ContributionCalendar-day" data-date="{self.today + timedelta(days=1)}" data-level="0"></td>'
        self.assertEqual(activity.parse_calendar(html, self.today), activity.parse_calendar(calendar_html(self.today), self.today))

    def test_repository_pages_and_counts_reconcile(self):
        pages = [[repository(i, fork=i % 5 == 0, archived=i % 7 == 0) for i in range(1, 101)], [repository(101)]]
        requested = []
        def fetcher(url, accept):
            requested.append(url)
            return json.dumps(pages[len(requested) - 1]).encode()
        counts = activity.fetch_repositories(fetcher)
        self.assertEqual(counts, {"public_total": 101, "public_forks": 20, "public_originals": 81, "archived_public_originals": 12, "active_public_originals": 69})
        self.assertTrue(requested[0].endswith("page=1"))
        self.assertTrue(requested[1].endswith("page=2"))

    def test_nonpublic_wrong_owner_and_duplicate_repositories_fail(self):
        for mutation in ({"private": True}, {"visibility": "private"}, {"owner": {"login": "someone-else"}}, {"fork": "false"}):
            invalid = repository(1)
            invalid.update(mutation)
            with self.assertRaises(activity.ActivityError):
                activity.fetch_repositories(lambda url, accept: json.dumps([invalid]).encode())
        with self.assertRaises(activity.ActivityError):
            activity.fetch_repositories(lambda url, accept: json.dumps([repository(1), repository(1)]).encode())

    def test_failed_second_fetch_preserves_every_existing_file(self):
        def failing_fetcher(url, accept):
            if url == activity.CALENDAR_URL:
                return self.fetcher(url, accept)
            raise URLError("simulated rate limit")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            activity.refresh(root, self.now, self.fetcher)
            before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
            with self.assertRaises(URLError):
                activity.refresh(root, self.now, failing_fetcher)
            self.assertEqual(before, {path: path.read_bytes() for path in root.rglob("*") if path.is_file()})
            self.assertEqual(len(before), 5)

    def test_bad_source_data_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            activity.refresh(root, self.now, self.fetcher)
            before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
            with self.assertRaises(activity.ActivityError):
                activity.refresh(root, self.now, lambda url, accept: b'<html>maintenance</html>')
            self.assertEqual(before, {path: path.read_bytes() for path in root.rglob("*") if path.is_file()})

    def test_unchanged_refresh_does_not_rewrite_timestamp_or_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(len(activity.refresh(root, self.now, self.fetcher)), 5)
            self.assertEqual(activity.refresh(root, self.now + timedelta(hours=2), self.fetcher), [])
            saved = json.loads((root / "data/activity.json").read_text())
            self.assertEqual(saved["fetched_at"], "2024-03-01T12:00:00Z")

    def test_svg_variants_have_truthful_metrics_and_correct_cell_counts(self):
        snapshot = self.snapshot()
        for theme in activity.THEMES:
            for mobile in (False, True):
                svg = activity.render_svg(snapshot, theme, mobile)
                root = ET.fromstring(svg)
                self.assertEqual(root.attrib["width"], "640" if mobile else "1200")
                self.assertIn("anonymized private", svg)
                self.assertIn("excluding forks and archives", svg)
                cells = [element for element in root.iter("{http://www.w3.org/2000/svg}rect") if list(element)]
                cutoff = activity.sunday(self.today) - timedelta(weeks=25 if mobile else 52)
                expected = sum(date.fromisoformat(entry["date"]) >= cutoff for entry in snapshot["days"])
                self.assertEqual(len(cells), expected)
                self.assertIn("2024-02-29: intensity", svg)
                self.assertNotIn("<script", svg)
                self.assertNotIn("http://", svg.replace("http://www.w3.org/2000/svg", ""))

    def test_snapshot_rejects_tampered_counts_dates_and_levels(self):
        for mutate in (lambda data: data["repositories"].update(public_total=99), lambda data: data["days"][0].update(level=True), lambda data: data["days"].pop(40), lambda data: data.update(profile="other")):
            snapshot = self.snapshot()
            mutate(snapshot)
            with self.assertRaises(activity.ActivityError):
                activity.validate_snapshot(snapshot)


if __name__ == "__main__":
    unittest.main()
