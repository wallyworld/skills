# Probes for independent review

**Read when**: Review mode, code-review mode, or self-review process.

## The five defect classes

For each finding, demand evidence: a `file:line` or commit citation, or
the finding is a belief and must be labeled unverified.

1. **Partial-read**: the plan describes a change to a function (its
   aggregation math, its skip branches, its parse keys, its default
   values) from grep- or diff-level knowledge instead of a full read in
   the target tree. **Probe:** for every function the deltas touch, confirm
   the plan's description matches a full read of that function in the
   CURRENT target tree.
2. **Name-match assertion**: the plan claims a function "already does X"
   or "already covers Y" based on its name or the author's own design,
   without reading the body. **Probe:** verify the cited function's body
   actually implements the claimed semantics, including its skip/early-
   return branches.
3. **Intent vs specification**: deltas describe behavior ("wire X, fail
   closed") without naming call sites, function signatures, the tests
   that mock the seams they break, byte-identical constraints, or
   red-green mechanics. **Probe:** an independent agent who follows the plan
   verbatim should never need to invent a signature or choose a call
   site. Intent-level text is acceptable only for the author's own
   same-turn execution.
4. **Mixed mental model**: one clause blends facts from two different
   sources (two implementations, two branches, two time states), e.g.
   documenting values from one tree while describing changes to another.
   **Probe:** for every comparison in the plan, the values must be traceable
   to exactly one named source each; re-read each sentence twice, once
   per source.
5. **Stale state**: repo-state claims (index staged or not, branches,
   file contents, commit history) come from memory of an earlier session
   rather than the current tree. **Probe:** re-run `git status` (index,
   worktree, and untracked separately), `git log --oneline -5`, and
   re-read the cited files at review time. State that this was done.

## Code review probes (applied to implemented code deltas)

6. **Exception tracing**: every new error or failure path is traced to
   the boundary that handles it, with a test through that boundary.
7. **Wire-format evidence**: a parser change on a fail-closed path
   carries evidence of the actual wire format (a fixture test with a
   realistic response). An offline-unverifiable format is a blocker on
   live validation, not runtime readiness.
8. **Lenient-branch audit**: every optional, skip, or fallback branch is
   audited against fail-closed discipline: an error must never read as an
   absence, a default, or a pass. This includes implicit defaults in
   dereferences of external data (`x or {}`, `.get(k, {})`): a default is
   absence handling, not shape handling - a wrong-typed value passes
   through it. Enumerate every dereference (`.get`, `.items`, index,
   `sorted`) applied to data from an external response, transitively from
   the parse boundary, not just each reader function's entry point.
9. **Malformed input testing**: every new validator's test matrix includes
   schema-valid-but-malformed inputs, not only the happy and rejected
   shapes.
10. **Positive-path validation**: every fail-closed behavior requires a
    positive-path test (the success it must produce), not only
    failure-path tests.
11. **Claim audit**: every declarative statement in the changed text - a
    docstring sentence, a comment, a marker or suffix's stated meaning, a
    type assertion, an error message, a documentation sentence, a
    task-ordering claim - is read as a claim and checked against the
    implementation. The author wrote code, tests, and prose from one
    mental model, so prose is the least-tested surface; a claim the code
    does not honor is a finding.

## Self-review probes (applied to own diff)

Self-review applies probes 6-11 plus:

12. **Data threading**: computed values reach their consuming calls, not raw or stale copies
13. **Composed reads**: read the full function as it exists after the change, not just the diff hunks

When the artifact under review is a skill, apply the skill-review probes
in skill-review.md.