## Summary

Brief description of what this PR does.

## Changes

- 
- 

## Version bump (if skill was changed)

Type: [ ] patch — wording or clarity fix   [ ] minor — new content or behaviour   [ ] major — breaking change to output format or interface

Reason: 

## Checklist

- [ ] Skill name matches directory name and `name` field in frontmatter exactly
- [ ] Frontmatter includes: `name`, `description`, `version`, `tags`, `tool_agnostic: true`, `authors`
- [ ] Version bumped in frontmatter (patch / minor / major — see above)
- [ ] `python3 scripts/validate.py` passes locally
- [ ] `python3 scripts/index_builder.py` run and `index.yaml` updated
- [ ] CHANGELOG.md updated — `[Unreleased]` promoted to versioned entry if version was bumped
- [ ] Pitfalls and trade-offs included where relevant — not just happy paths
- [ ] No credentials, API keys, or provider-specific tokens in skill content
- [ ] If skill is deprecated: `deprecated_since` and `superseded_by` set in frontmatter
