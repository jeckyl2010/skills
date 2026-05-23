---
name: risk-and-control-extraction
version: 1.0.0
description: Extract risk scenarios, control statements, evidence requirements, and ownership from architecture and governance documents into structured controls.
tags: [risk, controls, governance, architecture, manufacturing, compliance, extraction]
tool_agnostic: true
---

# Risk and Control Extraction

Turn architecture and governance text into structured risk and control material.

## Use When

- Building or enriching a risk assessment and controls catalogue
- Converting architecture documents into control candidates
- Extracting evidence requirements, applicability rules, or reassessment triggers
- Splitting baseline controls from workload-specific overlays (e.g. surveillance, supplier AI use, vendor-delivered services)

## Do Not Use When

- The user wants a prose summary only
- The source document is too immature to contain stable control intent
- The task is legal interpretation rather than architecture and control extraction

## Extraction Standard

Do not copy paragraphs blindly. Normalize each item into something that can be assessed.

Default fields to derive where possible:

1. Control domain
2. Control statement
3. Risk scenario addressed
4. Applies when
5. Required evidence
6. Control owner
7. Exception allowed or not
8. Reassessment or review trigger

Optional fields when the source supports them:

1. Inherent risk theme
2. Residual risk note
3. Linked vendor obligation
4. Linked regulatory driver

## Procedure

1. **Separate baseline controls from overlays.**
   Keep universal controls apart from workload-specific controls for surveillance, AI use, supplier obligations, or regional/legal edge cases.

2. **Normalize the language.**
   Convert prose into direct control statements. Remove filler, commentary, and duplicated restatements.

3. **Identify applicability conditions.**
   A good control is not just what must be true — it is also when it applies.

4. **Extract evidence needs.**
   Prefer concrete evidence: architecture flow, audit event, approval record, configuration proof, vendor term, or assessment status.

5. **Flag weak source material.**
   If the source uses vague language, mixed intent, or no ownership, say so instead of pretending the control is well formed.

## Output Shape

When the user does not specify a format, default to a flat structured list with one control per item:

1. Identifier or short label
2. Domain
3. Statement
4. Applies when
5. Evidence
6. Owner
7. Exceptions allowed
8. Review trigger

## Common Extraction Errors To Avoid

- Treating principles and controls as the same thing
- Duplicating the same control across multiple domains
- Missing workload-specific overlays
- Producing controls with no owner or no evidence path
- Turning legal nuance into false technical certainty
- Keeping statements too vague to test or score
