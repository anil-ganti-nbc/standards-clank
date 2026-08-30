---
id: baseline-epoch-continuity
domain: data-ontology
clusters: [A, D, F]
confidence: STRONG
priority: HIGH
---

# Baseline / Epoch Continuity After Data Loss or Restore

## Concern

When a Clank's database is lost, restored from an older backup, or
re-baselined from scratch, the resulting discontinuity must be represented
as an explicit fact (a new epoch, a recorded gap) — never silently treated
as either "nothing happened" (risking absence-inside-the-gap being read as
zero/novelty) or "this is fresh discovery" (flooding false novelty).

## Current terminology

`OperationalEpoch` (watch-clank), `core/continuity.py` /
`ContinuityEvent` (feature-phone-clank, smartwatch-clank — smartwatch-clank
explicitly names `EPOCH_ID`), `DATABASE_LIFECYCLE.md` epoch cutover
(oem-radar, documentation-only, no schema column), `ADR-0006
"Observational Continuity and Epoch Semantics"` (clank-architecture,
PROPOSED draft), `NEW_EPOCH`/`DB-LOSS-RESTORE`/`DB-LOSS-NEW-EPOCH` (golden
incidents, clank-architecture).

## Repos surveyed

watch-clank, oem-radar, feature-phone-clank, tablet-clank,
smartwatch-clank, smartphone-clank, chinese-tech-wire, korean-tech-wire —
plus clank-architecture (ADR-0006) and diagnostic-clank (golden incidents
DB-LOSS-RESTORE / DB-LOSS-NEW-EPOCH / DB-008).

## Independent evidence

- **watch-clank**: `OperationalEpoch` model, exactly one active epoch per
  DB; a second, independent mechanism (`initial_fill.py`) was added after
  discovering the epoch mechanism alone was insufficient for
  bounded-per-run-budget catalogues.
- **feature-phone-clank**: `core/continuity.py`, built in direct response
  to a real 2026-08-23 data-loss incident (no backup existed at the time).
- **smartwatch-clank**: `core/continuity.py`, built in direct response to
  a real 2026-08-23 data-loss incident — but **explicitly cites
  clank-architecture's ADR-0006** as its architectural authority, not an
  independent invention (see Inherited evidence).
- **oem-radar**: a documentation-only epoch-cutover procedure with an
  explicit preflight check (`count_unseeded_listings()` must be 0 before
  cutover) — a different mechanism (no schema column at all; "the epoch
  boundary *is* which file is currently at `data/radar.db`"), same intent.

## Inherited evidence

smartwatch-clank's `continuity.py` is the one confirmed case in this pass
of a Clank explicitly building its data model against a named
architectural document (`clank-architecture` ADR-0006 and
`DATA_SURVIVABILITY.md`) rather than inventing it locally. watch-clank,
feature-phone-clank, and oem-radar's mechanisms show no cross-citation to
each other or to ADR-0006 — independently converged, not copied.

## Incidents

- watch-clank: three related, dated incidents (Epoch-1 freshness,
  Timex baseline absorption, Timex catalogue backfill burst) — the last
  one's addendum documents a **live, unresolved production risk**:
  Hetzner's `operational_epochs` table is empty; baseline protection
  depends entirely on a manually-passed `--force-baseline` flag with no
  automated safeguard. Three remediation options proposed, none
  implemented. See incident-ledger.md INC-03.
- feature-phone-clank: 2026-08-23 destructive volume deletion, no backup
  existed, new epoch declared with the lost epoch's identity permanently
  recorded as unknown (not fabricated). INC-13.
- smartwatch-clank: 2026-08-23 destructive volume deletion, restored from
  an older backup — **handled correctly**: the continuity ledger's seed
  event explicitly states "absence inside this window is never zero and
  never novelty; post-gap returns must be evaluated without backfilling."
  INC-21.
- oem-radar: baseline events masquerading as fresh alerts (INC-07),
  structurally the same failure shape as watch-clank's INC-01 but at the
  "flag exists but isn't read downstream" layer rather than the epoch
  layer itself.
- clank-architecture golden incidents `DB-LOSS-RESTORE` and
  `DB-LOSS-NEW-EPOCH` are executable fixtures matching this exact concern,
  independent of any specific Clank's incident.

## Implementations

Four independent implementations exist (watch-clank, oem-radar,
feature-phone-clank, smartwatch-clank), plus one explicit unimplemented
draft standard (ADR-0006) that already specifies the contract
(`ContinuityEvent` types: `DATA_LOSS`/`RESTORE_FROM_BACKUP`/`NEW_BASELINE`/
`EPOCH_BOUNDARY`/`OBSERVATION_GAP`/`SCHEDULER_OUTAGE`/`UNKNOWN_CONTINUITY`;
"a fresh baseline is never novelty"; "absence is never zero").

## Counterexamples

tablet-clank and korean-tech-wire have no continuity/epoch mechanism at
all and no documented data-loss incident — genuinely inapplicable so far,
not a conflation. smartphone-clank has **no epoch/continuity concept
whatsoever** despite having its own real, ongoing schema-integrity
near-miss (INC-19, "still completely real and still unresolved" per the
repo's own docs) — this is a gap, not a counterexample against the
invariant.

## Harm if violated

Demonstrated directly: false novelty floods (watch-clank INC-03, ~1045
events), false negative-certainty (absence-as-zero risk explicitly named
in ADR-0006 and avoided by smartwatch-clank INC-21), and a currently-live
production exposure with no automated safeguard (watch-clank's empty
Hetzner `operational_epochs` table).

## Likely domain

Data/ontology, core case. Overlaps operations only at the trigger point
(a data-loss event is operational; how it's *represented* afterward is
squarely data/ontology).

## Unresolved questions

1. Should `--force-baseline` (or equivalent) ever be allowed to be a
   manually-invoked, un-audited flag, or must epoch/baseline state always
   be database-resident and automatically detected? watch-clank's live
   unresolved risk is a direct test case.
2. Should Standards Clank adopt, adapt, or explicitly decline
   clank-architecture's ADR-0006 as the fleet-wide contract? It already
   exists, in draft, and one Clank already builds against it.
3. Why do independent implementations (watch-clank, oem-radar,
   feature-phone-clank) not cite ADR-0006 at all — was it written after
   them, or is it simply unknown to those teams?

## Confidence: STRONG
## Adjudication priority: HIGH
