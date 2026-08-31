---
cluster: schema-code-compatibility
likely_domain: DEPLOYMENT
priority: HIGH
evidence_strength: STRONG
---
# Schema/code compatibility

**Concern:** new code, migrations, and persisted schemas can cross a deploy boundary in an incompatible order, including a start that appears successful before runtime failure.

- **Supporting incidents:** DEP-INC-001, DEP-INC-002.
- **Positive implementations:** watch schema check exits on mismatch; smartphone makes Alembic sole authority and fails entrypoints closed.
- **Lineage:** two independent incident lineages; Operations seed `schema-deploy-fail-closed-gating` reused.
- **Strongest evidence:** smartphone recurrence proves an implementation-shaped migration action was not a safe compatibility gate.
- **Contrary evidence:** CTW/tablet/feature-phone lack an equivalent gate without a known incident; SemInt’s check is post-hoc health.
- **Overlap:** Data/Ontology (schema authority), Testing, Operations; architecture GIC-14.
- **Severity / recurrence:** high / high.
- **Candidate standardisation risk:** universal migration mechanics would violate heterogeneous implementation scope.
- **Unanswered questions:** is fail-closed before traffic essential, or can a demonstrably equivalent compatibility gate suffice?
