---
name: adr-generator
version: 1.0.0
description: Generate Architecture Decision Records (MADR format) from design context, discussions, or review findings. Structured, auditable decision artifacts.
tags: [architecture, adr, decision-records, documentation, governance]
tool_agnostic: true
---

# ADR Generator

Generate a well-formed Architecture Decision Record (ADR) from design context, a decision under discussion, or findings from a review.

## Use When

- A significant architectural decision has been made or is being finalized
- A design discussion needs to be formalized before implementation begins
- A code or architecture review surfaces a decision that should be captured
- A team needs a lightweight audit trail for technical direction

## Do Not Use When

- The decision is trivial or easily reversible with no downstream impact
- The artifact needed is a full architecture proposal (use target-state-pattern-authoring instead)
- The task is primarily about documenting implementation steps

## ADR Format (MADR)

Use Markdown Architectural Decision Records (MADR) format unless the user specifies otherwise.

```markdown
# [Short title: problem and solution in plain terms]

Date: YYYY-MM-DD
Status: [Proposed | Accepted | Superseded by ADR-XXXX | Deprecated]

## Context and Problem Statement

[What is the situation and what decision needs to be made?
Be concrete. State the forces at play: technical constraints, operational requirements, team capabilities, cost.]

## Decision Drivers

* [Primary force shaping the decision]
* [Secondary force]
* [Add more as needed]

## Considered Options

* [Option A]
* [Option B]
* [Option C — include at least two alternatives]

## Decision Outcome

Chosen option: [Option X], because [plain justification tied to the decision drivers].

### Consequences

* Good: [What improves or becomes easier]
* Bad: [What gets harder, costs more, or introduces risk]
* Neutral: [What changes but is neither better nor worse]

## Pros and Cons of the Options

### [Option A]
* Good, because [...]
* Bad, because [...]

### [Option B]
* Good, because [...]
* Bad, because [...]

## Links

* [Link to related ADR, proposal, or ticket if applicable]
```

## Procedure

1. **Extract the decision.** Identify what is actually being decided — the specific architectural question, not the surrounding context.

2. **Identify decision drivers.** What constraints, risks, or requirements make this decision non-trivial? Pull these from the context provided.

3. **Name the alternatives.** Even if the decision is obvious, document at least two options. If only one option was considered, say so and note why alternatives were ruled out early.

4. **State the chosen option plainly.** One sentence. Tied directly to the decision drivers.

5. **Be honest about consequences.** The "Bad" consequences are as important as the "Good" ones. An ADR that only lists positives is not trustworthy.

6. **Set the status correctly.**
   - Proposed: decision is drafted but not yet agreed
   - Accepted: agreed and in effect
   - Superseded: replaced by a newer ADR (link to it)
   - Deprecated: no longer relevant

## Output

Produce the complete ADR in Markdown, ready to commit to a `docs/adr/` or `docs/decisions/` directory.

Filename convention: `NNNN-short-hyphenated-title.md` — e.g. `0012-use-event-sourcing-for-order-history.md`

## Common Mistakes To Avoid

- Vague problem statements that could apply to any project
- Only one option considered (makes the record useless for future readers)
- Consequences that are all positive (signals the decision was post-rationalized)
- Missing date and status
- Mixing implementation detail into a decision record (save that for runbooks)
