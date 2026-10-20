# Harness controls for skill invocation

**Read when**: deciding whether a skill loads automatically or only on
command.

- OpenCode 1.x: set `metadata["opencode/autoinvoke"]: "false"` to keep
  the skill out of model-facing automatic selection. Set
  `metadata["opencode/slash"]: "true"` to expose it as a `/name`
  command.
- OpenCode 2: `opencode/slash` is not interpreted, so a skill exposes
  no `/name` command. Load it by mentioning `@skill-id` in the prompt,
  or through the `skill` tool; the ID derives from the file path, so
  the directory name stays the handle. `opencode/autoinvoke: false`
  still hides a skill from the model's available list
  (`disable-model-invocation: true` is an alias; `opencode/autoinvoke`
  wins when both are set). `/name` commands are a separate mechanism:
  a `.opencode/commands/<name>.md` file whose body is the prompt
  template. The name/directory match and the 1-1024 character
  description limit are no longer enforced, but the discovery paths
  are unchanged.
- Claude Code: use the `disable-model-invocation` field to block
  automatic loading.

These are harness-specific features; use them when a skill is expensive
or should only run on demand. All six skills in this repository set
`opencode/slash: "true"` and keep automatic selection enabled.