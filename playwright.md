# ai-agent-node.spec.ts: AI Agent Node @pr-check > AI Agent node persists prompt after save/reload

Action: quarantine
Created: 2026-09-01
Issue: AAP-90922
Source: https://github.com/syntara-orchestration/syntara/actions/runs/33537293724/job/99957250460

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

# workflow-import-export.spec.ts

Action: quarantine
Re-quarantine of the whole spec (previously quarantined for 11-31% flake rate; loginAs fixture race / insufficient waitForUIReady guards). Auto-dropped by the 10-day-window cleanup, failed again in CI.
Created: 2026-09-09
Issue: AAP-92036
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34364593064/job/102512411003
