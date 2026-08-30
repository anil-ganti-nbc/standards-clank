# Standards Clank

## What is it?

Standards Clank is the normative, machine-readable standards layer for the
Clank fleet. It will eventually define versioned MUST/SHOULD/MAY
requirements for how Clanks are built and operated — with rationale,
evidence, exceptions, and audit trails attached to every rule.

## Why does it exist?

Individual Clanks (watch-clank, oem-radar, semiconductor-intelligence,
chinese-tech-wire, korean-tech-wire, feature-phone-clank, smartphone-clank,
smartwatch-clank, tablet-clank, ...) have accumulated hard-won operational
lessons independently. [Diagnostic Clank](https://github.com/anil-ganti-nbc/diagnostic-clank)
records what failed and what was learned. Standards Clank exists to turn
*sufficiently supported* lessons into explicit, stable, auditable rules,
instead of leaving them as tribal knowledge or scattered incident notes.

## What does it standardise?

Contracts, invariants, semantics, and observable behaviour — see
[docs/charter.md](docs/charter.md) — across domains: UI, collectors,
sources, classification, events, evidence, health, delivery, soak,
security, and operator workflow. See [standards/README.md](standards/README.md)
for the full domain list.

## What does it not do?

It does not operate collectors, schedule production, own source data,
overwrite individual Clank history, auto-approve exceptions, or silently
reinterpret old standards. It is not a collector, scheduler, fleet
controller, deployment system, or a replacement for Diagnostic Clank or
Motherclank. See [docs/charter.md](docs/charter.md) section C.

As of Operator Ratification Decision 002 (2026-08-30), 12 standards under
[standards/ui/](standards/ui/README.md) are `RATIFIED`; 3 more are
`PROPOSED` (2 revised Pass 1 candidates, 1 revised Pass 2 candidate). See
[docs/gui-ratification-pass-1.md](docs/gui-ratification-pass-1.md),
[docs/gui-ratification-pass-2.md](docs/gui-ratification-pass-2.md),
[decisions/0003-operator-ratification-decision-001.md](decisions/0003-operator-ratification-decision-001.md),
and
[decisions/0004-operator-ratification-decision-002.md](decisions/0004-operator-ratification-decision-002.md)
for evidence and both ratification decisions made so far. Ratification of
a standard does not by itself authorize remediating any existing Clank
against it — that is separate, not-yet-commissioned work.

**Implementing or auditing a Clank UI?** Don't start from the raw
`standards/ui/*.json` files — read
[docs/ui/constitution.md](docs/ui/constitution.md) (the compact,
agent-facing summary of every RATIFIED UI rule, with inline citations) and
follow [docs/ui/agent-implementation-workflow.md](docs/ui/agent-implementation-workflow.md).

## How is a standard created?

1. Someone (operator or agent) proposes it as a JSON file conforming to
   [schemas/standard.schema.json](schemas/standard.schema.json), status
   `PROPOSED`, with at least one evidence reference.
2. It's reviewed — status moves to `REVIEWED` with a recorded review
   artefact.
3. The operator explicitly ratifies it — status moves to `RATIFIED`. An
   agent cannot perform this step on its own authority.

Full detail: [docs/standards-lifecycle.md](docs/standards-lifecycle.md) and
[docs/governance.md](docs/governance.md).

## How is a standard ratified?

Only by explicit operator sign-off, never by an agent self-ratifying. See
[decisions/0002-no-agent-self-ratification.md](decisions/0002-no-agent-self-ratification.md).

## How are exceptions handled?

A Clank can hold a recorded, auditable exception to a ratified standard.
Agents may propose an exception; only a human operator may approve one.
See [exceptions/README.md](exceptions/README.md).

## Where are standards located?

`standards/<domain>/<STD-ID>.json`, one file per standard. Which standards
apply to which Clank is determined by [profiles/](profiles/README.md), not
hardcoded per-Clank.

## Lifecycle at a glance

```
incident / requirement
  -> proposal
  -> review
  -> ratification
  -> profile adoption
  -> conformance
  -> later supersession if needed
```

## Repository layout

```
docs/         charter, governance, terminology, lifecycle, ratification passes, docs/ui/ (agent constitution + workflow)
standards/    one subdirectory per domain; standards/ui/ also holds the generated ratified-index.json / agent-checklist.json
schemas/      JSON Schema for standard / profile / exception / evidence-reference
profiles/     which standards apply to which class of Clank
exceptions/   recorded deviations from ratified standards
audits/       conformance-check records
decisions/    architecture/governance decisions about this repo itself
evidence/     evidence-reference pointers (not duplicated history)
tools/        shared Python used by scripts/ and tests/ (e.g. tools/ui_agent_layer.py)
scripts/      one-off/regeneration scripts (e.g. scripts/generate_ui_agent_layer.py)
tests/        repository-contract tests (schema/fixture validation, generated-file drift checks)
```

## Tests

```bash
python -m pytest
```

Validates fixtures against the same constraints as the JSON Schema files
in `schemas/` (see [tests/validators.py](tests/validators.py) for why a
lightweight hand-written validator is used instead of the `jsonschema`
package).
