# smartwatch-clank — M5 qualification provenance/reset remediation evidence

```json
{
  "clank": "smartwatch-clank",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-003",
      "kind": "conformance",
      "summary": "CONFORMS / CLOSED at canonical Smartwatch main revision a631421e276b58ce3499787cc2bc72218648ce72: source-level qualification provenance, stable material identity, pre-gate epoch reset, auditable reset lineage, and fail-closed qualification gating are implemented and focused coverage is green."
    }
  ]
}
```

## Scope and final narrow verdict

This is a Standards evidence-recording pass for the Smartwatch M5 source-level
remediation of `STD-OPS-COM-003`. The audited Smartwatch `main` revision and
`origin/main` are both
`a631421e276b58ce3499787cc2bc72218648ce72`. The final narrow verdict is
**CONFORMS / CLOSED** for `STD-OPS-COM-003` at that revision.

This record does not close or imply conformance for `STD-UI-COM-011`,
`STD-DEPLOY-COM-001`, or `STD-DEPLOY-COM-002`, and it does not claim that
Smartwatch is fully conforming overall. No Semiconductor conformance is
inferred. No host, deployment, live collector, or live-proof action occurred
in this pass.

## Takeover and evidence lineage

Standards Clank was taken over at clean `HEAD` = `origin/master`:
`a56e8dc1ddce54e229096ec55bec90c1e2ec6e15`. The immutable UI,
Data/Ontology, Operations, and Deployment v1.0 tags were not changed. The
canonical source revision was independently verified on Smartwatch before
recording this evidence.

The original M1 fleet blind audit recorded Smartwatch with 22 applicable
standards, 18 conformances, 0 non-conformances, and 4 insufficient findings:

- `STD-UI-COM-011`
- `STD-OPS-COM-003`
- `STD-DEPLOY-COM-001`
- `STD-DEPLOY-COM-002`

For `STD-OPS-COM-003`, the M1 finding was
`INSUFFICIENT_EVIDENCE`: the source-only sweep found no current qualification
reset lineage or fail-closed qualification gate, while target observation and
compatibility evidence also remained outside that pass. The M4 planning record
classified Smartwatch in the **RICH_ORM_JOB_PROVENANCE** family with
Semiconductor Intelligence, while preserving each target's local boundaries.

## Smartwatch remediation evidence

The implementation keeps the contract descriptive rather than prescribing a
fleet-wide storage or runtime shape:

- Execution authority supplies structured provenance. The supported vocabulary
  is `SCHEDULED`, `MANUAL`, and `UNKNOWN`; absent or invalid provenance stays
  `UNKNOWN`.
- A stable qualification material identity covers release/config/schema scope
  (including app version, config fingerprint, baked git revision, SQLite
  schema version, execution scope, and contract version), rather than content,
  host, process, or timestamp observations.
- Material identity is compared before prior qualification evidence is read.
  A material change starts a new qualification epoch and records the reset
  before any changed-run gate evaluation.
- Reset records persist explicit prior and new identities, reason, authority,
  execution identity, provenance, and time. Historical unknowns remain null or
  `UNKNOWN`; they are not backfilled into claimed provenance.
- Qualification evidence is linked to the current execution and epoch, so old-
  epoch evidence cannot qualify the first execution after a material change.
  Reset and terminal facts can coexist for one execution, and terminal
  persistence is idempotent.
- The qualification gate fails closed for absent, unknown, stale, divergent,
  or untrusted evidence. Scheduler, CLI, and dashboard paths preserve the
  execution provenance they establish; downstream consumers do not fabricate
  `NATURAL` or an equivalent provenance.

These observations establish Smartwatch's source-level conformance at the
audited SHA. They do not turn these implementation choices into new normative
requirements for other Clanks.

## Validation evidence

The exact evidence recorded for M5 is:

- Focused qualification/provenance coverage: **40 passed**.
- Final gate-focused rerun: **13 passed**.
- Full remediation command: `$env:PYTHONPATH='src'; python -m pytest`.
- Full remediation result: **243 passed, 1 skipped, 2 failed, 0 warnings,
  exit 1, 20.99s**.
- Baseline result at `08a23f90297f7c0fbaffdb4018116c13d5e60b84`: **235 passed,
  1 skipped, 2 failed**.

The same two `dcrainmaker_specialist` tier-expectation failures reproduce at
baseline and remediation. They are classified explicitly as
**PRE_EXISTING / BASELINE_ATTRIBUTED**. M5 introduced no new full-suite
failure; focused remediation coverage is green. The full suite is not reported
as green, and the baseline-attributed failures remain outside this remediation
scope.

## Smartwatch M5 implementation checks

| Check | Result |
|---|---|
| A. Authority-origin provenance | YES |
| B. Missing provenance trusted downstream | NO |
| C. Old epoch qualifies first changed execution | NO |
| D. Reset before gated use | YES |
| E. Stable explicit material identity | YES |
| F. Prior/new reset identities auditable | YES |
| G. Legacy unknowns preserved | YES |
| H. Reset and terminal coexist | YES |
| I. Terminal persistence idempotent | YES |
| J. Gate fails closed | YES |
| K. Alternate path bypasses preparation | NO |

These are Smartwatch-specific closure checks, not a fleet-wide conformance
assertion.

## Preserved M1 state

The following Smartwatch findings remain exactly `INSUFFICIENT_EVIDENCE` and
were not re-audited or altered by this record:

- `STD-UI-COM-011`
- `STD-DEPLOY-COM-001`
- `STD-DEPLOY-COM-002`

The canonical M1 applicability set remains the source for the 22 applicable
standards; closing `STD-OPS-COM-003` does not change those three lifecycle
states or claim overall target conformance.

## Rich ORM/job qualification family

Smartwatch is the **FIRST VALIDATED MEMBER OF THE RICH ORM/JOB QUALIFICATION REMEDIATION FAMILY**. This is descriptive process evidence only: the shared
qualification contract has been demonstrated once in this implementation
family. It does not make Semiconductor conforming, prescribe copying the
Smartwatch schema, make the exact Smartwatch implementation mandatory, or
transfer evidence to another target. Semiconductor still requires independent
implementation and proof.

## Operations known-evidence admission

Only this narrow fact is admitted through the existing generated Operations
known-evidence layer:

`smartwatch-clank` +
`a631421e276b58ce3499787cc2bc72218648ce72` + `STD-OPS-COM-003` +
`CONFORMS / CLOSED`.

The prior M1 insufficiency remains historical evidence. The new active audit
supersedes that exact OPS-COM-003 assessment for this Smartwatch revision in
the evidence layer without deleting or rewriting history. No unrelated
standard is admitted.

## Safety and freeze declarations

Smartwatch was not modified during this Standards pass. No target repository,
host, deployment, scheduler, database, collector, or live-proof action was
performed. Frozen standard files and immutable v1.0 tags were not changed or
moved. This record does not begin Semiconductor work.
