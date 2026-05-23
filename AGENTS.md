# AGENTS.md — skills repo conventions

Rules for any AI agent working in this repository. Follow these on every task
without being asked.

---

## Skill frontmatter — owned skills only

Every skill we write and own must have this exact frontmatter. No exceptions.

```yaml
---
name: skill-name              # kebab-case, matches directory name exactly
description: one-liner        # required, max 150 characters
version: "1.0.0"              # quoted SemVer
tags: [tag1, tag2]            # array
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []                 # optional: ['claude-sonnet-4.6 (YYYY-MM-DD)']
# deprecated_since: "x.y.z"  # optional: set when deprecating; triggers validator warning
# superseded_by: skill-name  # optional: set alongside deprecated_since
---
```

Rules:
- `triggers` is not a valid field — never use it
- Hub-sourced or third-party skills (missing `authors: [Anders Hybertz]`) are not ours to modify
- Description must be under 150 characters — validate before committing
- When deprecating a skill: set `deprecated_since` + `superseded_by`, update CHANGELOG, do not delete until superseding skill is stable

---

## Every skill change (add, update, delete)

### Adding or updating a skill

1. Ensure frontmatter passes the rules above
2. Bump `version` in frontmatter — patch for wording/clarity fixes, minor for new content or behaviour, major for breaking output format or interface changes
3. Update `CHANGELOG.md` — add the change under `[Unreleased]`, then promote `[Unreleased]` to a versioned entry matching the new version
4. Run: `python3 ~/Repos/hermes-config/sync-skills.py push "<message>"` — this rebuilds `index.yaml`, validates, commits, and pushes in one step. Do not run `git push` manually for skill changes.

### Deleting a skill

All of the following must be updated to reflect the deletion — no orphaned references:

1. Remove the skill directory
2. `index.yaml` — rebuilt automatically by sync-skills.py, but verify the entry is gone
3. `CHANGELOG.md` — add a `Removed` entry under `[Unreleased]`
4. `README.md` — remove from the Categories table
5. Any other skill that cross-references the deleted skill by name

Then run `sync-skills.py push` as above.

---

## CHANGELOG format

Format: `## [version] — dd.MM.yyyy` (day-first, 24h — e.g. `23.05.2026`)

- Keep an empty `## [Unreleased]` section at the top at all times
- When releasing, promote `[Unreleased]` entries to a new versioned section — do not leave changes stranded under `[Unreleased]` after the version is known
- Use standard Keep a Changelog section headers: `Added`, `Changed`, `Fixed`, `Removed`

---

## Commit convention

One commit per logical group:

- `feat: add <skill-name> skill`
- `improve: <skill-name> — <what changed>`
- `fix: <skill-name> — <what was wrong>`
- `docs: update CHANGELOG, README, index for <skill-name> removal`
- `ci: <workflow changes>`
- `chore: <repo maintenance>`
