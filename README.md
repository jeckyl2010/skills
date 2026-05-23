# skills

A personal library of reusable AI skills by Anders Hybertz — owner of
COM<tech> (comtechconsulting.dk), software architecture consultant, Copenhagen.

Three decades of industry experience distilled into composable, tool-agnostic
skill files. Each skill encodes judgment, not just instructions.

[![CI](https://github.com/jeckyl2010/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/jeckyl2010/skills/actions/workflows/ci.yml)
[![CodeQL](https://github.com/jeckyl2010/skills/actions/workflows/codeql.yml/badge.svg)](https://github.com/jeckyl2010/skills/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/jeckyl2010/skills/badge)](https://securityscorecards.dev/viewer/?uri=github.com/jeckyl2010/skills)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/jeckyl2010/skills)](https://github.com/jeckyl2010/skills/commits/main)

## What is a skill

A skill is a focused, reusable prompt unit — one clear purpose, portable across
AI tools. Think of them as functions: single-responsibility, composable,
parameterizable.

Each skill is a markdown file with YAML frontmatter (metadata) and a structured
body (context, goals, checklists, pitfalls, output guidance). Supporting files
live in subdirectories alongside the SKILL.md.

## Structure

```
skills/
  engineering/          — architecture, development, code review, static sites
  design/               — UI/UX judgment, accessibility, visual hierarchy
  tooling/              — specific tool workflows (Astro, PDF extraction, etc.)
  schemas/              — JSON Schema for skill frontmatter validation
  scripts/              — repo-level tooling (validate, index builder)
```

Each skill directory follows this convention:

```
skill-name/
  SKILL.md              — the skill itself (frontmatter + body)
  examples/             — input/output pairs showing the skill in action
  references/           — supporting reference material
  templates/            — copy-paste code/config templates
  scripts/              — executable scripts the skill references
```

Only the directories that are actually needed are present — no empty scaffolding.

## Frontmatter schema

```yaml
---
name: skill-name              # required, kebab-case
description: one-liner        # required
version: "1.0.0"              # required, quoted SemVer
tags: [tag1, tag2]            # optional, for discovery
tool_agnostic: true           # optional, signals broad portability
authors: [Anders Hybertz]     # required
---
```

Validate against `schemas/skill_schema.json` using `scripts/validate.py`.

## Using these skills

### With Hermes Agent

Drop the skill directory into `~/.hermes/skills/<category>/`. Hermes picks it
up automatically on next invocation.

### With other tools

Copy the SKILL.md body (below the frontmatter) into your tool's system prompt
or instruction file. The content is deliberately tool-agnostic.

### Validate and index

```bash
python3 scripts/validate.py       # check all skills against schema
python3 scripts/index_builder.py  # regenerate index.yaml
```

## Categories

| Category | Skills |
|---|---|
| engineering | senior-software-architecture, senior-software-development, codebase-review-and-design-assessment, astro-static-sites, static-site-seo-and-og |
| design | senior-ui-ux |
| tooling | extract-pdf-text-on-macos-with-pypdf |

## License

GPL v3 — see [LICENSE](LICENSE).
