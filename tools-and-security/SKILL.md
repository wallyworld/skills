---
name: tools-and-security
description: >
  Use when wiring tools into an agent, designing agent-facing tools, or
  configuring permissions and credentials: isolate credentials outside
  the agent-readable environment, sandbox the loop, and prefer CLI-first
  integration.
metadata:
  opencode/slash: "true"
---

# Tool integration and security

## Feeding context efficiently

- **Hand over the artifact, not its address.** Where the harness
  supports `@file` references, use them; prose describing where code
  lives still costs the agent a read. Paste images when layout matters;
  pipe data in when only the answer matters.
- **Reach for a CLI first** when its output is short, stable, and
  self-describing via `--help`; a typed API or MCP tool wins where
  output is verbose or schemas matter. Neither wins everywhere.
- **Connector protocols** - open standards for wiring external tools
  (issue trackers, databases, design surfaces) - beat bespoke glue:
  one client implementation reaches a growing ecosystem.

## Tool design is prompt engineering

Write each tool as a brief for a capable stranger who cannot ask a
follow-up question:

- If you would hesitate over the parameters, so will the model; spell
  out usage, edge cases, and the boundary against neighboring tools.
- **Poka-yoke the parameters**: make the wrong call hard to express.
  Relative file paths break after the working directory moves;
  requiring absolute paths fixed it completely.
- Keep formats close to what naturally occurs in text; avoid bookkeeping
  overhead (line counts, escaping) the model must maintain while writing.
  Give the model room to think before it writes itself into a corner.
- **Test tools like prompts**: run many example inputs, watch the
  mistakes, iterate on the definition.

## Permissions and sandboxing

Dial friction per task. Three mechanisms cover most of it:

1. **Allowlists** green-light the boring tools (linter, suite runner)
   so routine work proceeds unprompted.
2. **Sandboxing** fences filesystem and network at the OS level; the
   agent roams freely inside the fence.
3. **Classifier modes**, where offered, put a second model between the
   agent and the action; it pauses the risky-looking ones - scope
   escalation, unknown infrastructure - and waves the rest through. A
   block is information, not an obstacle to route around.

Routine work: pre-approved and sandboxed. Anything that mutates
infrastructure: a human approves it.

## Credential isolation

Scope isolation to a threat model: repository credentials, deployment
credentials, and third-party service credentials; provider-native
authentication is separate.

No credential may appear in:

- `.git/config`
- Remote URLs
- Environment variables the agent can read
- Logs or command output

The dangerous shape is the lethal trifecta: one agent that holds
private secrets, will meet hostile text, and can reach the outside -
the three capabilities combined are an exfiltration pipeline. If
a credential sits in the agent-readable environment, a prompt injection
only has to persuade the agent to read its own environment aloud.
Narrow scoping alone is not a durable fix: it assumes what the agent
cannot do with a limited token, and that assumption erodes as models
improve.

- **Vault and proxy with least privilege.** Use a credential helper or
  broker outside the agent-readable sandbox. The proxy fetches from the
  vault and makes the call; the harness never sees the secret. Least
  privilege is necessary but not sufficient: delegate to a broker
  whenever possible, and authorize and audit the broker as a distinct
  security surface; the broker can become a confused deputy.

## Session-level mechanics

- **Poll by observation, not by derived signal.** Each poll of a
  long-running process prints the actual content - the pane capture,
  the log tail, the artifact state - never a "done?" flag you have not
  proven fires on a known completion. Two content-identical polls mean
  read the content, not poll longer.
- **Anchor project-scoped commands to an explicit working directory**
  and print the resolved directory before the first mutating call. Do
  not assume the directory persists between invocations; pass an
  explicit workdir or absolute paths.
- **Run the touched tree's own gates immediately after writing into
  it.** Know each gate's scan scope before adding content near it;
  incremental gate runs catch the defect at edit time, not at suite
  time.

## Worktrees for parallel sessions

When using parallel sessions on the same repository, create git
worktrees so edits do not clobber each other and per-session state
stays isolated. Worktrees isolate code state; they do not reduce the
token count of a session.

## Skill invocation controls

Some harnesses can keep a skill out of automatic selection or expose it
only as a command. The OpenCode 1.x and Claude Code fields are
harness-specific: read references/harness-controls.md for the exact keys
and what each does.

## Sandbox the entire loop

Sandbox the whole agent loop, not just individual tool calls. A
container that contains only the repository and the tools the task
needs is the strongest boundary: it prevents a compromised tool from
reaching outside the intended domain.

## Provenance

Sources and adaptations: references/provenance.md.

## Non-goals

This skill does not implement an OS sandbox, replace provider-native
authentication, or authorize credentials for a task. It offers guidance,
not a security boundary. If a request falls outside these bounds, refuse
or hand off.