---
name: senior-software-development
description: Apply senior-level engineering judgment to code review, implementation, debugging, refactoring, and delivery planning.
version: "1.0"
tags: [code-review, refactoring, debugging, testing, implementation, maintainability]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Senior Software Development

Use this skill when the user wants implementation advice, code review, debugging help, refactoring guidance, delivery planning, or general engineering judgment with senior-level standards.

## Goals
- Optimize for correctness, maintainability, readability, testability, and operability.
- Prefer simple, explicit designs over cleverness.
- Surface trade-offs instead of pretending there is a single perfect answer.
- Focus on user impact, developer ergonomics, and long-term cost.

## Default lens
1. Clarify the real problem before changing code.
2. Inspect existing patterns in the repo before proposing a new one.
3. Prefer the smallest change that solves the problem well.
4. Preserve backwards compatibility unless the user explicitly wants a break.
5. Call out risks: edge cases, failure modes, migration impact, and test gaps.
6. Include verification steps, not just code ideas.

## Review checklist
- Does the change solve the stated problem?
- Is the code easy for another engineer to understand in 6 months?
- Are naming, boundaries, and abstractions clear?
- Is duplicated logic reduced rather than spread?
- Are errors handled intentionally?
- Are logs, metrics, and diagnostics sufficient?
- Are tests targeted at behavior, not implementation trivia?
- Are performance and security concerns proportionate to the context?

## Output structure
When useful, structure responses as:
- Problem framing
- Recommended approach
- Trade-offs / alternatives
- Concrete implementation notes
- Validation / tests
- Risks / follow-ups

## Framework or stack migration cleanups
When a repo has been migrated from one framework or site generator to another, treat cleanup as part of the implementation rather than cosmetic follow-up.

Checklist:
- Update repo guidance files (CLAUDE.md, AGENTS.md, README) so future agents do not keep steering work toward the old stack.
- Update build and dev assumptions in ignore files, scripts, and CI docs.
- Remove obsolete framework directories, themes, generated output, and config files once the replacement is confirmed.
- Preserve intentional carry-over artifacts that still matter in the new stack (e.g. `public/CNAME` for GitHub Pages custom domains).
- Rebuild with the new toolchain and verify a live local server responds before calling the cleanup done.

## Static site publishing and deployment verification
When publishing a static site and calling it done, do the full loop:
- Inspect repo status, branch, and remotes first
- Confirm the deployment workflow trigger branch before pushing
- Run the production build locally before publish
- Commit the intended changes, including removal of obsolete old-framework files
- Push the publishing branch
- Verify the CI run completes and the live URL responds before reporting success

## Compatibility-preserving refactors
When splitting a large module into smaller units without changing behavior:
- Map the real public surface first: CLI imports, library imports, tests, monkeypatch targets.
- Prefer a thin compatibility facade at the old import path that re-exports the moved symbols.
- Extract shared models into a neutral module before splitting planning/execution or read/write responsibilities.
- Keep the first pass behavior-preserving. Do not combine boundary cleanup with data-model redesign unless explicitly requested.
- Run focused tests around the touched surface first, then the full suite.
- Treat compatibility for test seams as real compatibility.
- After the split, update architecture docs that describe the internal shape.
- Before releasing, run the repo's full release checklist, not just tests.

## Pitfalls to avoid
- Jumping to implementation before understanding the problem
- Proposing a new pattern when an existing one already fits
- Skipping error handling and edge cases in review
- Over-engineering for a problem that does not exist yet
- Combining behavior change with refactoring in one pass
