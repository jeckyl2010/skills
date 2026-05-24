---
name: material-for-mkdocs
description: Author and maintain Material for MkDocs sites — .pages nav, assets, frontmatter, Mermaid, admonitions, and Diátaxis structure.
version: "1.0.0"
tags: [mkdocs, material, documentation, static-site, diátaxis]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Material for MkDocs

Use when creating, reviewing, or extending pages in a Material for MkDocs site. Covers the full authoring cycle: frontmatter, content structure, .pages nav registration, and assets.

## Project conventions (manufacturing-target-architecture)

- Framework: Material for MkDocs. Config at `mkdocs.yml`.
- Serve: `mkdocs serve` (activate `venv` first).
- Build: `mkdocs build`.
- Publish: GitHub Actions `.github/workflows/deploy.yml`.
- Custom hooks: `hooks.py` — do not remove or rename.
- Structure principle: Diátaxis (tutorials / how-to / explanation / reference).
- Mermaid diagrams render natively — use fenced ` ```mermaid ``` ` blocks.
- Global legend/glossary snippet: `--8<-- "includes/legend-glossary.md"` — include near top of every page, before the first heading.
- Run `/humanizer` on any prose before it lands in `docs/`.

## Page authoring workflow

1. Check whether a draft already exists in the target folder before creating a new file.
2. Read two or three sibling pages to calibrate style, frontmatter tags, and admonition usage.
3. Write or update the page content.
4. Wire the page into `.pages` (see nav registration below).
5. If the page references an image, add it to the co-located `assets/` folder (see assets pattern).

## Frontmatter baseline

```yaml
---
title: <Short descriptive title>
description: <One sentence — what this page covers and why it matters.>
tags:
  - <primary-domain>
  - <secondary-tag>
  - ...
---
```

Tags follow lowercase-hyphenated convention. Common domain tags: `values`, `iam`, `jwt`, `api-gateway`, `authentication`, `security`, `microservices`, `isa-95`, `idmz`, `observability`, `keycloak`.

## Standard page structure (values pages)

```
--8<-- "includes/legend-glossary.md"

## Introduction
<2–3 paragraphs. What the pattern is, what problem it solves, what it is not.>

!!! note "Scope"
    <One sentence: what this page covers and what it explicitly excludes.>

!!! info "Related document"
    <Cross-link to the most relevant companion page.>

[optional: image — see assets pattern]

## High-level <flow/architecture/overview>
<Mermaid diagram>

---

## Core Values
### <Value 1>
### <Value 2>
...

---

## Trade-offs and Constraints
### <Trade-off 1>
...

---

## Architectural Guardrail
!!! success "Guardrail"
    <Single bold statement of the non-negotiable.>

---

## Summary
<2–3 sentences. Restate the why, the condition that makes it hold, and the risk if violated.>
```

## Admonition types in use

| Type | Use |
|---|---|
| `!!! note` | Scope statements, neutral clarifications |
| `!!! info` | Cross-links, supplementary context |
| `!!! success` | Guardrails, confirmed recommendations |
| `!!! warning` | Known risks, failure modes |
| `!!! danger` | Hard constraints, production anti-patterns |

## Mermaid diagram style

Use `classDef` blocks for consistent colour coding:

```mermaid
classDef actor    fill:#f5f5f5,stroke:#6b7280,color:#1f1f1f;
classDef identity fill:#e8f1fb,stroke:#4f81bd,color:#1f1f1f;
classDef gateway  fill:#fff2cc,stroke:#c9a227,color:#1f1f1f;
classDef service  fill:#eef7ea,stroke:#6aa84f,color:#1f1f1f;
classDef risk     fill:#fce8e6,stroke:#cc0000,color:#1f1f1f;
```

Keep diagrams to one level of abstraction per diagram. Split into multiple diagrams rather than adding a second conceptual layer.

## .pages nav registration

Every new page must be added to the `.pages` file in its folder. Format:

```yaml
nav:
    - <Human-readable title>: <filename.md>
    - <Human-readable title>: <filename.md>
```

Sequence by logical reading order — not alphabetical. Cross-referencing pages (e.g. Keycloak → JWT) should be adjacent in the nav.

Always add the new entry; never remove existing entries unless the file is deleted.

## Assets pattern

Images and other static assets go in a folder-local `assets/` directory:

```
docs/explanation/values/
  assets/
    jwt-api-gateway-auth.jpeg
  jwt-api-gateway-auth-values.md
  keycloak-values.md
```

Reference in Markdown with a relative path:

```markdown
![Alt text describing the image](assets/filename.ext)
```

Place the image between the scope/related-document admonitions and the first Mermaid diagram — it gives the reader the source reference before the abstracted architectural view.

Name image files to match the page slug (e.g. `jwt-api-gateway-auth.jpeg` for `jwt-api-gateway-auth-values.md`).

## Pitfalls

- Missing .pages entry: the page renders in the site but does not appear in the sidebar nav. Always update `.pages` as part of every new page task.
- Forgetting the legend-glossary snippet: sibling pages all include it — omitting it breaks glossary term tooltips on the new page.
- Absolute image paths: MkDocs resolves images relative to the page. Use `assets/filename.ext`, not `/docs/explanation/values/assets/filename.ext`.
- Editing `ai-context/architecture-context.md` directly: it is regenerated by Repomix. Treat as read-only.
- Committing `site/`, `venv/`, or `__pycache__/`: all are in .gitignore but easy to add accidentally via `git add .`.
