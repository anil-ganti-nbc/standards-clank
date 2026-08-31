---
id: safe-manual-intervention-during-soak
domain: operations
topics: [15]
confidence: MODERATE
priority: MEDIUM
---

## Concern

Can an operator manually intervene (force a run, pause, restart, abort)
during a soak/maturity window without corrupting the soak clock or the
data it's meant to validate? Distinct from cluster E (natural-vs-manual
trigger *provenance*): this cluster is about whether intervention is
*safe to perform at all*, not about whether its trigger source is later
verifiable.

## Current terminology

No shared vocabulary.

## Repos surveyed

watch-clank, oem-radar, smartphone-clank, feature-phone-clank,
chinese-tech-wire, korean-tech-wire, tablet-clank, smartwatch-clank,
`clank-architecture`.

## Independent evidence

- watch-clank: policy-only prohibition ("do NOT add manual re-runs
  outside schedule"); any manual DB surgery during soak disqualifies
  promotion evidence by gate, but no code-level guard was found
  preventing an operator from running a collector manually mid-soak.
- oem-radar, feature-phone-clank: architectural isolation (fully
  separate DB/checkout/lock for experimental work) makes the question
  largely moot — a manual production run cannot touch the soak clock
  because the soak clock lives somewhere else entirely.
- smartphone-clank: the mechanism found is tag-and-exclude — a manual
  "controlled validation" run is explicitly labeled and excluded from
  the natural-cycle tally, rather than disallowed outright; also
  demonstrated live restart-cycle testing *during* soak with explicit
  before/after integrity checks proving no corruption.
- korean-tech-wire: **a real, acknowledged gap** — because due-ness is
  derived purely from persisted run history, a manual run is
  indistinguishable, in storage, from a natural one, and *can* reset the
  same `consecutive_failures`/backoff state a scheduled run would
  (overlaps cluster E directly).
- tablet-clank (INC-032): the one dated incident in this cluster — an
  operator manually aborted a soak campaign mid-run to move hosts;
  handled carefully (read-only DB preflight, integrity verification,
  explicit exclusion of the partial cycles from later promotion
  evidence), but exposed an unfixed Windows signal-delivery gap along
  the way.
- smartwatch-clank: no formal soak-clock mechanism exists at all, so
  manual and scheduled runs share the same lock domain and the question
  doesn't arise in the same form.

## Inherited evidence

`clank-architecture` ADR-0006: manual/operator recovery actions after an
incident do not reset the soak clock; affected lanes instead report
UNKNOWN/NOT-YET-MATURE. `QC_SOAK_PRECONDITION_VERIFICATION.md`: pause/
restart authority over a Clank's own soak is explicitly withheld from
the fleet-level supervisor (Motherclank) until a future, not-yet-written
M5 ADR ("NOT NOW") — i.e. even the fleet's own supervisory-tooling design
treats "who may intervene in a soak" as an unresolved, deliberately
deferred question.

## Incidents

INC-032 (tablet-clank, the only dated incident — handled well, exposed a
residual OS-level gap left unfixed).

## Implementations

Best mitigations found: smartphone-clank's tag-and-exclude pattern,
oem-radar/feature-phone-clank's architectural isolation. Real gap:
korean-tech-wire's schema (manual runs indistinguishable from natural
ones in storage).

## Counterexamples

None.

## Harm if violated

Speculative for most of the fleet (no confirmed incident of manual
intervention corrupting soak evidence) — the one incident found
(INC-032) shows manual intervention handled *carefully* rather than
harmfully, though only because the operator, not the system, enforced
correctness.

## Likely domain

Operations.

## Unresolved questions

- Given only one dated incident, and that one shows the system being
  handled correctly rather than failing, should this stay MEDIUM
  priority, or does the korean-tech-wire structural gap (a manual run
  IS indistinguishable from natural evidence) push it toward HIGH given
  its overlap with cluster E's already-HIGH-priority concern?
- Is "safe manual intervention" better served by a standard requiring
  architectural isolation (oem-radar/feature-phone-clank's approach) or
  one requiring tag-and-exclude accounting (smartphone-clank's approach)
  — they are not mutually exclusive, but a standard may need to pick
  which consequence it actually requires versus merely permits.
