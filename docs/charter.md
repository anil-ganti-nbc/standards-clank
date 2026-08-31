# Charter

## A. Purpose

Standards Clank is the normative standards layer for Clank design and
operation. It exists to turn operational experience — incidents, operator
requirements, cross-Clank best practices — into explicit, versioned,
machine-readable requirements that individual Clanks can be built and audited
against.

It is downstream of [Diagnostic Clank](https://github.com/anil-ganti-nbc/diagnostic-clank),
which records what failed and what was learned. Standards Clank turns
sufficiently supported lessons into normative design rules. Individual Clanks
implement the standards appropriate to their profile.

## B. Scope

Standards Clank may define standards for:

- GUI/UI
- collector behaviour
- specialist source scoping
- source authority
- provenance/evidence
- classification
- event semantics
- novelty
- health
- delivery/Discord
- soak
- deployment/migration contracts
- operator workflows
- feedback/QC
- security/secrets
- auditability

This is a list of what Standards Clank *may* standardise, not a work
list of domains it is obligated to fill. See section F.

## C. Non-goals

Standards Clank does not:

- operate collectors
- schedule production
- own source data
- overwrite individual Clank history
- auto-approve exceptions
- silently reinterpret old standards

It is not a collector, a scheduler, a fleet controller, a deployment system,
a replacement for Diagnostic Clank, a replacement for Motherclank, or an
automatic code rewriter. It has no authority to silently change production
Clanks.

## D. Philosophy

Standardise:

- contracts
- invariants
- semantics
- observable behaviour

Do **not** unnecessarily standardise:

- programming language
- framework
- database engine
- hosting provider
- internal implementation details

A standard should describe what a Clank must guarantee, not how it must be
built.

## E. Principle

Standards should be evidence-driven and should improve because of real
operational learning, not speculation. See
[standards-lifecycle.md](standards-lifecycle.md) for how a standard moves
from evidence to ratification, and [governance.md](governance.md) for who
may do what at each step.

## F. Completion

Standards Clank is complete when all materially evidenced fleet-wide
normative concerns have been either standardized, explicitly rehomed,
held with reopening triggers, or rejected. Completion does not require
every chartered domain to contain standards, and empty domain scaffolding
(section B's list, or an empty `standards/<domain>/` directory) is not
itself evidence of a standards gap.

New domains are created from evidence, not from taxonomy. A domain should
not be populated merely because it exists in the original charter.

This is the same evidence-driven discipline as section E, applied to the
project as a whole rather than to one standard: a domain that has never
been evidence-mined is not "missing" standards any more than a Clank that
has never logged an incident is "missing" a bug report.
