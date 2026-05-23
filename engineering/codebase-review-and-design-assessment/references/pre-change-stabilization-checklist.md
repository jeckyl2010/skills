# Pre-change stabilization checklist

Use this when the review intent is: "we're about to do a big update — want the foundation solid first."

## Principle violations (fix before branching)

- [ ] Is any core logic duplicated across server and client? (e.g. matchesCondition in both evaluator.ts and a client component)
- [ ] Are any shared types declared in multiple places? (Facts, EvaluateResult, etc.)
- [ ] Is there a canonical owner for each type that others import from, not redeclare?
- [ ] Do API shapes and client-side types stay in sync, or drift independently?

## Test coverage

- [ ] Are the engine/domain-logic functions covered by tests?
- [ ] If no tests: is the logic short enough that 15-20 cases would cover it? If yes — write them before branching.
- [ ] Are there existing test fixtures (sample data, model files) that tests can run against?

## Structural seams

- [ ] Are layer boundaries clean? (lib/ = server logic, components/ = UI, hooks/ = client API adapters)
- [ ] Does any component reimplement logic that belongs in lib/?
- [ ] Are there obvious coupling points that would make the big update touch too many files?

## Data quality

- [ ] Are any stats, counts, or summaries displayed to users derived from real data rather than constants or rough estimates?
- [ ] Are any fields using null to mean both "absent" and "explicitly cleared"? (Subtle answered/unanswered bugs)

## Motion/animation (for UI projects)

- [ ] Are animations restricted to opacity fades only?
- [ ] No y-axis slides, no staggered list entries?
- [ ] If framer-motion is present: is it wrapped and constrained, or used pervasively with defaults?

## Security posture (light check)

- [ ] Are any API endpoints exposing unrestricted filesystem paths?
- [ ] Are there Windows-specific paths in cross-platform config files that will silently fail?

## Output for the user

Close a pre-change stabilization review with two explicit lists:
1. "Lock in before you start" — the principles to enforce
2. "Fix now" vs "can live a bit longer" — prioritized with clear reasoning
