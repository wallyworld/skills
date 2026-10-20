---
name: independent-review
description: >
  Use to review a plan, diff, or skill, or at self-handoff before
  reporting done: commission a fresh-context reviewer against the goal,
  demand evidence per finding, and never let the author grade alone.
metadata:
  opencode/slash: "true"
---

# Independent review

The person who best understands the intended behavior is the person
least likely to test its absence. Every layer an implementer can reach -
code, tests, gates, completion report - carries the mental model that
produced the work, and a defect born of that model passes every gate the
model built.

## Modes

Pass the mode as the first argument:

- `audit <plan-file-or-text>` - apply the checklist in
  references/audit-checklist.md to the plan; return severity-graded
  findings. Default when no argument is given.
- `emit-prompt <plan-file>` - produce a standalone review prompt from
  references/emit-prompt-template.md for the user to run in an
  independent model; no context from this session may be required.
- `review <plan-or-skill>` - derive your own verification plan, then
  cross-check the claims; run the probe lists in
  references/probe-lists.md, output the disposition table and verdict.
  For a change affecting a delivery interface, also run the entry point
  or its acceptance test.
- `code-review <commit-range-or-diff>` - review implemented code deltas
  against the code-review probes in references/probe-lists.md; findings
  cite file:line.

## Self-review as a report contract

Before declaring done, run an adversarial pass over your own diff using
probes 6-13 from references/probe-lists.md: trace every new error path to
the boundary that handles it, thread every computed value to its
consuming call, read each touched function in full as it now exists, and
audit every declarative claim in the diff against the code. The report is
malformed without a "probes fired" section or an explicit
`Review pass skipped: <reason>` line, and malformed without the
independent line: which fresh-context reviewer ran and what it found or
fixed, or a statement that none was available. Self-review is necessary,
insufficient - it inherits the author's blind spots.

At self-handoff, escalate: delegate the diff to a fresh-context reviewer
(subagent or new session) whose prompt is the goal, the applicable
checklist, and the diff - never your reasoning or conclusions - and
require it to derive its own falsification probes. Treat its findings as
findings, fix them, and re-run until a clean pass; a pass with no probes
fired is not a pass.

## Commission against the goal, never the plan

Hand the reviewer the goal, the tree, and the classes of past failure,
and instruct them to derive their own verification plan. A reviewer that
receives a claim checklist verifies the claims and misses what was not
on the list - they check the map, not the terrain.

Two cautions when commissioning:

- Ask a reviewer to hunt problems and it will deliver problems, sound
  work or not; every chased finding buys abstraction for a case that
  cannot occur. Restrict the brief to gaps that change correctness,
  requirements, security, or operability.
- Spend fresh-eyes audits on risk boundaries, not suspicion - before a
  major upgrade merges, after a cross-cutting change, at a release. The
  audit that never ran is always the one after the riskiest operation.

## Parallel fresh-context patterns

- **Split author from critic**: one session builds; a second, which
  never watched the first reason, reads the diff cold for edge cases
  and pattern drift, and the writer answers. Tests divide the same
  way: written in one session, satisfied in another.
- **Subagent reviewers** run in their own context and return findings,
  keeping the review's bulk reading out of the main window.

## The ratchet

A defect that escapes every layer is a routing instruction: ask *where
should this have been caught*, and put the rule there - a test first
(with fixtures, red before the fix), then a hook at the moment of
authoring, then a workflow gate with an approval trail, and prose last.
Pull-request review is the backstop, not the net: by the time a defect
reaches a PR comment it has escaped every earlier layer.

Two counterweights: triage before converting - a finding earns machinery
only when it could recur silently, when neither a test nor a reviewer
would catch the next one cheaply; and retire rules that stop firing,
deliberately, in a commit that says why.

## Reviewing a skill

When the artifact under review is a skill, apply
references/skill-review.md: description routing accuracy, references
existence, non-goals and refusal, state checks, progressive disclosure,
and "I can't determine this" as a legitimate outcome.

## After the review returns

If the verdict is APPROVE WITH CHANGES or REJECT: incorporate every
finding into the plan in the same pass, re-audit, and state which
findings were closed before the plan is re-submitted or executed. Never
soften a finding in the summary; record CLOSED / PARTIALLY CLOSED /
REOPENED per finding with evidence.

The handoff addendum appended to plans given to implementing agents is in
references/handoff-addendum.md.

## Provenance

Sources and adaptations: references/provenance.md.

## Non-goals

This skill does not implement fixes, replace CI, or verify claims absent
from the tree or transcript. It cannot make an unverified belief true. If
a request falls outside these bounds, refuse or hand off.