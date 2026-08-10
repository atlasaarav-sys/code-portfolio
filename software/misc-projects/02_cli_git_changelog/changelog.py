"""Generates a CHANGELOG.md from git log, grouped by Conventional Commit type."""

import argparse
import re
import subprocess
from collections import defaultdict

COMMIT_TYPE_PATTERN = re.compile(r"^(\w+)(\([^)]*\))?:\s*(.+)$")

TYPE_LABELS = {
    "feat": "Features",
    "fix": "Bug Fixes",
    "docs": "Documentation",
    "refactor": "Refactoring",
    "perf": "Performance",
    "test": "Tests",
    "chore": "Chores",
    "other": "Other",
}
TYPE_ORDER = ["feat", "fix", "perf", "refactor", "docs", "test", "chore", "other"]


def parse_commit_line(line):
    """line format: '<hash>\\x1f<subject>'. Returns (hash, type, scope, subject)."""
    commit_hash, subject = line.split("\x1f", 1)
    match = COMMIT_TYPE_PATTERN.match(subject)
    if match:
        commit_type = match.group(1).lower()
        scope = match.group(2)[1:-1] if match.group(2) else None
        description = match.group(3)
        if commit_type not in TYPE_LABELS:
            commit_type = "other"
            description = subject
    else:
        commit_type = "other"
        scope = None
        description = subject

    return {"hash": commit_hash, "type": commit_type, "scope": scope, "description": description}


def get_git_log(rev_range=None, limit=None):
    args = ["git", "log", "--pretty=format:%h\x1f%s"]
    if limit:
        args += [f"-{limit}"]
    if rev_range:
        args += [rev_range]

    result = subprocess.run(args, capture_output=True, text=True, check=True)
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return [parse_commit_line(line) for line in lines]


def group_commits(commits):
    groups = defaultdict(list)
    for commit in commits:
        groups[commit["type"]].append(commit)
    return groups


def render_changelog(groups, title="Changelog"):
    lines = [f"# {title}", ""]
    for commit_type in TYPE_ORDER:
        commits = groups.get(commit_type)
        if not commits:
            continue
        lines.append(f"## {TYPE_LABELS[commit_type]}")
        lines.append("")
        for commit in commits:
            scope_str = f"**{commit['scope']}**: " if commit["scope"] else ""
            lines.append(f"- {scope_str}{commit['description']} (`{commit['hash']}`)")
        lines.append("")
    return "\n".join(lines)


def get_last_tag():
    result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def main():
    parser = argparse.ArgumentParser(description="Generate a CHANGELOG.md from git history")
    parser.add_argument("--from", dest="from_ref", help="starting ref (default: last tag)")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="ending ref (default: HEAD)")
    parser.add_argument("--last", type=int, help="use the last N commits instead of a ref range")
    parser.add_argument("--output", help="write to this file instead of stdout")
    args = parser.parse_args()

    if args.last:
        commits = get_git_log(limit=args.last)
    else:
        from_ref = args.from_ref or get_last_tag()
        rev_range = f"{from_ref}..{args.to_ref}" if from_ref else args.to_ref
        commits = get_git_log(rev_range=rev_range)

    groups = group_commits(commits)
    changelog = render_changelog(groups)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(changelog)
        print(f"Wrote {len(commits)} commits to {args.output}")
    else:
        print(changelog)


if __name__ == "__main__":
    main()
