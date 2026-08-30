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

**No standard in this repository is ratified yet.** The initial commit was
repository and governance groundwork only. GUI Ratification Pass 1
(2026-08-30) has since added 9 evidence-backed `PROPOSED` candidates under
[standards/ui/](standards/ui/README.md) — see
[docs/gui-ratification-pass-1.md](docs/gui-ratification-pass-1.md) for the
ratification table. They are proposals, not ratified rules, until the
operator moves them through review and ratification.

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
docs/         charter, governance, terminology, lifecycle
standards/    one subdirectory per domain, empty for now
schemas/      JSON Schema for standard / profile / exception / evidence-reference
profiles/     which standards apply to which class of Clank
exceptions/   recorded deviations from ratified standards
audits/       conformance-check records
decisions/    architecture/governance decisions about this repo itself
evidence/     evidence-reference pointers (not duplicated history)
tests/        repository-contract tests (schema/fixture validation)
```

## Tests

```bash
python -m pytest
```

Validates fixtures against the same constraints as the JSON Schema files
in `schemas/` (see [tests/validators.py](tests/validators.py) for why a
lightweight hand-written validator is used instead of the `jsonschema`
package).
