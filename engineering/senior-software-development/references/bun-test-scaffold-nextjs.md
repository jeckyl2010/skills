# Bun test scaffold — Next.js monorepo

See SKILL.md for the full workflow. This file collects runtime quirks and scaffold patterns.

## Setup (Bun workspace)

1. Add `@types/bun` as devDependency inside the `web/` package (not the root workspace):
   ```
   cd web && bun add -d @types/bun
   ```
   If placed at root only, `bun:test` imports and `import.meta.dir` will show LSP errors in `web/` files — but tests still run. Add it under `web/` to suppress the false positives.

2. Add test scripts to `web/package.json`:
   ```json
   "test": "bun test tests/",
   "test:watch": "bun test --watch tests/",
   "test:coverage": "bun test --coverage tests/"
   ```

3. Test layout mirrors `src/`:
   ```
   web/
     src/lib/evaluator.ts
     tests/lib/evaluator.test.ts
   ```

## Path aliases in tests

Bun picks up `tsconfig.json` automatically. `@/lib/...` aliases resolve without extra config.

## Runtime quirks

- `fs.access()` in Bun resolves to `null` on success, not `undefined` (unlike Node). Test expectations must use `null`.
- `typeof [] === "object"` is `true` in JS — storage guards that use only `typeof` will pass arrays silently. Use `Array.isArray()` check as well.
- `import.meta.dir` works in Bun test context for resolving fixture paths.

## FS-coupled storage: snapshot/restore pattern

When `storage.ts` hardcodes `findRepoRoot(process.cwd())` with no injection point:

```ts
let originalContent: string;
beforeAll(async () => {
  originalContent = await fs.readFile(portfolioPath, "utf-8");
});
afterAll(async () => {
  await fs.writeFile(portfolioPath, originalContent, "utf-8");
});
```

Write test artifacts to `os.tmpdir()`, never into real project directories.
Use timestamped test IDs (`test-${Date.now()}-${Math.random()}`) to avoid collisions.

## Deterministic engine tests: coverage shape

For a pure evaluation engine (rules engine, guardrail evaluator):
- One `describe` block per public function
- One integration test using a real fixture YAML file (e.g. `TestMe.yaml`)
- Test accumulating lists (e.g. `because[]`) for multi-rule additive behaviour
- Mock only file-system error paths, not the loader itself

## Parser function coverage shape

For `parseX(unknown[])` functions that silently drop bad entries:
- Each valid variant
- Each skip condition in isolation
- Optional field presence/absence
- Sub-array value filtering
- Mixed valid+invalid input (verify count AND order)
- Empty array input
- Real-file integration test confirming `result.length === expectedCount`

## YAML serialisation contracts

When storage writes entries to a YAML file, test the contract at the serialised layer — not just in-memory:

```ts
it("stores paths as relative, not absolute", async () => {
  await storage.addSystem({ name: "foo", path: "/Users/me/Repos/foo" });
  const raw = parse(await fs.readFile(portfolioPath, "utf-8")) as Portfolio;
  const entry = raw.systems.find((s) => s.name === "foo")!;
  expect(path.isAbsolute(entry.path)).toBe(false);
});
```

Key assertions:
- `path.isAbsolute(entry.path) === false` — portable across machines
- Round-trip: write then read back and compare to input value
- Field ordering and whitespace do not matter; only the parsed value matters
- Use `import { parse } from "yaml"` (not `JSON.parse`) to read back — yaml preserves comments and multiline strings differently than JSON

## Last updated
Session: risk-assistant project revival (2026-05)
