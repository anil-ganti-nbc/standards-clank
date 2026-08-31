# Deployment Pass 1 — Drafting

This pass drafts exactly the two Pass 0B ADVANCE candidates as PROPOSED,
version-1 standards. It is not a ratification or review pass, and it does not
recrawl the fleet.

| Candidate | Draft | Dossier | Recommendation |
|---|---|---|---|
| DEP-A | [STD-DEPLOY-COM-001](../../../standards/deployment/STD-DEPLOY-COM-001.json) | [dossier-dep-a-materialisation-truth.md](dossier-dep-a-materialisation-truth.md) | READY FOR REVIEW |
| DEP-D | [STD-DEPLOY-COM-002](../../../standards/deployment/STD-DEPLOY-COM-002.json) | [dossier-dep-d-schema-code-compatibility.md](dossier-dep-d-schema-code-compatibility.md) | READY FOR REVIEW |

Evidence accounting is deliberately unchanged: all 10 Deployment Pass 0A
incidents were reused from Operations Pass 0; newly discovered
Deployment-specific incidents: **0**. This pass makes no new evidence claim.

Not drafted: destructive production-state mutation (rehomed to ADR-0009 and
Architecture/Security/Recovery); a standalone target-environment identity
standard (rejected, retained only as COM-001 target scope); the merged running
identity and partial-wiring facets as separate standards. No target Clank or
`clank-architecture` was modified.
