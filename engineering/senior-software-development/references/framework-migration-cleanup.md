# Framework/site-generator migration cleanup reference

Use this when a repository has already been migrated to a new stack, but traces of the old one remain and keep misleading future work.

Durable cleanup pattern
- First inspect active runtime/build entrypoints (`package.json`, framework config, CI workflow) so cleanup follows the live architecture rather than assumptions.
- Search for old-stack references in docs and active source paths before touching deletions.
- Expect whole-repo searches to be noisy because they pull in `node_modules`, generated output, screenshots, `.git`, and caches. Narrow searches to active project paths whenever possible.
- Update guidance files early. Stale repo instructions are high-leverage sources of repeated wrong actions.
- Remove old source/config/theme directories only after confirming the new stack builds successfully.
- Keep cross-stack assets that are still valid, such as `public/CNAME` for GitHub Pages.
- After cleanup, run a fresh build and start the local server. Verify with an HTTP response check before reporting success.

Applied example from this repo class
- Old Hugo setup files removed: `config.toml`, `content/`, `layouts/`, `assets/`, `themes/PaperMod/`, `archetypes/default.md`
- Docs updated to Astro: `CLAUDE.md`, `GEMINI.md`
- Ignore rules simplified to Astro-era generated files
- `public/CNAME` kept while old Hugo-generated `public/` artifacts were removed
- Validation pattern: `npm run build` then `npm run dev -- --host 0.0.0.0 --port 4321`, followed by `curl -I http://127.0.0.1:4321`
