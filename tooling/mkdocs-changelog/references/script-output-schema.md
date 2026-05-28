# changelog_data.py — Output Schema

Script lives at `.mk2conf/scripts/changelog_data.py` after `mk2conf install-skill`.
Stdlib only. Run from project root.

## Invocation

```
python .mk2conf/scripts/changelog_data.py [--docs-dir docs] [--since YYYY-MM-DD]
```

## JSON output shape

```json
{
  "date": "2026-05-27",
  "mode": "changelog_commit | since_date",
  "since": "2026-05-01 | null",
  "baseline_commit": "<sha>",
  "commits": [
    { "sha": "abc123", "subject": "feat: ...", "author": "Anders Hybertz", "date": "2026-05-27" }
  ],
  "contributors": ["Anders Hybertz"],
  "changes": {
    "added":    [{ "path": "docs/configuration/index.md", "title": "Configuration reference" }],
    "modified": [{ "path": "docs/getting-started.md",    "title": "Getting started" }],
    "deleted":  [{ "path": "docs/old-page.md",           "title": null }]
  },
  "docs_dir": "docs"
}
```

## Field notes

- `mode`: `changelog_commit` = baseline is last commit touching CHANGELOG.md (or root commit).
  `since_date` = baseline is last commit before `--since` date. Drives different SKILL.md rules.
- `title`: H1 heading read from the file on disk. `null` if file is non-.md, unreadable, or has no H1.
  Use as link text where natural; fall back to a short descriptive phrase for generic titles.
- `contributors`: unique author names, first-seen order. Plain text only — no GitHub URLs.
- `changes.deleted`: paths only, no title lookup (file is gone from disk). Never link deleted pages.
- Paths in `changes` are relative to project root (e.g. `docs/config/index.md`).
  CHANGELOG.md lives at `<docs_dir>/CHANGELOG.md`, so relative links drop the `docs/` prefix.

## Baseline resolution logic

1. `--since DATE` supplied → last commit strictly before DATE
2. No `--since` + CHANGELOG.md exists → last commit that touched CHANGELOG.md
3. No `--since` + no CHANGELOG.md → root commit (full repo history)
