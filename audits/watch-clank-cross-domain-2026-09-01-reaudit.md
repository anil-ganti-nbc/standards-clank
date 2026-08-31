# watch-clank — M4A informed cross-domain re-audit

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[]}
```

This is a read-only re-audit. No Watch source, deployment, host, frozen
standard, frozen tag, or known-evidence index was changed.

## Identity and applicability

Standards Clank: `6654c758551cc99dd64691dfdbc8a1f3af24d5b9` (`origin/master`).
Watch: `89d159dff59f242de176498444a20abf98a3df7f` (`origin/main`). Both trees
were clean at takeover. The frozen resolver was regenerated with
`python scripts/resolve_clank_standards.py watch-clank --json`: all 25
standards remain APPLIES; no trigger fact changed. The four v1.0 tag object
IDs are recorded in the adjacent JSON and were unchanged.

## Verdicts and prior comparison

| State | Count | Standards |
|---|---:|---|
| CONFORMS | 23 | The 22 prior conforming standards, plus OPS-COM-004 |
| NON_CONFORMING | 1 | OPS-COM-003 |
| INSUFFICIENT_EVIDENCE | 1 | DEPLOY-COM-001 |
| NOT_APPLICABLE / UNKNOWN | 0 / 0 | none |

The full standard-by-standard ledger is in the adjacent JSON. All 22 prior
CONFORMS are STILL_CONFORMS; no regression was found.

### WC-M1-001 / OPS-COM-004 — CLOSED

`RunLockService` now holds a platform advisory-lock handle for the protected
lifetime. PID/timestamp JSON is diagnostic; neither `acquire()` nor
`is_locked()` decides ownership from it or from a DB RUNNING record. Caller
paths in pipeline and specialist-lead services release in `finally` blocks.
The stale-metadata and release tests support the closure.

### OPS-COM-003 — STILL OPEN

Migration 013 and `QualificationService` are useful partial remediation, but
the current authority path is event delivery, not the qualifying execution
path described by the Watch soak contract. Its first persisted record is
always `NATURAL`; it cannot distinguish scheduled, manual, deploy-verification
or recovery execution. Its epoch only hashes the experimental set, so material
code/source changes are not represented as reset causes. The record therefore
does not yet satisfy the structurally-verifiable qualification requirement.

### DEPLOY-COM-001 — LIVE PROOF PENDING

The repository now has a real status mechanism: `deployment_status.py` takes
a target and intended revision, obtains distinct observed inputs, and delegates
to a comparator that cannot report COMPLETE for missing/mismatched running
revision, config/wiring mismatch, or non-convergence. This proves repository
mechanism, not that any target is materially running the intended state. No
host observer or live target evidence was available or authorized, so the
standard verdict remains INSUFFICIENT_EVIDENCE and the lifecycle is
LIVE_PROOF_PENDING rather than CLOSED.

## Test evidence

Watch's reported remediation validation was focused `287 passed`, migration
`6 passed`, and full non-live `495 passed, 2 skipped`, exit code 0. This audit
also independently ran Standards Clank's direct suite before changes:
`785 passed in 8.45s`.

## Admission recommendation and next action

**DO NOT ADMIT — GAPS REMAIN.** Do not modify known evidence. The exact next
action is a bounded Watch remediation for OPS-COM-003's real scheduled/manual/
deploy/recovery qualification provenance and material-reset semantics, then a
new re-audit; separately authorize host observation before resolving the
DEPLOY-COM-001 live-proof lifecycle.
