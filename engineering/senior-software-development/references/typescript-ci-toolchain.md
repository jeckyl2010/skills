# TypeScript CI Toolchain (Bun / Next.js)

Reference setup for wiring a TypeScript project with quality gates matching a
mature Python project (mypy + ruff + vulture + bandit + pip-audit + CodeQL +
Scorecard + Dependabot). This is the full pattern applied to risk-assistant.

---

## Tool mapping: Python → TypeScript

| Python              | TypeScript equivalent         | Purpose                        |
|---------------------|-------------------------------|--------------------------------|
| gitleaks            | gitleaks (language-agnostic)  | Secret scanning                |
| mypy                | tsc --noEmit (already there)  | Type checking                  |
| ruff                | Biome                         | Lint + format                  |
| vulture             | **knip**                      | Dead exports / unused code     |
| bandit              | (CodeQL covers it)            | SAST                           |
| pip-audit           | osv-scanner or `bun audit`    | Dep vulnerability audit        |
| pytest-cov→Codecov  | bun test --coverage → Codecov | Coverage reporting             |
| CodeQL              | CodeQL (js: javascript-typescript) | SAST                      |
| OSSF Scorecard      | same                          | Supply chain                   |
| Dependabot          | same                          | Dep updates                    |
| radon               | (skip — less relevant for TS) | Complexity                     |

---

## Knip — dead code detection

**Install:**
```bash
cd web && bun add -d knip
```

**knip.json** (place in `web/`):
```json
{
  "entry": [
    "app/**/*.{ts,tsx}",
    "src/**/*.{ts,tsx}",
    "src/components/ui/**/*.{ts,tsx}"
  ],
  "project": ["src/**/*.{ts,tsx}", "app/**/*.{ts,tsx}"],
  "ignoreDependencies": [
    "tailwindcss"
  ]
}
```

Key decisions:
- `src/components/ui/**` added to `entry` (not `ignore`) — shadcn-style component
  library exports are intentional public API, not dead code. Using `ignore` is
  wrong here; that suppresses the path from being analysed at all.
- `tailwindcss` in `ignoreDependencies` — consumed via PostCSS/config, not
  imported in code, so knip incorrectly flags it as unused.
- `ignoreDependencies: []` should be left empty initially; add to it only after
  confirming a flagged dep is genuinely used via a non-import mechanism.

**What knip finds (real vs false positive):**
- Unused files — often real (superseded components, scaffold leftovers)
- Unused deps — often real (@radix-ui/react-dialog etc. left over from abandoned features)
- Unused exports from `src/components/ui/` — false positive (component library)
- Unused types from schema/constants files — often false positive (they're API surface)

**Add to package.json scripts:**
```json
"knip": "knip"
```

---

## GitHub Actions workflow structure

Mirrors the Python pattern: a reusable `checks.yml` called from `ci.yml`.

### ci.yml
```yaml
name: CI
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

permissions: {}

jobs:
  checks:
    uses: ./.github/workflows/checks.yml
    secrets: inherit
    permissions:
      security-events: write
      contents: read
```

### checks.yml (reusable)
Steps in order:
1. `actions/checkout@v4` — `fetch-depth: 0` (gitleaks needs full history)
2. `gitleaks/gitleaks-action@v2` — secret scan
3. `oven-sh/setup-bun@v2` — install bun
4. `bun install --frozen-lockfile` (working-directory: web)
5. `bun run typecheck`
6. `bun run lint` (Biome)
7. `bunx knip` — dead code
8. `bun run test`
9. `bun test tests/ --coverage --coverage-reporter=lcov` (output: `coverage/lcov.info`)
10. osv-scanner — dep audit, `if: always()` (see osv-scanner note below)
11. `codecov/codecov-action@v6` — coverage upload, `files: web/coverage/lcov.info`, `fail_ci_if_error: false`

**Coverage upload pitfall:** pass `files: web/coverage/lcov.info` explicitly to the
codecov action. Without it the action searches the repo root and may upload nothing.
Bun generates lcov only with `--coverage-reporter=lcov` — default output is text-only.
The `coverage/` dir is created at `working-directory` level, so the path in the action
must be relative to the repo root (e.g. `web/coverage/lcov.info`).

### codeql.yml
```yaml
- uses: github/codeql-action/init@v3
  with:
    languages: javascript-typescript
    queries: security-extended
- uses: github/codeql-action/analyze@v3
  with:
    category: "/language:javascript-typescript"
```
Schedule: weekly Monday 06:00 + push/PR to main.

### scorecard.yml
Same as Python version — publish_results: true, results as SARIF artifact.

### dependabot.yml
Two ecosystems:
```yaml
- package-ecosystem: "github-actions"
  directory: "/"
- package-ecosystem: "npm"
  directory: "/web"   # ← point to the workspace subdir, not root
```
Both: weekly Monday 06:00, Europe/Copenhagen, grouped PRs.

---

## Pre-commit hooks

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks

  - repo: local
    hooks:
      - id: biome
        name: biome
        entry: bash -c 'cd web && bun run lint'
        language: system
        types_or: [ts, tsx]
        pass_filenames: false

      - id: typecheck
        name: typecheck
        entry: bash -c 'cd web && bun run typecheck'
        language: system
        types_or: [ts, tsx]
        pass_filenames: false

      - id: knip
        name: knip
        entry: bash -c 'cd web && bunx knip'
        language: system
        types_or: [ts, tsx]
        pass_filenames: false
```

Install: `pre-commit install` in the repo root.

---

## osv-scanner — dep vulnerability audit

**Do NOT use `google/osv-scanner-action@v2` as a step action.** It does not
publish a floating `v2` tag — only point releases like `v2.3.8`. It is also a
reusable *workflow*, not a composite action, so `uses:` in a step context fails
with "unable to find version `v2`".

**Correct pattern — CLI download in a run step:**
```yaml
- name: Dependency audit (osv-scanner)
  if: always()
  run: |
    curl -fsSL https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 \
      -o /usr/local/bin/osv-scanner
    chmod +x /usr/local/bin/osv-scanner
    osv-scanner --lockfile=web/bun.lock || true
```

The `|| true` keeps CI green when vulnerabilities are found — osv-scanner exits
non-zero on any finding. Remove `|| true` to make the step fail-hard.

`bun.lock` is the lockfile name for Bun workspaces. Pass the path relative to
the repo root when `working-directory` is not set on the step.

---



### Schema version drift
Biome pins its schema version in `biome.json`. After `bun update`, the installed
CLI version and the schema version in the file may differ, causing:

```
The configuration schema version does not match the CLI version 2.4.15
Expected: 2.4.15 / Found: 2.4.12
```

Fix: `bunx biome migrate --write` — updates the schema URL in place.

Run this any time after a Biome version bump.

### Auto-fix vs unsafe fix
`bunx biome check --write` applies only safe fixes (formatting, import ordering).
Some lint rules (unused parameters, dead imports after unsafe transforms) require:

```bash
bunx biome check --write --unsafe .
```

Safe to run — "unsafe" refers to code semantics (e.g. removing a parameter),
not filesystem risk. Review the diff before committing.

### Unused parameters in function signatures
Biome flags `index` in `.map((item, index) => {...})` if `index` is unused.
Convention: prefix with underscore → `_index`. This suppresses the warning
without removing the parameter slot.

Same applies to destructured function props:
```ts
// before
function QuestionCard({ ..., index, ... }: Props)
// after
function QuestionCard({ ..., index: _index, ... }: Props)
```

### Missing button type
Biome enforces `type="button"` on `<button>` elements. Without it, a button
inside a `<form>` defaults to `type="submit"` which causes silent form
submissions in React apps. Add `type="button"` to any non-submit button.

---

## GitHub repo metadata (About panel + topics)

Set description, homepage, and topics in one `gh` call:

```bash
gh repo edit owner/repo \
  --description "One-line description of the project" \
  --homepage "https://github.com/owner/repo" \
  --add-topic topic-a \
  --add-topic topic-b \
  --add-topic topic-c
```

Good topic choices for a Next.js + Bun TypeScript project:
`nextjs`, `typescript`, `bun`, `react`, `tailwindcss`, plus domain-specific terms.

Note: `gh repo edit` does NOT support `--topics` as a replace-all flag — use
repeated `--add-topic` calls. To remove a topic use `--remove-topic`.

---

## License (GPLv3)

Always fetch the canonical text — do not write it by hand:

```bash
curl -fsSL https://www.gnu.org/licenses/gpl-3.0.txt -o LICENSE
```

Then commit `LICENSE` to the repo root. GitHub detects it automatically and
shows it in the About panel.

---

## README badges

Full badge block for a TypeScript project with this CI toolchain:

```markdown
[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
[![CodeQL](https://github.com/OWNER/REPO/actions/workflows/codeql.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/OWNER/REPO/graph/badge.svg)](https://codecov.io/gh/OWNER/REPO)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/OWNER/REPO/badge)](https://securityscorecards.dev/viewer/?uri=github.com/OWNER/REPO)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Bun](https://img.shields.io/badge/runtime-Bun-fbf0df?logo=bun&logoColor=black)](https://bun.sh)
[![code style: Biome](https://img.shields.io/badge/code%20style-Biome-60a5fa.svg)](https://biomejs.dev)
[![Last commit](https://img.shields.io/github/last-commit/OWNER/REPO)](https://github.com/OWNER/REPO/commits/main)
```

Notes:
- Scorecard badge resolves from `api.securityscorecards.dev` — shows "unknown"
  for a few hours after the first successful scorecard.yml run, then resolves.
- Codecov badge URL uses `/graph/badge.svg` (not `/branch/main/graph/badge.svg`).
  The repo must be activated on codecov.io after first upload — token alone
  does not auto-register it. Visit codecov.io/gh/OWNER/REPO to activate.
- Badge order convention: CI → CodeQL → coverage → security → license → stack signals → freshness.
- Static stack badges (TypeScript, Bun, Biome) have no live data; use the exact
  color/logo values above for visual consistency.

---

## Post-setup checklist (GitHub settings)

After pushing workflows to main:
1. Repo Settings → Code security → Code scanning → Enable
   (required for CodeQL and Scorecard SARIF uploads to appear in Security tab)
2. Repo Settings → Secrets → Actions → Add `CODECOV_TOKEN`
   (optional — `fail_ci_if_error: false` means CI won't break without it)
3. Verify first CI run completes on the push that added the workflows
