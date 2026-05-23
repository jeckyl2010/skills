---
name: github-repo-professionalise
description: Analyse a GitHub repo and bring it up to a professional, maintainable standard — CI quality gates, security tooling, community health files, badges, Dependabot, OSSF Scorecard, CodeQL, coverage reporting. Covers TypeScript/Bun and Python/uv stacks.
version: "1.0.0"
tags: [github, ci, quality-gates, security, badges, dependabot, codeql, scorecard, codecov, pre-commit, community-health, typescript, python, bun, uv]
tool_agnostic: true
authors: [Anders Hybertz]
---

# GitHub Repo Professionalisation

Two battle-tested reference implementations:
- Python/uv: `jeckyl2010/mkdocs2confluence`
- TypeScript/Bun: `jeckyl2010/risk-assistant`

Template files are in `templates/` — load with `skill_view(file_path=...)`.

---

## Phase 1 — Gather information (ask before touching anything)

1. **License** — GPL v3, MIT, Apache 2.0, or other?
2. **Maintainer GitHub handle** — for CODEOWNERS and advisory links
3. **Codecov** — do they want coverage reporting? Is `CODECOV_TOKEN` already set?
4. **Stack** — auto-detect from files, but confirm: Python/uv, TypeScript/Bun, TypeScript/npm, other?
5. **Package registry** — PyPI, npm, or not published? Affects README badges.
6. **Timezone** — for Dependabot schedule (default: Europe/Copenhagen)
7. **Pre-commit** — installed locally? (`pre-commit --version`)

---

## Phase 2 — Analyse the repo

```bash
# Detect stack
ls pyproject.toml uv.lock requirements*.txt     # Python/uv
ls package.json bun.lock web/package.json        # TypeScript/Bun

# What already exists
find .github -type f | sort
ls *.md LICENSE .pre-commit-config.yaml

# Repo metadata
gh repo view --json name,description,homepageUrl,repositoryTopics
```

Identify gaps against the checklist before writing anything.

---

## Phase 3 — Apply the checklist

### 3a. Repo metadata

```bash
gh repo edit \
  --description "One-line description" \
  --homepage "https://..." \
  --add-topic "topic1" --add-topic "topic2"
```

Use 6–8 topics: language, framework, domain terms.

---

### 3b. LICENSE

Download — do not generate from memory.

```bash
curl -fsSL "https://www.gnu.org/licenses/gpl-3.0.txt" -o LICENSE
```

---

### 3c. .github/CODEOWNERS

```
* @<handle>
```

---

### 3d. Dependabot

Load the right template with `skill_view`:
- Python: `templates/dependabot-python.yml`
- TypeScript/Bun: `templates/dependabot-typescript-bun.yml`

Save as `.github/dependabot.yml`. Adjust `timezone` and `directory` as needed.

---

### 3e. GitHub Actions workflows

**ci.yml** (caller — same for both stacks):
Load `templates/ci.yml`

**checks.yml** (reusable — all quality gates):
- Python: `templates/checks-python.yml`
- TypeScript/Bun: `templates/checks-typescript-bun.yml`

**codeql.yml:**
- Python: `templates/codeql-python.yml`
- TypeScript/Bun: `templates/codeql-typescript.yml`

**scorecard.yml** (same for both stacks):
Load `templates/scorecard.yml`

Save all to `.github/workflows/`. Adjust `working-directory` in checks if `package.json` is not at `web/`.

Python: ensure `pyproject.toml` has pytest configured to emit both `coverage.xml` and `junit.xml`:
```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=xml --junitxml=junit.xml -q"
```

---

### 3f. Pre-commit hooks

- Python: `templates/pre-commit-python.yaml`
- TypeScript/Bun: `templates/pre-commit-typescript-bun.yaml`

Save as `.pre-commit-config.yaml`. Then install:

```bash
pip install pre-commit   # or: brew install pre-commit
pre-commit install
pre-commit run --all-files   # verify clean before first commit
```

---

### 3g. Community health files

| File | Required | Notes |
|------|----------|-------|
| `README.md` | ✅ | See section 3j |
| `LICENSE` | ✅ | Full text, downloaded not generated |
| `SECURITY.md` | ✅ | Private advisory link, real risk surface — not generic boilerplate |
| `CONTRIBUTING.md` | ✅ | Dev setup, test expectations, PR scope |
| `CHANGELOG.md` | ✅ | Keep a Changelog format, seed Unreleased section |
| `.github/ISSUE_TEMPLATE/bug_report.md` | ✅ | Environment, steps, output block |
| `.github/ISSUE_TEMPLATE/feature_request.md` | ✅ | Problem / solution / alternatives |
| `.github/PULL_REQUEST_TEMPLATE.md` | ✅ | Checklist anchored to actual project standards |
| `CODE_OF_CONDUCT.md` | ❌ | Skip for single-maintainer projects — performative overhead |
| `SUPPORT.md` | ❌ | Skip unless there is a community to support |

SECURITY.md advisory link format: `https://github.com/<owner>/<repo>/security/advisories/new`

---

### 3h. README badges

Order: CI, CodeQL, codecov, Scorecard, License, stack, tooling, last-commit.

**Always applicable:**
```markdown
[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](...)
[![CodeQL](https://github.com/<owner>/<repo>/actions/workflows/codeql.yml/badge.svg)](...)
[![codecov](https://codecov.io/gh/<owner>/<repo>/graph/badge.svg)](https://codecov.io/gh/<owner>/<repo>)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/<owner>/<repo>/badge)](...)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/<owner>/<repo>)](...)
```

**Python stack additions:**
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

**TypeScript/Bun stack additions:**
```markdown
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Bun](https://img.shields.io/badge/runtime-Bun-fbf0df?logo=bun&logoColor=black)](https://bun.sh)
[![code style: Biome](https://img.shields.io/badge/code%20style-Biome-60a5fa.svg)](https://biomejs.dev)
```

---

### 3i. Knip config (TypeScript only)

```json
{
  "entry": ["src/index.ts", "src/components/ui/**"],
  "ignoreDependencies": ["tailwindcss"]
}
```

UI barrel export files (shadcn etc.) must be in `entry`, not `ignore` — otherwise every exported-but-internally-uncalled component is flagged as dead code.

---

### 3j. README structure and docs/ strategy

The README should be navigable in 60 seconds. Aim for under 150 lines.
Everything verbose belongs in `docs/`.

**Required structure (in order):**
1. Title + one-line tagline
2. Badges
3. 2–3 sentence description — what it is, what problem it solves, what it is NOT
4. Quick start — minimal path to running, nothing else
5. Docs table — links into docs/
6. Architecture — brief summary only
7. Development — commands only, no prose

**docs/ folder:**

| File | Content |
|------|---------|
| `docs/setup.md` | Full install, manual steps, prerequisites detail |
| `docs/commands.md` | Full CLI/API reference, all flags and options |
| `docs/features.md` | Capability matrix, known limitations |
| `docs/architecture.md` | Deep-dive: components, data flow, design decisions |
| `docs/deployment.md` | Container setup, infrastructure, environment config |
| `docs/development.md` | Test strategy, coverage expectations, model/schema changes |

Create only the files that have real content. Stub files are noise.

**Assessment checklist for an existing README:**
- Does it describe what the project is NOT (where that matters)?
- Is quick start truly minimal, or does it have manual-setup detail inline?
- Is there a deployment section that belongs in `docs/deployment.md`?
- Is there an architecture section longer than ~10 lines? Move the detail.
- Are numbered manual steps inline that belong in `docs/setup.md`?
- Does CONTRIBUTING.md duplicate README dev-setup content? Pick one.

Refactor: move content into docs/ files, replace with one-line summary + link. Commit README and docs/ together.

---

## Phase 4 — Verify

```bash
pre-commit run --all-files

gh run list --repo <owner>/<repo> --limit 5
# Codecov: codecov.io/gh/<owner>/<repo>
# Scorecard: securityscorecards.dev/viewer/?uri=github.com/<owner>/<repo>
```

---

## Commit convention

One commit per logical group:
- `ci: add quality gates (biome, typecheck, knip, gitleaks, osv-scanner, CodeQL, Scorecard)`
- `docs: add GPLv3 license, update README with badges`
- `docs: add SECURITY, CONTRIBUTING, CHANGELOG, issue templates, PR template`
- `chore: set repo metadata and topics`

---

## Pitfalls

**osv-scanner-action has no floating @v2 tag.** Only point releases (`@v2.3.8`). Also a reusable workflow, not a composite action — cannot be used as a step. Always use the CLI download in `templates/checks-typescript-bun.yml`.

**Codecov empty token in reusable workflow.** `secrets: inherit` in ci.yml passes repo secrets through, but `checks.yml` must declare `CODECOV_TOKEN` under `on.workflow_call.secrets`. If `INPUT_CODECOV_TOKEN:` is blank in CI logs, check the declaration and secret name match exactly.

**Codecov badge shows "unknown".** Repo must be activated on codecov.io after the first upload. Go to `codecov.io/gh/<owner>/<repo>` and activate. Takes 30 seconds.

**Scorecard badge delay.** Shows "unknown" for a few hours after first push. securityscorecards.dev needs to index the first run. Resolves automatically.

**lcov not generated by default in Bun.** `bun test --coverage` prints a table but does not write a file. Pass `--coverage-reporter=lcov`. Output: `coverage/lcov.info` relative to working-directory.

**Biome schema version mismatch in pre-commit.** After updating biome, run `bunx biome migrate --write`. Otherwise pre-commit fails with a schema version error.

**knip flags UI barrel exports.** Add UI barrel files (shadcn etc.) to `entry`, not `ignore`. See section 3i.
