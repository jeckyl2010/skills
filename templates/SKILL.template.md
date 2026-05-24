---
# SKILL TEMPLATE
# Copy this file to your skill directory and fill in each field.
# Lines starting with # are comments — remove them before committing.
# Run: python3 scripts/validate.py to check before pushing.

name: my-skill-name
# Required. Kebab-case. Must exactly match the directory name.
# Pattern: ^[a-z0-9]+(-[a-z0-9]+)*$
# Example: code-reviewer-strict, grill-me, caveman

description: One sentence that says what this skill does and when to use it.
# Required. Max 150 characters (schema-enforced — validate.py will catch overruns).
# Tip: "Does X when Y" beats "A skill that does X" — lead with the action.
# Count: run `echo -n "your description" | wc -c` to check before committing.

version: "1.0.0"
# Required. Semver. Start at 1.0.0 for new skills, bump meaningfully on changes.

tags: [tag1, tag2]
# Optional but recommended. Used for discovery and filtering.
# Common tags: code-review, git, testing, communication, documentation,
#              planning, refactoring, architecture, automation, debugging

specificity: generic
# Optional. Scope of this skill:
#   generic          — principles and patterns, language-agnostic
#   stack-specific   — tied to a tech or toolchain (Next.js, Bun, CSS)
#   context-specific — tied to a domain or project
# Omit for skills that do not participate in a parent/child hierarchy.

# parent: parent-skill-name
# Optional. Kebab-case name of the parent skill this extends.
# When set, the parent skill should be loaded first — this skill adds to it.
# Only set on child skills (specificity: stack-specific or context-specific).

# triggers: [keyword1, keyword2]
# Optional. Keywords signalling this child skill is relevant to the current task.
# Lets the agent decide whether to load this skill without reading the full body.
# Only meaningful on child skills.

tool_agnostic: true
# Optional. Set true if the body contains no tool-specific syntax, CLI names,
# or provider references — meaning any AI agent can follow the instructions.
# Set false (or omit) if the skill requires specific tools, CLIs, or platforms.

authors: []
# Optional. Add if skill originates from a third party or has multiple contributors.
# Example: [greptileai] or [your-name]

tested_on: []
# Optional but recommended. List models this skill has been verified on.
# Format: ['model-name (YYYY-MM-DD)']
# Example: ['claude-sonnet-4.6 (2026-05-23)', 'gpt-4o (2026-05-20)']

# deprecated_since: "1.2.0"
# Optional. Set if this skill is no longer recommended. Triggers a validator warning.
# Must be a semver version string.

# superseded_by: other-skill-name
# Optional. Set alongside deprecated_since to point users to the replacement.
# Must be a valid kebab-case skill name.
---

# Skill Title

One sentence on what this skill is for and the problem it solves.

## When to use

- Trigger phrase or condition 1
- Trigger phrase or condition 2

## Steps

1. First step — be specific. Include exact commands where relevant.
2. Second step.
3. Third step.

## Pitfalls

- Known failure mode 1 and how to avoid it.
- Edge case to watch out for.

## Verification

How to confirm the skill worked correctly.

---

<!--
ADOPTING FROM THE INTERNET — checklist before committing

Strip from the original:
  [ ] Tool-specific frontmatter fields (trigger, allowed-tools, license, compatibility,
      metadata.author, etc.) — move attribution to an HTML comment like this one
  [ ] Hardcoded file paths that assume a specific project structure
  [ ] References to internal tooling (.factory/, petitions/, custom daemons)
  [ ] Credentials, tokens, or environment-specific values

Add or update:
  [ ] Schema-compliant frontmatter: name, description (≤150 chars!), version, tags, tool_agnostic
  [ ] MIT/Apache/etc attribution in an HTML comment if the original has a license
  [ ] authors: [original-author] if clearly attributed

Validate:
  [ ] Directory name matches `name` in frontmatter exactly
  [ ] python3 scripts/validate.py passes clean
  [ ] python3 scripts/index_builder.py runs without error
  [ ] Skill body still makes sense after stripping tool-specific parts

Reference files:
  [ ] Place supporting docs under references/, templates/, scripts/, or assets/
  [ ] Update them if they contain tool-specific API calls that differ from what
      the converted skill now expects
-->
