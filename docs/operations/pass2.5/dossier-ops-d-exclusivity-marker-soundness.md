# Pass 2.5 Dossier — OPS-D: Exclusivity-marker soundness

**Drafted as:** [STD-OPS-COM-004](../../../standards/operations/STD-OPS-COM-004.json)

## Candidate

Exclusivity/ownership markers must be validated by structurally
observable proof. Where a Clank uses a run lock, lease, or ownership
record to coordinate execution across process/context boundaries, that
marker's validity must be determinable from state the granting authority
itself observes — never inferred by the validating context from a
reusable or context-ambiguous identifier (PID, hostname). Reclaiming a
marker, honoring it as live, and acting on the process it identifies all
carry the same standard of proof.

## Source clusters

Pass 0A cluster `pid-namespace-unsafe-stale-lock-reclaim` (topic 10),
adjudicated by Pass 0B as `KEEP DISTINCT`, candidate name "OPS-D Lock
reclaim soundness," recommendation `ADVANCE` — but left undrafted at Pass
1 because Pass 1's commission named only OPS-A/B/C. Resolved by Pass 1.5
(candidate card `ops-d-exclusivity-marker-soundness.md`, disposition
ADVANCE AS OPS-D, standard drafting explicitly deferred) and reviewed by
Pass 2 (verdict `DRAFT AS STD-OPS-COM-004`, with explicit drafting
constraints — title, invariant, trigger, minimum acceptance/forbidden
concepts, implementation freedoms — all followed by this draft).

## Pass 0B disposition

`ADVANCE` (cluster 2, table row 2 of `docs/operations/pass0/adjudication.md`,
with an additive Pass 1.5 resolution note appended, original verdict text
preserved verbatim).

## Evidence strength

STRONG — four independent-environment discoveries of the identical
unsoundness across four different repos and three different failure
directions (starvation, wrong-process termination, one-shot-container
falsely-alive, duplicate-daemon-from-stale-PID-file). The shared *fix*
lineage (OS-level advisory locks, propagated by explicit code-porting
across repos) is one implementation lineage, not counted as independent
evidence per Pass 2's evidence-discipline note — the *incidents* are what
justify advancement, and those are independent discoveries.

## Strongest incidents

- INC-009 — oem-radar: a crash left a lock recording PID 1; ~81
  consecutive hourly scheduler fires refused to start, concluding the
  prior run was still alive, because every Docker container is PID 1 to
  itself. Indefinite starvation.
- INC-006 — watch-clank: the inverse failure — a Windows liveness check
  keyed on a recorded PID could terminate an unrelated process that had
  since reused that PID.
- smartwatch-clank — the same PID/hostname reclaim logic independently
  proven unsound in a one-shot `docker run --rm` model.
- INC-015 — smartphone-clank: a stale PID file let a health-check job
  spawn a duplicate daemon against the same production database.

## Lineage assessment

Three of the four incidents are independent discoveries in different
environments (Docker/NAS, Windows, one-shot containers); the fourth
(smartphone-clank's stale PID file) is in the same identifier-liveness
family, independently found. The *remedy* — OS-level advisory locks
consulting no PID — propagated by explicit, named code-porting across at
least three repos (oem-radar ← Free Game Tracker; feature-phone-clank ←
oem-radar; smartwatch-clank ← oem-radar/FGT/a cited Diagnostic Clank
incident). Pass 2's evidence-discipline note is followed here: the fix
lineage is counted once, not as four separate votes.

## Fleet Law / ADR relationship

COMPLEMENT to Fleet Law 7 (ACTIVE — writer coordination as a principle)
and Fleet Law 5 (ACTIVE — single scheduler/notification authority per
lane). Neither Law addresses the validity-proof soundness of the
coordination primitive itself; this standard does not restate either.
DISTINCT from ADR-0009 (destructive production mutation authority) —
related in spirit (both forbid acting on unproven identity) but
different scope (routine execution coordination vs. destructive
administrative mutation); no overlap requiring reconciliation.

## Strongest counterexample

"Database advisory locks, lease services, and distributed lock managers
are legitimate and look nothing like `flock` — a standard naming OS
advisory locks would outlaw them or mandate lockfiles."

**Why it survives:** the invariant constrains *validity semantics*, not
mechanism. A DB-session advisory lock conforms because the database
server structurally observes connection death. An expiring lease
conforms because clock-based reclamation is provable by the grantor. A
fencing token conforms because the token is grantor-issued proof. Even a
hostname+PID+process-start-time tuple can conform, but only if the
start-time genuinely proves identity to the validating context —
provenance of the proof is the invariant, never the identifier's shape.
What fails is exactly what all four incidents did: reclaiming or honoring
a marker from an identifier the validating context could not itself
verify.

## No overlap with OPS-A, verified

A Clank deadlocked on a stale-but-unsound lock can satisfy
`STD-OPS-COM-001` (execution materialization truth) perfectly — every
refused fire is a recorded skip/no-work outcome — while starving
indefinitely, exactly as oem-radar's ~81 refused fires did. The two
standards bind different failure surfaces (whether execution truth is
recorded, vs. whether the coordination primitive that gates execution is
itself sound) and neither implies the other. `STD-OPS-COM-004`'s `notes`
field states this explicitly with the same example.

## Unresolved wording questions

- The `evidence` array counts the fleet-wide advisory-lock convergence as
  one `CROSS_CLANK_BEST_PRACTICE` entry (the remedy), separate from the
  four `DIAGNOSTIC_INCIDENT` entries (the failures) — worth a future
  reviewer confirming this split reads as evidence-honest rather than
  inflating the count.
- Two fleet members (chinese-tech-wire, korean-tech-wire) were noted at
  Pass 0A as not confirmed to have hit this bug — untested-but-exposed
  vs. safe-by-different-design remains genuinely unknown; this standard's
  `trigger` field scopes to "any Clank using a cross-context exclusivity
  marker" regardless, so the open verification question does not affect
  applicability, only which existing Clanks may already be non-conforming
  in practice (a conformance-audit question, out of this pass's scope).

## Recommendation

**READY FOR REVIEW** for the ratification survey — this candidate has
already passed one adversarial review pass (Pass 2, verdict `DRAFT AS
STD-OPS-COM-004`) before being drafted, one stage further through review
than OPS-A/B/C had gone when they were first drafted at Pass 1.
