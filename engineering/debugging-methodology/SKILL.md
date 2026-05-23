---
name: debugging-methodology
version: 1.0.0
description: Structured debugging workflow — hypothesis-driven, evidence-based, reproducible. Produces auditable findings, not just a fix.
tags: [debugging, troubleshooting, methodology, engineering, incident]
tool_agnostic: true
---

# Debugging Methodology

A structured, hypothesis-driven approach to debugging. The goal is not just to fix the immediate issue — it is to understand what actually happened and why, so the fix is correct and the knowledge is retained.

## Use When

- A bug is not immediately obvious from reading the code
- A system behaves differently than expected in ways that are hard to reproduce
- An incident needs a documented root cause, not just a patch
- A debugging session has been running in circles and needs a reset

## Do Not Use When

- The fix is obvious and the risk is low — just fix it
- The task is exploratory prototyping, not debugging a specific failure

## Core Principle

Never guess twice. Form a hypothesis, test it with the minimum action needed to confirm or deny it, then update your understanding. A bug fixed by trial and error is a bug that will return.

## Procedure

### Phase 1 — Establish the Baseline

1. **State the symptom precisely.** What is the observed behavior? What is the expected behavior? Where and when does it occur?

2. **Make it reproducible.** If you cannot reproduce the bug reliably, you cannot confirm you have fixed it. Invest in a minimal reproduction case.

3. **Gather evidence before touching anything.** Logs, stack traces, error messages, network traffic, database state, environment configuration. Capture the state before any changes.

4. **Define the blast radius.** What is affected? What is confirmed not affected? This scopes the investigation.

### Phase 2 — Form Hypotheses

5. **List 2-3 candidate hypotheses.** Each should be a falsifiable claim about the cause. "The database is slow" is not a hypothesis. "The N+1 query in `OrderService.getItems()` is causing timeouts under load" is.

6. **Order by likelihood and testability.** Test the most likely and easiest-to-test hypothesis first.

7. **State what evidence would confirm or deny each hypothesis.** Know what you are looking for before you look.

### Phase 3 — Test Systematically

8. **Change one thing at a time.** Multiple simultaneous changes make it impossible to know what fixed the problem.

9. **Test the hypothesis, not the fix.** Confirm the cause before applying the solution.

10. **Document what you tried and what it showed.** If you hand off the investigation or need to revisit it, this log is essential.

### Phase 4 — Fix and Verify

11. **Apply the fix once the cause is confirmed.** The fix should follow directly from the confirmed hypothesis.

12. **Verify the fix against the original reproduction case.** Confirm the symptom is gone.

13. **Check for regressions.** Run the relevant test suite. Check adjacent behavior.

14. **Confirm the fix under conditions close to production.** A fix that works locally but not under load or in a specific environment is not a fix.

### Phase 5 — Document and Close

15. **Write a brief root cause summary.** What was the actual cause? What masked it? Why did it occur?

16. **Note any systemic issues the bug exposed.** Missing test coverage, unclear ownership, configuration drift, absent monitoring.

17. **State what would catch this class of bug earlier.** A test, a log line, an alert, a linting rule.

## Output Shape

For anything non-trivial, produce a brief debugging record:

- **Symptom** — observed vs. expected behavior
- **Reproduction case** — minimum steps to trigger
- **Hypotheses tested** — what was tried and what each test showed
- **Root cause** — confirmed cause in plain terms
- **Fix applied** — what was changed and why
- **Verification** — how the fix was confirmed
- **Follow-up items** — systemic issues, missing coverage, monitoring gaps

## Common Mistakes To Avoid

- Starting with a fix before understanding the cause
- Changing multiple things simultaneously
- Closing a bug when the symptom disappears without confirming the root cause
- Ignoring evidence that contradicts the favored hypothesis
- Treating a workaround as a fix
- Not checking whether the bug can recur under different conditions
