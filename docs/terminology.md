# Terminology

**Clank** — an independent web-scraping/editorial-QC project in the fleet
(e.g. watch-clank, oem-radar, tablet-clank). Each is its own repository.

**Standard** — a single normative requirement, identified by a stable `id`,
with a `level` (MUST/SHOULD/MAY) and a `status` (PROPOSED/REVIEWED/
RATIFIED/SUPERSEDED/RETIRED). Defined in
[../schemas/standard.schema.json](../schemas/standard.schema.json).

**Domain** — the area a standard belongs to (ui, collectors, sources,
classification, events, evidence, health, delivery, soak, security,
operator-workflow). Encoded in the standard's `id` (e.g. `STD-UI-COM-001`)
and its `domain` field.

**Profile** — a named class of Clank (e.g. news-based, sku-based) that
determines which standards apply to a given Clank. See
[../profiles/README.md](../profiles/README.md).

**Exception** — a recorded, time-bounded deviation from a ratified standard
for a specific Clank. See [../exceptions/README.md](../exceptions/README.md).

**Evidence** — a reference to the origin of a standard: an incident, an
operator requirement, a cross-Clank pattern, an architectural invariant, a
regression, or an experimental finding. Standards Clank stores references,
not duplicated history. See [../evidence/README.md](../evidence/README.md).

**Ratification** — the explicit act, by the operator, of moving a standard
from REVIEWED to RATIFIED. Cannot be performed by an AI agent on its own
proposal. See [governance.md](governance.md).

**Conformance** — whether a specific Clank meets a specific ratified
standard. Assessed via [../audits/README.md](../audits/README.md); not
something Standards Clank enforces automatically.

**Diagnostic Clank** — the separate repository that records what failed and
what was learned in production. Standards Clank references its incidents as
evidence; it does not duplicate its ledger.

**Motherclank** — the separate fleet-orchestration system. Standards Clank
is not Motherclank and does not schedule, deploy, or operate anything.
