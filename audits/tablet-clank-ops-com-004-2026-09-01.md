# tablet-clank — M3 OPS-COM-004 remediation evidence

```json
{
  "clank": "tablet-clank",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-004",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical tablet-clank main revision 568fcfc9b80a2bffcebe8af475b3319f2304ad76: SoakLock and canonical-lock preflight use a held OS advisory lock; PID and marker metadata are diagnostic only."
    }
  ]
}
```

## Scope and verdict

This is the Tablet target record for the two-target M3 lock-authority
remediation. The audited target is the canonical `main` revision
`568fcfc9b80a2bffcebe8af475b3319f2304ad76`; the commit and `origin/main` were
verified equal. This record admits only `STD-OPS-COM-004`. It does not assert
overall Fleet conformance: the M1 inventory remains **18 CONFORMS, 0
NON_CONFORMING, 4 INSUFFICIENT_EVIDENCE** out of 22 applicable standards.

## Implementation evidence

`tablet_clank/soak.py` now keeps a descriptor open for the whole run and takes
a non-blocking exclusive `fcntl.flock`/`msvcrt.locking` grant. Its persistent
JSON marker records role, PID, timestamps, and
`lock_authority=os_advisory_lock` for diagnosis only. Acquisition and release
never consult or delete a marker based on PID liveness.

`tablet_clank/campaign.py` uses `SoakLock.inspect` to probe the same kernel
authority for canonical preflight. A held grant is reported active; a readable
marker with no held grant is retained as stale for reporting compatibility.
Malformed metadata remains unreadable. No second PID-based authority exists.

## Regression and suite evidence

The target-specific lock and campaign regression set passed (`102 passed` in
the focused integration command). It covers first acquisition, contention,
release/reacquisition, failure cleanup, readable metadata, stale/dead/reused
PID metadata without a grant, stale metadata while a real grant remains held,
and read-only canonical preflight behavior.

The exact direct full non-live suite passed **118 tests** (`118 passed`).
No qualification/provenance, persistent-state compatibility, deployment, host,
or live-proof evidence is admitted here.
