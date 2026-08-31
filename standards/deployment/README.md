# deployment

Deployment standards govern whether intended repository/configuration state has
become the materially running target state, and whether evolving persistent
state is compatible before normal work begins. They do not prescribe Git,
SSH, Docker, systemd, SQL, or any deployment topology.

**2 `PROPOSED`, 0 `RATIFIED`. This domain is not frozen.** These drafts came
from the Deployment Pass 0A evidence inventory and Pass 0B adjudication; they
are not ratified requirements and must not be treated as such.

| id | title | version | status |
|---|---|---:|---|
| [STD-DEPLOY-COM-001](STD-DEPLOY-COM-001.json) | Deployment completion must be verified as intended state materially running | 1 | PROPOSED |
| [STD-DEPLOY-COM-002](STD-DEPLOY-COM-002.json) | Persistent-state compatibility must gate normal operation | 1 | PROPOSED |

Read [Pass 1](../../docs/deployment/pass1/README.md) for provenance and
distinctness. Destructive-state mutation remains rehomed to the ADR-0009
Architecture/Security/Recovery path; target identity is a facet of COM-001,
not a standalone standard.
