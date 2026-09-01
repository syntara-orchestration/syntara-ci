# tests/an_example.py::test_some_test

Just an example entry

# tests/unit/test_xfail_demo.py::test_always_fails

Intentionally broken test to validate the xfail-from-url mechanism

# tests/e2e/workflows/test_workflow_agentic_e2e.py::test_agentic_in_condition_true_branch

Action: quarantine
Failing in the automation-orchestrator-api-tests Konflux PipelineRun (run-ao-api-tests task).
Created: 2026-08-26
Issue: AAP-89731
Source: https://konflux-ui.apps.kflux-prd-rh03.nnv1.p1.openshiftapps.com/ns/nexus-tenant/applications/ansible-automation-orchestrator-devel/pipelineruns/automation-orchestrator-api-tests-devel-pull-request-4cfbc/logs?task=run-ao-api-tests

# tests/e2e/workflows/test_workflow_execution.py::TestNodeFailurePropagation::test_failure_does_not_affect_independent_branch

Action: quarantine
A failure in one fork branch cancels the independent sibling branch: `branch_ok` ends `cancelled` instead of `completed`.
Created: 2026-08-31
Issue: AAP-90400
Source: https://github.com/syntara-orchestration/syntara/pull/458
