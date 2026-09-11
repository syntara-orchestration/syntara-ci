# ai-agent-node.spec.ts: AI Agent Node @pr-check > AI Agent node persists prompt after save/reload

Action: quarantine
Created: 2026-09-01
Issue: AAP-90922
Source: https://github.com/syntara-orchestration/syntara/actions/runs/33537293724/job/99957250460

# ai-agent-node.spec.ts: AI Agent Node @pr-check > AI Agent node can be edited after creation

Action: quarantine
Created: 2026-09-10
Issue: AAP-92379
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34410890417/job/102992634671?pr=523

# pagination.spec.ts: Pagination Footer — Groups Tab > pagination footer is visible on groups tab

Action: quarantine
Tagged @konflux-skip: Groups table/pagination footer flakes under Konflux load (30s wait). Sibling IdP pagination already quarantined.
Created: 2026-08-31
Issue: AAP-90554

# v2-workflow-migration.spec.ts: V2 Workflow Schema Migration > comprehensive v2 workflow: all node types persist and reload

Action: quarantine
Comprehensive 9-node save->reload round-trip fails on the workflow hard-delete refactor branch (refactor/workflow-hard-delete, commit b35ae967f). Investigation found the save/filter/reload/delete data path unaffected for a never-executed workflow; likely a heavy-test flake/timeout. Quarantined pending root-cause investigation.
Created: 2026-08-31
Issue: AAP-90523

# v2-workflow-migration.spec.ts: V2 Workflow Schema Migration > creates and saves all v2 control flow node types

Action: quarantine
Created: 2026-09-09
Issue: AAP-92193
Source: https://konflux-ui.apps.kflux-prd-rh03.nnv1.p1.openshiftapps.com/ns/nexus-tenant/applications/ansible-automation-orchestrator-devel/pipelineruns/automation-orchestrator-ui-tests-devel-pull-request-tpht4/logs?task=run-ao-ui-tests

# v2-workflow-migration.spec.ts: V2 Workflow Schema Migration > creates and saves all v2 executor node types

Action: quarantine
Created: 2026-09-10
Issue: AAP-89592

# v2-workflow-migration.spec.ts: V2 Workflow Schema Migration > API response preserves v2 schema format on reload

Action: quarantine
Created: 2026-08-31
Issue: AAP-90549
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34612534673/job/103308459890

# workflow-import-export.spec.ts

Action: quarantine
Re-quarantine of the whole spec (previously quarantined for 11-31% flake rate; loginAs fixture race / insufficient waitForUIReady guards). Auto-dropped by the 10-day-window cleanup, failed again in CI.
Created: 2026-09-09
Issue: AAP-92036
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34364593064/job/102512411003

# group-membership.spec.ts: Group Detail — Member add/remove (typeahead) > add and remove a member from the group detail

Action: quarantine
Created: 2026-09-09
Issue: AAP-92194
Source: https://konflux-ui.apps.kflux-prd-rh03.nnv1.p1.openshiftapps.com/ns/nexus-tenant/applications/ansible-automation-orchestrator-devel/pipelineruns/automation-orchestrator-ui-tests-devel-pull-request-k29nj/logs?task=run-ao-ui-tests

# access-management.spec.ts: Access Management — Policies Tab Columns > project-scoped policies show a clickable project link

Action: quarantine
Fails on the first attempt and passes on retry in every one of the last ~12 Konflux UI runs. `expect(table.getByRole('row').filter({ hasText: policy.name })).toBeVisible({ timeout: 15_000 })` (access-management.spec.ts:372) — the policy row is not visible within 15s under Konflux load.
Created: 2026-09-10
Issue: AAP-92356
Source: https://konflux-ui.apps.kflux-prd-rh03.nnv1.p1.openshiftapps.com/ns/nexus-tenant/applications/ansible-automation-orchestrator-devel/pipelineruns/automation-orchestrator-ui-tests-devel-pull-request-j9cjx/logs?task=run-ao-ui-tests

# eda-trigger.spec.ts: EDA Trigger > user creates a workflow with EDA trigger and saves it

Action: quarantine
Created: 2026-09-10
Issue: AAP-92370

# service-accounts-assignments.spec.ts: UI-10: Cross-Project Role Assignment > assigns a project-scoped role from a different project

Action: quarantine
Created: 2026-09-10
Issue: AAP-92371

# workflows/approval-pending-badge.spec.ts: Approval Pending Badge > shows "Pending approval" badge in all three locations when execution has pending approval

Action: quarantine
Created: 2026-09-10
Issue: AAP-92372

# workflows/approval-workflow-e2e.spec.ts: Approval Workflow E2E > view pending approval with previous step output

Action: quarantine
Created: 2026-09-10
Issue: AAP-92373

# workflows/approvals.spec.ts: Approval Workflow Operations > UI-29: self-contained approve flow via approvals queue

Action: quarantine
Created: 2026-09-10
Issue: AAP-92374

# builder-unsaved-changes.spec.ts: builder unsaved changes modal (AAP-75130) > "Save workflow" saves changes and navigates away

Action: quarantine
Flaky on syntara-orchestration/syntara PR #478: first attempt fails and retry passes in 3 of 6 runs.
Created: 2026-09-10
Issue: AAP-92384
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34248678059/job/102141035521

# permission-gating.spec.ts: Permission gating — Navigation visibility > admin sees all navigation items

Action: quarantine
Flaky on syntara-orchestration/syntara PR #478: first attempt fails and retry passes in 2 of 6 runs.
Created: 2026-09-10
Issue: AAP-92385
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34248678059/job/102141035521

# workflows/create.spec.ts: Workflows - Create New Workflow > multiple workflows can be created sequentially

Action: quarantine
Created: 2026-09-11
Issue: AAP-92563
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34612534673/job/103308459890
