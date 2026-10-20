# Emit-prompt template

**Read when**: Using emit-prompt mode to create standalone review prompts.

Produce a fully standalone review prompt for an independent model.
The prompt must carry every fact the reviewer needs: no context
from this session may be required.

## Template

```markdown
# Review prompt: <plan title>

You are an independent code reviewer. Review the plan below against the
actual repository state and produce a verdict. Read-only: no file
modifications, no state-changing git commands (`git fetch` is allowed).
No context beyond this prompt and the repository is needed.

## Repository context
- Repo: <path/remote>. <Current checkout facts: branch or commit the
  plan assumes; uncommitted state if relevant.>
- <Upstream/other-branch facts the plan depends on, with commits to
  inspect.>

## Review task
- Derive your own verification plan from the goal, the tree, and the
  defect classes below. Do not rely solely on a claim list.
- Per delta: integration point in CURRENT code (re-derive; names may
  have drifted), existing tests at risk, red-green adequacy.
- Per delta adding an error path, a fail-closed behavior, an external-format
  parser, a CLI wiring, or a validator: the plan names its exception
  flow, positive-path test, wire-format evidence, real-path command
  test, and malformed-input cases; a missing one is a finding.
- New-defect scan (not just the claims).
- State explicitly what you could not verify read-only.

## Secondary cross-check
Claims the plan makes (verify each, but also scan for what this list omits):
1. <claim> - <file:line or function suspected>
2. ...

## The plan under review
<plan text, verbatim>

## Output format
1. Verdict: APPROVE / APPROVE WITH CHANGES / REJECT.
2. Findings: ID, severity, area, evidence, required action.
3. Claims disposition table: VERIFIED / REFUTED / PARTIALLY VERIFIED.
4. Open items + one-paragraph summary.
```