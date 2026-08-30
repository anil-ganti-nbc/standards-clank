# Governance

## Lifecycle

A standard moves through exactly these statuses, in order, with no skipped
steps:

```
PROPOSED -> REVIEWED -> RATIFIED -> SUPERSEDED / RETIRED
```

A standard may not move from `PROPOSED` directly to `RATIFIED`. A `REVIEWED`
status requires an explicit review artefact (a PR review, or a note in
[decisions/](../decisions/README.md)) that records who reviewed it and what
concerns were raised or resolved.

`SUPERSEDED` means a newer standard replaces this one; the new standard's
`supersedes` field must reference this one's `id`. `RETIRED` means the
standard no longer applies and nothing replaces it.

## Roles

- **Proposer** — drafts a standard or a change to one. May be a human
  operator or an AI agent.
- **Reviewer** — evaluates a proposal for correctness, evidence sufficiency,
  and conflicts with existing standards. May be a human operator or an AI
  agent, but see the restriction below.
- **Operator/ratifier** — the human accountable for the Clank fleet. Only
  the operator (or someone the operator explicitly authorises) may ratify.

## The ratification restriction

An AI agent may propose and analyse. **An AI agent may not self-ratify a
normative standard.** Ratification must be an explicit, recorded act by the
operator — a merged PR approval, or a note in a decision record naming the
operator as ratifier is sufficient; agent-authored commit messages or
self-approval are not.

This mirrors the exception-approval restriction in
[../exceptions/README.md](../exceptions/README.md): agents propose,
operators decide.

## Editorial vs. normative change

See [standards-lifecycle.md](standards-lifecycle.md) for the full
distinction. In short: an editorial correction (typo, clarified wording,
fixed example) may update a `RATIFIED` standard in place. Any change to what
the standard actually requires must produce a new version or a superseding
standard — never a silent in-place rewrite of meaning.

## Record-keeping

Every ratification and every normative change is recorded in
[../CHANGELOG.md](../CHANGELOG.md). Major governance and architecture
decisions about Standards Clank itself (not individual standards) go in
[../decisions/](../decisions/README.md).
