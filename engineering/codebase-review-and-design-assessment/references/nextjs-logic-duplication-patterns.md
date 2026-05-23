# Next.js + TypeScript — logic duplication anti-patterns

Session: risk-assistant codebase review, May 2026

## The matchesCondition duplication problem

In Next.js apps with a server-side evaluation engine and a client-side preview (e.g. live domain activation while the user fills out a form), there is a strong temptation to copy the server-side rule-matching function into the client component rather than import it. This creates a high-risk drift vector.

**The pattern to avoid:**
- `lib/evaluator.ts` has `matchesCondition(facts, cond)` — authoritative, server-side
- `components/systemEditor/SystemEditor.tsx` also has `matchesCondition(facts, cond)` — identical at point of copy, but independent

**Why it drifts:**
- The two copies have no shared type contract tying them together
- A model change (new operator, new field format) requires updating both — and the component copy is easy to miss in review
- The result: the editor shows domain X activating, but /api/evaluate does not return domain X — silent, hard to debug

**The fix:**
- Move `matchesCondition`, `deepGet`, `Facts`, and any other shared engine primitives to `lib/engine.ts` or keep them in `lib/evaluator.ts`
- Import from there in both the server and client paths
- The client components do not own engine logic; they own display and interaction

## Type declaration drift

Same pattern applies to `EvaluateResult` and `DerivedControls`. When a hook file like `hooks/useSystemApi.ts` redeclares the API response shape rather than importing it from `lib/evaluator.ts`, the hook and the server can drift.

Fix: export the canonical type from lib/, import it in the hook.

## Facts type

`Facts = Record<string, unknown>` is too generic to carry meaningful type safety, but at least make it one import, not two parallel declarations.
