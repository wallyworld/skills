---
name: verification
description: >
  Use when writing or reviewing tests, verifying a change before
  reporting done, or testing a skill: require executable evidence,
  red-before-green, fixture pairs, state checks, and a "not verified"
  column.
metadata:
  opencode/slash: "true"
---

# Verification and evidence

These rules prevent a defect shipping while validation reports are
green.

## The check the agent can run

- Give the agent a check it can execute: a suite, a build exit code, a
  linter, a diff against a fixture. Absent one, the only feedback the
  agent gets is its own say-so, and every mistake waits for the operator
  to catch it.
- Scale enforcement to autonomy. A check requested in the prompt; a goal
  the harness re-asserts each turn; a hook that refuses to end the turn
  until the gate is green; or an outside agent paid to find the flaw.
- Report evidence, not assertions: the test output, the command and
  its exit code, the diff. A recorded run can be audited from the
  transcript, which turns "all green" from a claim into an audit
  trail.

## Tests that test something

- **Internal tests are not interface tests.** A unit or API test can
  pass while the delivered entry point is broken. Every user-facing
  requirement needs an executable acceptance test through the real entry
  point on the real runtime.
- **Placeholders pass green.** An implementation that returns an empty
  list or a "demo only" message can satisfy a test that only asserts the
  endpoint responds. Assert the real transition or outcome, and fail on
  placeholder markers.
- **Red before green.** Run every new test against the pre-fix code and
  watch it fail; a test that was never red has an untested ability to
  pass vacuously. When a test runs red, name the guard that actually
  tripped - a red that fails a different assertion proves nothing about
  the one under test.
- **Fixture pairs.** Every new checker ships known-good and known-bad
  fixtures. A checker that can pass by matching nothing is a defect
  wearing a feature's clothes.
- **Positive paths for fail-closed behaviors.** A probe tested only on
  its failure modes can never succeed and still stay green. Every
  fail-closed behavior carries a fixture of a realistic successful
  input; parsers of external wire formats ship a fixture of a real
  response, or state a block on live validation instead of assuming a
  format.

Further shapes - malformed-input cases, material-cell coverage, fixtures
that are claims about their own bytes, closed-relation invariants,
partial-failure tests, canaries - are in references/test-shapes.md.

## State checks

An accepted command is an intention, not an outcome. After one lands,
confirm three things: the change you asked for exists, the work it
spawned has drained to zero, and the system has settled into a state
you would sign off on. Success is a reported ready state, not a
returned prompt.

## Environments and commands

- **Reproduce, never model.** A stripped-down local simulation carries
  installed extensions and warm caches a bare checkout lacks, so it
  passes when it shouldn't. The closest local proxy is a pristine export
  of the tracked files; CI remains the authority for definitive
  verification.
- **The documented command, not a stand-in.** A stand-in with different
  defaults validates the stand-in. If substitution is unavoidable, diff
  the defaults first and state the difference.
- **Full, unfiltered package runs.** A focused pre-pass is fine while
  iterating; the completion report cites the full package - a filtered
  green run is compatible with a broken package.
- **Re-verify owned state after mutating tools run.** After an
  installer, upgrader, or generator mutates state, diff the files it
  owns, not just the intended effects.
- **Survey mechanically.** When a change touches a counter, check every
  writer and reader; when it touches a shared pattern, enumerate every
  call site with the same defect shape.
- **Review the whole working tree.** Check staged changes, unstaged
  changes, and untracked files. A report that omits any of these can
  miss uncommitted or orphaned work.

## Proportional verification exceptions

Allow explicit exceptions when exhaustive testing is unavailable. The
completion report must include: what wasn't run and why (resource
constraints, environment requirements, time costs); what evidence stood
in instead (partial verification, design review, manual inspection); and
impact (risk level, confidence, remaining unknowns).

## Reporting

- Say what you did NOT verify, as a column and not a footnote: a list
  of what passed is evidence about the columns that were checked; the
  regressions live in the unchecked ones. Omission of a caveat is a lie
  by default.
- Verify every claim against the code at writing time: quote the error
  string, the version, the function name. Distinguish implemented
  behavior from intended behavior.
- Tests are context for the next session: a future agent that reads the
  test and its fixture inherits a precise definition of done.

## Testing skills

When the artifact under test is a skill, apply
references/skill-testing.md: static checks, routing tests, live tests,
and reconstruction tests, in rising cost, with "I can't determine this"
as a valid outcome.

## Provenance

Sources and adaptations: references/provenance.md.

## Non-goals

This skill does not prove product requirements, replace independent
review, guarantee that a local run matches CI, or turn a model judgement
into a deterministic gate. If a request falls outside these bounds,
refuse or hand off.