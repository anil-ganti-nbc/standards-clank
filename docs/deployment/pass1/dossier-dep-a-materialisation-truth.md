# Dossier — STD-DEPLOY-COM-001

- **Candidate provenance:** DEP-A, `docs/deployment/pass0/candidates/dep-a-deployment-materialisation-truth.md`.
- **Source clusters:** 01 materialisation truth, with 02 running revision identity, 04 partial wiring, 06 target scope, and charter DEP-C merged as facets.
- **Pass 0B disposition:** KEEP DISTINCT / ADVANCE. Target identity is rejected standalone; destructive mutation is rehomed.
- **Recommendation:** **READY FOR REVIEW**.

## Strongest evidence and accounting

The Garmin wrapper divergence (DEP-INC-004) is strongest: a corrected
code/config path was insufficient because the separately maintained production
execution path lacked required wiring. Stale image selection (DEP-INC-001) and
live host/repository drift (DEP-INC-009) corroborate the congruence gap.
All four cited incidents are **REUSED FROM OPERATIONS PASS 0**. Pass 0A has 10
reused incidents and **0 newly discovered Deployment-specific incidents**.

## Independent lineages

Three independent causal lineages support the concept: stale tag/image,
wrapper/config divergence, and host/repository drift. Five-way/three-way
runtime identity practices are positive convergence, not independent incident
votes.

## Existing-standard distinctness proof

OPS-COM-001 asks whether execution materialised and what outcome it produced;
OPS-COM-002–004 address health, promotion evidence, and ownership validity.
They can all be true for a stale old revision. COM-001 instead asks whether
what is materially running equals the declared intended deployment state.
Data/Ontology rules govern data meaning and structure, not intended-to-running
deployment equality.

## Fleet Law / ADR relationship

Fleet Law 5 remains ACTIVE authority for scheduler exclusivity. Fleet Law 6
remains ACTIVE authority for host-evidenced SHA/digest mechanics; this draft
requires comparable intended/running provenance but does not restate its
mechanics. Law 9 remains DEFERRED. ADR-0008 is complementary. ADR-0009 is
unaffected and remains PROPOSED — REVIEWED DRAFT.

## Strongest counterexample and trigger analysis

A Git-less managed/serverless deployment has no SSH host, Docker, systemd, or
repository checkout. It survives: platform-native build/alias identity can
compare declared and served artifact state. The trigger is any represented
deployment transition, not any particular implementation. A purely local tool
without such a transition is N/A.

## Acceptance analysis and implementation freedom

The draft requires a stated target scope; comparable intended/running artifact
identity; deploy-critical config only where divergence matters; required
runtime wiring only where it matters; and explicit partial/in-progress status.
It does not require atomic rollout, config hashes, Git, immutable images,
containers, systemd, restart commands, or a particular topology.

## Unresolved wording questions

Should future review require a durable record of a completion claim, or only
verification capable of supporting one? The draft intentionally says the
latter. Review should also test whether “deploy-critical” is sufficiently
bounded without demanding a universal configuration inventory.
