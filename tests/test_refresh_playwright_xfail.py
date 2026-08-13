from pathlib import Path

import pytest

from tools.refresh_playwright_xfail import (
    body_from_action,
    heading_from_action,
    parse_existing,
    parse_spec_listing,
    parse_title_from_name,
    resolve_spec,
    spec_from_heading,
)


# -- parse_existing -----------------------------------------------------------


def test_parse_existing_single_entry(tmp_path):
    md = tmp_path / "playwright.md"
    md.write_text("# login.spec.ts: form > submit\n\nflaky on CI\n")
    entries = parse_existing(md)
    assert entries == {"login.spec.ts: form > submit": "flaky on CI"}


def test_parse_existing_multiple_entries(tmp_path):
    md = tmp_path / "playwright.md"
    md.write_text("# one\n\nreason one\n\n# two\n\nreason two\n")
    entries = parse_existing(md)
    assert entries == {"one": "reason one", "two": "reason two"}


def test_parse_existing_empty_body(tmp_path):
    md = tmp_path / "playwright.md"
    md.write_text("# pattern\n")
    entries = parse_existing(md)
    assert entries == {"pattern": ""}


def test_parse_existing_missing_file(tmp_path):
    md = tmp_path / "does-not-exist.md"
    assert parse_existing(md) == {}


def test_parse_existing_multiline_body(tmp_path):
    md = tmp_path / "playwright.md"
    md.write_text("# pattern\n\nline one\nline two\n")
    entries = parse_existing(md)
    assert entries == {"pattern": "line one\nline two"}


# -- parse_title_from_name ----------------------------------------------------


def test_parse_title_comma_separated():
    name = 'Quarantine test: "Cancel Execution,clicking cancel"'
    assert parse_title_from_name(name) == "Cancel Execution > clicking cancel"


def test_parse_title_commas_in_test_name():
    name = 'Quarantine test: "Suite,user adds node, configures, and saves"'
    assert parse_title_from_name(name) == "Suite > user adds node, configures, and saves"


def test_parse_title_no_comma():
    name = 'Quarantine test: "user clears decision"'
    assert parse_title_from_name(name) == "user clears decision"


def test_parse_title_no_quotes():
    assert parse_title_from_name("Quarantine test: no quotes") is None


def test_parse_title_multiple_segments():
    name = 'Quarantine test: "A,B,C"'
    assert parse_title_from_name(name) == "A > B > C"


# -- spec_from_heading --------------------------------------------------------


def test_spec_from_heading_file_colon_title():
    assert spec_from_heading("auth/login.spec.ts: form > submit") == "auth/login.spec.ts"


def test_spec_from_heading_file_angle_title():
    assert spec_from_heading("login.spec.ts > form > submit") == "login.spec.ts"


def test_spec_from_heading_bare_file():
    assert spec_from_heading("login.spec.ts") == "login.spec.ts"


def test_spec_from_heading_no_spec():
    assert spec_from_heading("some random heading") is None


def test_spec_from_heading_js_extension():
    assert spec_from_heading("test.spec.js: suite > test") == "test.spec.js"


def test_spec_from_heading_colon_in_title_not_file():
    assert spec_from_heading("API status: 200 > works") is None


# -- resolve_spec --------------------------------------------------------------


def test_resolve_spec_exact_match():
    specs = {"auth/login.spec.ts"}
    assert resolve_spec("auth/login.spec.ts", specs, {}) == "auth/login.spec.ts"


def test_resolve_spec_basename_remapped():
    specs = {"workflows/builder.spec.ts"}
    basename_map = {"builder.spec.ts": "workflows/builder.spec.ts"}
    assert resolve_spec("builder.spec.ts", specs, basename_map) == "workflows/builder.spec.ts"


def test_resolve_spec_ambiguous_basename():
    specs = {"builder.spec.ts", "workflows/builder.spec.ts"}
    basename_map = {"builder.spec.ts": None}
    assert resolve_spec("builder.spec.ts", specs, basename_map) == "builder.spec.ts"


def test_resolve_spec_unknown():
    assert resolve_spec("deleted.spec.ts", set(), {}) == "deleted.spec.ts"


def test_resolve_spec_already_has_path():
    specs = {"workflows/builder.spec.ts"}
    basename_map = {"builder.spec.ts": "workflows/builder.spec.ts"}
    assert resolve_spec("workflows/builder.spec.ts", specs, basename_map) == "workflows/builder.spec.ts"


# -- parse_spec_listing --------------------------------------------------------


def test_parse_spec_listing_basic():
    listing = (
        "frontend/packages/syntara-ui/e2e/login.spec.ts\n"
        "frontend/packages/syntara-ui/e2e/auth/signup.spec.ts\n"
        "frontend/packages/syntara-ui/e2e/README.md\n"
    )
    specs, basename_map = parse_spec_listing(listing)
    assert specs == {"login.spec.ts", "auth/signup.spec.ts"}
    assert basename_map == {"signup.spec.ts": "auth/signup.spec.ts"}


def test_parse_spec_listing_ambiguous_basename():
    listing = (
        "frontend/packages/syntara-ui/e2e/sub1/builder.spec.ts\n"
        "frontend/packages/syntara-ui/e2e/sub2/builder.spec.ts\n"
    )
    specs, basename_map = parse_spec_listing(listing)
    assert specs == {"sub1/builder.spec.ts", "sub2/builder.spec.ts"}
    assert basename_map == {"builder.spec.ts": None}


def test_parse_spec_listing_root_and_subdir():
    listing = (
        "frontend/packages/syntara-ui/e2e/builder.spec.ts\n"
        "frontend/packages/syntara-ui/e2e/workflows/builder.spec.ts\n"
    )
    specs, basename_map = parse_spec_listing(listing)
    assert specs == {"builder.spec.ts", "workflows/builder.spec.ts"}
    # root-level file doesn't enter basename_map; subdir one does
    assert basename_map == {"builder.spec.ts": "workflows/builder.spec.ts"}


def test_parse_spec_listing_empty():
    specs, basename_map = parse_spec_listing("")
    assert specs == set()
    assert basename_map == {}


# -- heading_from_action -------------------------------------------------------


def _action(matcher_conds, name="test action", ops=None):
    """Helper to build a minimal action dict."""
    return {
        "name": name,
        "action": [{"op": op} for op in (ops or ["quarantine"])],
        "matcher": {"cond": matcher_conds, "op": "AND"},
        "actionId": "abc123",
    }


SPEC_FILES = {"login.spec.ts", "workflows/builder.spec.ts", "auth/signup.spec.ts"}
BASENAME_MAP = {"signup.spec.ts": "auth/signup.spec.ts"}


def test_heading_file_and_titlepath():
    action = _action([
        {"type": "file", "op": "eq", "value": "login.spec.ts"},
        {"type": "titlePath", "op": "eq", "value": ["Suite", "test name"]},
    ])
    result = heading_from_action(action, {}, SPEC_FILES, BASENAME_MAP)
    assert result == "login.spec.ts: Suite > test name"


def test_heading_file_and_title():
    action = _action([
        {"type": "file", "op": "eq", "value": "login.spec.ts"},
        {"type": "title", "op": "eq", "value": "test name"},
    ])
    result = heading_from_action(action, {}, SPEC_FILES, BASENAME_MAP)
    assert result == "login.spec.ts: test name"


def test_heading_file_only():
    action = _action([
        {"type": "file", "op": "eq", "value": "login.spec.ts"},
    ])
    result = heading_from_action(action, {}, SPEC_FILES, BASENAME_MAP)
    assert result == "login.spec.ts"


def test_heading_file_resolved_from_basename():
    action = _action([
        {"type": "file", "op": "eq", "value": "signup.spec.ts"},
        {"type": "titlePath", "op": "eq", "value": ["form"]},
    ])
    result = heading_from_action(action, {}, SPEC_FILES, BASENAME_MAP)
    assert result == "auth/signup.spec.ts: form"


def test_heading_testid_resolved_via_lookup():
    action = _action(
        [{"type": "testId", "op": "eq", "value": "abc-def"}],
        name='Quarantine test: "Suite,test name"',
    )
    title_to_spec = {"Suite > test name": "login.spec.ts"}
    result = heading_from_action(action, title_to_spec, SPEC_FILES, BASENAME_MAP)
    assert result == "login.spec.ts: Suite > test name"


def test_heading_testid_unresolved():
    action = _action(
        [{"type": "testId", "op": "eq", "value": "abc-def"}],
        name='Quarantine test: "Unknown,test"',
    )
    result = heading_from_action(action, {}, SPEC_FILES, BASENAME_MAP)
    assert result is None


def test_heading_testid_no_quotes_in_name():
    action = _action(
        [{"type": "testId", "op": "eq", "value": "abc-def"}],
        name="Quarantine test: no quotes here",
    )
    result = heading_from_action(action, {}, SPEC_FILES, BASENAME_MAP)
    assert result is None


# -- body_from_action ----------------------------------------------------------


def test_body_with_description():
    action = {
        "action": [{"op": "quarantine"}],
        "description": "5% flakiness",
        "actionId": "abc123",
    }
    body = body_from_action(action, "PROJ1")
    assert body == (
        "Action: quarantine\n"
        "5% flakiness\n"
        "Source: https://app.currents.dev/projects/PROJ1/actions/abc123"
    )


def test_body_without_description():
    action = {
        "action": [{"op": "skip"}],
        "description": None,
        "actionId": "xyz789",
    }
    body = body_from_action(action, "PROJ1")
    assert body == (
        "Action: skip\n"
        "Source: https://app.currents.dev/projects/PROJ1/actions/xyz789"
    )


def test_body_multiple_ops():
    action = {
        "action": [{"op": "quarantine"}, {"op": "tag"}],
        "description": None,
        "actionId": "multi",
    }
    body = body_from_action(action, "PROJ1")
    assert "Action: quarantine, tag" in body
