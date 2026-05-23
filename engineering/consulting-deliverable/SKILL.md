---
name: consulting-deliverable
version: 1.0.0
description: "Write client-ready consulting deliverables: findings reports, architecture recommendations, executive summaries. Evidence-based, no fluff."
tags: [consulting, deliverables, reports, findings, architecture, writing]
tool_agnostic: true
---

# Consulting Deliverable

Structure and write client-ready consulting deliverables: findings reports, assessment outputs, architecture recommendations, executive summaries, and briefing notes.

## Use When

- Turning raw notes, review findings, or analysis into a structured client document
- Writing an architecture assessment output or modernization recommendation
- Producing an executive summary from a technical review
- Structuring a risk or findings report for stakeholder consumption

## Do Not Use When

- The output is internal working notes, not a client artifact
- The task is pure copy-editing on an already well-structured document
- The document is a technical runbook or implementation guide (different audience, different register)

## Guiding Principles

- Evidence before recommendation. Claims need to be grounded in something observable.
- Findings before praise. Lead with what matters, not with what went well.
- One recommendation per issue. Avoid option lists unless the decision genuinely requires client input.
- Calibrate depth to audience. Board-level: outcomes and risk. Technical stakeholder: mechanism and evidence. Both may appear in the same document as separate sections.
- Write like a senior practitioner, not a junior analyst padding word count.

## Standard Structure

Adapt as needed, but default to this:

### 1. Executive Summary
3-5 sentences. What was assessed, the single most important finding, and the recommended next action.
No jargon. Readable by someone who will not read the rest of the document.

### 2. Scope and Approach
What was included and what was out of scope. How the assessment was conducted (interviews, document review, workshops, codebase analysis). Duration and key participants.

### 3. Findings
One finding per section. For each finding:

- **Observation** — what was found, with evidence
- **Risk or implication** — what it means if left unaddressed
- **Recommendation** — the specific action to take

Order by severity: critical → high → medium → low.

### 4. Recommendations Summary
A numbered list of all recommendations, one line each. Ordered by priority.

### 5. Next Steps
The 3-5 concrete actions the client should take, with suggested owners and a rough timeframe.

### 6. Appendix (if needed)
Supporting detail, raw data, reference material that would interrupt the main narrative.

## Finding Severity Definitions

- **Critical** — immediate risk to safety, operations, compliance, or security posture
- **High** — significant risk that should be addressed within the current programme
- **Medium** — meaningful gap that should be planned for in the near term
- **Low** — improvement opportunity with limited urgency

## Procedure

1. **Read all source material first.** Notes, transcripts, diagrams, prior documents. Do not start writing until you have the full picture.

2. **Identify the 3-5 most important findings.** Not everything deserves equal weight. Ruthlessly prioritize.

3. **Write the executive summary last.** It is easier to summarize what you have already written than to predict what you will write.

4. **Check each recommendation for specificity.** "Improve security posture" is not a recommendation. "Implement network segmentation between the OT and corporate LAN at the IDMZ boundary" is.

5. **Check tone against the ai-humanizer patterns.** Consulting deliverables are particularly prone to inflated significance, vague attribution, and promotional language.

## Common Mistakes To Avoid

- Findings that describe symptoms without naming the cause
- Recommendations that are too vague to act on
- An executive summary that repeats the table of contents
- Burying the most critical finding in section 4
- Writing for the author's comfort rather than the reader's decision-making
- Padding word count with background context the client already knows
