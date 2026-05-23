---
name: extract-wisdom
version: 1.0.0
description: Extract decisions, action items, open questions, and key insights from meetings, transcripts, and workshops. Structured output, no padding.
tags: [meetings, notes, transcripts, workshops, extraction, consulting, knowledge]
tool_agnostic: true
---

# Extract Wisdom

Extract the useful signal from messy inputs — meeting notes, transcripts, workshop outputs, long documents, stakeholder interviews — and turn it into structured, actionable material.

## Use When

- Processing notes from a client discovery session or stakeholder interview
- Distilling a workshop output into decisions and next steps
- Extracting key insights from a long document, report, or paper
- Producing a clean record from a raw transcript before it gets filed and forgotten

## Do Not Use When

- The source is already well-structured and just needs formatting
- The task is a full document rewrite rather than extraction

## Extraction Categories

Pull from the source into these buckets. Only include a bucket if it has content — do not produce empty sections.

### Decisions Made
Things that were agreed, confirmed, or resolved. Be specific. A decision needs to be attributable and actionable.

Format: [Decision] — [context or rationale if stated]

### Action Items
Concrete next steps with an owner and a timeframe where available.

Format: [What] — Owner: [who] — By: [when or "TBD"]

### Open Questions
Unresolved questions that need an answer before something can move forward. Flag the owner or next step for each where possible.

Format: [Question] — Owner: [who will resolve it] or "Unassigned"

### Key Insights
Observations, patterns, or statements that are worth retaining even if they don't map to a specific action. Include direct quotes where the phrasing matters.

### Assumptions and Constraints
Explicitly stated or clearly implied constraints that will shape decisions going forward.

### Parking Lot
Items raised but not discussed or resolved in this session. Needs a home somewhere.

## Procedure

1. **Read the full source before extracting anything.** Context at the end of a meeting often reframes something said at the start.

2. **Extract signal, not volume.** A 90-minute meeting should not produce a 4-page extraction. If something is not actionable or insightful, leave it out.

3. **Be precise about ownership.** "The team will..." is not an owner. Name a person or role. If no owner was assigned, mark it "Unassigned" — that itself is a signal.

4. **Preserve direct quotes where the exact wording matters.** Paraphrase everywhere else.

5. **Flag ambiguity.** If a decision is unclear, or an action item has no owner, or two participants seem to have disagreed without resolving it, surface that — don't smooth it over.

6. **Keep it short.** The goal is to make the material useful to someone who was not there. If they need to read the full transcript to understand the extraction, the extraction has failed.

## Output Format

Return clean structured Markdown. Use the category headings above. Skip any category with no content.

Example opening:

```
Source: [document title or meeting description]
Date: [date if available]
Participants: [names or roles if available]

## Decisions Made
...

## Action Items
...

## Open Questions
...
```

## Common Mistakes To Avoid

- Copying paragraphs verbatim instead of extracting the point
- Producing action items with no owner
- Including everything instead of prioritizing signal
- Resolving ambiguity that exists in the source rather than surfacing it
- Conflating a decision with an opinion or preference
- Writing an executive summary instead of structured extraction (different tool)
