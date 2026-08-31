# Operations Pass 1.5 — OPS-D Scope-Omission Resolution (2026-08-31)

**Disposition: A — ADVANCE AS OPS-D** (distinct candidate; standard
drafting deferred to a separately commissioned pass).

## Resolution chain (recorded, nothing rewritten)

1. **Pass 0B** adjudicated cluster 2
   (pid-namespace-unsafe-stale-lock-reclaim) as **KEEP DISTINCT,
   candidate OPS-D "Lock reclaim soundness," recommendation ADVANCE**
   ([../pass0/adjudication.md](../pass0/adjudication.md) table row 2 and
   prose section 2). No candidate card was produced at the time — the
   adjudication carried a one-paragraph justification only.
2. **Pass 1** was commissioned (by the operator handoff) for exactly
   OPS-A/B/C and explicitly forbade drafting a fourth standard. It
   drafted the three standards and correctly **recorded the
   discrepancy** rather than silently dropping OPS-D — see
   [README.md](README.md), "A note on scope: three cards, not four
   dispositions."
3. **Pass 1.5 (this pass)** resolves the discrepancy under operator
   commission: OPS-D is adjudicated as a genuine, distinct
   implementation-neutral Operations candidate and advances as
   **OPS-D "Exclusivity-marker soundness."**

The full candidate card lives at
[../pass0/candidates/ops-d-exclusivity-marker-soundness.md](../pass0/candidates/ops-d-exclusivity-marker-soundness.md)
— produced now to close the card gap Pass 1's README recorded, while the
handoff's "do NOT draft STD-OPS-COM-004 yet" instruction is respected:
no `STD-OPS-*` file for OPS-D exists or was created.

## Adjudication (why the invariant survives abstraction)

The known implementation shape (stale locks, PID reuse, namespaces,
unsafe reclaim) is mechanism detail. The incidents share one deeper
failure: **an exclusivity/ownership marker was validated or acted upon
solely from an identifier whose liveness or ownership the validating
context could not prove.** The three named incidents fail in three
different directions across three environments — honor-a-dead-marker
(oem-radar, ~81 refused fires), kill-a-live-innocent (watch-clank,
reused PID), false-alive-in-one-shot-containers (smartwatch-clank) — and
smartphone INC-015 (stale PID file → duplicate daemons) is a fourth
instance in the same family. The invariant abstracts to:

> An operational exclusivity/ownership marker must not be reclaimed,
> honored, or acted upon solely on the basis of an identifier whose
> liveness or ownership cannot be proven within the current execution
> context; marker validity must be structurally observable by the
> authority that grants it.

**Counterexamples tested and survived:** database session-scoped
advisory locks (the DB server structurally observes owner death —
conforms), expiring leases (clock-based reclamation is provable —
conforms), distributed lock managers (conform if grantor-observable).
What fails the invariant is any reclaim/honor decision resting on an
identifier the context cannot verify — which is exactly what all four
incidents did. The invariant is therefore mechanism-neutral (flock,
`msvcrt.locking`, DB locks, and leases all conform) and survives without
host-narrowing: PID reuse defeats bare-identifier proofs everywhere, not
only in containers.

## Relationship to OPS-A and Fleet Laws 5/7

- **Not OPS-A:** OPS-A (execution materialization truth) binds whether
  invocations and outcomes are recorded; OPS-D binds whether the
  exclusivity marker coordinating writers is *valid*. A Clank deadlocked
  on a stale lock can satisfy OPS-A perfectly (each refused fire is a
  recorded skip) while starving — oem-radar's ~81 refused fires did
  exactly that. Distinct invariants; both needed.
- **Fleet Law 5 (ACTIVE)** owns "single scheduler/notification authority
  per lane" — governance against creating competing authorities. OPS-D
  does not restate it; it binds marker-validity soundness of whatever
  coordination primitive a Clank runs, which Law 5 does not address.
- **Fleet Law 7 (ACTIVE)** owns writer coordination as a principle;
  OPS-D is the mechanism-soundness complement to it.

## What this resolution did and did not do

- Produced the OPS-D candidate card (closes the card gap Pass 1's README
  recorded) and appended an additive resolution note to Pass 0B's
  adjudication table/prose.
- Did **not** draft `STD-OPS-COM-004` (explicitly reserved for a
  separately commissioned pass).
- Did **not** rewrite any Pass 0/1 history; the Pass 0B ADVANCE verdict
  and Pass 1's scope note stand as recorded.
- Did **not** modify any target Clank, the frozen UI/DATA baselines, or
  the three existing PROPOSED OPS standards.
- Open items recorded for the operator (from the cluster file, unchanged
  by this pass): whether korean-tech-wire's `RunLock` and
  semiconductor-intelligence's `LeaseManager` are structurally
  marker-sound (never observed failing, never audited); whether the
  fleet's four copy-owned lock implementations should be consolidated
  into one shared library (implementation-consolidation question, out of
  scope for a standard).
