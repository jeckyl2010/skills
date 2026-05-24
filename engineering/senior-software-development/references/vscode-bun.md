# VS Code tasks for Bun workspaces

When a project uses Bun and VS Code, the editor defaults to yarn/npm for its built-in task runner. This causes "command not found: yarn" errors when running npm scripts from the VS Code task panel.

Fix: create `.vscode/tasks.json` with explicit bun commands, and pin `npm.packageManager` in `.vscode/settings.json`.

See `templates/vscode-tasks-bun.json` for a ready-to-use `tasks.json` for a Next.js + Bun monorepo (copy to `.vscode/tasks.json`, adjust `cwd` if the web dir is named differently).

## Key configuration details

- All task `command` fields use `bun run <script>` or `bun test` directly — never `npm run` or `yarn`
- Set `"options": { "cwd": "${workspaceFolder}/web" }` for monorepos where scripts live in a subdirectory
- Mark `dev` and `test:watch` as `"isBackground": true` with a `problemMatcher` so the terminal stays open
- Set `"group": { "kind": "build", "isDefault": true }` on the build task so Cmd+Shift+B works immediately
- Set `"group": { "kind": "test", "isDefault": true }` on the test task so Cmd+Shift+T works
- Add `"npm.packageManager": "bun"` to `settings.json` — stops VS Code guessing yarn/npm for other integrations
- Add a top-level `"options": { "env": { "PATH": "${env:HOME}/.bun/bin:${env:PATH}" } }` block — VS Code task shells do NOT inherit the user's `.zshrc` PATH, so bun will fail with `command not found` without this. This is the most common failure point after initial setup.

## NPM Scripts sidebar panel — known bun limitation

The sidebar "NPM SCRIPTS" panel in VS Code Explorer does NOT support bun as a runner. The `npm.packageManager` setting only accepts `auto`, `npm`, `yarn`, or `pnpm` — passing `"bun"` is silently ignored and the panel falls back to yarn. This is a VS Code limitation, not a config error.

Consequence: clicking scripts in the NPM Scripts sidebar will always fail with `command not found: yarn` when bun is the actual runner.

Resolution: use Terminal > Run Task (from `tasks.json`) instead of the sidebar panel. Optionally hide the NPM Scripts panel to avoid confusion: right-click the Explorer sidebar > uncheck "NPM Scripts".

The `packageManager: "bun@x.y.z"` field in `package.json` is still worth setting — it signals intent, supports Corepack, and may be picked up by future VS Code versions — but it does not fix the sidebar runner today.

## `.gitignore` strategy for `.vscode/`

The default is to ignore the entire `.vscode/` directory, but shared config should travel with the repo so other developers get the same setup.

Correct pattern — replace the blanket ignore with targeted exclusions:
```
# Instead of: .vscode/
.vscode/*.code-snippets
.vscode/launch.json
```

Track: `tasks.json`, `settings.json`, `extensions.json` — shared tooling config
Ignore: `launch.json`, `*.code-snippets` — personal debugger and snippet preferences that vary per developer
