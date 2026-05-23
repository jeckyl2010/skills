# Contributing

Contributions are welcome. A good skill is focused, portable, and honest.

## What makes a good skill

- Single responsibility — one skill, one purpose
- Tool-agnostic — no provider names, API keys, or tool-specific syntax in the body
- Evidence-based — checklists and pitfalls grounded in real experience, not theory
- Honest — includes pitfalls and trade-offs, not just happy paths
- Parameterizable — uses `{{placeholders}}` for variable content where relevant

## Adding a skill

1. Create a directory under the appropriate category: `engineering/`, `design/`, or `tooling/`
2. Name it kebab-case: `my-skill-name/`
3. Create `SKILL.md` with valid frontmatter (see schema below)
4. Add `examples/`, `references/`, `templates/`, or `scripts/` only if needed
5. Run `python3 scripts/validate.py` — all skills must pass
6. Run `python3 scripts/index_builder.py` to update `index.yaml`
7. Open a PR with a clear description of what the skill does and why it belongs here

## Frontmatter requirements

```yaml
---
name: skill-name          # required, must match directory name
description: one-liner    # required, max 120 chars
version: "1.0"            # required, semver
tags: [tag1, tag2]        # optional
tool_agnostic: true       # optional
---
```

See `schemas/skill_schema.json` for the full schema.

## Updating a skill

Bump `version` in the frontmatter when making meaningful changes.
Add a note at the bottom of the SKILL.md body under `## Changelog` if the
change affects how the skill should be used.

## Proposing a new category

Open an issue first. Categories should represent genuinely distinct domains,
not just organizational preference.
