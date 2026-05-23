---
name: codebase-review-and-design-assessment
description: Review an unfamiliar codebase and produce a grounded design assessment with explicit judgment and pragmatic recommendations.
version: "1.0"
tags: [code-review, architecture, assessment, design, maintainability]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Codebase review and design assessment

Use this skill when asked to read a project, review a codebase, assess the current design, evaluate architecture, or give a grounded opinion on maintainability and technical direction.

## Core rule

Do not answer from stale conversational context or from a previous task summary. Start by re-grounding in the current repository and current request. A design review that is not tied to the actual codebase is worse than no review.

## Outcome

Produce a review that:
- is grounded in the repository as it exists now
- distinguishes observations from inferences
- identifies strengths, weaknesses, risks, and next moves
- is pragmatic rather than theatrical
- speaks with senior software development and software architecture judgment

## Required workflow

1. Re-anchor on scope.
   - Restate the requested review target in one line.
   - Treat requests like "have a read at this project" as a fresh task, even if previous turns discussed other work.

2. Read project instructions first.
   - Check repository guidance files before forming opinions.
   - Respect the repo's declared source of truth for coding and agent instructions.

3. Map the codebase before judging it.
   - Identify the main entrypoints, core packages/modules, public API surface, tests, and configuration.
   - Look for boundaries: domain logic, orchestration, IO/adapters, CLI, rendering, persistence, integrations.

4. Review implementation evidence.
   - Read representative files, not just names.
   - Inspect how data flows through the main path.
   - Compare intended structure with actual coupling.
   - Use tests to infer expected behavior and stability boundaries.

5. Assess the design on concrete axes.
   - Module boundaries and cohesion
   - Coupling and dependency direction
   - Public API clarity
   - Error-handling strategy
   - Testability and test shape
   - Extensibility and change cost
   - Operational risk and failure modes

6. Deliver the review in a useful shape.
   - Brief overall verdict
   - What is working well
   - What is structurally weak or fragile
   - Most important risks
   - Recommended next steps, prioritized
   - Explicitly separate "do now" from "later if worth it"

## Review intent variants

The framing of the review request changes what you prioritize:

### "I haven't looked at this in a while, is it okay?"
Standard health check. Cover all axes. Flag anything that would cost time to fix later.

### "We're about to do a big update — want to make sure the foundation is solid"
This is a pre-change stabilization review. Different priority order:
- Principle violations first — things that will compound across many files when the big update touches them (duplicated logic, type drift, undeclared contracts)
- Missing tests second — the big update needs a safety net; flag if there is none
- Structural seam problems third — boundaries that will make the update hard to execute cleanly
- Polish and local smells last — fine to note, but don't let them dominate a pre-change review
- End with an explicit "lock these in before you start" list of principles, not just a to-do list

For this intent, the output should give the user confidence about what is stable and a clear list of what to fix before branching.

### "Review this PR / feature"
Standard diff-focused review. See code-reviewer-strict for this path.

## Good review heuristics

- Prefer evidence over vibes. Name files/modules/functions when making claims.
- Call out duplication only when it affects change cost, correctness risk, or conceptual clarity.
- Distinguish a local code smell from a design problem.
- Recognize when the current design is good enough and should not be over-abstracted.
- Reward stable seams, focused modules, and strong tests.
- Critique with precision: what hurts, why it hurts, and what a smaller better shape looks like.

## Support files

- `references/pre-change-stabilization-checklist.md` — structured checklist for the "solid foundation before a big update" review intent.
- `references/nextjs-logic-duplication-patterns.md` — common duplication patterns in Next.js apps (server/client logic drift, type redeclaration) and how to fix them.

## Pitfalls to avoid

- Responding with a summary of unrelated prior work
- Skipping the repository-reading step and jumping straight to recommendations
- Inventing architectural intent that is not visible in the code or docs
- Recommending a large redesign when a smaller boundary cleanup would solve the actual problem
- Giving only negatives; note what should be preserved
- Claiming a config file is absent without actually checking
