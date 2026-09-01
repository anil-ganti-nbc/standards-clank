# feature-phone-clank — M3 OPS-COM-004 remediation evidence

```json
{
  "clank": "feature-phone-clank",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-004",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical feature-phone-clank main revision 890ab339234381b04c6f27e710e3382fa70bc076: RunLock exclusivity is granted by a held OS advisory lock; PID and marker metadata are diagnostic only."
    }
  ]
}
```

## Scope and verdict

This is the Feature Phone target record for the two-target M3 lock-authority
remediation. The audited target is the canonical `main` revision
`890ab339234381b04c6f27e710e3382fa70bc076`; the commit and `origin/main` were
verified equal. This record admits only `STD-OPS-COM-004`. It does not assert
overall Fleet conformance: the M1 inventory remains **18 CONFORMS, 0
NON_CONFORMING, 4 INSUFFICIENT_EVIDENCE** out of 22 applicable standards.

## Implementation evidence

`src/feature_phone_clank/core/run_lock.py` now keeps one descriptor open for
the whole run and takes a non-blocking exclusive `fcntl.flock`/`msvcrt.locking`
grant. The JSON marker records `pid`, timestamps, and
`lock_authority=os_advisory_lock` for diagnosis; no PID liveness check,
staleness window, marker deletion, or PID-based reclaim can grant or deny the
lock. Release unlocks and closes the descriptor, so the granting authority
determines when the grant ends.

## Regression and suite evidence

The target-specific lock regression file `tests/test_run_lock.py` passed all
six tests. It covers first acquisition, contention, release/reacquisition,
failure cleanup, readable metadata, stale/dead/reused PID metadata without a
grant, and stale metadata while a real grant remains held.

The exact direct full non-live suite was intentionally recorded against both
the parent and remediation revisions:

- baseline `4051b64fe7ba4dc188ec1e1a6920ce72b14f013d`: `214 passed, 2 skipped,
  4 failed`;
- remediation `890ab339234381b04c6f27e710e3382fa70bc076`: `214 passed, 2
  skipped, 4 failed`.

The same four pre-existing environmental/runtime-contract tests failed at both
revisions: the three HealthPayload tests fail against the installed shared
`clank_runtime`/Pydantic schema, and the CLI contract test fails in the
Windows Python 3.14 subprocess-handle path. No new failure appeared in the
remediation commit, and none of these failures touches the lock implementation.

This record is descriptive evidence of the source-level closure only; no host,
deployment, scheduler, database, or live-proof claim is made.
