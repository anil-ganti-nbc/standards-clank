# OEM Radar — M9B `STD-OPS-COM-003` applicability correction

```json
{
  "clank": "oem-radar",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-003",
      "kind": "not_applicable",
      "summary": "NOT_APPLICABLE for OEM Radar at d720e0635894ddcc9a39f116e2aa4a1768090042: the M9 checkpoint established stateless one-shot telemetry with no reusable qualification/maturity evidence or gate. This is an applicability correction, not a conformance admission."
    }
  ]
}
```

## Correction scope

This Standards-only record corrects OEM Radar's current applicability ledger
for `STD-OPS-COM-003` at canonical `main`/`origin/main` revision
`d720e0635894ddcc9a39f116e2aa4a1768090042`. The Standards takeover was
`421aab2a3e185a6ad6d72fef2ac5b3aa762e5be1`, with a clean tree. The authoritative
source investigation is the M9 checkpoint
[`oem-radar-ops-com-003-applicability-m9-2026-09-01.md`](oem-radar-ops-com-003-applicability-m9-2026-09-01.md).

The corrected current applicability is **`NOT_APPLICABLE`**. This means the
standard is out of scope for this target; it does not mean OEM Radar satisfies
the qualification contract. OEM Radar has durable `crawler_runs.id` telemetry
and related snapshots/events, but no persistent reusable soak/promotion
evidence, qualification/maturity gate, material qualification identity, or
qualification epoch/reset semantics. Its production-frozen posture is not an
application gate. No remediation is warranted.

## Historical chain and resolver boundary

The original M1 fleet sweep remains untouched at its canonical state:
`STD-OPS-COM-003` was retained as unresolved/insufficient for OEM Radar while
the resolver lacked a target fact. M9 then performed the source-level
applicability investigation and established `NOT_APPLICABLE`. This M9B record
is the additive current-state correction:

`M1 uncertainty → M9 applicability investigation → M9B NOT_APPLICABLE`.

The resolver input is deliberately not fabricated or silently repaired.
`tools/fleet_standards_resolver.py` still maps this standard to
`has_promotion_soak`, and `profiles/fleet-adoption.json` still has an empty
OEM Radar `facts` object. The raw resolver disposition therefore remains
`UNKNOWN`; this target-scoped adjudication is the current applicability record
for the audited revision, while resolver fact coverage remains a separate
governance/data-quality limitation.

No resolver code, profile, frozen standard wording, tag, or M1 artifact was
changed. No conformance evidence was admitted, and the `not_applicable`
finding is excluded by the Operations known-evidence generator.

## Current counts

The counts below are mechanically carried from the canonical M1 OEM Radar row
and changed only for this one applicability decision (25 ratified standards):

| State | Before (M1) | After (M9B) |
|---|---:|---:|
| APPLIES | 22 | 21 |
| NOT_APPLICABLE | 3 | 4 |
| CONFORMS (among applicable) | 18 | 18 |
| NON_CONFORMING | 0 | 0 |
| INSUFFICIENT_EVIDENCE (among applicable) | 4 | 3 |

The three remaining OEM Radar insufficiencies are preserved exactly:
`STD-UI-COM-011`, `STD-DEPLOY-COM-001`, and `STD-DEPLOY-COM-002`. No unrelated
standard or target verdict changed, and no overall target-conformance claim is
made.

## Safety and validation

This pass changed only the paired M9B applicability-correction artifact and its
narrow guard test. OEM Radar was not modified, tested, collected, deployed,
or accessed on a host. No compatibility remediation, live proof, or
known-evidence admission occurred. The full Standards suite was run directly
and unpiped after the artifacts were added: **840 passed, 0 skipped, 0 failed,
exit 0**.

The next action is not target remediation: preserve this record as the current
OEM Radar applicability decision and continue only with separately authorized
`STD-DEPLOY-COM-002` / `STD-DEPLOY-COM-001` work. The missing
`has_promotion_soak` resolver fact remains explicitly unresolved.
