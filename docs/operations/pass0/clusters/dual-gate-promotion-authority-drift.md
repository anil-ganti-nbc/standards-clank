---
id: dual-gate-promotion-authority-drift
domain: operations
topics: [5]
confidence: STRONG
priority: HIGH
---

## Concern

Where promotion to production requires two independently-maintained gates
to both agree (e.g. a maturity/tier flag AND a separate allowlist), the
two gates can drift apart, and only one of them being updated during a
promotion can leave a source silently promotable, silently blocked, or
(worst case) silently believed-safe while actually still exposed.

## Current terminology

See [terminology-map.md](../terminology-map.md) "Lifecycle / maturity
states" table for the specific gate names per repo.

## Repos surveyed

smartphone-clank, feature-phone-clank, tablet-clank, smartwatch-clank,
oem-radar, korean-tech-wire, semiconductor-intelligence,
`clank-architecture`.

## Independent evidence

- smartphone-clank (INC-013): two independent, uncross-checked gates
  (`WAVE1_PRODUCTION_SCOPE` vs `config.yaml::manufacturers`); only one
  was updated during a promotion, and the baseline-completion tracker
  evaluated *before* the second gate, marking a source's baseline
  "complete" while 18 real candidates were silently dropped. Would have
  produced 18 false newsroom alerts on the next scheduled run had it not
  been caught same-day.
- feature-phone-clank: explicitly built its (deliberately simpler,
  single-YAML-list) allowlist *because of* the smartphone-clank incident
  — direct, cited lineage (see [evidence-log.md](../evidence-log.md)
  lineage sections).
- tablet-clank: explicitly two-gate (`state` + `PRODUCTION_ALLOWLIST`)
  but designed so demoting `state` automatically removes production
  eligibility even if the allowlist tuple is stale — a structural
  mitigation for the same failure shape smartphone-clank suffered.
- smartwatch-clank: two-gate (`CollectorTier` + `production_allowlist`),
  and separately, `BLOCKED` status exists only as a ticket/prose label,
  never enforced by either gate (INC-033's collector remained
  structurally promotable by a careless future allowlist edit despite
  being "BLOCKED" in review notes) — a related but distinct drift risk
  (prose status vs. enforced gate, not two-gates-drifting-from-each-other).
- semiconductor-intelligence: append-only `CandidatePromotionEvent` audit
  trail plus a caught transactional bug (INC-024) where a rollback would
  have silently discarded a just-committed promotion — a different
  failure mode (promotion silently undone) within the same broad concern
  (promotion-state integrity).

## Inherited evidence

`clank-architecture/FLEET_LAWS.md` Law 8 ("Promotion gates": "No source
reaches production scheduling without soak evidence, an explicit
promotion record, and rollback state; conversely every production-scheduled
source appears in a promotion record") is **ACTIVE** governance, with
named historical violators across three different Clanks (tablet
"approved-never-scheduled promotion theater"; smartwatch "stage-c
merged-but-undeployed latent notify"; oem-radar "bankai soaks operated
outside any record until Phase 2A landed them") — i.e. this exact concern
already has adopted fleet-wide governance and a documented violation
history independent of this survey's own findings.

## Incidents

INC-013 (the clearest, most severe example — caught same-day, would have
produced 18 false alerts), INC-023 (korean-tech-wire's Samsung Newsroom
Korea — reliability alone insufficient promotion evidence, caught before
harm), INC-024 (semiconductor-intelligence's promotion-commit-ordering
bug), INC-033 (smartwatch-clank's prose-only BLOCKED status).

## Implementations

Best mitigations found: tablet-clank's demotion-cascades-through-both-gates
design, feature-phone-clank's single-list simplification,
semiconductor-intelligence's append-only audit trail. Still-open gap:
smartwatch-clank's BLOCKED-is-prose-only status (see also cluster N,
lifecycle states).

## Counterexamples

None disputing the concern.

## Harm if violated

INC-013's near-miss (18 false alerts averted only by same-day catch) is
the clearest quantified harm. `FLEET_LAWS.md`'s own violator list shows
this is not hypothetical at fleet scale — three separate Clanks have had
real promotion-authority-record gaps.

## Likely domain

Operations.

## Unresolved questions

- Like cluster C, this concern already has ACTIVE fleet governance
  (`FLEET_LAWS.md` Law 8). Should a Standards Clank standard here restate
  Law 8, narrow it, or explicitly defer to it? Same reconciliation
  question as cluster C — see [README.md](../README.md).
- Is "collapse to a single gate" (feature-phone-clank/tablet-clank's
  approach) or "keep two gates but make demotion of either cascade
  through both" (tablet-clank's specific mechanism) the better
  consequence to require, given both are represented in the fleet as
  working mitigations?
