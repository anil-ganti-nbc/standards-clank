# watch-clank — M4G final OPS-COM-003 closure re-audit

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[],"superseded_by":"audits/watch-clank-cross-domain-2026-09-01-final.md"}
```

Read-only source re-audit of Watch `d03bc4b2f90289686331af0447d5ca4e8cf55822`
against Standards `b88aa7ddf18d4ba709ab7046974ca493fd5d3e98`. Both trees
were clean at takeover. No Watch, host, deployment, frozen standard/tag, or
known-evidence state was changed.

## Result

| State | Count |
|---|---:|
| CONFORMS | 24 |
| NON_CONFORMING | 0 |
| INSUFFICIENT_EVIDENCE | 1 |

The frozen resolver remains 25 APPLIES, 0 NOT_APPLICABLE, 0 UNKNOWN. All 23
previous conformances still conform. OPS-COM-004 remains CLOSED. DEPLOY-COM-
001 remains LIVE_PROOF_PENDING because no authorized host observation exists.

## OPS-COM-003 — CLOSED

The execution authority path supplies `SCHEDULED`/`MANUAL` at the primary
entrypoint and supports `DEPLOY`, `RECOVERY`, and `UNKNOWN` structurally.
Qualification records retain run ID, material identity and outcome. The real
pipeline creates a run, prepares its material reset before event processing,
then records terminal qualification evidence at the terminal boundary.

Missing evidence at `delivery_allowed()` fails closed without manufacturing
NATURAL or SCHEDULED provenance. Unknown remains non-qualifying. Migration 014
keeps legacy delivery-derived NATURAL honest by relabelling unlinked rows to
UNKNOWN. Migration 015 is additive and makes reset lineage durable: prior and
new material identities, prior and new epochs, reason, timestamp and run link
are present on a new reset; historical missing lineage remains null.

M4F resolves the final identity collision. A reset is associated with the run
but has a reset reason; terminal deduplication checks the same execution ID
only against rows whose reset reason is null. Thus the pre-event RESET/RUNNING
record and terminal execution record are distinct durable facts for the same
run. The extended first-changed-run regression proves old evidence is blocked,
one reset is idempotent, one terminal record is idempotent, both rows coexist,
and terminal evidence has SUCCESS, new epoch, and new material identity.

This is the complete required qualification chain, not merely model capacity:
authority → provenance/run/material identity → pre-event reset → fail-closed
gate → terminal evidence → current-epoch qualification. OPS-COM-003 is
therefore CONFORMS / CLOSED.

## Regression and live-proof state

Grant-backed RunLockService authority remains held in its advisory-lock handle;
metadata is diagnostic and release paths remain, so OPS-COM-004 / WC-M1-001
remains CONFORMS / CLOSED. The repository deployment comparator and schema
compatibility barrier remain present, but actual target observation was outside
scope: DEPLOY-COM-001 remains INSUFFICIENT_EVIDENCE / LIVE_PROOF_PENDING.

Standards direct pre-audit suite: `791 passed in 7.41s`. Independent Watch
qualification/schema checks: `15 passed in 3.74s`. M4F additionally recorded
a direct full non-live run: `500 passed, 2 skipped`, exit 0, 53.922s.

**ADMIT AFTER LIVE PROOF.** OPS-COM-003 is now closed. This audit is retained
as historical evidence and is superseded by the final Watch audit after the
separately authorized DEPLOY-COM-001 live proof.
