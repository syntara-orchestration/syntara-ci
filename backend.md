# tests/integration/audit/test_outbox_write_throughput.py::TestTransactionalWritePath::test_baseline_p95_within_threshold

Action: quarantine
Wall-clock p95 latency threshold (`latency.p95 < AUDIT_PERF_P95_BASELINE_MS`) over 200 serial DB commits; sensitive to CI runner/DB load. Baseline not tuned for CI.
Created: 2026-09-11
Issue: AAP-92569

# tests/integration/core/websocket/test_receive_only_channels.py::TestReceiveOnlyChannelIntegration::test_receive_only_channel_stays_alive_until_disconnect

Action: quarantine
Real WebSocket connect + 5 `recv()` calls against a live example server (:9999); server-ready / receive timing race. Failed on unrelated PR #540.
Created: 2026-09-11
Issue: AAP-92610
Source: https://github.com/syntara-orchestration/syntara/actions/runs/34638136897/job/103390997998?pr=540
