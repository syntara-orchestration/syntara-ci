# syntara-xfail

Centralized xfail list for the Syntara test suites, maintained by @syntara-ci-stability.

## Format

Each `.md` file corresponds to a test suite (e.g. `backend.md`). Tests to mark
as xfail are listed as H1 headings with the full pytest node-id. The text below
each heading explains the reason:

```markdown
# tests/e2e/workflows/test_wait_node.py::test_wait_node_zero_duration_fails

orchestration bug: _process_node_result swallows failed-status dicts
```

## Usage

### Backend (pytest)

The Syntara backend Makefile fetches `backend.md` automatically and passes it to
pytest via `--xfail-from-url`. To override or disable:

```bash
# Use the default xfail list (automatic)
make test-e2e

# Override with a different URL
make test-e2e XFAIL_URL=https://raw.githubusercontent.com/…/backend.md

# Disable xfail entirely
make test-e2e XFAIL_URL=
```

### Frontend (Playwright)

Set the `SYNTARA_PLAYWRIGHT_XFAIL_SOURCE` environment variable to point at `playwright.md`.
The Playwright fixture fetches the file once per worker and marks matching tests
as expected failures via `test.fail()`. Test identifiers use the format
`file.spec.ts > Describe block > test name`.

```bash
# Run with xfail list
SYNTARA_PLAYWRIGHT_XFAIL_SOURCE=https://raw.githubusercontent.com/…/playwright.md npx playwright test

# Disable (default — no env var)
npx playwright test
```
