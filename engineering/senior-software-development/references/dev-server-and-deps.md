# Dev server, dependency updates, and cross-platform portability

## Dev server startup verification (Next.js + Turbopack)

Next.js dev server writes startup output to stderr, not stdout. When starting with a background process manager that captures only stdout, the log will appear empty even when the server is running.

Correct verification sequence:
1. Start server in background
2. Wait ~5s for Turbopack compilation
3. Check: `lsof -i :3000` — confirms the process is listening
4. Check: `curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/` — confirms a 200 response

Do not rely on log output to confirm readiness when using background process tracking.

If a second `bun run dev` call exits immediately with "Another next dev server is already running" and exit code 1, this is NOT a startup failure. Next.js detects the existing instance on port 3000 and terminates gracefully, printing the PID and log path of the running instance. Use `kill <pid>` from the log output if a restart is needed.

## RSC payload errors after dep update restart

After a dependency update that restarts the Next.js dev server, the browser's cached RSC connection may produce "Failed to fetch RSC payload for ... Falling back to browser navigation" errors in the dev server log. These are not real errors — the browser reconnects automatically and pages load fine. This is expected noise from the hot restart, not a broken route. Confirm page health with `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/<route>` if in doubt.

## Dependency update workflow (Bun monorepo)

Correct sequence when updating deps in a Bun workspace:
1. `cd web && bun update` — updates all packages to latest matching semver ranges
2. If `bun update` resolves to the same version (lockfile has pinned it), force the bump: `bun add next@16.2.6 react@19.2.6` — explicit version wins over range resolution
3. `bun run typecheck` (or `tsc --noEmit`) — verify no type regressions introduced
4. Pay special attention to major-version bumps (Zod 3→4, etc.) — check for API changes in `safeParse`, schema declarations
5. Only run the test suite after typecheck passes — no point diagnosing test failures caused by type errors

### Version verification when an outdated check shows an unfamiliar version

If `bun outdated` shows a version that seems unexpected (e.g. `next 16.x` when you expected 14.x or 15.x), verify it exists on npm before researching breaking changes:
```
curl -s "https://registry.npmjs.org/<package>" | python3 -c "import json,sys; p=json.load(sys.stdin); print(p['dist-tags']['latest'])"
```
If the version is confirmed on npm, treat it as normal. Patch releases are safe to apply without deep research.

## Cross-platform portability on project revival

When picking up a project that was last active on a different OS (e.g. Windows → macOS):
- Scan all YAML/config files for absolute paths — `portfolio.yaml`, `docker-compose.yml`, `.env` files. Windows absolute paths (`C:\\Repos\\...`) fail silently on macOS; convert to relative paths.
- Check `next.config.ts` / similar for hardcoded dev machine IPs in `allowedDevOrigins` — harmless but dead config, clean up.
- Verify runtime tools: `bun`, `node`, `python3`. Bun binary at `~/.bun/bin/bun` may not be on PATH in subshells — always `export PATH=$HOME/.bun/bin:$PATH` when invoking bun in scripts or execute_code.

### Portable manifest paths

When code writes paths into a shared config file (`portfolio.yaml`, `docker-compose.yml`, registry manifests), always store paths relative to the config file's directory — not the raw user-supplied path (which may be absolute) and not the resolved absolute path.

```ts
// ✗ Stores whatever the caller passed — could be absolute
manifest.systems.push({ name: id, path: systemPath });

// ✓ Stores a path relative to where portfolio.yaml lives — portable across machines
manifest.systems.push({
  name: id,
  path: path.relative(path.dirname(portfolioFilePath), absoluteSystemPath),
});
```

Cover with a test assertion that `path.isAbsolute(entry.path) === false` after the write — load the YAML and check the stored entry directly.
