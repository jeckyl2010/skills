# GitHub Pages publish verification for static sites

Use this when a repo publishes a static site to GitHub Pages from a workflow on `main`.

## Minimal safe publish loop
1. Check `git status`, current branch, and remotes.
2. Confirm the workflow trigger branch in `.github/workflows/deploy.yaml`.
3. Run the production build locally before pushing.
4. Commit the intended changes, then push the publishing branch.
5. Verify deployment with GitHub CLI:
   - `gh run list --workflow deploy.yaml --limit 10`
   - `gh run watch <run-id> --exit-status`
   - `gh run view <run-id> --json status,conclusion,url`
   - `gh api repos/<owner>/<repo>/pages --jq '.html_url, .status, .cname'`

## Pitfalls
- `gh run watch` does not accept `--workflow`; it requires a concrete run ID.
- Prefer `gh api ... --jq ...` for simple field extraction instead of piping JSON into Python.
- GitHub Pages may report `source.branch` as `gh-pages` even when the deployment workflow is triggered by pushes to `main`; treat the Pages API as the source of truth for live-site status.
- For framework migrations, include removal of obsolete generated output and old theme/framework directories in the same publish commit once the replacement build is verified.
- Keep generated `dist/` ignored unless the user explicitly asks to commit build output.

## Report back
Include:
- commit SHA
- pushed branch
- workflow run URL
- live site URL
- any non-blocking warnings such as GitHub Actions runtime deprecations
