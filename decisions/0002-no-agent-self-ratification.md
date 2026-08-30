# 0002 — Explicit ratification; no agent self-ratification

Date: 2026-08-30
Status: Accepted

## Decision

Standards Clank uses an explicit ratification step
(`PROPOSED -> REVIEWED -> RATIFIED`, see
[../docs/governance.md](../docs/governance.md)) and does not permit an AI
agent to ratify a standard it proposed, or any standard, on its own
authority. The same restriction applies to exception approval (see
[../exceptions/README.md](../exceptions/README.md)): an agent may propose
an exception but may not approve it.

## Rationale

Standards Clank is meant to become the normative layer other Clanks are
measured against. If an agent could propose and ratify in the same action,
the review and ratification steps would be theater rather than a real
check. The operator is the accountable party for the fleet and must remain the
final decision-maker for anything that becomes binding.

## Consequence

Any tooling built on top of this repository (CI checks, PR automation,
future agent workflows) must treat a `RATIFIED` status change and an
`APPROVED` exception status change as requiring a human-attributable
approval, not merely a passing schema check.
