# Deployment Pass 0A → Pass 0B Handoff

**DO NOT RECRAWL THE FLEET.** Use this inventory first; perform only a targeted
verification for an identified unresolved claim.

- **Canonical Standards Clank HEAD:** `1ecc2530544f2c1995c6074d8aad0ba100730099` before this pass.
- **Survey scope:** eleven GitHub repositories, read-only, with exact SHAs in `evidence-log.md`.
- **Confirmed deployment-relevant incident records:** 10. **Reused Operations incidents:** 10 (all; no new vote created).
- **Clusters:** 6 — HIGH 3, MEDIUM 2, LOW 1.
- **Strongest clusters:** materialisation truth; running revision identity; schema/code compatibility; partial wiring; rollback/recovery mutation (critical impact but governance-owned).
- **Weakest:** target environment identity: one missed-host incident, no confirmed wrong-host deployment.
- **Independent convergence:** multi-way runtime revision parity across at least six repositories; independent fail-closed schema safeguards in watch and smartphone; explicit isolated-lane topology in feature-phone.
- **Shared/inherited lineages:** all ledger records are reused Operations evidence; volume-loss incidents are one ADR-0009 family, not two independent votes. Fleet Laws 5/6 are shared governance.
- **Governance:** Fleet Law 5 and 6 are ACTIVE and CI-backed; Law 9 is DEFERRED. ADR-0009 is verified **PROPOSED — REVIEWED DRAFT**; do not activate it or create competing authority.
- **Likely rehomes:** destructive mutation/recovery → Architecture/Security/Recovery; scheduler authority → Operations/active Law 5; schema authority has Data/Ontology overlap.
- **Original Operations rehomes:** all survive as deployment concerns, but do not collapse them automatically: materialisation, runtime identity, and schema compatibility have distinct failure shapes.
- **Targeted verification candidates:** current ADR-0008 status/wording if relied on; whether any live NAS incident path becomes available; whether Law 6 CI is adopted in every target repo (architecture suite is confirmed, per-repo adoption is not).

Read in this order: `README.md`, `incident-ledger.md`, all six `clusters/*.md`, `evidence-log.md`, `terminology-map.md`. No adjudication, standards drafting, ratification, target repair, Delivery work, or fleet recrawl belongs in Pass 0A.
