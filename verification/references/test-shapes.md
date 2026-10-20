# Test shapes

**Read when**: designing or reviewing a test matrix beyond the core
red-green rules in the skill body.

- **Malformed inputs.** Validator matrices include schema-valid-but-
  malformed cases: a string where a number is expected, an empty value,
  a duplicate.
- **Material cells and risk-based coverage.** For any cross-product
  (actors x actions, inputs x states), enumerate the mechanically
  derived cells. Prioritize material cells: hard actors on high-value
  actions. For the long tail, use pairwise or risk-based coverage. A
  material cell with no test and no explicit non-scenario is a defect;
  unmapped non-material cells are not.
- **A fixture is a claim about its own bytes.** When a fixture encodes
  a runtime behavior, run the producer or scenario and assert the
  fixture matches. Running the loud variant and testing the quiet one
  is an embarrassingly easy error.
- **Author tests as if written with the original suite.** Generic,
  property-based names; state the invariant the test verifies, not the
  regression that motivated it.
- **Standing claims become standing tests.** A one-off session
  confirmation dies with the session. If the claim outlives the step,
  the check belongs in the suite.
- **State the invariant as a closed relation.** Tests should reject
  missing entries as well as undeclared ones, and reject invalid values
  as well as accept valid ones. One negative fixture proves one
  direction, not the relation.
- **One entity tested, many affected.** When an operation moves from a
  single entity to many, add a partial-failure test and an end-to-end
  test on the real invocation path.
- **Redundant fields are claims.** When a record carries raw entries
  and derived fields, validate the derivation, including the empty
  case.
- **Classification by search is fragile.** Match structured external
  responses at the raw boundary rather than searching a formatted
  message for a substring.
- **Sweeps carry canaries.** Before trusting a corpus sweep, plant a
  known token and prove the sweep finds it; enumerate the coverage
  explicitly.