---
cluster: rollback-recovery-and-mutation
likely_domain: ARCHITECTURE / SECURITY / DEPLOYMENT overlap
priority: MEDIUM
evidence_strength: MODERATE
---
# Rollback, recovery, and deploy-time state mutation

**Concern:** rollback claims are incomplete when durable state is incompatible or destructive deploy actions lack resolved identity and recovery proof.

- **Supporting incidents:** DEP-INC-005.
- **Positive implementations:** smartwatch pre-deploy readable backup; Diagnostic checklist records restore evidence and compatible rollback artifact as required evidence.
- **Lineage:** one incident family, explicitly inherited into ADR-0009 rather than independent convergence.
- **Strongest evidence:** two naming-inference volume-loss incidents, one unrecoverable.
- **Contrary evidence:** no contrary evidence; limited independent incident count.
- **Overlap:** Architecture, Security, Recovery. ADR-0009 is PROPOSED — REVIEWED DRAFT, not ACTIVE; its conformance is partial.
- **Severity / recurrence:** critical / high.
- **Candidate standardisation risk:** competing authority with ADR-0009; likely rehome/defer rather than a Deployment concern.
- **Unanswered questions:** who owns activation and what recovery proof is applicable per storage topology?
