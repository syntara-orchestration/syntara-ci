# tests/an_example.py::test_some_test

Just an example entry

# tests/integration/audit/test_mixed_workload_contention.py::TestRowLevelLockContention::test_concurrent_drain_workers_skip_locked

- Error: `AssertionError: Drains processed 400 seeded rows total, but only 200 were seeded — SKIP LOCKED may not be working correctly`
- Log: https://github.com/syntara-orchestration/syntara/actions/runs/31630805654/job/94228942309?pr=129
- Jira: https://redhat.atlassian.net/browse/AAP-87600

# tests/unit/test_xfail_demo.py::test_always_fails

Intentionally broken test to validate the xfail-from-url mechanism

# tests/e2e/workflows/test_workflow_execution.py::TestNodeFailurePropagation::test_failure_does_not_affect_independent_branch

Action: quarantine
A failure in one fork branch cancels the independent sibling branch: `branch_ok` ends `cancelled` instead of `completed`.
Created: 2026-08-31
Issue: AAP-90400
Source: https://github.com/syntara-orchestration/syntara/pull/458
