#!/usr/bin/env python3
"""Drop quarantine entries for tests that are no longer flaky.

The input, ``flaky.tests.json``, is a dump of the ao-triage flakiness report,
generated with::

    ./node_modules/.bin/ao-triage-api flaky.tests > flaky.tests.json

Each ``.items[]`` entry carries ``.trend.lastFailDay`` (the most recent day the
test failed). We keep only the tests that are *still* flaky -- those whose last
failure is within the last ``WINDOW_DAYS`` days -- and strip every H1 section
from ``playwright.md`` / ``backend.md`` whose test is not in that keep-list.

Matching flaky-report ids to the markdown headings:

* backend: heading ``pkg/mod.py::Class::method`` normalizes to the report id
  ``pkg.mod.Class::method`` (``pkg.mod::method`` when there is no class).
* playwright: heading ``file.spec.ts: <title>`` maps to report id
  ``file.spec.ts::<title>``. The report always carries the full title path
  (``Describe > ... > test``); a heading may drop the leading describe blocks,
  so a heading matches when its title equals, or is a trailing ``>``-segment
  of, a kept report title. The report mixes ``>`` and ``›`` separators, so
  both are folded to ``>`` before comparing.
"""

import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WINDOW_DAYS = 10
FILES = {"playwright": ROOT / "playwright.md", "backend": ROOT / "backend.md"}


def norm_title(title):
    """Fold the two title-path separators the report uses into one."""
    return title.replace("›", ">").strip()


def heading_to_backend_id(heading):
    """``pkg/mod.py::Class::method`` -> ``pkg.mod.Class::method``."""
    modpart, rest = heading.split(".py::", 1)
    mod = modpart.replace("/", ".")
    cls, sep, method = rest.partition("::")
    if sep:
        return f"{mod}.{cls}::{method}"
    return f"{mod}::{rest}"


def heading_to_pw(heading):
    """Split a playwright heading into (spec, normalized_title or None)."""
    spec, sep, title = heading.partition(": ")
    if sep and spec.endswith((".spec.ts", ".spec.js")):
        return spec, norm_title(title)
    if heading.endswith((".spec.ts", ".spec.js")):
        return heading, None
    return None, None


def build_keep_sets(items, threshold):
    """From the report items still flaky since ``threshold`` build lookups."""
    backend = set()
    playwright = {}  # spec -> set of normalized titles
    for item in items:
        if (item.get("trend") or {}).get("lastFailDay", "") < threshold:
            continue
        fid = item["id"]
        spec, sep, title = fid.partition("::")
        if spec.endswith((".spec.ts", ".spec.js")) and sep:
            playwright.setdefault(spec, set()).add(norm_title(title))
        else:
            backend.add(fid)
    return backend, playwright


def is_kept(kind, heading, keep_backend, keep_pw):
    if kind == "backend":
        if ".py::" not in heading:
            return False
        return heading_to_backend_id(heading) in keep_backend
    spec, title = heading_to_pw(heading)
    if spec is None:
        return False
    titles = keep_pw.get(spec)
    if not titles:
        return False
    if title is None:
        return True  # whole-file heading: kept if the spec is still flaky
    return any(t == title or t.endswith(" > " + title) for t in titles)


def strip_sections(path, keep_pred):
    """Rewrite ``path`` keeping only H1 sections for which keep_pred is True."""
    lines = path.read_text().split("\n")
    heading_idxs = [i for i, l in enumerate(lines) if l.startswith("# ")]
    heading_idxs.append(len(lines))

    kept, removed = [], []
    for j in range(len(heading_idxs) - 1):
        start, end = heading_idxs[j], heading_idxs[j + 1]
        heading = lines[start][2:].strip()
        if keep_pred(heading):
            kept.append(lines[start:end])
        else:
            removed.append(heading)

    new_text = "\n".join("\n".join(b) for b in kept)
    new_text = new_text.rstrip("\n") + "\n" if new_text.strip() else ""
    path.write_text(new_text)
    return kept, removed


def main():
    items = json.loads((ROOT / "flaky.tests.json").read_text())["items"]
    threshold = (
        datetime.date.today() - datetime.timedelta(days=WINDOW_DAYS)
    ).isoformat()
    keep_backend, keep_pw = build_keep_sets(items, threshold)
    print(f"keeping tests with lastFailDay >= {threshold} "
          f"({len(keep_backend)} backend, {len(keep_pw)} playwright specs)")

    for kind, path in FILES.items():
        kept, removed = strip_sections(
            path, lambda h: is_kept(kind, h, keep_backend, keep_pw)
        )
        print(f"== {path.name} ==")
        print(f"  kept {len(kept)}, removed {len(removed)} of "
              f"{len(kept) + len(removed)} sections")
        for r in removed:
            print(f"    - {r}")


if __name__ == "__main__":
    main()
