# Skill / Prompt Repository Governance Patterns

Patterns applied to `jeckyl2010/skills` (2026-05-23). Reference when professionalising
any AI skill, prompt, or instruction library repo.

## Metadata fields worth adding to skill frontmatter

```yaml
tested_on: ['claude-sonnet-4.6 (2026-05-23)']  # verified model + date
deprecated_since: "1.2.0"                        # triggers validator warning
superseded_by: replacement-skill-name            # points users to replacement
```

## CI quality gates specific to skill repos

### Index staleness gate
Regenerate index and fail if committed version differs:
```yaml
- name: Regenerate index and check for diff
  run: |
    python3 scripts/index_builder.py
    if ! git diff --exit-code index.yaml; then
      echo "index.yaml is out of date. Run python3 scripts/index_builder.py locally."
      exit 1
    fi
```

### Validator with deprecation warnings
validate.py should warn (not error) on deprecated skills:
```python
if "deprecated_since" in data:
    superseded = data.get("superseded_by")
    msg = f"deprecated since {data['deprecated_since']}"
    if superseded:
        msg += f" — superseded by '{superseded}'"
    warnings.append(msg)
```

## PR template additions for skill repos

Add a semver bump justification block:
```
## Version bump (if skill was changed)
Type: [ ] patch — wording/clarity   [ ] minor — new content/behaviour   [ ] major — breaking change
Reason:
```

Checklist additions:
- Version bumped and type justified
- `[Unreleased]` promoted to versioned CHANGELOG entry
- `deprecated_since` / `superseded_by` set if deprecating

## GitHub Discussions

Enable for skill repos — low friction way to surface "skill misbehaves on model X"
without requiring a formal bug report. Badge:
```markdown
[![Discussions](https://img.shields.io/github/discussions/<owner>/<repo>)](https://github.com/<owner>/<repo>/discussions)
```

Enable via: `gh api repos/<owner>/<repo> --method PATCH --field has_discussions=true`

## AGENTS.md

Every skill/prompt repo should have an AGENTS.md at the root encoding:
- Required frontmatter fields and format
- Version bump semantics (patch / minor / major — what each means for skills)
- CHANGELOG discipline (Unreleased → versioned, same commit)
- Sync/push workflow (e.g. sync-skills.py — not raw git push)
- Deletion checklist (all cross-references must be updated)
- Deprecation workflow

Hermes injects AGENTS.md automatically when working in that repo directory.

## Patterns from reference repos (research 2026-05-23)

Sources reviewed: openai/evals, microsoft/semantic-kernel, promptfoo/promptfoo,
github/copilot-instructions, langchain-hub, sindresorhus/awesome-lint,
anthropic/claude-code-best-practices, f/awesome-chatgpt-prompts.

HIGH VALUE for personal skill libraries:
- Deprecation metadata (above) — almost no open-source repos do this
- Index staleness CI gate — langchain-hub pattern
- Semver justification in PR template — brexhq/prompt-engineering pattern
- tested_on field — copilot-instructions compatibility field adapted for model verification
- GitHub Discussions — FlowGPT/PromptBase pattern brought to GitHub

SKIPPED (overkill for personal library):
- LLM-judge rubric assertions (promptfoo) — fine for community repos
- Machine-readable prompt/parameter separation (semantic-kernel) — not needed unless building tooling
- Baseline model results in READMEs — useful for community repos, overhead here
- Minimum test case count (openai/evals) — too formal for personal use
