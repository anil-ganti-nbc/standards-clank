# Deployment Pass 0A — Evidence Inventory

This is an evidence-only archaeology pass. It records what the inspected
repositories and incident records show about the transition from intended
repository/configuration state to materially running target-environment state.
It creates no Deployment standard, candidate, normative status, or target-repo
change. Pass 0B must adjudicate the clusters; it must not treat them as rules.

## Scope and result

Eleven repositories were inspected read-only at the SHAs recorded in
[evidence-log.md](evidence-log.md). The original Operations rehomes survived,
but only after re-framing: config drift, remote-host truth, and schema gating
are distinct deployment concerns which overlap around materialisation.

| Cluster | Priority | Evidence strength |
|---|---:|---:|
| [01-materialisation-truth](clusters/01-materialisation-truth.md) | HIGH | STRONG |
| [02-running-revision-identity](clusters/02-running-revision-identity.md) | HIGH | STRONG |
| [03-schema-code-compatibility](clusters/03-schema-code-compatibility.md) | HIGH | STRONG |
| [04-partial-deployment-wiring](clusters/04-partial-deployment-wiring.md) | MEDIUM | MODERATE |
| [05-rollback-recovery-and-mutation](clusters/05-rollback-recovery-and-mutation.md) | MEDIUM | MODERATE |
| [06-target-environment-identity](clusters/06-target-environment-identity.md) | LOW | LIMITED |

The evidence distinguishes a successful deploy command from proof that the
intended state is materially running. See the terminology map and ledger for
the underlying language and causal records.
