---
name: workflow-patterns
description: >
  Use when planning how to structure a feature or decompose work: decide
  whether to plan at all, explore read-only first, choose a decomposition
  shape, avoid over-abstraction, and design skills as packages.
metadata:
  opencode/slash: "true"
---

# Workflow patterns and planning

## Research, plan, implement, commit

Code written before the question is understood answers a question
nobody asked. Separate research from execution:

1. **Research** - in a read-only planning mode, the agent reads files
   and answers questions without changing anything.
2. **Plan** - a detailed implementation plan against what the
   research found.
3. **Implement** - execute against the plan, verifying as it goes.
4. **Commit** - only when explicitly authorized. Default is no commit;
   the operator reviews and commits, or grants explicit permission to
   commit and open a pull request.

**When the diff fits in a sentence, the plan is the diff.** Write a
plan when the approach is contested, the change crosses many files, or
the terrain is new; skip it for the typo. And a deliberately vague
prompt is sometimes right: you are sampling how the agent frames the
problem before you pin it down.

## Decomposition shapes

- **Chaining**: fixed sequential steps, each processing the previous
  output, with a programmatic **gate** between them catching drift
  early. Use when the task decomposes cleanly into known subtasks.
- **Routing**: classify the input first, then dispatch to a specialized
  handler. Use when distinct input classes want different treatment.
- **Parallelization**: run independent subtasks simultaneously
  (**sectioning**) or run the same task several times and aggregate
  (**voting**). Use for speed on independent pieces, or for confidence
  where diverse outputs and a vote threshold beat one attempt -
  reviewing code for vulnerabilities is the classic voter.
- **Orchestrator-workers**: a central agent dynamically decomposes the
  task, delegates to workers, and synthesizes results. Use when the
  subtasks are unpredictable and the coordination cost is justified by
  the complexity or duration.
- **Evaluator-optimizer**: one agent generates, another critiques, in a
  loop. Use when the evaluation criteria are clear and the work
  demonstrably improves under articulated feedback.

Add complexity only when it demonstrably improves outcomes: measure
before and after, keep the simplest thing that measures well.

## Design before you fan out

**Models invent structure.** Given a free hand, an agent drafts
scaffolding nobody asked for, and then you own a shape no one chose.
Approve the shape before implementation; refactor toward a form you
picked deliberately.

**Concurrency multiplies whatever it is given.** K parallel sessions
commit to a wrong shape K times. Lock the core shape first, then
parallelise the independent, well-specified parts. Code structure as a
context strategy is owned by context-budget.

## TDD as a self-assessment loop

Plant the failing test before the code: it fixes the goalpost while
there is nothing yet to move it. Once green, the test doubles as the
tightest brief a later session can read - behavior, minus the prose.

## Prompting on the interaction side

- **Be specific**: name the file and the case, say which source holds
  the answer, and define "fixed" as a reproducing test plus the fix.
- **Interrogate, then specify**: before a large feature, let the agent
  question you until the corners are covered, write a standalone spec,
  then hand it to a **fresh session** to build.
- **Delegate execution, never decisions.** At a decision point, ask for
  a trade-off table with failure modes and decide yourself; "whatever
  is best" transfers the decision and the risk at exactly the moment it
  matters most.

## Skill design

A skill is a package, not a prompt: entry map, references, workflows,
non-goals, and state checks, with detail deferred to `references/` pages.
For the full checklist and the four evaluation levels, read
references/skill-design.md.

## Spec-driven development and handoffs

For the spec-driven loop, its enforcement layers, scope authorization,
and the handoff contracts between skills, read
references/spec-driven.md and references/handoffs.md.

## Provenance

Sources and adaptations: references/provenance.md.

## Non-goals

This skill does not replace project-specific design review, choose a
specification tool, or authorize scope beyond the product requirements.
If a request falls outside these bounds, refuse or hand off.