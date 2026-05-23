---
name: target-state-pattern-authoring
version: 1.0.0
description: Author target-state architecture patterns and proposals with clear problem, constraints, recommendation, trade-offs, risks, ownership, and next step.
tags: [architecture, target-state, patterns, proposals, manufacturing, documentation]
tool_agnostic: true
---

# Target State Pattern Authoring

Write architecture patterns and target-state documents that are defensible, operable, and repeatable.

## Use When

- Drafting a new target-state pattern or architecture proposal
- Restructuring a weak draft that reads like strategy prose, product marketing, or implementation detail
- Writing a repeatable position for multiple sites, regions, or vendor choices
- Turning a discussion note into a defensible architecture document

## Do Not Use When

- The task is code design inside a single application
- The artifact is primarily a detailed implementation plan or sprint breakdown
- The task is just proofreading or formatting

## Writing Standard

Write like a lead architect, not a consultant and not a developer writing feature specs.

The document must make these things explicit:

1. What problem is being solved
2. Which constraints materially shape the architecture
3. What the recommended target state is
4. What trade-offs are being accepted
5. What the top risks are and how they are mitigated
6. Who owns it, operates it, and approves exceptions
7. What the next smallest credible step is

## Preferred Structure

Use this unless the repository document type already defines one:

1. Context and problem
2. Hard constraints and assumptions
3. Recommendation
4. Key trade-offs
5. Risks and mitigations
6. Operating model and ownership
7. Evidence or approval needs
8. Next smallest step

## Procedure

1. **Start from the architectural hurdle.**
   State the real problem in blunt terms. If the hurdle is unclear, the document will drift.

2. **Pull constraints forward.**
   Make boundary conditions, survivability requirements, cost window, support model, and standardization constraints first-class — not footnotes.

3. **Recommend one default position.**
   Do not hide behind option lists unless the decision really is genuinely open. If you have a view, state it.

4. **Write trade-offs honestly.**
   If the recommended direction is politically awkward but technically right, say so.

5. **Keep implementation detail below the target-state layer.**
   Enough detail to be defensible, not so much that the pattern becomes a runbook.

## Anti-Patterns — Call These Out

- Product comparison disguised as architecture
- Abstract principles with no recommended operating model
- Cloud-first language that ignores outage behavior
- Soft statements with no owner or approval path
- Too many options with no recommendation
- Local exceptions quietly baked into a supposed standard
- Designs that are technically correct but operationally undeliverable in the real environment
