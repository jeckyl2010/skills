---
name: github-repo-professionalise
description: >
  Analyse a GitHub repo and bring it up to a professional, maintainable standard:
  CI quality gates, security tooling, community health files, badges, Dependabot,
  OSSF Scorecard, CodeQL, coverage reporting. Covers TypeScript/Bun and Python/uv stacks.
  Based on jeckyl2010/risk-assistant (TypeScript) and jeckyl2010/mkdocs2confluence (Python).
triggers:
  - "professionalise this repo"
  - "set up the repo properly"
  - "add ci and quality gates"
  - "make this repo look professional"
  - "add security scanning"
  - "add badges"
  - "community health files"
---

# GitHub Repo Professionalisation

Two battle-tested reference implementations:
- Python/uv: `jeckyl2010/mkdocs2confluence`
- TypeScript/Bun: `jeckyl2010/risk-assistant`

---

## Phase 1 — Gather information (ask these before touching anything)

Ask the user these questions up front. Do not assume.

1. **License** — GPL v3, MIT, Apache 2.0, or other? (affects LICENSE file and badges)
2. **Maintainer GitHub handle** — for CODEOWNERS and advisory links
3. **Codecov** — do they want coverage reporting? If yes, is a CODECOV_TOKEN secret already set in the repo?
4. **Stack** — auto-detect from files, but confirm: Python/uv, TypeScript/Bun, TypeScript/npm, other?
5. **Package registry** — is this a published package (PyPI, npm)? Affects README badges (version, downloads).
6. **Timezone** — for Dependabot schedule (default: Europe/Copenhagen)
7. **Pre-commit** — already installed locally? (`pre-commit --version`)

---

## Phase 2 — Analyse the repo

```bash
# Detect stack
ls pyproject.toml uv.lock requirements*.txt   # Python/uv
ls package.json bun.lock web/package.json      # TypeScript/Bun
ls package.json package-lock.json              # TypeScript/npm

# Existing quality tooling
find .github -type f | sort
ls *.md LICENSE .pre-commit-config.yaml

# gh metadata
gh repo view --json name,description,homepageUrl,repositoryTopics
```

Identify gaps against the checklist below before writing anything.

---

## Phase 3 — Apply the checklist

Work top to bottom. Each item is independent unless noted.

### 3a. Repo metadata (gh CLI)
```bash
gh repo edit \
  --description "One-line description" \
  --homepage "https://..." \
  --add-topic "topic1" --add-topic "topic2"
```
Topics: use 6–8. Include language (python / typescript), framework, and domain terms.

---

### 3b. LICENSE
Download from gnu.org or choosealicense.com — do not generate from memory.
```bash
# GPL v3 example
curl -fsSL "https://www.gnu.org/licenses/gpl-3.0.txt" -o LICENSE
```

---

### 3c. .github/CODEOWNERS
```
* @<handle>
```

---

### 3d. .github/dependabot.yml

Always include two ecosystems: `github-actions` + the project's package manager.
Schedule: weekly, Monday 06:00, correct timezone. Group all deps into one PR per ecosystem.

**Python/uv:**
```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule: { interval: weekly, day: monday, time: "06:00", timezone: Europe/Copenhagen }
    labels: [dependencies, github-actions]
    groups:
      github-actions: { patterns: ["*"] }
    commit-message: { prefix: ci }
    open-pull-requests-limit: 10

  - package-ecosystem: pip
    directory: /
    schedule: { interval: weekly, day: monday, time: "06:00", timezone: Europe/Copenhagen }
    labels: [dependencies, python]
    versioning-strategy: increase-if-necessary
    groups:
      python-deps: { patterns: ["*"] }
    commit-message: { prefix: chore, include: scope }
    open-pull-requests-limit: 10
```

**TypeScript/Bun (npm ecosystem, point directory at package.json location):**
```yaml
  - package-ecosystem: npm
    directory: /web          # adjust to where package.json lives
    schedule: { interval: weekly, day: monday, time: "06:00", timezone: Europe/Copenhagen }
    labels: [dependencies, npm]
    groups:
      npm: { patterns: ["*"] }
    commit-message: { prefix: chore }
    open-pull-requests-limit: 10
```

---

### 3e. GitHub Actions workflows

#### ci.yml (caller — thin)
```yaml
name: CI
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
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

#### checks.yml (reusable — all quality gates)

Common steps (both stacks):
1. `actions/checkout@v6` with `fetch-depth: 0` (gitleaks needs full history)
2. `gitleaks/gitleaks-action@v2` secret scan
3. Install runtime + deps
4. Typecheck / mypy
5. Lint
6. Dead code detection
7. Tests
8. Coverage (with lcov/xml output for Codecov)
9. Dependency audit
10. Upload coverage to Codecov (`fail_ci_if_error: false`)

**Python-specific steps:**
```yaml
- uses: astral-sh/setup-uv@v7
- run: uv sync --all-extras --frozen
- run: uv run pytest -q                          # tests
- run: uv run ruff check src tests               # lint
- run: uv run mypy src                           # typecheck
- run: uv run vulture src --min-confidence 80    # dead code
- run: uv run bandit -r src -ll -q -f sarif -o bandit.sarif || true   # SAST → SARIF
- uses: github/codeql-action/upload-sarif@v4     # upload bandit SARIF
  with: { sarif_file: bandit.sarif, category: bandit }
- run: uv run radon cc src -a -n C --md >> "$GITHUB_STEP_SUMMARY"     # complexity
  continue-on-error: true
- run: uv run pip-audit                          # dep audit
- uses: codecov/codecov-action@v6
  with: { token: ${{ secrets.CODECOV_TOKEN }}, files: coverage.xml, fail_ci_if_error: false }
- uses: codecov/codecov-action@v6                # test results (separate)
  with: { token: ${{ secrets.CODECOV_TOKEN }}, files: junit.xml, report_type: test_results, fail_ci_if_error: false }
```

pytest must be configured to emit both coverage.xml and junit.xml:
```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=xml --junitxml=junit.xml -q"
```

**TypeScript/Bun-specific steps:**
```yaml
- uses: oven-sh/setup-bun@v2
  with: { bun-version: latest }
- run: bun install --frozen-lockfile
  working-directory: web
- run: bun run typecheck
  working-directory: web
- run: bun run lint                              # biome
  working-directory: web
- run: bunx knip
  working-directory: web
- run: bun run test
  working-directory: web
- run: bun test tests/ --coverage --coverage-reporter=lcov
  working-directory: web
- run: |                                         # dep audit — no floating v2 tag on osv-scanner-action
    curl -fsSL https://github.com/google/osv-scanner/releases/latest/download/osv-scanner_linux_amd64 \
      -o /usr/local/bin/osv-scanner
    chmod +x /usr/local/bin/osv-scanner
    osv-scanner --lockfile=web/bun.lock || true
  if: always()
- uses: codecov/codecov-action@v6
  with: { token: ${{ secrets.CODECOV_TOKEN }}, files: web/coverage/lcov.info, fail_ci_if_error: false }
```

**PITFALL — osv-scanner-action:** `google/osv-scanner-action` has no floating `@v2` tag — only point releases like `@v2.3.8`. It is also a reusable workflow, not a composite action, so it cannot be used as a step. Always use the direct CLI download approach shown above.

**PITFALL — Codecov token in reusable workflow:** `secrets: inherit` on the `ci.yml` caller passes repo secrets through. The reusable `checks.yml` must declare `CODECOV_TOKEN` under `on.workflow_call.secrets`. Verify `INPUT_CODECOV_TOKEN:` is not blank in the CI log; if it is, check secret name matches exactly.

**PITFALL — lcov not generated by default in Bun:** `bun test --coverage` prints a table to stdout but does not write `lcov.info` unless `--coverage-reporter=lcov` is also passed. The file lands at `coverage/lcov.info` relative to working-directory.

#### codeql.yml
```yaml
name: CodeQL
on:
  push: { branches: [main] }
  pull_request: { branches: [main] }
  schedule: [{ cron: "0 6 * * 1" }]
permissions: {}
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions: { security-events: write, actions: read, contents: read }
    steps:
      - uses: actions/checkout@v6
      - uses: github/codeql-action/init@v4
        with:
          languages: python          # or: javascript-typescript
          queries: security-extended
      - uses: github/codeql-action/analyze@v4
        with:
          category: "/language:python"   # or: /language:javascript-typescript
```

#### scorecard.yml
```yaml
name: Scorecard
on:
  push: { branches: [main] }
  schedule: [{ cron: "0 6 * * 1" }]
  workflow_dispatch:
permissions: {}
jobs:
  analysis:
    runs-on: ubuntu-latest
    permissions: { security-events: write, id-token: write, contents: read, actions: read }
    steps:
      - uses: actions/checkout@v6
        with: { persist-credentials: false }
      - uses: ossf/scorecard-action@v2.4.3
        with: { results_file: results.sarif, results_format: sarif, publish_results: true }
      - uses: actions/upload-artifact@v7
        with: { name: SARIF file, path: results.sarif, retention-days: 5 }
      - uses: github/codeql-action/upload-sarif@v4
        with: { sarif_file: results.sarif }
```

---

### 3f. Pre-commit hooks (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.27.2
    hooks:
      - id: gitleaks
```

**Python additions:**
```yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.12
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy src
        language: system
        pass_filenames: false
```

**TypeScript/Bun additions:**
```yaml
  - repo: local
    hooks:
      - id: biome
        name: biome
        entry: bunx biome check --write .
        language: system
        pass_filenames: false
      - id: typecheck
        name: typecheck
        entry: bash -c "cd web && bun run typecheck"
        language: system
        pass_filenames: false
      - id: knip
        name: knip
        entry: bash -c "cd web && bunx knip"
        language: system
        pass_filenames: false
```

**PITFALL — biome schema version mismatch:** After updating biome, run `bunx biome migrate --write` to update the schema URL in `biome.json`. Otherwise pre-commit fails with a schema version error.

---

### 3g. Community health files

| File | Required | Notes |
|------|----------|-------|
| `README.md` | ✅ | Badges, architecture, quick start, dev setup |
| `LICENSE` | ✅ | Full license text, downloaded not generated |
| `SECURITY.md` | ✅ | Private advisory link, real risk surface for this project |
| `CONTRIBUTING.md` | ✅ | Dev setup, test expectations, PR scope |
| `CHANGELOG.md` | ✅ | Keep a Changelog format, seed Unreleased section |
| `.github/ISSUE_TEMPLATE/bug_report.md` | ✅ | Environment, steps, output block |
| `.github/ISSUE_TEMPLATE/feature_request.md` | ✅ | Problem / solution / alternatives |
| `.github/PULL_REQUEST_TEMPLATE.md` | ✅ | Checklist anchored to actual project standards |
| `CODE_OF_CONDUCT.md` | ❌ | Skip for single-maintainer projects — performative overhead |
| `SUPPORT.md` | ❌ | Skip unless there is a community to support |

SECURITY.md must reference the actual risk surface — not generic boilerplate.
Link format: `https://github.com/<owner>/<repo>/security/advisories/new`

---

### 3h. README badges

Order: CI status, CodeQL, codecov, Scorecard, License, stack/language, tooling, last-commit.

**Always applicable:**
```markdown
[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](...)
[![CodeQL](https://github.com/<owner>/<repo>/actions/workflows/codeql.yml/badge.svg)](...)
[![codecov](https://codecov.io/gh/<owner>/<repo>/graph/badge.svg)](https://codecov.io/gh/<owner>/<repo>)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/<owner>/<repo>/badge)](...)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/<owner>/<repo>)](...)
```

**Python stack:**
```markdown
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type--checked-mypy-blue.svg)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
```

**If published to PyPI:**
```markdown
[![PyPI](https://img.shields.io/pypi/v/<package>)](https://pypi.org/project/<package>/)
[![Downloads](https://img.shields.io/pypi/dm/<package>)](https://pypi.org/project/<package>/)
[![Latest Release](https://img.shields.io/github/v/release/<owner>/<repo>)](...)
```

**TypeScript/Bun stack:**
```markdown
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Bun](https://img.shields.io/badge/runtime-Bun-fbf0df?logo=bun&logoColor=black)](https://bun.sh)
[![code style: Biome](https://img.shields.io/badge/code%20style-Biome-60a5fa.svg)](https://biomejs.dev)
```

**PITFALL — Scorecard badge delay:** Shows "unknown" for a few hours after first push. securityscorecards.dev needs to index the first successful run. No action needed — it resolves automatically.

**PITFALL — Codecov badge shows "unknown":** The repo must be activated on codecov.io after the first upload. Go to `codecov.io/gh/<owner>/<repo>` and activate. CODECOV_TOKEN secret must be set in the repo (`gh secret set CODECOV_TOKEN`).

---

### 3i. Knip config (TypeScript only)

```json
{
  "entry": ["src/index.ts", "src/components/ui/**"],
  "ignoreDependencies": ["tailwindcss"]
}
```

**PITFALL:** `ignore` globs do not suppress export warnings. UI barrel export files (shadcn, etc.) must be listed under `entry` so knip treats them as public API. Otherwise every exported but internally-uncalled component is flagged as dead code.

---

### 3j. README.md — structure and docs/ strategy

The README should be navigable in 60 seconds, not a complete manual.
Aim for under 150 lines. Everything verbose lives in `docs/`.

**Required structure (in order):**

```
1. Title + one-line tagline
2. Badges (see 3h)
3. 2–3 sentence description
   - What it is
   - What problem it solves
   - What it is NOT (if there is a common misconception)
4. Quick start — minimal path to running, nothing else
5. Docs table — links into docs/
6. Architecture — brief summary, diagram if one exists
7. Development — commands only, no prose
```

**docs/ folder — what goes there:**

| File | Content |
|------|---------|
| `docs/setup.md` | Full install, manual setup steps, prerequisites detail |
| `docs/commands.md` | Full CLI/API reference, all flags and options |
| `docs/features.md` | Capability matrix, known limitations |
| `docs/architecture.md` | Deep-dive on components, data flow, design decisions |
| `docs/deployment.md` | Container setup, infrastructure, environment config |
| `docs/development.md` | Test strategy, coverage expectations, model/schema changes |

Not every project needs all of these — create the ones that have real content.
Stub files are noise. If it fits in three lines, it stays in the README.

**The docs table in README:**

```markdown
## Documentation

| | |
|---|---|
| [docs/setup.md](docs/setup.md) | Full install and manual setup |
| [docs/commands.md](docs/commands.md) | CLI reference |
| [docs/architecture.md](docs/architecture.md) | Component overview and data flow |
```

**Assessment checklist for an existing README:**

- Is there a description that says what it is AND what it is not?
- Is the quick start actually minimal, or does it have manual-setup detail inline?
- Is there a deployment/infrastructure section that should be in docs/?
- Is there an architecture section longer than ~10 lines? Move the detail.
- Are there numbered manual steps inline that belong in docs/setup.md?
- Does CONTRIBUTING.md duplicate dev-setup content from the README? Pick one.

**Refactor approach:** move content out of README into docs/ files, replace with
a one-line summary + link. Commit README and docs/ changes together.

---

## Phase 4 — Verify

```bash
# Pre-commit hooks pass
pre-commit run --all-files

# CI green
gh run list --repo <owner>/<repo> --limit 5

# Codecov receiving uploads
# Check: codecov.io/gh/<owner>/<repo>

# Scorecard indexed
# Check: securityscorecards.dev/viewer/?uri=github.com/<owner>/<repo>
```

---

## Commit convention

One commit per logical group:
- `ci: add quality gates (biome, typecheck, knip, gitleaks, osv-scanner, CodeQL, Scorecard)`
- `docs: add GPLv3 license, update README with badges`
- `docs: add SECURITY, CONTRIBUTING, CHANGELOG, issue templates, PR template`
- `chore: set repo metadata and topics`
