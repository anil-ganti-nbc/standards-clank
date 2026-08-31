---
cluster: running-revision-identity
likely_domain: DEPLOYMENT
priority: HIGH
evidence_strength: STRONG
---
# Running revision identity

**Concern:** source SHA, image label, host checkout, and running process can disagree; a deployment claim needs target-evidenced identity and stated host coverage.

- **Supporting incidents:** DEP-INC-003, DEP-INC-008, DEP-INC-009, DEP-INC-010.
- **Positive implementations:** smartwatch five-way parity; watch/oem-radar three-way identity; SemInt’s explicit UNVERIFIED_PRODUCTION hold.
- **Lineage:** independent convergence across watch, oem-radar, smartwatch, CTW, SemInt; shared governance in Fleet Law 6 and deferred Law 9.
- **Strongest evidence:** tablet’s missed-host false negative plus documented live allowlist drift.
- **Contrary evidence:** no contrary evidence; not every repo has a live host available for verification.
- **Overlap:** Architecture governance; Diagnostic inventory; Fleet Law 6 ACTIVE and Law 9 DEFERRED.
- **Severity / recurrence:** high / high.
- **Candidate standardisation risk:** directly restating ACTIVE Law 6; Pass 0B must distinguish a standards gap from enforcement coverage.
- **Unanswered questions:** what is minimum identity evidence where no OCI image exists?
