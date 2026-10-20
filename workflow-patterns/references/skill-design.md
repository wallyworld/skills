# Skill design

**Read when**: authoring or restructuring a skill.

A skill is a package: a route in, a set of procedures, a boundary
against scope, and the evidence that it works.

- **Entry document.** One short file that orients: what the skill
  covers, which workflow answers which request, and which reference
  holds which facts. Everything else lives behind it.
- **References.** Checklists, probe lists, templates, and worked
  examples, loaded only when the body says so. A reviewer should be
  able to verify the skill from the references without its author in
  the room.
- **Routing surface.** The description is the contract with the
  harness. Test three requests against it: the essential command, an
  out-of-scope job, and a dangerous one. Only the first should be
  accepted.
- **Templates.** Link them, and say which workflow uses which.
- **External docs.** Product documentation is final for product facts;
  the repository's docs and tests are final for local behavior.
- **Non-goals.** What the skill will not do, and when it declines or
  hands off. A skill that cannot say no is not scoped; it is
  improvising.
- **State checks.** For any state-changing command the skill
  recommends: the change, the work it spawns, the settled state.
- **"I can't determine this."** An honest gap beats an invented
  answer; say which claims the transcript cannot support.

## Budgets

The description rides along every turn; the body loads on demand. Keep
the description short and trigger-first, the body under a fixed word
budget, and no section so large its detail cannot move to a
reference.

## Evaluating a skill

Evidence in rising cost - static checks, routing tests, live runs, and
reconstruction - with the full doctrine in the verification skill's
`skill-testing` reference.