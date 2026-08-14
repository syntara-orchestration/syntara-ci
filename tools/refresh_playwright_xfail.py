#!/usr/bin/env python3
"""Refresh playwright.md with quarantined/skipped tests from currents.dev Actions."""

import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

API_BASE = "https://api.currents.dev/v1"
SYNTARA_E2E_PREFIX = "frontend/packages/syntara-ui/e2e/"


def api_get(api_key, path, params=""):
    url = f"{API_BASE}{path}?{params}" if params else f"{API_BASE}{path}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    if data.get("status") != "OK":
        print(f"API error: {data}", file=sys.stderr)
        sys.exit(1)
    return data


def fetch_actions(api_key, project_id):
    return api_get(api_key, "/actions", f"projectId={project_id}&status[]=active")["data"]


def fetch_title_to_spec(api_key, project_id):
    """Build a title->spec lookup from the Tests Explorer."""
    lookup = {}
    page = 0
    while True:
        data = api_get(
            api_key,
            f"/tests/{project_id}",
            f"date_start=2026-01-01T00:00:00Z&date_end=2099-01-01T00:00:00Z&limit=50&page={page}",
        )
        for t in data["data"]["list"]:
            lookup[t["title"]] = t["spec"]
        next_page = data["data"].get("nextPage")
        if next_page is False or next_page is None:
            break
        page = next_page
    return lookup


def get_spec_files(repo_path, branch):
    """List Playwright spec files from the syntara repo.

    Returns (spec_set, basename_to_path) where basename_to_path maps
    bare filenames to their full relative path when unambiguous.
    """
    result = subprocess.run(
        ["git", "-C", repo_path, "ls-tree", "-r", "--name-only", branch,
         "--", SYNTARA_E2E_PREFIX],
        capture_output=True, text=True, check=True,
    )
    return parse_spec_listing(result.stdout)


def parse_spec_listing(listing):
    """Parse git ls-tree output into (spec_set, basename_map)."""
    specs = set()
    basename_map = {}
    for line in listing.splitlines():
        if line.endswith(".spec.ts"):
            rel = line.removeprefix(SYNTARA_E2E_PREFIX)
            specs.add(rel)
            basename = rel.rsplit("/", 1)[-1]
            if basename != rel:
                if basename in basename_map:
                    basename_map[basename] = None
                else:
                    basename_map[basename] = rel
    return specs, basename_map


def spec_from_heading(heading):
    """Extract the spec file from a heading like 'file.spec.ts: title > path' or 'file.spec.ts'."""
    if ": " in heading:
        file_part = heading.split(": ", 1)[0]
        if file_part.endswith((".spec.ts", ".spec.js")):
            return file_part
    if " > " in heading:
        file_part = heading.split(" > ", 1)[0]
        if file_part.endswith((".spec.ts", ".spec.js")):
            return file_part
    if heading.endswith((".spec.ts", ".spec.js")):
        return heading
    return None


def parse_existing(path):
    """Parse playwright.md into {heading: body} pairs."""
    entries = {}
    try:
        content = path.read_text()
    except FileNotFoundError:
        return entries

    blocks = re.split(r"^# ", content, flags=re.MULTILINE)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 1)
        heading = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        entries[heading] = body
    return entries


def parse_title_from_name(name):
    """Extract the test title from an action name like 'Quarantine test: "Describe,test"'."""
    m = re.search(r'"(.+)"', name)
    if not m:
        return None
    return re.sub(r",(?!\s)", " > ", m.group(1))


def resolve_spec(spec, spec_files, basename_map):
    """Resolve a spec path against the repo, fixing bare basenames."""
    if spec in spec_files:
        return spec
    if "/" not in spec and spec in basename_map and basename_map[spec]:
        return basename_map[spec]
    return spec


def heading_from_action(action, title_to_spec, spec_files, basename_map):
    """Build a playwright.md heading from an action's matcher conditions."""
    conds = action["matcher"]["cond"]
    file_val = None
    title_path = None
    title_val = None

    for c in conds:
        if c["type"] == "file":
            file_val = c["value"]
        elif c["type"] == "titlePath":
            title_path = c["value"]
        elif c["type"] == "title":
            title_val = c["value"]

    if file_val:
        file_val = resolve_spec(file_val, spec_files, basename_map)

    if file_val and title_path:
        return file_val + ": " + " > ".join(title_path)
    if file_val and title_val:
        return file_val + ": " + title_val
    if file_val:
        return file_val

    title = parse_title_from_name(action.get("name", ""))
    if title and title in title_to_spec:
        spec = resolve_spec(title_to_spec[title], spec_files, basename_map)
        return spec + ": " + title
    return None


def body_from_action(action, project_id):
    """Build a body block for a currents.dev action entry."""
    parts = []
    ops = ", ".join(a["op"] for a in action["action"])
    parts.append(f"Action: {ops}")
    if action.get("description"):
        parts.append(action["description"])
    parts.append(
        f"Source: https://app.currents.dev/projects/{project_id}/actions/{action['actionId']}"
    )
    return "\n".join(parts)


def main():
    api_key = os.environ.get("CURRENTS_API_KEY")
    if not api_key:
        print("Error: CURRENTS_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    project_id = os.environ.get("CURRENTS_PROJECT_ID", "F510Y3")
    syntara_repo = os.environ.get("SYNTARA_REPO", str(Path.home() / "git_repos/nexus/syntara"))
    syntara_branch = os.environ.get("SYNTARA_BRANCH", "devel")
    playwright_md = Path(__file__).resolve().parent.parent / "playwright.md"

    existing = parse_existing(playwright_md)
    actions = fetch_actions(api_key, project_id)

    title_to_spec = None
    needs_lookup = any(
        all(c["type"] not in ("file",) for c in a["matcher"]["cond"])
        for a in actions
    )
    if needs_lookup:
        print("Fetching test catalog from Tests Explorer...", file=sys.stderr)
        title_to_spec = fetch_title_to_spec(api_key, project_id)
        print(f"Loaded {len(title_to_spec)} tests", file=sys.stderr)

    spec_files, basename_map = get_spec_files(syntara_repo, syntara_branch)
    print(f"Found {len(spec_files)} spec files in {syntara_branch}", file=sys.stderr)

    skipped = 0
    added = 0
    for action in actions:
        heading = heading_from_action(action, title_to_spec or {}, spec_files, basename_map)
        if not heading:
            skipped += 1
            continue
        if heading in existing:
            continue
        existing[heading] = body_from_action(action, project_id)
        added += 1

    filtered = 0
    final = {}
    for heading, body in existing.items():
        spec = spec_from_heading(heading)
        if spec and spec not in spec_files:
            filtered += 1
            continue
        final[heading] = body

    lines = []
    for heading in sorted(final):
        lines.append(f"# {heading}")
        lines.append("")
        lines.append(final[heading])
        lines.append("")

    playwright_md.write_text("\n".join(lines))

    total = len(final)
    print(
        f"playwright.md: {total} entries ({added} added from currents.dev, "
        f"{skipped} unresolved actions skipped, {filtered} filtered out — spec not in {syntara_branch})"
    )


if __name__ == "__main__":
    main()
