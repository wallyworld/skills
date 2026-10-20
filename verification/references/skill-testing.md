# Skill testing

**Read when**: the artifact under test is a skill.

Four levels of evidence, in rising cost. None of them substitutes for
another:

1. **Static.** No agent involved: assert that every command, path,
   flag, and scenario the text cites exists in the repository, that
   frontmatter parses, that formatting holds. Ship known-good and
   known-bad fixtures for the checker itself, or you may publish a
   validator that never fails.
2. **Routing.** Present user requests to the skill's description and
   ask: does the essential request reach the right workflow? Does an
   out-of-scope request get refused or handed off? Does a dangerous
   one? Precise requirements take text checks; what the answer is
   actually prescribing takes a judgment.
3. **Live.** Give an agent the skill and real tools and let it act on a
   real system. Capture commands and system state independently of the
   agent's own report, and assert on the captured state, not on the
   agent's final sentence.
4. **Reconstruction.** Withdraw the skill's documentation and ask an
   agent to rebuild the key instructions from the name and a goal.
   Invented commands are failures; a named gap and a handoff are
   passes.

**Cost tiers.** Static is nearly free; routing costs a model call;
live costs an environment; reconstruction costs both. Pay for the depth
the change's risk justifies, and keep the cheap levels for every edit.

**Both ends of the truth.** A run can pass while the system it
describes is still mid-flight; a grader can fail a correct answer when
its model drifts; a truncated run can dress partial output up as
complete. Gate on captured state, not exit codes alone; record which
model graded a run and when; stamp saved responses with a date and a
recheck window before trusting them as live.

**Assertion choice.** `contains` proves a command was named, not that
it was recommended - a warning that mentions the dangerous command is
correct, so a blanket not-contains fails it. Where the semantics move
faster than the vocabulary, grade with a rubric instead of a string.