# skills

Self-contained agent skills for agentic coding. Each skill is a directory
with a `SKILL.md` that carries `name` and `description` frontmatter (the
load trigger) and a lean body that defers detail to `references/` pages
the body tells the agent to read.

## Skills

| Skill | Loads when |
|---|---|
| **verification** | Writing/reviewing tests, verifying a change before reporting done, testing a skill |
| **context-budget** | Start of long or multi-task sessions, mid-session degradation, splitting work across sessions |
| **workflow-patterns** | Planning how to structure a feature, decomposing work, designing a skill |
| **tools-and-security** | Wiring tools, designing agent-facing tools, configuring permissions and credentials |
| **independent-review** | Reviewing plans, diffs, or skills; at self-handoff before reporting done |
| **readme-authoring** | Creating or rewriting a README, testing documentation claims |

## Structure and size budget

Each skill is an entry map plus references:

- `SKILL.md` - short intro, the rules that must apply immediately, and
  pointers that name each `references/` file and when to read it.
- `references/` - checklists, templates, and worked detail, loaded only
  when the body says so.

Budgets, enforced by `tests/test_skills.py`:

- Description: at most 300 characters, trigger-first.
- `SKILL.md` body: at most 900 words; no section over 250 words.
- No doctrine duplicated across skill bodies, beyond the standard
  refusal and provenance sentences; one canonical owner per rule.
- References may be longer; detail belongs there, not in the body.

A portable skill names no project path; project-scoped conventions (for
example the session manifest) live in a `references/` page marked
optional and project-scoped.

## Directory layout

```
skills/
├── context-budget/
│   ├── SKILL.md
│   └── references/
│       ├── session-continuity.md
│       └── provenance.md
├── independent-review/
│   ├── SKILL.md
│   └── references/
│       ├── probe-lists.md
│       ├── emit-prompt-template.md
│       ├── audit-checklist.md
│       ├── skill-review.md
│       ├── handoff-addendum.md
│       └── provenance.md
├── readme-authoring/
│   ├── SKILL.md
│   └── references/
│       ├── style.md
│       └── provenance.md
├── tools-and-security/
│   ├── SKILL.md
│   └── references/
│       ├── harness-controls.md
│       └── provenance.md
├── verification/
│   ├── SKILL.md
│   └── references/
│       ├── skill-testing.md
│       ├── test-shapes.md
│       └── provenance.md
└── workflow-patterns/
    ├── SKILL.md
    └── references/
        ├── skill-design.md
        ├── spec-driven.md
        ├── handoffs.md
        └── provenance.md
```

## Convention

Each `SKILL.md` has YAML frontmatter with `name` and `description`. The
description is the load trigger: a harness surfaces it at session start
and injects the body only when the task matches. OpenCode 1.x also recognizes
`metadata` keys: set `opencode/slash: "true"` to expose the skill as a
`/name` command, and `opencode/autoinvoke: "false"` to keep it out of
model-facing automatic selection.

All six skills set `opencode/slash: "true"` and keep automatic selection
enabled, so after installation they are available as `/context-budget`,
`/workflow-patterns`, `/verification`, `/tools-and-security`,
`/independent-review`, and `/readme-authoring`, and each may also load
automatically when its trigger matches. `independent-review` also fires
at self-handoff, before an agent reports done.

## Using with a harness

### OpenCode support

OpenCode discovers skills from these paths (documented at
https://opencode.ai/docs/skills/):
- `.opencode/skills/<name>/SKILL.md` in a project
- `.claude/skills/<name>/SKILL.md` in a project
- `.agents/skills/<name>/SKILL.md` in a project
- Global: `~/.config/opencode/skills/<name>/SKILL.md`
- Global: `~/.claude/skills/<name>/SKILL.md`
- Global: `~/.agents/skills/<name>/SKILL.md`

These paths and the slash metadata are the OpenCode 1.x mechanics.
OpenCode 2 differs concretely: `opencode/slash` is not interpreted,
so these skills expose no `/name` commands there. Load a skill by mentioning
`@skill-id` in the prompt, or define `/name` commands separately under
`.opencode/commands/`. `opencode/autoinvoke` carries over
(`disable-model-invocation` is an alias), the discovery paths above are
unchanged, and the name/directory match and description length limit
are no longer enforced. The agent-facing invocation reference is
`tools-and-security/references/harness-controls.md`.

### Other harnesses

Other harnesses are unvalidated. If a harness discovers skills from
standard frontmatter (name, description), symlink or copy skill
directories into its skills path.

## Adding a skill

1. Create a directory named after the skill.
2. Write `SKILL.md`: trigger-first description, lean body, and pointers
   that name each reference file and when to read it.
3. Put checklists, templates, and worked detail in `references/`.
4. State non-goals.
5. Add the skill to `EXPECTED_SKILLS` in `tests/test_skills.py` and to
   the README table.
6. Run `python3 -m pytest`.

## Prior art and provenance

These skills re-express published guidance as loadable packages. The
repository records, per skill, which material was adapted from which
source and what is original: see [PROVENANCE.md](PROVENANCE.md). The
original content of this repository is released under the MIT licence
(see [LICENSE](LICENSE)); third-party material cited in PROVENANCE.md
remains the property of its authors.

## Testing skills

Static checks are automated: run `python3 -m pytest`. The suite validates
frontmatter, description and body budgets, section sizes, references
(existence and reverse-citation), README consistency, Markdown list
formatting, cross-skill duplication, and portability, with known-good and
known-bad fixtures for the validators themselves.

Routing, live, and reconstruction tests are manual procedures documented
in `tests/routing/README.md`; they are not run in CI.