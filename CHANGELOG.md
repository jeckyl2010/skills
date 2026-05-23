# Changelog

All notable changes to this skill library.

Format: `## [version] — dd.MM.yyyy`

---

## [Unreleased]

---

## [1.2.0] — 23.05.2026

### Added
- `schemas/skill_schema.json`: `tested_on`, `deprecated_since`, `superseded_by` fields
- `scripts/validate.py`: deprecation warnings for skills with `deprecated_since` set
- `scripts/index_builder.py`: surfaces `tested_on`, `deprecated_since`, `superseded_by` in index
- `.github/workflows/checks.yml`: `index-fresh` job — fails CI if `index.yaml` is out of sync
- `.github/PULL_REQUEST_TEMPLATE.md`: semver bump type + justification section; deprecation checklist item
- `templates/SKILL.template.md`: documented `tested_on`, `deprecated_since`, `superseded_by` fields
- `AGENTS.md`: updated frontmatter reference, semver bump guidance, deprecation workflow
- `README.md`: Discussions badge
- GitHub Discussions enabled on repo



### Added
- `AGENTS.md`: repo-specific conventions for AI agents — skill format rules, change workflow, CHANGELOG format, commit convention

### Changed
- `github-repo-professionalise`: Phase 1 questions now asked one at a time with multiple/single choice options where applicable; description shortened to pass 150 char schema limit

---

## [1.0.0] — 23.05.2026

Initial release.

Skills included:

**engineering/**
- senior-software-architecture 1.0
- senior-software-development 1.0
- codebase-review-and-design-assessment 1.0
- astro-static-sites 1.0
- static-site-seo-and-og 1.0

**design/**
- senior-ui-ux 1.0

**tooling/**
- extract-pdf-text-on-macos-with-pypdf 1.0
