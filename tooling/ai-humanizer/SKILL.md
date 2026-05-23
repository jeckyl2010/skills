---
name: ai-humanizer
version: 2.5.1
description: "Remove AI writing patterns. Fixes 29 named tells: inflated significance, vague attribution, em dash overuse, AI vocabulary, soulless structure."
tags: [writing, editing, humanizer, ai-writing, copy, documentation]
tool_agnostic: true
---

# AI Humanizer

Identify and remove signs of AI-generated text to make writing sound natural and human. Based on Wikipedia's "Signs of AI writing" guide (WikiProject AI Cleanup).

## Your Task

When given text to humanize:

1. Scan for the patterns listed below
2. Rewrite problematic sections — replace AI-isms with natural alternatives
3. Preserve meaning — keep the core message intact
4. Maintain voice — match the intended tone (formal, casual, technical)
5. Add soul — don't just remove bad patterns; inject actual personality
6. Do a final anti-AI pass: ask "What makes this so obviously AI generated?" Answer briefly with remaining tells, then revise

## Voice Calibration (Optional)

If the user provides a writing sample, analyze it before rewriting:

1. Note sentence length patterns, word choice level, paragraph starts, punctuation habits, verbal tics, transition style
2. Match their voice in the rewrite — don't just remove AI patterns, replace them with patterns from the sample
3. When no sample is provided, fall back to natural, varied, opinionated voice

### How to provide a sample
- Inline: "Humanize this. Here's a sample of my writing: [sample]"
- File: "Humanize this. Use my writing style from [file path] as a reference."

## What Good Writing Has

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop.

- Opinions, not just neutral reporting
- Varied rhythm — short punchy sentences, then longer ones that take their time
- Acknowledgment of complexity and mixed feelings
- First person when it fits
- Specific feelings, not vague concern
- Some mess allowed — tangents, asides, half-formed thoughts are human

## Content Patterns

### 1. Inflated Significance
Words: stands/serves as, testament/reminder, vital/significant/crucial/pivotal/key role, underscores/highlights importance, reflects broader, symbolizing, contributing to, setting the stage, marks a shift, key turning point, evolving landscape, indelible mark, deeply rooted

Remove statements about how arbitrary things represent or contribute to broader topics.

### 2. Undue Notability Claims
Words: independent coverage, local/regional/national media outlets, active social media presence

Replace with specific, sourced facts.

### 3. Superficial -ing Analyses
Words: highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

Remove present participle phrases tacked on to add fake depth.

### 4. Promotional Language
Words: boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, nestled, in the heart of, groundbreaking, renowned, breathtaking, stunning

Replace with plain description.

### 5. Vague Attributions
Words: Industry reports, Observers have cited, Experts argue, Some critics argue, several sources

Replace with named, specific sources.

### 6. Formulaic Challenges Sections
Words: Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

Replace with specific facts.

## Language Patterns

### 7. AI Vocabulary Overuse
High-frequency AI words: actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant

These words co-occur in AI text. Remove or replace.

### 8. Copula Avoidance
Words: serves as/stands as/marks/represents [a], boasts/features/offers [a]

Replace with simple is/are/has.

### 9. Negative Parallelisms and Tailing Negations
"Not only...but...", "It's not just about...", tailing fragments like "no guessing", "no wasted motion"

Rewrite as straightforward clauses.

### 10. Rule of Three Overuse
Ideas forced into groups of three to appear comprehensive. Break the pattern.

### 11. Synonym Cycling
AI substitutes synonyms to avoid repetition. Pick one word and use it consistently.

### 12. False Ranges
"From X to Y" where X and Y aren't on a meaningful scale. Rewrite as a plain list.

### 13. Passive Voice and Subjectless Fragments
"No configuration file needed", "The results are preserved automatically." Add the actor.

## Style Patterns

### 14. Em Dash Overuse
LLMs use em dashes (—) more than humans. Replace most with commas, periods, or parentheses.

### 15. Boldface Overuse
AI bolds phrases mechanically. Remove bold from inline text that isn't genuinely critical.

### 16. Inline-Header Bullet Lists
Items starting with **bolded header:** followed by a sentence. Merge into prose.

### 17. Title Case in Headings
## Strategic Negotiations And Global Partnerships → ## Strategic negotiations and global partnerships

### 18. Emojis in Headings or Bullets
Remove. Replace with plain text.

### 19. Curly Quotation Marks
Replace "..." (curly) with "..." (straight) where consistency requires it.

## Communication Patterns

### 20. Chatbot Artifacts
"I hope this helps", "Of course!", "Certainly!", "Would you like...", "let me know", "here is a..."
Remove entirely.

### 21. Knowledge-Cutoff Disclaimers
"As of [date]", "Up to my last training update", "While specific details are limited..."
Replace with what is actually known or admit the gap plainly.

### 22. Sycophantic Tone
"Great question!", "You're absolutely right!", "That's an excellent point."
Remove. State the substance directly.

## Filler and Hedging

### 23. Filler Phrases
"In order to achieve this goal" → "To achieve this"
"Due to the fact that" → "Because"
"At this point in time" → "Now"
"The system has the ability to" → "The system can"
"It is important to note that" → remove

### 24. Excessive Hedging
"It could potentially possibly be argued that... might have some effect" → "It may affect"

### 25. Generic Positive Conclusions
"The future looks bright", "Exciting times lie ahead", "a major step in the right direction"
Replace with a specific fact about what happens next.

### 26. Hyphenated Word Pair Overuse
third-party, cross-functional, client-facing, data-driven, decision-making, high-quality, real-time, end-to-end

Humans are inconsistent with these. Use sparingly and inconsistently, as a human would.

### 27. Persuasive Authority Tropes
"The real question is", "at its core", "in reality", "what really matters", "fundamentally", "the heart of the matter"

These add ceremony to ordinary statements. Remove the framing, keep the point.

### 28. Signposting and Announcements
"Let's dive in", "let's explore", "here's what you need to know", "without further ado"

Start the content. Don't announce it.

### 29. Fragmented Headers
A heading followed by a one-line paragraph that restates the heading before the real content. Remove the filler sentence, start with the substance.

## Process

1. Read the input text carefully
2. Identify all instances of the patterns above
3. Rewrite each problematic section
4. Verify the revised text sounds natural when read aloud, varies sentence structure, uses specific details over vague claims, and maintains appropriate tone
5. Draft humanized version
6. Ask: "What makes this so obviously AI generated?" — answer briefly with remaining tells
7. Revise based on the audit
8. Present the final version

## Output Format

1. Draft rewrite
2. Remaining AI tells (brief bullets)
3. Final rewrite
4. Brief summary of changes made (optional)

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.
Key insight: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
