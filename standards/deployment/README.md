# deployment

Deployment standards govern whether intended repository/configuration state has
become the materially running target state, and whether evolving persistent
state is compatible before normal work begins. They do not prescribe Git,
SSH, Docker, systemd, SQL, or any deployment topology.

**2 `RATIFIED`, 0 `PROPOSED`** (2026-08-31, by operator acceptance of
[decisions/0018](../../decisions/0018-deploy-com-001-decision.md) and
[decisions/0019](../../decisions/0019-deploy-com-002-decision.md), following
the [Pass 3 ratification survey](../../docs/deployment/pass3/ratification-survey.md)).
The domain is **not frozen** — no hold-resolution/final-gap pass has been
performed and no baseline/tag exists yet.

| id | title | version | status |
|---|---|---:|---|
| [STD-DEPLOY-COM-001](STD-DEPLOY-COM-001.json) | Deployment completion must be verified as intended state materially running | 1 | RATIFIED |
| [STD-DEPLOY-COM-002](STD-DEPLOY-COM-002.json) | Persistent-state compatibility must gate normal operation | 1 | RATIFIED |

Agent-facing layer: [ratified-index.json](ratified-index.json),
[agent-checklist.json](agent-checklist.json), and
[docs/deployment/constitution.md](../../docs/deployment/constitution.md).
No known-evidence-index exists because no Deployment conformance audit has
been performed against any Clank.

Read [Pass 1](../../docs/deployment/pass1/README.md) for provenance and
distinctness. Destructive-state mutation remains rehomed to the ADR-0009
Architecture/Security/Recovery path (PROPOSED — REVIEWED DRAFT, not
activated); target identity is a facet of COM-001, not a standalone
standard.
