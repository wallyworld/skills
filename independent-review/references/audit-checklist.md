# Audit checklist

**Read when**: Using audit mode to produce severity-graded findings against a plan.

Used in audit mode to produce severity-graded findings against a plan.

## Checklist

1. `git status --short` run within this session, citing index vs
   worktree vs untracked explicitly? If the plan contains mechanics that
   depend on repo state (stash, branch, checkout), the state must match.
2. Every factual claim about code carries `file:line` or a commit, or is
   marked unverified?
3. Every delta names: call sites, signatures, tests that mock the seams,
   byte-identical constraints, and red-green mechanics?
4. Every new error or failure path is traced to the boundary that handles
   it, with a test through that boundary. Every fail-closed behavior names
   its positive-path test; every parser delta over an external wire format
   names its fixture evidence (and blocks on live validation when the
   format is offline-unverifiable); every new CLI wiring names a
   command-level test on its real (discovery/default) path, not only
   the flag path; every new validator names its schema-valid-but-malformed
   input cases?
5. No sentence blends facts from two sources (one named source per
   value)?
6. Full reads, not diffs, for every function the plan changes? (Diffs
   answer "what differs"; the plan must answer "what the function does".)
7. Anything the plan says the author did NOT verify is stated as such?
8. If the plan will be executed outside this session: it is standalone
    (self-contained, no session context required)?
9. If the plan is a skill: every check in skill-review.md (in this
    `references/` directory) holds. That file is the single source for
    skill-review probes - routing accuracy, referenced files, non-goals,
    state checks; read them there rather than here.
10. Every claimed requirement traces to a product requirement, and no
    capability was authorized by clarify rather than by the product source?