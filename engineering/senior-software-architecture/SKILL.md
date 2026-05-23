---
name: senior-software-architecture
description: Apply senior architectural judgment to systems, boundaries, scalability, reliability, and technical decision-making.
version: "1.0.1"
tags: [architecture, system-design, scalability, reliability, trade-offs]
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []
---

# Senior Software Architecture

Use this skill when designing systems, evaluating platform choices, planning integrations, reviewing service boundaries, or making medium/long-term technical decisions.

## Goals
- Align architecture with business goals, delivery constraints, and team capability.
- Favor understandable, evolvable systems over theoretical elegance.
- Make trade-offs explicit across complexity, cost, performance, reliability, and speed.
- Design for operability, failure handling, and incremental change.

## Default lens
1. Begin with requirements: scale, latency, consistency, compliance, team size, budget, and delivery timeline.
2. Identify the highest-risk constraints first.
3. Choose the simplest architecture that satisfies today's needs with a believable path for tomorrow.
4. Prefer well-defined boundaries, contracts, and ownership.
5. Design for observability, rollback, and failure isolation from the start.
6. Avoid irreversible decisions when uncertainty is high.

## Review checklist
- What problem does this architecture solve better than a simpler option?
- Are service and module boundaries aligned with domain and ownership?
- Where are the key bottlenecks, failure modes, and coupling points?
- What are the data consistency and migration implications?
- How will this be tested, deployed, observed, and rolled back?
- What is the operational cost in people, tooling, and cognitive load?
- What decision can be deferred until there is more evidence?

## Existing codebase architecture reviews
When reviewing an existing repository rather than designing from scratch:
- Start by comparing the documented architecture with the live code paths and entrypoints.
- Trace one or two real end-to-end flows so the review is grounded in execution, not just folder names.
- Look for orchestration gravity: oversized CLI, pipeline, or client modules that accumulate cross-layer responsibilities.
- Check for boundary erosion: compile concerns leaking into publishing, transport concerns leaking into domain logic, or workflow policy living in presentation layers.
- Call out abandoned or half-adopted abstractions separately from active architecture; these often create more confusion than active code smells.
- Use module size and concentration as heuristics, not proof: very large files often mark hotspots worth architectural attention.
- When possible, run the test suite before final judgment so design critique is paired with current system health.
- Distinguish clearly between strong foundations, near-term refactor targets, and strategic long-term risks.

## Output structure
When useful, structure responses as:
- Context and constraints
- Recommended architecture
- Key trade-offs
- Data / interface boundaries
- Reliability and observability considerations
- Security / compliance considerations
- Evolution path and next decisions

## Strong defaults
- Prefer modular monoliths until distribution is justified.
- Make APIs and events explicit and versioned where needed.
- Keep ownership clear for services, schemas, and runbooks.
- Build observability with logs, metrics, traces, and alerts that map to user impact.
- Design for graceful degradation and recovery.
- Document assumptions and decision records for consequential choices.

## Pitfalls to avoid
- Distributed systems where a modular monolith would do
- Over-optimizing for scale before product fit or usage evidence
- Architecture diagrams with no operational story
- Coupling teams through shared databases or unclear ownership
- Ignoring migration paths and rollback plans
- Selecting technologies because they are fashionable rather than appropriate
