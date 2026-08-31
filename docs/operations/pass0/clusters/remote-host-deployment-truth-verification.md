---
id: remote-host-deployment-truth-verification
domain: operations
topics: [12, 14]
confidence: STRONG
priority: HIGH
---

## Concern

A repository's HEAD, a tag/branch name, or an operator's belief about
what's deployed on a remote host are all, independently, insufficient
evidence of what's actually running there. Repeatedly, only a direct,
live check of the remote host (not the repo, not a label) surfaced the
truth — and the fleet has independently converged on a multi-way
cross-check pattern (comparing git SHA, OCI image label, and a
live-reported runtime identity) as the working mitigation.

## Current terminology

"Provenance verification," "commit parity," "three-way" or "five-way"
SHA check — no single shared name, but a strikingly consistent mechanism
across repos.

## Repos surveyed

watch-clank, oem-radar, smartphone-clank, feature-phone-clank,
smartwatch-clank, chinese-tech-wire, tablet-clank, semiconductor-intelligence,
`clank-architecture`, `diagnostic-clank`.

## Independent evidence

- watch-clank: three-way check (git SHA vs OCI label vs runtime
  `get_identity()`); also an honestly-disclosed, unresolved gap — an old
  invocation mechanism "is very likely still firing" against the same
  volume, and the team could not close this without root access.
- oem-radar: `DEPLOYMENT_PROCEDURE.md` mandates the same three-way check
  before trusting any deployment, citing a 2026-08-09 prior incident by
  reference (not independently located as a standalone doc in this
  survey).
- smartphone-clank: deployed SHA verified via the running service's own
  `WorkingDirectory`, not a tag/branch name; two real "invisible until
  deployed" bugs (missing `alembic` in requirements, an unanchored
  `.gitignore`) were found *only* by doing a genuinely clean remote
  checkout.
- smartwatch-clank: five-way commit-parity check (local main, GitHub
  main, Hetzner git checkout, Hetzner Docker image label, Hetzner running
  CLI identity) — the most thorough version found in the fleet.
- chinese-tech-wire: hand-maintained per-release identity tables; three
  independently-computed labels (OCI label, `--identity` output, GitHub
  SHA) checked equal rather than trusted from one source.
- tablet-clank (INC-030): a fleet-wide "timer not found" sweep covering
  NAS/WSL/Windows produced a **false negative** by never checking
  Hetzner, the one host where the timer was actually live — proof that
  even a deliberate cross-host sweep can itself be incomplete.
- semiconductor-intelligence: `PHASE0_CONTAINMENT.md` explicitly
  classifies itself `UNVERIFIED_PRODUCTION` until "the canonical fleet
  ledger records the deployed artifact digest and a real Windows task
  completes two unattended runs from the installed path" — a
  verification bar stated as a precondition, not assumed met.

## Inherited evidence

`clank-architecture/RISK_REGISTER.md` R-001 (Critical): "Repository head
is mistaken for the deployed artifact. Containment: Canonical ledger
separates `source_sha` from `deployed_sha`." `FLEET_LAWS.md` Deferred Law
9: "A repository's default branch must never trail its own production
checkout longer than one review cycle" — with named, still-open
violations at time of the fleet archaeology audit (KTW, SemInt). The
entire `diagnostic-clank/operations/phase0/` package
(`OPERATOR_INSTANCE_CHECKLIST.md`, `preflight.py`) exists specifically to
formalize this verification, keeping HETZNER/NAS deployment facts as
explicit `UNKNOWN` placeholders until operator-confirmed rather than
assumed.

## Incidents

INC-017 (smartphone-clank's clean-checkout-only-visible bugs), INC-030
(tablet-clank's false-negative sweep), INC-031 (tablet-clank's allowlist
drift, an ongoing instance), INC-038 (CTW's cutover-readiness finding —
"Hetzner canonical" was informal convention, never actually verified),
INC-039 (ClankLift census — access gaps themselves blocked
verification), INC-040 (diagnostic-clank's own instance found stale by
census, not by any automatic check).

## Implementations

The multi-way SHA/identity cross-check pattern (watch-clank, oem-radar,
smartphone-clank, smartwatch-clank, chinese-tech-wire, feature-phone-clank
all have some form of it) is the strongest, most consistently-adopted
mitigation in this entire survey — arguably a fleet-wide best practice
already, even without a formal standard. The weak point found is not the
mechanism but its *coverage*: INC-030 shows a verification sweep can
still miss a host if it isn't included in the sweep's own scope.

## Counterexamples

None disputing the concern.

## Harm if violated

INC-017's two "invisible until deployed" bugs demonstrate that trusting
repo state over live host state actively misses real defects. INC-030
demonstrates the inverse risk (a verification process itself being
incomplete) — worth noting a standard here needs to guard against both
directions of failure, not just "verify against the live host" alone.

## Likely domain

Operations.

## Unresolved questions

- Given how convergently the multi-way cross-check pattern is already
  adopted, is the standardizable gap actually "coverage completeness" —
  i.e. requiring that a deployment-truth verification process explicitly
  enumerate every host in scope rather than relying on an implicit or
  partial list (the exact shape of INC-030's failure)?
- Should a Standards Clank rule reference `clank-architecture`'s
  RISK_REGISTER R-001/Fleet Law 9 rather than restate them, given they
  already exist as adopted (Law 9 marked "Deferred" specifically,
  R-001 as an open risk-tracking item, not yet a ratified law)?
