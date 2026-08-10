import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from changelog import parse_commit_line, group_commits, render_changelog


class TestChangelog(unittest.TestCase):
    def test_parses_conventional_commit_with_scope(self):
        commit = parse_commit_line("abc123\x1ffeat(api): add pagination to /notes")
        self.assertEqual(commit["type"], "feat")
        self.assertEqual(commit["scope"], "api")
        self.assertEqual(commit["description"], "add pagination to /notes")
        self.assertEqual(commit["hash"], "abc123")

    def test_parses_conventional_commit_without_scope(self):
        commit = parse_commit_line("def456\x1ffix: correct off-by-one in pagination")
        self.assertEqual(commit["type"], "fix")
        self.assertIsNone(commit["scope"])

    def test_non_conventional_commit_falls_back_to_other(self):
        commit = parse_commit_line("ghi789\x1fWIP: messing around")
        self.assertEqual(commit["type"], "other")
        self.assertEqual(commit["description"], "WIP: messing around")

    def test_unknown_type_falls_back_to_other(self):
        commit = parse_commit_line("jkl012\x1fbanana: not a real conventional commit type")
        self.assertEqual(commit["type"], "other")

    def test_group_and_render(self):
        commits = [
            parse_commit_line("h1\x1ffeat: add login"),
            parse_commit_line("h2\x1ffix: crash on empty input"),
            parse_commit_line("h3\x1ffeat: add logout"),
        ]
        groups = group_commits(commits)
        self.assertEqual(len(groups["feat"]), 2)
        self.assertEqual(len(groups["fix"]), 1)

        rendered = render_changelog(groups)
        self.assertIn("## Features", rendered)
        self.assertIn("## Bug Fixes", rendered)
        self.assertIn("add login", rendered)
        self.assertIn("(`h1`)", rendered)
        # Features section should come before Bug Fixes per TYPE_ORDER.
        self.assertLess(rendered.index("## Features"), rendered.index("## Bug Fixes"))


if __name__ == "__main__":
    unittest.main()
