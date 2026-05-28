# GitHub Actions Security Patterns

## Shell injection via `${{ inputs.* }}` in `run:` blocks

**The vulnerability:** When you write `${{ inputs.foo }}` directly inside a `run:` block, GitHub Actions performs template substitution *before* the shell sees the script. If `foo` contains shell metacharacters, they execute. This is a pre-shell injection — the shell never gets a chance to quote or sanitise the value.

Compounding pattern: building a command string with `eval` or string concatenation and then calling `eval cmd` amplifies the risk — any injected content runs in the shell context.

**Safe pattern — env vars + bash array:**

```yaml
# UNSAFE — template substitution happens before the shell
run: |
  ARGS="--config ${{ inputs.config }}"
  [[ "${{ inputs.dry-run }}" == "true" ]] && ARGS="$ARGS --dry-run"
  eval mk2conf publish $ARGS

# SAFE — bind inputs to env vars; build a bash array; drop eval
env:
  INPUT_CONFIG:   ${{ inputs.config }}
  INPUT_DRY_RUN:  ${{ inputs.dry-run }}
  INPUT_SECTION:  ${{ inputs.section }}
run: |
  ARGS=(--config "$INPUT_CONFIG")
  [[ "$INPUT_DRY_RUN" == "true" ]] && ARGS+=(--dry-run)
  [[ -n "$INPUT_SECTION" ]]        && ARGS+=(--section "$INPUT_SECTION")
  mk2conf publish "${ARGS[@]}"
```

**Why this works:**
- `${{ inputs.* }}` inside `env:` is still template-substituted, but the result is assigned to an env var — no shell interpretation of the value.
- The env var is then referenced with `"$INPUT_FOO"` — the shell quotes it properly.
- The bash array `ARGS+=(...)` keeps each argument as a discrete element — no word splitting, no glob expansion.
- `"${ARGS[@]}"` expands the array safely — each element remains its own argument.
- No `eval` anywhere.

**Practical risk level:** In composite actions where all inputs are provided by the repo owner (not external actors), the practical risk is low. Still worth fixing because Marketplace reviews flag it and it sets a bad precedent for forks.

**When to apply:** Any GitHub Actions `run:` block that interpolates `${{ inputs.* }}`, `${{ github.* }}`, or `${{ env.* }}` into a shell command string, especially if combined with `eval` or string concatenation.

## Slash command namespacing in `.claude/commands/`

Claude Code maps `.claude/commands/<name>.md` to the slash command `/<name>`. Generic names (`changelog`, `test`, `deploy`, `review`) will collide with:
- GitHub Copilot built-in commands (e.g. `/changelog`)
- Other tools installed by teammates
- Future CLI updates that reserve common names

**Rule:** always prefix commands installed by a tool or skill with the tool's identifier.

```
# Bad — collides with Copilot built-in
.claude/commands/changelog.md     → /changelog

# Good — namespaced, unambiguous
.claude/commands/mk2conf-changelog.md  → /mk2conf-changelog
```

Apply the same rule to Cursor rules (`.cursor/rules/`) and Copilot instructions (`.github/instructions/`): always use a `<tool>-` prefix on filenames installed by third-party tools or skills.
