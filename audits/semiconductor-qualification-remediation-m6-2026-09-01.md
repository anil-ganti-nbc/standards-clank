# Semiconductor Intelligence — M6 qualification provenance/reset remediation evidence

```json
{
  "clank": "semiconductor-intelligence",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-003",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical Semiconductor main revision 688b71a93b4988b5ce52ce85e46f09080b9a7948: target-local qualification provenance, deterministic material identity, pre-gate epoch reset, auditable reset lineage, independent terminal evidence, and fail-closed gating are implemented and focused coverage is green."
    }
  ]
}
```

## Scope and narrow verdict

This is a Standards-only evidence record for Semiconductor Intelligence M6.
The audited target revision and `origin/main` are both
`688b71a93b4988b5ce52ce85e46f09080b9a7948`. Only source-level
`STD-OPS-COM-003` qualification provenance/reset remediation is recorded:
**CONFORMS / CLOSED**. Semiconductor is not fully conforming overall.

## Lineage and preserved M1 state

Standards was taken over at clean `HEAD` = `origin/master`:
`3f729b9ff169105487cd875bd8ed9a0722b22f6e`. The canonical Semiconductor
source revision was independently verified before this record. The M1 ledger
recorded 23 applicable standards, 17 conformances, 0 non-conformances, and 6
insufficient findings:

- `STD-UI-COM-006`
- `STD-UI-COM-007`
- `STD-UI-COM-011`
- `STD-OPS-COM-003`
- `STD-DEPLOY-COM-001`
- `STD-DEPLOY-COM-002`

Only `STD-OPS-COM-003` is superseded by this record. The five remaining
insufficiencies stay untouched and unresolved: `STD-UI-COM-006`,
`STD-UI-COM-007`, `STD-UI-COM-011`, `STD-DEPLOY-COM-001`, and
`STD-DEPLOY-COM-002`.

## Semiconductor qualification evidence

The execution authority is `OperationalScheduler.run_job`. Scheduler, retry,
CLI, GUI, startup-catchup, and test paths converge on that job boundary. The
target-local vocabulary is `SCHEDULED`, `MANUAL_CLI`, `MANUAL_GUI`,
`STARTUP_CATCHUP`, `RETRY`, `TEST`, and `UNKNOWN`; no trusted `DEPLOY` or
`RECOVERY` value was invented. Missing provenance remains `UNKNOWN`, and a
downstream writer cannot upgrade it.

`QualificationMaterial` computes a deterministic `siq1-` SHA-256 identity
from job type, application version, implementation revision, configuration
fingerprint, policy version, and execution scope. Volatile timestamps, run
IDs, host/process details, and content observations are excluded. Unknown
material components make the identity untrusted at the gate.

`QualificationService` prepares the current durable epoch before reusable
qualification evidence can be gated. A material change creates an append-only
reset event with prior/new identities and reason; legacy rows retain nullable
unknown lineage. Reset and terminal events are independent facts and can
coexist for one execution. Terminal recording is idempotent. The gate fails
closed for absent, stale, divergent, unknown, untrusted, non-qualifying, or
unhealthy evidence.

These are descriptive Semiconductor implementation observations, not new
normative wording for other Clanks.

## Migration and validation evidence

Migration `c7d8e9f0a1b2` is additive: it adds `qualification_epochs`,
`qualification_events`, and nullable qualification fields on
`operational_job_runs`. Existing history is preserved; no production
migration occurred. Upgrade and downgrade both passed on disposable SQLite.

Focused qualification coverage: **21 passed**. The exact direct full-suite
command was `python -m pytest`:

- baseline `8a356a3bc87bea0f0d95e66c072c8e8a629156d5`: `877 passed, 1
  skipped, 2 failed`, exit code 1;
- final M6 `688b71a93b4988b5ce52ce85e46f09080b9a7948`: `898 passed, 1 skipped,
  2 failed, 38,541 warnings`, elapsed `1244.62s`, exit code 1.

The same two notification-adapter assertions failed before and after and are
classified **PRE_EXISTING / BASELINE_ATTRIBUTED**. The full suite is not
green. The full suite is not green. No new qualification or migration failures appeared, and no new
failure was introduced by M6. Remediation-specific focused coverage is green.

## Implementation checks

| Check | Result |
|---|---|
| A. Provenance begins at execution authority boundary | YES |
| B. Missing provenance can become trusted downstream | NO |
| C. Old epoch can qualify first changed execution | NO |
| D. Reset happens before gate | YES |
| E. Material identity stable/deterministic | YES |
| F. Old/new reset identity auditable where known | YES |
| G. Legacy unknowns preserved | YES |
| H. Reset and terminal can coexist | YES |
| I. Terminal persistence independently idempotent | YES |
| J. Gate fails closed on stale/unknown/untrusted evidence | YES |
| K. Alternate execution path bypasses preparation | NO |
| L. Trusted provenance can be overwritten downstream | NO |

## Rich ORM/job family result

This independently closes the shared contract in the second rich ORM/job
target, so the descriptive family result is
`RICH_ORM_JOB_RECIPE_VALIDATED` for:

- Smartwatch: `a631421e276b58ce3499787cc2bc72218648ce72`
- Semiconductor: `688b71a93b4988b5ce52ce85e46f09080b9a7948`

Smartwatch and Semiconductor retain independent job, provenance, storage, and
gate mechanics. Semiconductor uses `OperationalJobRun`/trigger provenance,
the target-local qualification projection/migration, and a separate editorial
promotion model. This does not transfer evidence or conformance to Feature
Phone, Tablet, KTW, OEM Radar, or any other target.

## Operations known-evidence admission

The existing generated Operations layer admits exactly one new fact:

`semiconductor-intelligence` +
`688b71a93b4988b5ce52ce85e46f09080b9a7948` + `STD-OPS-COM-003` +
`CONFORMS / CLOSED`.

The prior M1 insufficiency remains historical evidence. No unrelated standard
or target was admitted.

## Safety and freeze declarations

Semiconductor was not modified during this Standards pass. No host, deployment, live collector, live proof, or production-database action occurred. Frozen standards and immutable tags were not changed or moved.
