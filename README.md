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

Set `SYNTARA_XFAIL_SOURCE` to a base URL or local folder path. Both the backend
and frontend append their own filename (`backend.md` / `playwright.md`).

```bash
# URL (CI default)
export SYNTARA_XFAIL_SOURCE=https://raw.githubusercontent.com/syntara-orchestration/syntara-ci/refs/heads/main/

# Local folder
export SYNTARA_XFAIL_SOURCE=./path/to/xfail/
```

### Backend (pytest)

The Makefile reads `SYNTARA_XFAIL_SOURCE`, appends `backend.md`, and passes the
result to pytest via `--xfail-from-url`:

```bash
# Use the CI xfail list
SYNTARA_XFAIL_SOURCE=https://raw.githubusercontent.com/…/ make test-e2e

# Use a local folder
SYNTARA_XFAIL_SOURCE=./xfail/ make test-e2e

# Disable xfail entirely (default when unset)
make test-e2e
```

### Frontend (Playwright)

The Playwright fixture reads `SYNTARA_XFAIL_SOURCE`, appends `playwright.md`,
and fetches the file once per worker. Matching tests are marked as expected
failures via `test.fail()`. Test identifiers use the format
`file.spec.ts > Describe block > test name`.

```bash
# Run with xfail list
SYNTARA_XFAIL_SOURCE=https://raw.githubusercontent.com/…/ npx playwright test

# Disable (default — no env var)
npx playwright test
```
