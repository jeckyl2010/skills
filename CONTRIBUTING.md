# Contributing

Contributions are welcome. A good skill is focused, portable, and honest.

## What makes a good skill

- Single responsibility — one skill, one purpose
- Tool-agnostic — no provider names, API keys, or tool-specific syntax in the body
- Evidence-based — checklists and pitfalls grounded in real experience, not theory
- Honest — includes pitfalls and trade-offs, not just happy paths
- Parameterizable — uses `{{placeholders}}` for variable content where relevant

## Adding a skill

Start from the template — it covers both new skills and adopted ones:

```
cp templates/SKILL.template.md engineering/my-skill-name/SKILL.md
```

1. Create a directory under the appropriate category: `engineering/`, `design/`, or `tooling/`
2. Name it kebab-case: `my-skill-name/` — must match the `name` field in frontmatter exactly
3. Fill in `SKILL.md` from the template (remove all comment lines before committing)
4. Add `references/`, `templates/`, `scripts/`, or `assets/` subdirs only if needed
5. Run `python3 scripts/validate.py` — all skills must pass
6. Run `python3 scripts/index_builder.py` to update `index.yaml`
7. Open a PR with a clear description of what the skill does and why it belongs here

## Adopting a skill from the internet

The template's adoption checklist (bottom of `templates/SKILL.template.md`) covers the full
process. Short version: strip tool-specific frontmatter fields, add schema-compliant fields,
preserve attribution in an HTML comment, validate.

## Frontmatter requirements

```yaml
---
name: skill-name          # required, must match directory name
description: one-liner    # required, max 150 chars (validate.py enforces this)
version: "1.0.0"          # required, semver
tags: [tag1, tag2]        # optional
tool_agnostic: true       # optional
authors: [name]           # optional, use for third-party attribution
---
```

See `schemas/skill_schema.json` for the full schema and `templates/SKILL.template.md` for an
annotated example.

## Updating a skill

Bump `version` in the frontmatter when making meaningful changes.
Add a note at the bottom of the SKILL.md body under `## Changelog` if the
change affects how the skill should be used.

## Proposing a new category

Open an issue first. Categories should represent genuinely distinct domains,
not just organizational preference.
