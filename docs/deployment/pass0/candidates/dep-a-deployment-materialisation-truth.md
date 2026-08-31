# Candidate Card — DEP-A: Deployment Materialisation Truth

Status: CANDIDATE (Pass 0B adjudication). Not drafted, not ratified, not
normative.

## Candidate name
Deployment Materialisation Truth (from Pass 0A cluster 01; absorbs facets of
clusters 02, 04, 06 and charter DEP-C).

## Plain-language invariant
A deployment may be represented as complete or successful only when the
declared intended deployed state — intended revision/artifact, deploy-critical
configuration, and required runtime wiring components — is verified as
materially running in a stated target environment.

## Trigger / applicability
Any Clank deployment that is represented as complete. N/A only where no
deployment representation is made. Facets collapse (but do not fail) on
platforms with immutable/externally managed artifacts.

## Strongest evidence
Garmin production/soak wrapper divergence (DEP-INC-004): the corrected code/
config path did not repair the separately maintained production wrapper —
a successful deployment pathway left required runtime wiring silently
displaced. Supported by stale-image compose start (DEP-INC-001) and
unresolved host/repo drift (DEP-INC-009).

## Incident references
DEP-INC-001, DEP-INC-004, DEP-INC-006, DEP-INC-009 (all reused from
Operations Pass 0 — see accounting in adjudication.md §5).

## Independent lineage count
3 (DEP-INC-001; DEP-INC-004; DEP-INC-009). DEP-INC-006 shares the drift
shape but is not counted as a fourth independent vote.

## Reused incident count
4. Newly discovered deployment-specific incidents: 0.

## Existing-standard distinctness proof
STD-OPS-COM-001/002/003 govern truthful records about whatever is running
(invocation/outcome facts, health axes, promotion/soak evidence); COM-004
governs ownership validity; Data standards govern meaning and record
discipline. An implementation conforming to all of them can still fail this
invariant: an old revision keeps running correctly and records perfect OPS
evidence while the intended state never materialised. No ratified standard
requires intended-vs-running equality.

## Fleet Law / ADR relationship
- Fleet Law 5 (ACTIVE): COMPLEMENTARY — owns scheduler authority exclusivity.
- Fleet Law 6 (ACTIVE): DEFER TO EXISTING AUTHORITY for identity-evidence
  mechanics; this candidate requires parity but does not restate Law 6.
- Law 9 (DEFERRED), ADR-0008: no conflict; no competing authority.

## Strongest counterexample
Serverless/managed-platform deployment: there is no host, no unit file, no
compose; the platform is the deploy authority.

## Why it survives
The counterexample still owes the same duty in platform terms: the declared
revision/alias must be verified as the served revision in the stated target
before the deployment is represented as complete. The invariant is a
verification duty over an equality, not a mechanism — it survives every
listed counterexample (Git-less packages via package version/digest/build
metadata; immutable images via baked config; blue/green via lane-scoped
completeness claims; declarative platforms via declared-vs-synced parity).

## Implementation freedoms
Any tool or none: manual checklists, scripts, platform-native revision
aliases, CI gates. Verification may be eager at deploy time or at a defined
readiness point. Identity may be a Git SHA, OCI digest, package version, or
build metadata. No systemd, Docker, SSH, cron, or deploy-script requirement.
Intentional, declared, isolated lane divergence remains legitimate.

## Evidence strength
STRONG.

## Fleet impact
HIGH.

## Standardisation risk
MEDIUM — mitigated by implementation neutrality and explicit Law 5/6
deference.

## Recommendation
ADVANCE (to drafting in a later pass, only if the operator schedules one).
