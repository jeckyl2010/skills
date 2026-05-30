---
name: senior-software-development
description: Apply senior-level engineering judgment to code review, implementation, debugging, refactoring, and delivery planning.
version: "1.2.6"
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
- **CSS/style reviews done incrementally miss dead rules and drift — and reviews scoped only to cards miss everything else.** The user has explicitly flagged that a "detailed review" that only checks card chrome still leaves numerous issues in buttons, blockquotes, labels, inline styles, icon containers, and markup classes. Correct scope for a CSS review: (1) read ALL files in full before touching anything — global CSS plus every page/component with a local style block; (2) audit ALL element categories, not just cards — see `references/css-dead-rule-audit.md` for the full checklist; (3) build the complete finding list first; (4) only then patch. An incremental pass that narrows to one element type is not a detailed review — it is a partial pass that will draw a correction.

- **Dead CSS rules are invisible unless you verify all selectors against the markup.** For each CSS rule found in a style block or stylesheet, confirm the selector matches at least one element in the current HTML/template. Classes left over from removed features, renamed elements, or layout refactors are otherwise silent — they cost nothing at runtime but mislead every future reviewer. Common missed cases: a class renamed in markup but not in CSS; a section removed from the page but whose styles stayed; a `:hover` rule always shadowed by a more specific sibling rule (e.g. `.foo:hover` always beaten by `.foo-static:hover` when every element carries both classes).

- **multi-file patch(mode='patch') can silently skip files with no error.** The diff output only shows files that changed — a file that was targeted but skipped due to a context mismatch produces no warning. Always verify each target file with a content check (read_file) before reporting success. When in doubt, use mode='replace' with a unique old/new pair — it fails loudly if the match is not found.
- **skill_view reads a cached snapshot, not disk.** After patching a skill file, skill_view may return the pre-patch state. Use read_file on the actual path (e.g. `~/.hermes/skills/engineering/<name>/SKILL.md`) to confirm the edit landed before acting on it.
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
| `references/css-dead-rule-audit.md` | CSS dead-rule audit technique: full-read-first sequence, specificity traps, Comtech-site examples, shared-class consolidation pattern |
| `references/mk2conf-image-pipeline.md` | mk2conf image pipeline: parser → IR → emitter stages, alignment mechanics, auto-center design notes |
