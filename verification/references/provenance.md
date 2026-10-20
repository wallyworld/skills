# Provenance for verification

Adapted sources (ideas re-expressed here in new wording):

- Anthropic, *Claude Code best practices*
  (https://code.claude.com/docs/en/best-practices): a runnable check as
  the core signal, the enforcement ladder (requested in the prompt, a
  per-turn goal, a stop hook, a second opinion), and evidence over
  assertion.
- akonev, *A skill is more than just a prompt* (Oct 2026)
  (https://discourse.canonical.com/t/a-skill-is-more-than-just-a-prompt/8251):
  the three-stage state check, and the four-level skill-testing
  doctrine (static, routing, live, reconstruction) elaborated in
  skill-testing.md.
- josecabralf, *Failing AI engineering so you don't have to* (Aug 2026)
  (https://discourse.canonical.com/t/failing-ai-engineering-so-you-dont-have-to/7920):
  tests as the most precise context a later session inherits.

Original to this repository: the failure taxonomy (placeholders,
fixture pairs, positive paths for fail-closed code, half-invariants),
environment reproduction, canary sweeps, the full-package rule, the
exception report, and the "not verified" column.