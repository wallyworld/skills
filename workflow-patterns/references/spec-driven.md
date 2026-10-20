# Spec-driven development

**Read when**: a feature's intent is worth writing down, or you are
hardening a spec-driven loop.

Structure the work as a loop around written intent; each stage produces
an artifact the next stage reads:

1. **Specify** - user stories with acceptance scenarios, functional
   requirements, edge cases.
2. **Plan** - derive the technical plan from the spec.
3. **Tasks** - ordered, independently testable units.
4. **Implement** - execute the tasks, running tests as it goes.
5. **Reconcile** - re-read the artifacts, diff the code against them,
   append what is missing rather than declare done.

Around the loop sit a few **written project principles** that each plan
and task list is checked against.

## The catch: prompts are not checks

In a prompt-driven spec workflow, each stage is a prompt, not a check -
the built-in checks are model judgements, not deterministic gates; they
can be skipped or share the same blind spot as the author, and the
principles are prose the agent is asked to honor. What closes the gap is
enforcement in four layers:

1. **Deterministic checkers over the artifacts** - e.g. verify every
   requirement ID in the spec appears in the plan and in at least one
   task, and run the check over every committed spec in CI.
2. **Authoring-time injection** - put the checklist in context at the
   moment the agent writes the artifact the rules govern (a hook, a
   template, or a prompt step, depending on your harness).
3. **Workflow gates** - the same checks composed into CI, with an
   approval trail naming what was attested.
4. **Mirrors in the test suite** - plain tests re-check everything
   above, so the repository fails loudly on drift even if the workflow
   tooling is uninstalled.

If the same rule exists in several forms (command, checklist, hook
prompt), derive the copies from one source and test that they match.
Duplication is distribution only when locked with a mechanical check; a
hand-edited copy is a build failure, not a drift.

## Scope authorization

Scope authorization is separate from content coverage. Every
functional requirement should trace to a product requirement. A
capability that is absent from the product source is a requirements
change, not an implementation detail. Clarify resolves ambiguity in
the spec; it does not authorize new scope. Review the plan for this.