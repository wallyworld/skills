# Provenance

These skills re-express published guidance as loadable packages: lean
entry documents, deferred references, stated non-goals, and budgets
enforced by tests. This file records where each skill's material was
adapted from, what is related work, and what is original to this
repository. Each skill also carries a shorter mapping in its own
`references/provenance.md`.

## Sources

| Source | Link | Used by |
|---|---|---|
| Anthropic, *Claude Code best practices* (engineering post Apr 18, 2025; living docs) | https://code.claude.com/docs/en/best-practices | context-budget, verification, workflow-patterns, tools-and-security, independent-review |
| josecabralf, *Failing AI engineering so you don't have to* (Aug 20, 2026; Canonical Discourse, login required) | https://discourse.canonical.com/t/failing-ai-engineering-so-you-dont-have-to/7920 | context-budget, workflow-patterns, verification |
| akonev, *A skill is more than just a prompt* (Oct 10, 2026; Canonical Discourse, login required) | https://discourse.canonical.com/t/a-skill-is-more-than-just-a-prompt/8251 | verification, workflow-patterns, independent-review, readme-authoring |
| Anthropic, *Building effective agents* (Dec 19, 2024) | https://www.anthropic.com/engineering/building-effective-agents | workflow-patterns |
| Anthropic, *Effective context engineering for AI agents* (Sep 29, 2025) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | context-budget |
| Anthropic, *Writing effective tools for agents - with agents* (Sep 11, 2025) | https://www.anthropic.com/engineering/writing-tools-for-agents | tools-and-security |
| Anthropic, *Equipping agents for the real world with Agent Skills* (Oct 16, 2025) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | workflow-patterns, context-budget |
| Simon Willison, *The lethal trifecta for AI agents* (Jun 16, 2025) | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | tools-and-security |
| OpenCode skill docs | https://opencode.ai/docs/skills/ | tools-and-security, README |
| obra/superpowers (MIT, Oct 2025) | https://github.com/obra/superpowers | related work only; no text taken |
| mattpocock/skills (MIT) | https://github.com/mattpocock/skills | upstream of the handoff pattern quoted by [1] |

The two Canonical Discourse posts are readable behind a Canonical login.

## What is original here

- The rule-channel hierarchy (context, gates, after the fact) and the
  mantra of moving each rule to the earliest channel where it can fire;
  this generalizes the Claude Code docs' line that instructions are
  advisory while hooks are deterministic.
- The ratchet with its two counterweights: triage before converting a
  finding into machinery, and retiring rules that stop firing; this
  extends the Claude Code docs' prune-or-convert fix for bloated
  instruction files.
- Commissioning reviews against the goal instead of a claim checklist.
- The probe lists and the self-review report contract: a completion
  report is malformed without a "probes fired" section and an
  independent-reviewer line.
- The verification failure taxonomy: checkers that prove less than they
  claim, half-invariants, fail-closed code that can never succeed,
  happy-path validators, canary sweeps, material cells, the "not
  verified" column, and the exception-report shape.
- Spec-driven development's enforcement layers and the scope-
  authorization gap (content coverage vs authorized scope).
- The tools-and-security synthesis: poka-yoke parameters, the
  credential broker as its own audited surface, polling by
  observation, and sandboxing the whole loop.
- The packaging: six skills, budgets enforced by tests, and the
  division of doctrine to one canonical owner per rule.

## Licence

The original content of this repository is released under the MIT
licence (see LICENSE). Third-party material referenced above remains
the property of its authors; where adapted, it is re-expressed here in
new wording and cited per skill in `references/provenance.md`.