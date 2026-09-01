# deployment

Deployment standards govern whether intended repository/configuration state has
become the materially running target state, and whether evolving persistent
state is compatible before normal work begins. They do not prescribe Git,
SSH, Docker, systemd, SQL, or any deployment topology.

**2 `RATIFIED`, 0 `PROPOSED`** (2026-08-31, by operator acceptance of
[decisions/0018](../../decisions/0018-deploy-com-001-decision.md) and
[decisions/0019](../../decisions/0019-deploy-com-002-decision.md), following
the [Pass 3 ratification survey](../../docs/deployment/pass3/ratification-survey.md)).
The domain is **READY TO FREEZE DEPLOYMENT STANDARDS V1.0** following the
[Pass 4 hold-resolution/final-gap audit](../../docs/deployment/holds-disposition.md):
**NO ESSENTIAL DEPLOYMENT CONTRACT MISSING**. It is not frozen yet; no
baseline or tag exists until a separate mechanical freeze pass.

| id | title | version | status |
|---|---|---:|---|
| [STD-DEPLOY-COM-001](STD-DEPLOY-COM-001.json) | Deployment completion must be verified as intended state materially running | 1 | RATIFIED |
| [STD-DEPLOY-COM-002](STD-DEPLOY-COM-002.json) | Persistent-state compatibility must gate normal operation | 1 | RATIFIED |

Agent-facing layer: [ratified-index.json](ratified-index.json),
[agent-checklist.json](agent-checklist.json), and
[docs/deployment/constitution.md](../../docs/deployment/constitution.md).
The admitted Deployment evidence layer is
[known-evidence-index.json](known-evidence-index.json), generated from active
`audits/*.md` structured blocks by `tools/deployment_agent_layer.py`. It records
the confirmed Watch conformance audit separately from the normative ratified
index; historical failed/insufficient audits remain preserved and are
superseded rather than rewritten.

Read [Pass 1](../../docs/deployment/pass1/README.md) for provenance and
distinctness. Destructive-state mutation remains rehomed to the ADR-0009
Architecture/Security/Recovery path (PROPOSED — REVIEWED DRAFT, not
activated); target identity is a facet of COM-001, not a standalone
standard.
