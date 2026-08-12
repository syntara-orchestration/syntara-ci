# tests/an_example.py::test_some_test

Just an example entry

# tests/integration/audit/test_mixed_workload_contention.py::TestRowLevelLockContention::test_concurrent_drain_workers_skip_locked

- Error: `AssertionError: Drains processed 400 seeded rows total, but only 200 were seeded — SKIP LOCKED may not be working correctly`
- Log: https://github.com/syntara-orchestration/syntara/actions/runs/31630805654/job/94228942309?pr=129
- Jira: https://redhat.atlassian.net/browse/AAP-87600
