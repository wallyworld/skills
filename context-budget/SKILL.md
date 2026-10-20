---
name: context-budget
description: >
  Use at the start of long or multi-task sessions, when output degrades
  mid-session, or when planning how to split work across sessions:
  clear context between tasks, scope investigations, delegate research
  to subagents, and write durable handoffs.
metadata:
  opencode/slash: "true"
---

# Context is a budget

Everything the agent reads, runs, or writes enters its context window.
Reasoning tokens are billed but invisible to the prompt; whether they
persist across compactions depends on the provider. Performance degrades
as the window fills: the agent starts forgetting earlier instructions and
making mechanical mistakes. Treat the window as the scarcest resource
in the loop.

## The iteration loop has a context twin

Every correction becomes part of the window, and the window is now the
problem it was correcting. Two rounds of failed correction on one issue
is the ceiling: past that, re-prompt in a clean session with the lesson
embedded. The mistakes of a long, corrected session are precisely the
mechanical ones a fresh session would never make.

## Hygiene rules

- **Clear context between unrelated tasks.** Mixing an unrelated
  question into a task buries the task's own history; the agent is
  quietly worse at both.
- **Scope investigations narrowly.** "Investigate the auth flow"
  invites a trawl across the whole tree; "read this file and summarise
  how refresh works" invites a paragraph.
- **Use subagents for research.** A research subagent reads in its own
  window and hands back only the conclusion; the files it opened never
  touch yours. Reserve direct reads for the few files whose verbatim
  content is needed.
- **Know your harness's subagent semantics.** If subagents return only
  summaries, run read-only deterministic commands directly in the parent
  session so the verbatim output returns; reserve subagents for work
  where a summary is acceptable.
- **Start a fresh session per phase** - research to implementation,
  implementation to review. A reviewer in a clean session has no
  loyalty to choices it watched being made.
- **Budget for reasoning.** Reasoning tokens consume the token and cost
  budget and occupy the window; persistence across compactions depends
  on the provider, so do not assume they are retained. Where the harness
  exposes effort settings, spend high effort on hard steps and low on
  routine ones, rather than uniformly.
- **Load only the skills the phase needs.** Skill descriptions are
  surfaced at session start and re-sent on long turns; keep the enabled
  set small and defer detail to each skill's `references/` pages.

## Durable handoff

A handoff document placed in a temporary directory can be referenced in
the next session's first prompt. List the key repositories, any
uncommitted work, and the most recent change. Cite files by absolute
path; include branch, commit, and the last command run. Reference
artifacts by path or URL. Redact secrets, tokens, and credentials. The
document can also suggest which skills to load next.

- **Ask, then roll back.** When a read-only question would force a new
  skill into the window, ask it, let the turn run, and reverse that
  turn if the harness allows. Do not assume any particular rollback
  mechanism exists.
- **Front-load the brief.** On a long-running task, open with the
  repository, the constraints that bind every command, the shape the
  artifact must fit, and two or three approaches already tried and
  rejected. A hundred tokens of preamble beats a hundred turns of
  back-and-forth.
- **Structure is a token strategy.** Boundaries that hold, small files,
  truthful names, and behavior-describing tests shrink the context the
  next reader - human or model - must load to work in the project.

## Durable records beat window memory

Compaction and trimming are lossy; the harness may retain the full
transcript, but the model stops seeing the older tokens. Anything that
must survive the session belongs in a file, not the window: a spec, a
plan, or a notes file. For the optional session-manifest convention
(registration, cross-session discovery, retention), read
references/session-continuity.md; it is a project-scoped convention, not
part of this skill's core rules.

## Provenance

Sources and adaptations: references/provenance.md.

## Non-goals

This skill does not implement a session manager, replace a durable spec,
or guarantee that a harness retains compacted context. The manifest
convention is optional and project-scoped. If a request falls outside
these bounds, refuse or hand off.