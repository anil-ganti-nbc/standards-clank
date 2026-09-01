# watch-clank — M4E OPS-COM-003 closure re-audit

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[]}
```

Read-only source re-audit of Watch `c192e799babf687eb98708a5bfd900b4f7c9aac2`
against Standards `48b4cafb5c761dc84d621efa3354b42b6cc28423`. Both trees
were clean at takeover. No Watch source, host, deployment, frozen standard,
tag, or known-evidence index was changed.

## Result

| State | Count |
|---|---:|
| CONFORMS | 23 |
| NON_CONFORMING | 1 |
| INSUFFICIENT_EVIDENCE | 1 |

The frozen resolver still classifies all 25 standards as APPLIES. The 22
previous conformances remain conforming; OPS-COM-004 remains CLOSED. DEPLOY-
COM-001 remains LIVE_PROOF_PENDING because no host proof was authorized.

## OPS-COM-003 — STILL OPEN: terminal evidence is lost on a changed run

M4D closes both M4C defects. `delivery_allowed()` now returns false with no
evidence instead of writing NATURAL/SCHEDULED provenance; the focused test
proves no row is created. Migration 015 is additive and adds nullable
`prior_material_identity` and `prior_epoch_id`; the reset creator stores both
prior values alongside the new `material_identity`, new `epoch_id`, reason,
timestamp and execution link. Historical nulls remain honest, and 013/014 are
unchanged (014 continues to relabel delivery-derived legacy NATURAL to UNKNOWN).

But `prepare_epoch_for_run()` creates its changed-material reset with
`execution_id=run.id` and `outcome="RUNNING"`. At terminal completion,
`record_execution()` first queries any evidence by that same execution ID and
returns it unchanged. Therefore a first changed run never obtains a terminal
outcome/evidence record: the durable row remains the RUNNING reset. This
contradicts the required terminal-evidence-after-pre-event-reset sequence and
leaves the execution qualification contract incomplete. It is a distinct
source-level residual, so OPS-COM-003 remains NON_CONFORMING / STILL_OPEN.

## Other checks

`scripts/run_pipeline.py` supplies SCHEDULED or MANUAL at its real primary
entrypoint and accepts DEPLOY, RECOVERY and UNKNOWN explicitly. The
qualification service preserves supplied values and only SCHEDULED receives
an eligible gate. The real delivery boundary fails closed for missing,
unknown, reset, stale, or drifted evidence. Pipeline entrypoints invoke the
pre-event prepare call immediately after run creation and before processing;
the existing first-changed-run test confirms reset-before-gate and idempotent
prepare. The missing terminal transition is the remaining failure.

RunLockService still uses its held advisory grant as authority with metadata
diagnostic only, and callers retain release paths; OPS-COM-004 remains CLOSED.
The deployment completion comparator and schema compatibility barrier remain
repository mechanisms, but no target observation was taken: DEPLOY-COM-001 is
still INSUFFICIENT_EVIDENCE / LIVE_PROOF_PENDING.

## Test evidence and recommendation

Standards direct pre-audit suite: `789 passed in 7.51s`. Independent Watch
safe checks: `tests/test_standards_remediation_m3.py` plus
`tests/test_schema_check.py`, `15 passed in 3.85s`. The reported M4D full
non-live run remains inconclusive: 502 tests were collected and its final
summary/exit was truncated; it is not represented as a green full-suite result.

**DO NOT ADMIT — GAPS REMAIN.** The exact next action is a bounded Watch fix
that separates or updates the reset record at terminal completion so changed
runs retain terminal outcome/evidence without weakening pre-event reset; then
repeat this re-audit. DEPLOY-COM-001 remains parked pending separately
authorized live proof.
