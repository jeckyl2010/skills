---
name: senior-software-development
description: Apply senior-level engineering judgment to code review, implementation, debugging, refactoring, and delivery planning.
version: "1.2.2"
specificity: generic
tags: [code-review, refactoring, debugging, testing, implementation, maintainability]
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []
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

## Verify stale notes before acting on them
When resuming from a "remaining work" list in memory or session notes, always check current state first — items may have been addressed while the project was idle. Do not fix what is already fixed.
- Run a quick scan of every file mentioned in the remaining work list before proposing changes.
- Cross-reference findings against the actual code — a finding about "hardcoded magic number" or "path traversal risk" may already be fixed.
- Only surface items that are still outstanding. Surface the false-positives too so the user knows the list was audited, not blindly skipped.

## Code hygiene principles

**Broken windows** — one crack signals nobody cares, so more cracks follow. Dead CSS rules, empty rule blocks, stale TODO comments, a test suite that is always red. Each one lowers the bar for the next person. Fix them on sight, even if they are not your mess.

**Boy Scout rule** — leave the codebase at least as clean as you found it. Ideally a little cleaner. Not a full refactor — just: remove the empty rule you noticed while adding a feature, rename the confusing variable while you are already in that file, delete the commented-out block that has been there for two years.

In practice:
- No empty blocks, dead rules, or unused declarations left behind.
- No commented-out code in commits unless it carries an explicit explanation.
- No TODO comments older than the current sprint without a linked issue.
- No unused imports, unused variables, unused constants.
- If you touch a file, leave it cleaner than you found it.

## Pitfalls

- Image generation via delegate_task (image_gen toolset) can return a false-positive "Saved to /path/file.png" when the file was never written. Always verify with a stat/ls check before referencing the path to the user. If missing, fall back to generating the image directly via execute_code + PIL (pillow). to avoid
- **Recommending creation of something that already exists.** Before suggesting the user create a GitHub Action, a config file, an abstraction, or any artifact — scan the repo first. `action.yml` present at the root means the Action is already there. "Inspect existing patterns" (Default lens step 2) applies to existence checks, not just style choices.
- **Transform pipeline short-circuits when required context is not threaded through.** A function that runs a transform (e.g. internal link resolution) silently produces wrong output when its required context (link map, config, nav tree) is missing — it runs, finds nothing, and produces a degraded result with no error. Pattern: search for every call site of the affected function and verify the context parameter is present at each one. When a publisher or compiler function is extracted from the main pipeline, explicitly check that all transform inputs travel with it — they will not automatically follow.
- **Synthetic nav/IR nodes built from path strings need humanised titles.** When constructing a synthetic node from a folder path or slug (e.g. `find_section_by_folder`), never pass the raw path string as the title. Apply `.replace("-", " ").replace("_", " ").title()` as the fallback, and prefer an explicit title from the resolved nav if one exists. Raw slugs as titles propagate visibly into Confluence page titles and headings.
- **Redundant computation at call sites.** When a function builds an expensive resource internally (a link map, a compiled schema, a resolved nav tree), consider returning it alongside the main result rather than discarding it. Callers that need it will otherwise rebuild it — sometimes multiple times in the same request. Pattern: change `-> Result` to `-> tuple[Result, ExpensiveArtifact]` and unpack at the call site. Check for redundant calls after any refactor that touches shared resources.
- **GitHub Actions shell injection via `${{ inputs.* }}` in `run:` blocks.** Template substitution happens before the shell sees the script — never interpolate inputs directly into a command string. Bind to env vars, build a bash array, and drop `eval`. See `references/github-actions-security.md` for the safe pattern.
- **Generic `.claude/commands/` names collide with built-in slash commands.** `/changelog`, `/test`, `/deploy` are reserved or commonly claimed. Always prefix with the tool identifier: `mk2conf-changelog.md` → `/mk2conf-changelog`. See `references/github-actions-security.md` for the full rule.
- Jumping to implementation before understanding the problem
- Proposing a new pattern when an existing one already fits
- Skipping error handling and edge cases in review
- Over-engineering for a problem that does not exist yet
- Combining behavior change with refactoring in one pass

## References

Load the relevant reference(s) for the current task. The principles above apply regardless of which you load.

| Reference | Load when |
|---|---|
| `references/bun-test-scaffold-nextjs.md` | Writing or fixing tests with Bun in a Next.js monorepo |
| `references/typescript-ci-toolchain.md` | Wiring up CI — Biome, knip, CodeQL, Codecov, osv-scanner |
| `references/dev-server-and-deps.md` | Dev server startup, dep updates, cross-platform portability |
| `references/nextjs-patterns.md` | Client/server boundary, API security, RSC noise, TypeScript deduplication |
| `references/framer-motion.md` | Framer-motion audit or full removal |
| `references/vscode-bun.md` | VS Code tasks for a Bun workspace |
| `references/framework-migration-cleanup.md` | Post-migration cleanup of old framework artifacts |
| `references/github-pages-publish-verification.md` | Publishing a static site to GitHub Pages |
| `references/github-actions-security.md` | GitHub Actions shell injection fix (env vars + bash array, no eval) and slash command namespacing |
