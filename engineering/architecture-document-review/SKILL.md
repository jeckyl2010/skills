---
name: architecture-document-review
version: 1.0.0
description: Review architecture documents for defensibility, boundary clarity, ownership, survivability, and testability. Works beyond manufacturing.
tags: [architecture, review, manufacturing, isa-95, idmz, ot, governance, risk]
tool_agnostic: true
---

# Architecture Document Review

Review architecture documents as architecture documents — not as general writing or implementation specs.

## Use When

- Reviewing target-state documents, patterns, proposals, standards, technical principles, ADRs, BDRs, or control baselines
- Checking whether a document is safe, testable, and usable across multiple sites or contexts
- Challenging weak claims, blurred ownership, vendor hand-waving, or cloud assumptions that would fail in production
- Pressure-testing architecture language before review with security, legal, OT, or platform stakeholders

## Do Not Use When

- The task is software implementation or code review
- The task is pure copy-editing, grammar cleanup, or branding polish only
- The document is a project plan or migration backlog rather than an architecture artifact

## Review Standard

Default to blunt, evidence-oriented review.

Check the document against these questions:

1. Is the architectural problem clear, or is the document just describing technology?
2. Are scope, assumptions, and hard constraints explicit?
3. Are trust boundaries, separation concerns, and support-access assumptions stated clearly where relevant?
4. Does the design survive WAN loss, cloud loss, vendor outage, and degraded-mode operation where production depends on it?
5. Is ownership explicit for design authority, approvals, operations, exceptions, and lifecycle?
6. Is the control model concrete enough to audit, test, or implement?
7. Are supplier obligations, exit constraints, and operating costs visible where external services are involved?
8. Is the document reusable across multiple sites or contexts, or does it quietly depend on local heroics?

## Grounding

Before reviewing, read the document carefully. For manufacturing architecture, also ground in:
- Any packed repository context (e.g. `ai-context/architecture-context.md`) as read-only compiled context
- Any directly related source documents that are more authoritative than packed context

## Procedure

1. **Identify the artifact type.**
   Distinguish between principle note, pattern, proposal, decision record, reference design, control standard, or vendor assessment.

2. **Identify the review lens.**
   Default is architectural defensibility. Add security, operating model, vendor, cost, rollout, or governance emphasis only when the document requires it.

3. **Review for findings first.**
   Lead with concrete issues, not summary praise. Focus on missing constraints, blurred ownership, broken boundary assumptions, and untestable or non-operable statements.

4. **Separate structural issues from writing issues.**
   Do not waste time on prose cleanup when the actual architecture is weak.

5. **State residual risk.**
   Even when no major findings exist, call out testing gaps, dependency risk, site-variation risk, or operating-model assumptions.

## Output Shape

1. Findings ordered by severity
2. Open questions or assumptions that need resolution
3. Short change summary only if useful

## Common Failure Modes To Call Out

- Generic "best practice" language with no enforceable meaning
- Cloud dependency that would stop production or critical operations
- Direct cross-boundary trust or hidden vendor-access shortcuts
- Missing ownership for exceptions, approvals, or operations
- No cost, lifecycle, support, or exit story
- Local effort assumed but not staffed or funded
- Principles that sound good but cannot be evidenced or tested
- Designs that are technically sound but operationally undeliverable in the actual environment
