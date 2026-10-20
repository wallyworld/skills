# Handoff contracts between skills

**Read when**: wiring a handoff from one skill to another.

Cross-skill handoffs require explicit contracts with triggers, inputs,
outputs, and fallback behavior.

## Verification-to-review handoff

- **Trigger**: before a completion report is written.
- **Inputs**: evidence block containing commands and their exit codes,
  a red-then-green test record showing before/after states, and a
  "not verified" column explaining what could not be checked.
- **Outputs**: complete diff with attached evidence block.
- **Unavailability behavior**: manual review initiation with explicit
  documentation - the reviewer states which evidence stand-ins were
  used and which assumptions remain unverified.

## Review-to-implementation handoff

- **Trigger**: APPROVE or APPROVE WITH CHANGES verdict.
- **Inputs**: corrected plan with findings incorporated plus handoff
  addendum.
- **Outputs**: implementation-ready task list with integration points.
- **Unavailability behavior**: manual verification of requirement
  coverage.