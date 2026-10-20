# Provenance for context-budget

Adapted sources (ideas re-expressed here in new wording):

- Anthropic, *Claude Code best practices*
  (https://code.claude.com/docs/en/best-practices): the context window
  as the governing constraint, the two-corrections ceiling, one session
  per phase, narrow scoping, and research subagents.
- josecabralf, *Failing AI engineering so you don't have to* (Aug 2026)
  (https://discourse.canonical.com/t/failing-ai-engineering-so-you-dont-have-to/7920):
  quadratic input growth, skill-set loading cost, handoff documents,
  ask-then-rewind, longer first prompts, and structure as context
  economy. The handoff pattern he quotes descends from
  mattpocock/skills.
- Anthropic, *Effective context engineering for AI agents* (Sep 2025)
  (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):
  context as a finite resource, compaction losses, sub-agents.

Original to this repository: the skill-loading rule, the durable-handoff
contract, the session-continuity convention (project-scoped, optional,
kept out of the portable body), and the reasoning-budget guidance.