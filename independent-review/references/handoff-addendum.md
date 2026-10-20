# Handoff addendum

**Read when**: appending the review handoff to a plan given to an
implementing agent.

The deliverable is not the verdict; it is the corrected plan plus this
addendum, appended verbatim so the implementing agent cannot satisfy the
plan without satisfying the seams:

> Before declaring any task done: trace every new error or failure path
> to the boundary that handles it with a test through that boundary,
> thread every computed value to its consuming call, read every touched
> function in full as it now exists, and run this skill's code-review
> mode over your own diff. Close its findings, then report which probes
> fired and what they found. A green test suite is not completion.