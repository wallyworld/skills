# Provenance for tools-and-security

Adapted sources (ideas re-expressed here in new wording):

- Anthropic, *Claude Code best practices*
  (https://code.claude.com/docs/en/best-practices): explicit file
  references, CLI-first integration, permission allowlists, sandboxing,
  classifier review, and worktrees for parallel sessions.
- Anthropic, *Writing effective tools for agents - with agents* (Sep
  2025)
  (https://www.anthropic.com/engineering/writing-tools-for-agents):
  tool descriptions as documentation, examples and edge cases, and
  evaluating tools with many inputs.
- Simon Willison, *The lethal trifecta for AI agents* (Jun 2025)
  (https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/): the
  private data + untrusted content + external communication threat
  model behind the credential rules.
- OpenCode skill docs (https://opencode.ai/docs/skills/) and Claude Code
  docs: the slash/autoinvoke and disable-model-invocation metadata
  described in harness-controls.md.

Original to this repository: the poka-yoke parameter guidance, the
credential broker as its own audited surface (confused-deputy framing),
polling by observation, anchoring project-scoped commands to a working
directory, and sandboxing the whole loop rather than single calls.