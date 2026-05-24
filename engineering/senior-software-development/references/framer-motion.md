# Framer-motion

## Audit and cleanup

When stripping y/x/scale/stagger animations across a codebase, work in two parallel batches (split at ~8 files each to stay within delegation limits). Use this decision matrix:

**Strip → plain element (no animation left):**
- `motion.div` with only `y` or `x` in initial/animate → convert to `<div>`
- `motion.h3/p/span/button` with mount-only y/scale → convert to native element
- `index * 0.05` stagger delays → remove entirely
- Sequential mount delays (0.1, 0.2, 0.3…) → remove entirely

**Strip partially → keep as motion element (opacity-only):**
- `motion.div` with both `opacity` and `y` → remove `y`, keep `opacity` fade
- Modal/dialog entry with `scale + opacity` → remove `scale`, keep `opacity`
- `AnimatePresence` + `exit={{ opacity: 0 }}` → always keep (exit animations require framer)

**Keep as-is (functional, not decorative):**
- `height: 0` → `height: "auto"` expand/collapse (communicates state change)
- Spring transitions on interactive state indicators (e.g. selected dot in sidebar)
- `AnimatePresence mode="popLayout"` on list reordering

**After the edit pass:**
- Delete `.next/` before restarting the dev server — Turbopack caches the old module graph. Stale `motion is not defined` runtime errors after import changes are almost always a `.next` cache issue, not a real import bug.
- Watch-pattern alerts on a background process can fire on old buffered output that predates the fix. Before re-diagnosing, read the full process log and check whether errors appear before or after the relevant code change. If the server has been serving 200s since the fix, the alerts are stale noise.
- Run `bun run build` after cleanup, not just `bun run typecheck` — the build catches client/server boundary issues that typecheck misses.

**Ideal end state:** a single `<FadeIn>` wrapper component (`initial={{ opacity: 0 }} animate={{ opacity: 1 }}`, short duration, no y/scale/stagger) that all fade-in usage routes through. Eliminates drift when framer-motion is updated or removed.

## Full removal (dependency uninstall)

**Replacement strategy:**
- `motion.div` with opacity fade → `<div className="animate-in fade-in duration-300">` (Tailwind 4, entry only)
- `motion.div` with only `y` offset → plain `<div>` (drop the animation entirely)
- `AnimatePresence` + conditional render → drop `AnimatePresence`, keep conditional render; exit snap is acceptable for non-critical UI
- `layoutId` indicator bars → plain div, instant snap is fine
- Uninstall: `bun remove framer-motion`

**Structural pitfall — `createPortal` + `AnimatePresence`:**
When `AnimatePresence` was the single child of `createPortal(child, container)`, stripping it leaves multiple sibling JSX nodes (comments + element) as direct arguments to `createPortal`, which is a syntax error. Wrap in a fragment:
```tsx
// Before (broken after AnimatePresence removal):
return createPortal(
  {/* comment */}
  <div ...>,
  document.body
);
// After:
return createPortal(
  <>
    {/* comment */}
    <div ...>
  </>,
  document.body
);
```

**Structural pitfall — orphaned `{open && (` after AnimatePresence strip:**
When `AnimatePresence` wraps `{open && ( <> ... </> )}`, stripping `AnimatePresence` leaves the conditional as a bare expression inside `return (...)`. Wrap the whole return in a fragment:
```tsx
return (
  <>
    {open && (
      <> ... </>
    )}
  </>
);
```

**biome-ignore comments shift with indentation:**
After removing an `AnimatePresence` wrapper, the previously-suppressed element moves up one indentation level. Biome re-evaluates the suppress target from scratch — an existing `biome-ignore` on line N now covers a different element. Re-read the file and move or re-add the ignore comment to sit directly above the new offending line.

**Python bulk-replace for motion.\* patterns:**
Using Python regex (`re.sub`) to replace all `motion.div` / `motion.button` etc. is effective for the attribute variants, but leaves structural issues to fix manually:
- Orphaned closing `</motion.div>` and `</AnimatePresence>` tags
- Remaining `{open && (` without a wrapper (see above)

Always run `bun run typecheck` immediately after the script pass and fix structural issues before committing.

**Pre-commit hook stash trap:**
The pre-commit hook stashes unstaged files and runs against the staged snapshot. If you make lint/format fixes after `git add -A`, those fixes are in the working tree but not staged — the hook sees the pre-fix version and fails. Always run `git add -A` again immediately before the commit attempt that follows any post-stage fixes.
