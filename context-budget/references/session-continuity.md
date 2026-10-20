# Session continuity (optional, project-scoped)

**Read when**: the project keeps a session manifest at
`.agents/session-manifest.json`, or you are deciding whether to adopt
one.

This is a local project convention, not an OpenCode feature. Use it only
if the project already keeps a manifest.

## Manifest protocol

1. Read the manifest before starting work.
2. Check that the active files exist; mark missing entries `archived`.
3. Update `last_accessed` for any files you read.
4. Ask before continuing with active files: "Continue with previous
   working files?"

When you create a working file, register it: a path relative to the
project root, a one-sentence purpose, and an updated `last_accessed`
whenever you read or reference it. Do not create working files without
registering them; orphaned files are invisible to later sessions.

At session end, move completed files to `archived`, update the current
session timestamp, and keep the last ten sessions in `previous`. Do this
with a script you have tested or by hand; check the result before relying
on it.

## File location strategy

| File type | Location | Retention | When to use |
|-----------|----------|-----------|-------------|
| Longer-term investigations | `.agents/work/investigation-*.md` | 30 days | Multi-session debugging, architectural decisions |
| Implementation plans | `.agents/work/plan-*.md` | 30 days | Structured implementation with clear end states |
| Research notes | `.agents/work/notes-*.md` | 30 days | Findings worth preserving |
| Quick scratch | `/tmp/opencode/quick-*.md` | 7 days | Temporary working notes |
| Test scripts | `/tmp/opencode/temp-*.py` | 7 days | Exploratory code experiments |
| Debug logs | `/tmp/opencode/debug-*.log` | 7 days | Debugging output artifacts |

## Cross-session file discovery

With a manifest, a new session can discover all active working files,
know why each exists, which session created it, and fall back to
scanning known directories when the manifest is missing.

## Cleanup

List files first; delete only after checking the list:

```bash
find /tmp/opencode -type f -mtime +7 -print
find .agents/work -type f -mtime +30 -print
```

Do not run a cleanup script whose dry run you have not inspected.

## Manifest schema version

Current schema version: `1.0.0`. Include the version in all manifests
and validate on read. Plan for backward compatibility as the schema
evolves.