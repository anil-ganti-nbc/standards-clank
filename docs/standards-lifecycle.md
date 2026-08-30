# Standards Lifecycle

## From evidence to ratification

```
incident / requirement
  -> proposal        (PROPOSED, status field set, evidence[] populated)
  -> review           (REVIEWED, review artefact recorded)
  -> ratification      (RATIFIED, operator sign-off recorded)
  -> profile adoption   (a profile's `standards` list references the id)
  -> conformance         (individual Clanks are audited against it)
  -> supersession (later, if needed: SUPERSEDED or RETIRED)
```

A standard should not be proposed from speculation alone. Every proposal
should be able to point at an [evidence](../evidence/README.md) reference —
a Diagnostic Clank incident, an explicit operator requirement, a
cross-Clank pattern, an architectural invariant, a regression, or an
experimental finding. See `origin` in
[../schemas/standard.schema.json](../schemas/standard.schema.json).

## Editorial correction vs. normative change

**Editorial correction** — the requirement's meaning is unchanged. Examples:
fixing a typo, clarifying ambiguous wording without changing what passes or
fails conformance, correcting a broken link, fixing an example that
illustrates the rule incorrectly. May be applied in place to a `RATIFIED`
standard without a version bump, but should still be noted in
[../CHANGELOG.md](../CHANGELOG.md).

**Normative change** — anything that changes what a Clank must do to
conform: a different `requirement`, a different `level` (MUST/SHOULD/MAY), a
narrower or broader `applies_to`, a changed `acceptance` contract. This must
either:

1. bump `version` on the same `id` and record the rationale in `notes`, or
2. introduce a new standard whose `supersedes` field names the old `id`,
   moving the old standard to `SUPERSEDED`.

A ratified standard's normative meaning is never silently rewritten in
place. If you are unsure whether a change is editorial or normative, treat
it as normative — the cost of an extra version is low; the cost of drifting
requirements under a stable ID is not.

## Versioning

`version` is a simple integer, starting at 1, incremented on every normative
change. Editorial corrections do not increment it.
