---
name: readme-authoring
description: >
  Use when asked to create, rewrite, review, or make a README less
  AI-sounding, or to test documentation claims: read the repository
  first, document only real commands and paths, then run static checks
  and a reconstruction test.
metadata:
  opencode/slash: "true"
---

# README Authoring

Write README files as project documentation for engineers who have just
opened the repository. Use direct language, concrete paths, and the
project's own terms. The README explains what the project provides, how
to get started, and where to find the parts needed for the next task.

## First read the project

Before writing:

1. Inspect the repository root, existing README files, relevant
   configuration, entry points, and the directories the README will
   describe.
2. Read the implementation or workflow documents that define the actual
   behavior.
3. Identify the intended reader: operator, contributor, implementation
   agent, or user.
4. List the concrete deliverables, commands, directories, and workflows
   that reader needs.

Do not invent commands, components, file paths, deployment steps, or
outcomes. If the README describes planned work, say that it describes
planned work.

## Recommended structure

Use only the sections that help the reader. A typical project README
contains:

```md
# Project name

One or two sentences describing the project and its purpose.

## Quick start

The shortest correct path to the first useful action.

## Overview of deliverables

The major components and how they fit together.

## Workflow

The normal sequence for using, generating, or operating the project.

## Directory layout

A short tree and explanations for the important directories.

## Configuration, validation, or handoff

Only when the project needs these sections.

## Glossary

Project-specific terms that appear elsewhere in the README.
```

For a specification repository, explain both the end product the
specifications describe and the workflow for producing specifications
and handing implementation work to agents. Include an indicative
operational workflow when several components work together.

## Style

Use normal source-project documentation language. The full style rules,
the avoid list, and the wording table are in references/style.md.

## Test the claims

- **Static checks**. Verify each command, path, flag, and referenced
  documentation file against the repository. Where possible, encode
  these checks as tests, not just a review pass.
- **Reconstruction test**. Remove the README from the agent's view,
  hand it the repository alone, and grade what it can rebuild: every
  invented path is a failure, every admitted gap is a finding. "I
  cannot determine this" is an acceptable answer.
- **Product docs are the last word**. For references to product
  documentation, the product docs are the final authority; local docs and
  tests prevail for the project's behavior.

## Review pass

Before finishing:

1. Check every path and command against the repository.
2. Remove sections that describe temporary generation or review files
   when the README's reader does not need them.
3. Confirm the component overview describes the completed system, not
   only the documentation process.
4. Check the workflow gives a reader enough context to use the project.
5. Search for repetitive, vague, or AI-sounding wording and replace it
   with plain project language.
6. Keep the README self-contained: define project-specific terms a new
   reader needs.

When refining an existing README, preserve correct project terminology
and structure; make focused edits instead of rewriting sections that
already read well.

## Provenance

Sources and adaptations: references/provenance.md.

## Non-goals

This skill does not invent commands or paths, document planned work as
shipped, or replace product documentation. If a request falls outside
these bounds, refuse or hand off.