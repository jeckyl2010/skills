---
name: senior-software-development
description: Apply senior-level engineering judgment to code review, implementation, debugging, refactoring, and delivery planning.
version: "1.0.6"
tags: [code-review, refactoring, debugging, testing, implementation, maintainability, bun, test-scaffold, deduplication, derived-stats, nextjs, client-server-boundary, vscode, framer-motion, animation-cleanup, turbopack-cache, dev-server, watch-alerts]
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

## Testing deterministic engines
When writing tests for a pure evaluation engine (rules engine, guardrail evaluator, query parser):
- Use real fixture files rather than mocking the loader — tests catch model/code drift, not just unit behavior.
- Mock only explicit error paths (missing file, malformed input).
- Group tests by function, not by file. Each public function gets its own `describe` block.
- Always include one full-integration test with a realistic input object — confirms the wiring holds end-to-end.
- For engines that accumulate results (e.g. `because[]` lists), test that multiple matching rules add to the list, not replace it.

See `references/bun-test-scaffold-nextjs.md` for Bun-specific setup in a Next.js monorepo, including the `@types/bun` placement pitfall and `import.meta.dir` usage.

## Testing defensive parser functions
When a module exposes pure parse functions that accept `unknown[]` and silently drop malformed entries, cover: each valid variant, each skip condition in isolation, optional field presence/absence, sub-array value filtering, mixed valid+invalid input (verify count and order), empty input, and a real-file integration test that confirms `result.length === raw.length` — catches silent data loss when model files add new fields the parser rejects.

See `references/bun-test-scaffold-nextjs.md` for the full test coverage shape.

## Testing YAML serialisation contracts
For a thin YAML wrapper, test the *contract*, not the library: key order, booleans as true/false not 1/0, null serialised as "null", no anchors/aliases emitted, round-trip fidelity, and error paths. For model path helpers, verify the resolved paths point to real files on disk.

See `references/bun-test-scaffold-nextjs.md` for the pattern.

## Testing FS-coupled storage modules
When a storage module hardcodes its path resolution (e.g. `findRepoRoot(process.cwd())`) with no injection point:
- Do NOT refactor to inject paths just to enable tests. Use a snapshot/restore pattern.
- Capture the real shared state file before the suite runs; restore it in `afterAll`.
- Write test artifacts to `os.tmpdir()`, never into the real project directories.
- Use timestamped test ids to avoid test-run collisions.
- When testing error paths, verify the actual engine behaviour — some guards have gaps (e.g. `typeof [] === "object"` passing an array as a valid object). Document bugs explicitly in test names; do not silently paper over them.

See `references/bun-test-scaffold-nextjs.md` for the full snapshot/restore pattern and Bun runtime quirks.

## Cross-platform portability on project revival
When picking up a project that was last active on a different OS (e.g. Windows → macOS):
- Scan all YAML/config files for absolute paths — `portfolio.yaml`, `docker-compose.yml`, `.env` files. Windows absolute paths (`C:\\\\Repos\\\\...`) fail silently on macOS; convert to relative paths.
- Check `next.config.ts` / similar for hardcoded dev machine IPs in `allowedDevOrigins` — harmless but dead config, clean up.
- Verify runtime tools: `bun`, `node`, `python3`. Bun binary at `~/.bun/bin/bun` may not be on PATH in subshells — always `export PATH=$HOME/.bun/bin:$PATH` when invoking bun in scripts or execute_code.

### Portable manifest paths (YAML config files)
When code writes paths into a shared config file (`portfolio.yaml`, `docker-compose.yml`, registry manifests), always store paths relative to the config file's directory — not the raw user-supplied path (which may be absolute) and not the resolved absolute path.

```ts
// ✗ Stores whatever the caller passed — could be absolute
manifest.systems.push({ name: id, path: systemPath });

// ✓ Stores a path relative to where portfolio.yaml lives — portable across machines
manifest.systems.push({
  name: id,
  path: path.relative(path.dirname(portfolioFilePath), absoluteSystemPath),
});
```

This applies everywhere the write path is computed server-side from a user-supplied input. Cover with a test assertion that `path.isAbsolute(entry.path) === false` after the write — easy to verify by loading the YAML with `loadYamlFile` and checking the stored entry directly.

### Verify stale notes before acting on them
When resuming from a "remaining work" list in memory or session notes, always check current state first — items may have been addressed while the project was idle. Do not fix what is already fixed.
- Run a quick scan (search_files + read_file at the flagged lines) of every file mentioned in the remaining work list before proposing changes.
- Cross-reference review findings against the actual code — a finding about "hardcoded magic number" or "path traversal risk" may already be fixed. A quick read is faster than diagnosing a non-existent bug.
- Only surface items that are still outstanding. Surface the false-positives too ("item 4 is already fixed") so the user knows the list was audited, not blindly skipped.

### Version verification when an outdated check shows an unfamiliar version
If `bun outdated` shows a version that seems unexpected (e.g. `next 16.x` when you expected 14.x or 15.x), verify it exists on npm before researching breaking changes:
```
curl -s "https://registry.npmjs.org/<package>" | python3 -c "import json,sys; p=json.load(sys.stdin); print(p['dist-tags']['latest'])"
```
If the version is confirmed on npm, treat it as normal. Patch releases are safe to apply without deep research.

## Dependency update workflow (Bun monorepo)
Correct sequence when updating deps in a Bun workspace:
1. `cd web && bun update` — updates all packages to latest matching semver ranges
2. If `bun update` resolves to the same version (lockfile has pinned it), force the bump: `bun add next@16.2.6 react@19.2.6` — explicit version wins over range resolution
3. `bun run typecheck` (or `tsc --noEmit`) — verify no type regressions introduced
4. Pay special attention to major-version bumps (Zod 3→4, etc.) — check for API changes in `safeParse`, schema declarations
5. Only run the test suite after typecheck passes — no point diagnosing test failures caused by type errors

## Dev server startup verification (Next.js + Turbopack)
Next.js dev server writes startup output to stderr, not stdout.
When starting with a background process manager that captures only stdout, the log will appear empty even when the server is running.
Correct verification sequence:
1. Start server in background
2. Wait ~5s for Turbopack compilation
3. Check: `lsof -i :3000` — confirms the process is listening
4. Check: `curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/` — confirms a 200 response
Do not rely on log output to confirm readiness when using background process tracking.

If a second `bun run dev` call exits immediately with "Another next dev server is already running" and exit code 1, this is NOT a startup failure. Next.js detects the existing instance on port 3000 and terminates gracefully, printing the PID and log path of the running instance. Use `kill <pid>` from the log output if a restart is needed.

## Deduplication via re-export (TypeScript)

### Behavioral divergence check
Before removing a local copy of a utility, check whether it silently diverged from the canonical version. Common divergence: a local `deepGet` returning `undefined` for missing keys where the canonical one returns `null`. Steps:
1. Diff the two implementations side-by-side — look for return values, error handling, and type coercions.
2. Check every call site of the local copy for how it consumes the return value (`=== null`, `=== undefined`, `!= null`, `!value`).
3. If consumers already guard both (`=== undefined || === null`), the divergence is harmless — remove the local copy safely.
4. If consumers only guard one side, either fix the guards or keep the local copy and document the difference.

### Type shadowing: rename the local, don't alias the import
When a local type has the same name as an imported type from the same domain, the forced alias (`LibEvaluateResult`, `BaseType2`) is the smell — not a reason to live with the ambiguity.

Pattern: the hook defines `EvaluateResult` (an API envelope with `modelDir`, `modelVersion`, `result`) while also importing `EvaluateResult` from the evaluator lib. This produces the alias hack. Fix: rename the local to be domain-specific (`EvaluateApiResponse`), import the lib type unaliased. The rename is mechanical — grep for the old export name and update all consumers.

When collapsing a local copy of a type or function into a re-export from the canonical module:
- The file must `import type { Foo }` before it can use `Foo` in local function signatures — even if it also `export type { Foo }`.
- Ordering matters: put the `import` before the `export` re-export declaration, or TypeScript raises "Cannot find name" on the local usages.
- Pattern that works:
  ```ts
  import type { Facts } from "@/lib/evaluator";      // local usage
  export type { Facts } from "@/lib/evaluator";       // re-export for callers
  export { deepGet } from "@/lib/evaluator";
  // ... local functions that use Facts as a type ...
  ```
- If the file only re-exports and has no local usages, the `import` line is unnecessary.

## RSC payload errors after dep update restart
After a dependency update that restarts the Next.js dev server, the browser's cached RSC connection may produce "Failed to fetch RSC payload for ... Falling back to browser navigation" errors in the dev server log. These are not real errors — the browser reconnects automatically and pages load fine. This is expected noise from the hot restart, not a broken route. Confirm page health with `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/<route>` if in doubt.

## Derived stats: use real model data, not hardcoded estimates
When a page shows aggregate stats (completion rate, average questions per system, etc.), always derive them from actual data flowing through the system. Hardcoded constants like `avgQuestionsPerSystem = 15` become silently wrong as the model evolves and differ per-system anyway.

Correct pattern:
- Extend the data-fetching layer (e.g. `buildPortfolio`) to include the real count alongside the existing data (e.g. `totalQuestions: res.required_questions.length` per row).
- Compute aggregates in the page/component from those real numbers: `rows.reduce((sum, r) => sum + r.totalQuestions, 0)`.
- The data is already available from `evaluateFacts` — it just needs to be surfaced up, not estimated.

## API route security: filesystem-serving endpoints
Any Next.js API route that accepts a `path` query parameter and calls `fs.readdir` / `fs.readFile` is a path traversal risk — it will serve `/etc`, `~/.ssh`, or any absolute path the caller supplies.

Fix pattern used in `web/app/api/browse/route.ts`:
1. Compute allowed roots at request time (repo root + `os.homedir()`). Use `path.resolve()` to normalise both.
2. Resolve the requested path with `path.resolve()` before any comparison — blocks `../../../etc` traversal.
3. Reject with 403 before touching the filesystem if `resolved.startsWith(root + path.sep)` fails for all roots.
4. Apply the same check to the "go up" parent link — don't let the UI offer navigation that escapes the boundary.
5. Default start path: the repo root, not bare homedir — more useful for the actual file-picker workflow.

```ts
function isPathAllowed(target: string, roots: string[]): boolean {
  const resolved = path.resolve(target);
  return roots.some((root) => resolved === root || resolved.startsWith(root + path.sep));
}
```

This is a general pattern for any tool that lets the browser navigate the host filesystem. The allowed roots must be computed server-side; never trust a client-supplied root.

## VS Code tasks for Bun workspaces
When a project uses Bun and VS Code, the editor defaults to yarn/npm for its built-in task runner. This causes "command not found: yarn" errors when running npm scripts from the VS Code task panel.

Fix: create `.vscode/tasks.json` with explicit bun commands, and pin `npm.packageManager` in `.vscode/settings.json`.

Key details:
- All task `command` fields use `bun run <script>` or `bun test` directly — never `npm run` or `yarn`
- Set `"options": { "cwd": "${workspaceFolder}/web" }` for monorepos where scripts live in a subdirectory
- Mark `dev` and `test:watch` as `"isBackground": true` with a `problemMatcher` so the terminal stays open
- Set `"group": { "kind": "build", "isDefault": true }` on the build task so Cmd+Shift+B works immediately
- Set `"group": { "kind": "test", "isDefault": true }` on the test task so Cmd+Shift+T works
- Add `"npm.packageManager": "bun"` to `settings.json` — stops VS Code guessing yarn/npm for other integrations
- Add a top-level `"options": { "env": { "PATH": "${env:HOME}/.bun/bin:${env:PATH}" } }` block — VS Code task shells do NOT inherit the user's `.zshrc` PATH, so bun will fail with `command not found` without this. This is the most common failure point after initial setup.

### VS Code NPM Scripts sidebar panel — known bun limitation
The sidebar "NPM SCRIPTS" panel in VS Code Explorer does NOT support bun as a runner. The `npm.packageManager` setting only accepts `auto`, `npm`, `yarn`, or `pnpm` — passing `"bun"` is silently ignored and the panel falls back to yarn. This is a VS Code limitation, not a config error.

Consequence: clicking scripts in the NPM Scripts sidebar will always fail with `command not found: yarn` when bun is the actual runner.

Resolution: use Terminal > Run Task (from `tasks.json`) instead of the sidebar panel. Optionally hide the NPM Scripts panel to avoid confusion: right-click the Explorer sidebar > uncheck "NPM Scripts".

The `packageManager: "bun@x.y.z"` field in `package.json` is still worth setting — it signals intent, supports Corepack, and may be picked up by future VS Code versions — but it does not fix the sidebar runner today.

### `.gitignore` strategy for `.vscode/`
The default is to ignore the entire `.vscode/` directory, but shared config should travel with the repo so other developers get the same setup.

Correct pattern — replace the blanket ignore with targeted exclusions:
```
# Instead of: .vscode/
.vscode/*.code-snippets
.vscode/launch.json
```

Track: `tasks.json`, `settings.json`, `extensions.json` — shared tooling config
Ignore: `launch.json`, `*.code-snippets` — personal debugger and snippet preferences that vary per developer

See `templates/vscode-tasks-bun.json` for a ready-to-use tasks.json for a Next.js + Bun monorepo (copy to `.vscode/tasks.json`, adjust `cwd` if the web dir is named differently).

## Next.js client/server module boundary
A `"use client"` component must not import — directly or transitively — any module that uses `node:fs`, `node:path`, or other Node-only APIs. The error surfaces at build time as:

```
the chunking context (unknown) does not support external modules (request: node:fs/promises)
```

The import trace in the error shows the full chain: client component → intermediate module → server module. Fix it by splitting the server module.

**Pattern: client-safe extraction**
1. Create `lib/facts.ts` (or similar) containing only pure functions and types — no imports from `node:*`, `yaml`, or any loader.
2. The server-side module (`lib/evaluator.ts`) imports and re-exports from `lib/facts.ts`, then adds its async/fs-dependent logic on top.
3. Client components import pure utilities from `lib/facts.ts` directly.

```
lib/facts.ts          ← pure: Facts, deepGet, matchesCondition. No imports.
lib/evaluator.ts      ← re-exports from facts.ts + server-side async evaluation
"use client" components ← import from lib/facts.ts, never lib/evaluator.ts
```

This keeps a single implementation of each function while respecting the client/server boundary. The re-export in `evaluator.ts` means server-side callers continue to get everything from one import.

**Dedup trap**: consolidating duplicated logic by pointing a client component at the server module will break the build if that module has any `node:*` in its import chain — even if the function being imported is itself pure. The fix is extraction, not just re-export.

## Framer-motion audit and cleanup
When stripping y/x/scale/stagger animations across a codebase, work in two parallel batches (split at ~8 files each to stay within delegation limits). Use this decision matrix:

**Strip → plain element (no animation left):**
- `motion.div` with only `y` or `x` in initial/animate → convert to `<div>`
- `motion.h3/p/span/button` with mount-only y/scale → convert to native element
- `index * 0.05` stagger delays → remove entirely
- Sequential mount delays (0.1, 0.2, 0.3…) → remove entirely

**Strip partially → keep as motion element (opacity-only):**
- `motion.div` with both `opacity` and `y` → remove `y`, keep `opacity` fade
- Modal/dialog entry with `scale + opacity` → remove `scale`, keep `opacity`
- `AnimatePresence` + `exit={{ opacity: 0 }}` → always keep (exit animations require framer)

**Keep as-is (functional, not decorative):**
- `height: 0` → `height: "auto"` expand/collapse (communicates state change)
- Spring transitions on interactive state indicators (e.g. selected dot in sidebar)
- `AnimatePresence mode="popLayout"` on list reordering

**After the edit pass:**
- Delete `.next/` before restarting the dev server — Turbopack caches the old module graph. Stale `motion is not defined` runtime errors after import changes are almost always a `.next` cache issue, not a real import bug. Clean build confirms it.
- Watch-pattern alerts on a background process can fire on old buffered output that predates the fix. Before re-diagnosing, read the full process log (process action='log') and check whether the errors appear before or after the relevant code change. If the server has been serving 200s since the fix, the alerts are stale noise, not a new problem.
- Run `bun run build` after cleanup, not just `bun run typecheck` — the build catches client/server boundary issues that typecheck misses.

**Ideal end state:** a single `<FadeIn>` wrapper component (`initial={{ opacity: 0 }} animate={{ opacity: 1 }}`, short duration, no y/scale/stagger) that all fade-in usage routes through. Eliminates drift when framer-motion is updated or removed.

## Framer-motion full removal (dependency uninstall)
When the decision is to remove framer-motion entirely (not just reduce it):

**Replacement strategy:**
- `motion.div` with opacity fade → `<div className="animate-in fade-in duration-300">` (Tailwind 4, entry only)
- `motion.div` with only `y` offset → plain `<div>` (drop the animation entirely)
- `AnimatePresence` + conditional render → drop `AnimatePresence`, keep conditional render; exit snap is acceptable for non-critical UI
- `layoutId` indicator bars → plain div, instant snap is fine
- Uninstall: `bun remove framer-motion`

**Structural pitfall — `createPortal` + `AnimatePresence`:**
When `AnimatePresence` was the single child of `createPortal(child, container)`, stripping it leaves multiple sibling JSX nodes (comments + element) as direct arguments to `createPortal`, which is a syntax error. Wrap in a fragment:
```tsx
// Before (broken after AnimatePresence removal):
return createPortal(
  {/* comment */}
  <div ...>,
  document.body
);
// After:
return createPortal(
  <>
    {/* comment */}
    <div ...>
  </>,
  document.body
);
```

**Structural pitfall — orphaned `{open && (` after AnimatePresence strip:**
When `AnimatePresence` wraps `{open && ( <> ... </> )}`, stripping `AnimatePresence` leaves the conditional as a bare expression inside `return (...)`. Wrap the whole return in a fragment:
```tsx
return (
  <>
    {open && (
      <> ... </>
    )}
  </>
);
```

**biome-ignore comments shift with indentation:**
After removing an `AnimatePresence` wrapper, the previously-suppressed element moves up one indentation level (and possibly one line number). Biome re-evaluates the suppress target from scratch — an existing `biome-ignore` on line N now covers a different element. Re-read the file and move or re-add the ignore comment to sit directly above the new offending line.

**Python bulk-replace for motion.\* patterns:**
Using Python regex (`re.sub`) to replace all `motion.div` / `motion.button` etc. is effective for the attribute variants (`motion.X initial=... animate=... className=...`), but leaves structural issues to fix manually:
- Orphaned closing `</motion.div>` and `</AnimatePresence>` tags
- Remaining `{open && (` without a wrapper (see above)
Always run `bun run typecheck` immediately after the script pass and fix structural issues before committing.

**Pre-commit hook stash trap:**
The pre-commit hook stashes unstaged files and runs against the staged snapshot. If you make lint/format fixes after `git add -A`, those fixes are in the working tree but not staged — the hook sees the pre-fix version and fails. Always run `git add -A` again immediately before the commit attempt that follows any post-stage fixes.

## TypeScript CI toolchain (Bun / Next.js)
When wiring up quality gates for a TypeScript project, use this tool stack:
- **gitleaks** — secret scanning (pre-commit + CI)
- **Biome** — lint + format (replaces ruff equivalent)
- **knip** — dead exports and unused deps (replaces vulture)
- **tsc --noEmit** — type checking
- **osv-scanner** — dep vulnerability audit (replaces pip-audit); use CLI download in a `run:` step — `google/osv-scanner-action` has no floating v2 tag and is a reusable workflow, not a step action
- **CodeQL** — SAST with `languages: javascript-typescript`
- **OSSF Scorecard** — supply chain
- **Dependabot** — `package-ecosystem: npm, directory: /web` for a workspace

Knip config: add `src/components/ui/**` to `entry` (not `ignore`) so shadcn-style component library exports are treated as intentional API surface. Add `tailwindcss` to `ignoreDependencies` — consumed via PostCSS, not imported in code.

Biome: run `bunx biome migrate --write` after any Biome version bump to update the schema URL. Use `--unsafe` flag to fix unused parameter and dead import warnings that safe mode won't touch.

See `references/typescript-ci-toolchain.md` for full workflow YAML, pre-commit config, knip.json template, GitHub post-setup checklist, repo metadata setup (`gh repo edit`), license fetch, and standard README badge block.

## Codecov lcov fix (Bun)
Bun's default coverage output is text-only (terminal table). To upload to Codecov,
generate lcov explicitly and pass the file path to the action:

CI step:
```bash
bun test tests/ --coverage --coverage-reporter=lcov
# produces: web/coverage/lcov.info  (relative to working-directory)
```

codecov-action config:
```yaml
- uses: codecov/codecov-action@v6
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: web/coverage/lcov.info    # ← relative to repo root
    fail_ci_if_error: false
```

Codecov also requires the repo to be activated on codecov.io after the first
successful upload — the CODECOV_TOKEN alone does not register the repo. Visit
codecov.io/gh/OWNER/REPO and activate it.

## Code hygiene principles

Two instincts, same outcome:

**Broken windows** — one crack signals nobody cares, so more cracks follow. Dead CSS rules, empty rule blocks, stale TODO comments, a test suite that is always red. Each one lowers the bar for the next person. Fix them on sight, even if they are not your mess.

**Boy Scout rule** — leave the codebase at least as clean as you found it. Ideally a little cleaner. Not a full refactor — just: remove the empty rule you noticed while adding a feature, rename the confusing variable while you are already in that file, delete the commented-out block that has been there for two years.

In practice:
- No empty blocks, dead rules, or unused declarations left behind.
- No commented-out code in commits unless it carries an explicit explanation.
- No TODO comments older than the current sprint without a linked issue.
- No unused imports, unused variables, unused constants.
- If you touch a file, leave it cleaner than you found it.

These are not perfection goals. They are hygiene — the baseline that keeps entropy from compounding.

## Pitfalls to avoid
- Jumping to implementation before understanding the problem
- Proposing a new pattern when an existing one already fits
- Skipping error handling and edge cases in review
- Over-engineering for a problem that does not exist yet
- Combining behavior change with refactoring in one pass
- Trusting background process logs for Next.js/Turbopack startup — use lsof + curl instead
- Hardcoding aggregate constants (avg questions, expected counts) — derive from real data instead
- Treating RSC payload errors after a server restart as real failures — they are browser reconnect noise
