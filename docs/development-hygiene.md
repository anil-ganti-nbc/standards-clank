# Development hygiene

Repository development notes for contributors (human or agent) working in
this repo. Not a standard: nothing here is `MUST`/`SHOULD` for a Clank,
it is not part of any frozen baseline, and it does not go through the
standards lifecycle in [docs/standards-lifecycle.md](standards-lifecycle.md).

## Always preserve pytest's exit status when running the suite

Run the test suite directly:

```bash
python -m pytest
```

or, if you need to capture output, preserve the exit code explicitly:

```bash
python -m pytest -q; echo "EXIT_CODE=$?"
```

**Do not** pipe `pytest`'s output through another command (`pytest | tail`,
`pytest | grep ...`) unless your shell is explicitly configured to
propagate the failing stage's exit code (e.g. `set -o pipefail` in bash,
and only if you've verified it) or you capture and check the exit code
some other way. In an unconfigured pipeline, `$?` reflects the exit
status of the *last* command in the pipe (`tail`, `grep`, etc.), not
`pytest` — so a failing suite whose output was merely filtered can look
green.

This is not a hypothetical concern. During this repository's Data/Ontology
holds-disposition pass, a piped verification command masked a real pytest
failure: commit `cd4384b` (the holds-disposition content change) landed on
`master` with a red suite, because the byte-identity pins in
`tests/test_pass2_draft_review.py` and `tests/test_pass3_data_ratification_survey.py`
had gone stale against the commit's own additive change to
`docs/data-ontology/pass0/candidates/holds-and-rejects.md`, and the pipe
hid the failure. Two follow-up commits (`a3eacfe`, `ae586c4`) were needed
to update the stale pins and restore a green `master`. No incorrect
standard or governance content resulted — the near-miss was entirely a
test-hygiene gap, not a normative one — but it is exactly the class of
mistake this note exists to prevent from recurring.

If you're about to commit and the verification command you ran involved a
pipe, re-run it unpiped (or check `$?` explicitly) before trusting a
"passed" reading.
