# Next.js patterns

## Client/server module boundary

A `"use client"` component must not import — directly or transitively — any module that uses `node:fs`, `node:path`, or other Node-only APIs. The error surfaces at build time as:

```
the chunking context (unknown) does not support external modules (request: node:fs/promises)
```

The import trace in the error shows the full chain: client component → intermediate module → server module. Fix it by splitting the server module.

**Pattern: client-safe extraction**
1. Create `lib/facts.ts` (or similar) containing only pure functions and types — no imports from `node:*`, `yaml`, or any loader.
2. The server-side module (`lib/evaluator.ts`) imports and re-exports from `lib/facts.ts`, then adds its async/fs-dependent logic on top.
3. Client components import pure utilities from `lib/facts.ts` directly.

```
lib/facts.ts          ← pure: Facts, deepGet, matchesCondition. No imports.
lib/evaluator.ts      ← re-exports from facts.ts + server-side async evaluation
"use client" components ← import from lib/facts.ts, never lib/evaluator.ts
```

This keeps a single implementation of each function while respecting the client/server boundary. The re-export in `evaluator.ts` means server-side callers continue to get everything from one import.

**Dedup trap**: consolidating duplicated logic by pointing a client component at the server module will break the build if that module has any `node:*` in its import chain — even if the function being imported is itself pure. The fix is extraction, not just re-export.

## Deduplication via re-export (TypeScript)

### Behavioral divergence check

Before removing a local copy of a utility, check whether it silently diverged from the canonical version. Common divergence: a local `deepGet` returning `undefined` for missing keys where the canonical one returns `null`. Steps:
1. Diff the two implementations side-by-side — look for return values, error handling, and type coercions.
2. Check every call site of the local copy for how it consumes the return value (`=== null`, `=== undefined`, `!= null`, `!value`).
3. If consumers already guard both (`=== undefined || === null`), the divergence is harmless — remove the local copy safely.
4. If consumers only guard one side, either fix the guards or keep the local copy and document the difference.

### Type shadowing: rename the local, don't alias the import

When a local type has the same name as an imported type from the same domain, the forced alias (`LibEvaluateResult`, `BaseType2`) is the smell — not a reason to live with the ambiguity.

Fix: rename the local to be domain-specific (`EvaluateApiResponse`), import the lib type unaliased. The rename is mechanical — grep for the old export name and update all consumers.

When collapsing a local copy of a type or function into a re-export from the canonical module:
- The file must `import type { Foo }` before it can use `Foo` in local function signatures — even if it also `export type { Foo }`.
- Ordering matters: put the `import` before the `export` re-export declaration, or TypeScript raises "Cannot find name" on the local usages.
- Pattern that works:
  ```ts
  import type { Facts } from "@/lib/evaluator";      // local usage
  export type { Facts } from "@/lib/evaluator";       // re-export for callers
  export { deepGet } from "@/lib/evaluator";
  // ... local functions that use Facts as a type ...
  ```
- If the file only re-exports and has no local usages, the `import` line is unnecessary.

## API route security: filesystem-serving endpoints

Any Next.js API route that accepts a `path` query parameter and calls `fs.readdir` / `fs.readFile` is a path traversal risk — it will serve `/etc`, `~/.ssh`, or any absolute path the caller supplies.

Fix pattern:
1. Compute allowed roots at request time (repo root + `os.homedir()`). Use `path.resolve()` to normalise both.
2. Resolve the requested path with `path.resolve()` before any comparison — blocks `../../../etc` traversal.
3. Reject with 403 before touching the filesystem if `resolved.startsWith(root + path.sep)` fails for all roots.
4. Apply the same check to the "go up" parent link — don't let the UI offer navigation that escapes the boundary.
5. Default start path: the repo root, not bare homedir — more useful for the actual file-picker workflow.

```ts
function isPathAllowed(target: string, roots: string[]): boolean {
  const resolved = path.resolve(target);
  return roots.some((root) => resolved === root || resolved.startsWith(root + path.sep));
}
```

The allowed roots must be computed server-side; never trust a client-supplied root.

## Derived stats: use real model data

When a page shows aggregate stats (completion rate, average questions per system, etc.), always derive them from actual data flowing through the system. Hardcoded constants like `avgQuestionsPerSystem = 15` become silently wrong as the model evolves and differ per-system anyway.

- Extend the data-fetching layer to include the real count alongside existing data (e.g. `totalQuestions: res.required_questions.length` per row).
- Compute aggregates in the page/component from those real numbers: `rows.reduce((sum, r) => sum + r.totalQuestions, 0)`.
- The data is already available at the source — it just needs to be surfaced up, not estimated.
