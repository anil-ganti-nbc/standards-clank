---
id: lifecycle-state-model-blocked-is-prose-not-code
domain: operations
topics: [4]
confidence: MODERATE
priority: MEDIUM
---

## Concern

Several fleet members record a source's "BLOCKED from production" (or
equivalent) status only as prose in a ticket/handoff doc, never as an
enforced enum value or database column — meaning nothing in the code
actually prevents a future careless promotion/allowlist edit from
re-including it.

## Current terminology

See [terminology-map.md](../terminology-map.md) "Lifecycle / maturity
states" table for the full per-repo breakdown.

## Repos surveyed

All nine fleet Clanks, plus `clank-architecture` and `diagnostic-clank`
(both of which have the most formally complete lifecycle contracts found
in the survey, neither yet adopted by any individual Clank's own code).

## Independent evidence

- smartwatch-clank: `coros_updates` is described as "BLOCKED from
  production promotion (2026-08-30 final review)" in a ticket, but
  remains coded as an ordinary `EXPERIMENTAL`-tier collector — the
  `CollectorTier` enum has only `PRODUCTION`/`EXPERIMENTAL` values,
  nothing structurally prevents promotion by a future allowlist edit.
- oem-radar: lifecycle states (`EXPERIMENTAL`/`SOAKING`/`RESEARCH_ONLY`)
  exist entirely in prose handoff docs — no enum found anywhere in the
  codebase.
- korean-tech-wire: `HOST-BLOCKED` is a prose classification inside a
  repair doc; the source (SK hynix) stays coded `status: PRODUCTION`
  in config even while completely non-functional.
- watch-clank: "retirement" (permanent removal) has "no explicit
  'deprecated' flag anywhere" — retirement is a full manual removal from
  every surface, not a state transition.
- semiconductor-intelligence: "if a source is permanently gone, there's
  currently no `remove-source` [command]... treat it as retired" — an
  explicit operator-convention substitute for a real state.
- tablet-clank, smartphone-clank: the two most formally-modeled repos
  (real enums/config fields for validation state), but even these have
  no distinct "temporarily blocked" vs. "permanently disabled" split.

## Inherited evidence

`clank-architecture/clank_runtime/contracts/lifecycle.py` defines the
most complete model found anywhere in the survey:
`ALLOWED_SOURCE_TRANSITIONS` (`DISCOVERED → RESEARCH → EXPERIMENTAL →
SOAK → PRODUCTION`, with parallel `DISABLED`/`QUARANTINED` states
reachable from nearly every state, and `PRODUCTION → SOAK` explicitly
allowed for "demote for re-soak after major change"). `NO_PROMOTION_POLICY.md`
separately defines `PROTOTYPE`/`UNVERIFIED_PRODUCTION`/
`VERIFIED_PRODUCTION`/`QUARANTINED` at the fleet-supervisory layer. **Neither
model has been adopted by any individual Clank's own code** — this is a
governance/contract-layer design that exists ahead of actual fleet
practice, not a description of it.

## Incidents

No incident was found where a BLOCKED-in-prose source was actually
re-promoted by accident — this cluster is evidenced by a clear,
convergent code/prose gap and the near-miss shape of INC-013 (a
different but related dual-gate drift), not by a confirmed harmful
promotion. INC-033 (smartwatch-clank's blocked `coros_updates`) is the
motivating example but was correctly kept blocked at time of survey.

## Implementations

Most complete formal models: `clank-architecture`'s
`lifecycle.py`/`NO_PROMOTION_POLICY.md` (contract-layer, unadopted).
Most complete *adopted* models: smartphone-clank (two independent state
machines, though the multiplicity is itself flagged in-repo as
confusing), tablet-clank (deliberately minimal, two states plus overlay
allowlists).

## Counterexamples

None disputing the concern.

## Harm if violated

Speculative — no confirmed incident of an actual accidental
re-promotion of a prose-blocked source was found, though the mechanism
gap (nothing code-level prevents it) is confirmed in at least two repos
(smartwatch-clank, korean-tech-wire, oem-radar).

## Likely domain

Operations.

## Unresolved questions

- Given `clank-architecture` already has a considerably more complete
  lifecycle contract than any individual Clank has adopted, should a
  Standards Clank Operations standard here point at
  `clank-architecture/clank_runtime/contracts/lifecycle.py` as the
  reference model to adopt, rather than defining a new one?
- Is the standardizable consequence "a BLOCKED/DISABLED determination
  must be enforced by code, not only recorded in prose," or is the
  weaker "a BLOCKED/DISABLED determination must at minimum be
  re-checked by an automated gate before promotion, even if the
  original block itself is prose-recorded" a more realistic bar given
  current fleet practice?
