# tests/integration/audit/test_outbox_write_throughput.py::TestTransactionalWritePath::test_baseline_p95_within_threshold

Action: quarantine
Wall-clock p95 latency threshold (`latency.p95 < AUDIT_PERF_P95_BASELINE_MS`) over 200 serial DB commits; sensitive to CI runner/DB load. Baseline not tuned for CI.
Created: 2026-09-11
Issue: AAP-92569

# tests/e2e/workflows/test_workflow_execution.py::TestParallelBranches::test_three_parallel_branches_all_complete

Action: quarantine
Created: 2026-09-30
Issue: AAP-95126
Source: https://konflux-ui.apps.kflux-prd-rh03.nnv1.p1.openshiftapps.com/ns/nexus-tenant/applications/ansible-automation-orchestrator-devel/pipelineruns/automation-orchestrator-api-tests-devel-pull-request-bwdz9/logs?task=run-ao-api-tests

# tests/integration/credentials/test_credential_router.py::TestListCredentials::test_list_returns_masked_metadata

Action: quarantine
Consistently returns 0 credentials (expects >=2) under xdist on Python 3.12. Root cause unclear — suspected audit outbox worker singleton state leak between tests. Fix attempted in PR #868.
Created: 2026-10-13

# tests/integration/credentials/test_credential_router.py::TestEnabledFilter::test_filter_enabled_false

Action: quarantine
Consistently returns 0 credentials (expects >=1) under xdist on Python 3.12. Same suspected cause as test_list_returns_masked_metadata above.
Created: 2026-10-13
