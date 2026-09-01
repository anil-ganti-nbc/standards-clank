# Fleet Remediation Planning M2 — 2026-09-01

```json
{"clank":"fleet","date":"2026-09-01","findings":[]}
```

This is a read-only remediation plan derived from the canonical M1 sweep at
[`c8969263a1b936c4ff888eb9d2dc9449b3d12fef`](fleet-blind-audit-sweep-m1-2026-09-01.json).
It proposes shared, implementation-neutral recipes; it does not change a
target, start remediation, perform live proof, or admit evidence. The full
ledger is in
[`fleet-remediation-planning-m2-2026-09-01.json`](fleet-remediation-planning-m2-2026-09-01.json).

## Pattern ledger

| Pattern | Affected Clanks | Standard(s) | Shared fix viable? | Per-target proof still needed? |
|---|---|---|---|---|
| PID/OpenProcess authority | Feature Phone, Tablet | `STD-OPS-COM-004` | **Yes, likely** — common grantor-observable authority recipe | **Yes** |
| Qualification provenance/reset | OEM, Semiconductor, KTW, Feature Phone, Smartwatch, Tablet | `STD-OPS-COM-003` | **Yes** — shared durable provenance/epoch/gate contract | **Yes** |
| Persistent-state compatibility | OEM, Semiconductor, CTW, KTW, Feature Phone, Smartwatch, Tablet | `STD-DEPLOY-COM-002` | **Yes** — shared fail-closed barrier contract; target-local mechanics | **Yes** |
| Live deployment identity | All eight | `STD-DEPLOY-COM-001` | **Common proof method only**; evidence is never shared | **Always, independently** |
| Resolver trigger-fact coverage | All eight | None | No remediation recipe; governance decision is separate | Applicability recheck only |

## Recommended order

1. **Feature Phone + Tablet:** close their actual `STD-OPS-COM-004`
   non-conformance with one invariant/test recipe and two independent source
   integrations.
2. **Qualification and compatibility patterns:** work by pattern across the
   affected Clanks, preserving each target's own provenance, storage, runtime,
   and migration mechanics. These are evidence gaps in M1, not blanket
   non-conformance findings.
3. **Fleet source re-audit:** reassess all eight targets, including unaffected
   Smartphone and the two lock remediations, before any live observation.
4. **Per-target read-only live proof:** run the Watch-derived comparator for
   each target separately. No target can inherit Watch's deployment result.

## Safety boundary

No target repository, deployment, scheduler, database, host, or known-evidence
layer was modified for M2. No target tests, collectors, live probes, or
admissions were performed. No new standard is proposed. The resolver's empty
target trigger facts remain a recorded process limitation, not an implicit
remediation task.
