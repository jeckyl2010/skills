---
name: technical-documentation-writing
description: Write unambiguous technical documentation — short sentences, active voice, explicit nouns, literal verbs, no pronoun ambiguity.
version: "1.0.0"
tags: [documentation, writing, technical-writing, clarity, style-guide]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Technical Documentation Writing

Write clear, precise instructions. Eliminate all linguistic ambiguity.

## Use When

- The task produces user-facing instructions, procedures, or reference documentation
- A document must survive translation or non-native readers
- Existing documentation is vague, passive, or pronoun-heavy and needs a rewrite

## Do Not Use When

- The output is prose meant to persuade or explain trade-offs (use consulting-deliverable instead)
- The task is removing AI writing patterns from existing copy (use antislop or ai-humanizer instead)
- The audience expects narrative, marketing, or conversational tone

## Structural Constraints

1. Limit descriptive sentences to a maximum of 20 words.
2. Limit instructional steps to a maximum of 15 words.
3. Limit paragraphs to a maximum of 3 sentences.
4. Use bulleted fragments for multi-item sequences. Do not embed lists inside narrative text.

## Grammar and Vocabulary Rules

1. Do not use the pronouns "it", "this", "that", "they", or "these" to refer to a previous concept. Always repeat the explicit noun.
2. Write exclusively in the active voice. Do not use passive verb configurations (e.g., "the variable is modified by").
3. Use single, literal verbs. Do not use phrasal verbs (e.g., use "start" instead of "spin up", use "remove" instead of "take down").
4. Limit noun strings to a maximum of two consecutive words. Use prepositions to break apart dense noun chains.
5. Pair a specific interface name with its literal functional type (e.g., "the Save button", "the configuration directory").

## Workflow

- Read the technical query from the user.
- Draft the technical response.
- Review every sentence against the structural constraints before output generation.
- Correct any pronoun ambiguity or passive phrasing.
- Output the finalized, compliant text.
