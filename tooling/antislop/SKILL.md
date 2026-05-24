---
name: antislop
description: Detect and fix AI writing patterns (slop). 45+ patterns across 3 severity tiers with scoring and an editor mode that fixes problems directly.
version: "1.0.0"
tags:
  - writing
  - ai-detection
  - humanizer
  - content-quality
  - editing
tool_agnostic: true
authors:
  - Anders Hybertz
---

## Trigger conditions

Load this skill when the user says any of: "check for slop", "does this sound like AI", "humanize this", "AI audit", "slop check", "clean up AI writing", antislop, or any request to detect or remove artificial-sounding patterns. Also use proactively before publishing any AI-assisted content.

---

## The 30-Second Test

**The Horoscope Test:**

> "Could anyone have written this, for anyone?"

If yes, it's slop. Like a horoscope — technically applicable to everyone, resonant with no one.

What fails:
- Vague claims without specific examples
- Advice that applies universally without context
- Content missing the author's distinct perspective
- Writing that could have any byline

What passes:
- Specific tools, dates, outcomes mentioned
- Personal observations grounded in experience
- Opinions that not everyone would agree with
- Details only this author would know

---

## How It Works

1. Run the Horoscope Test — could anyone have written this for anyone?
2. Scan for patterns — 45+ known AI tells across 6 categories
3. Calculate slop score — tiered severity with quantifiable scoring
4. Apply fixes — editor mode rewrites problems, not just flags them
5. Report changes — before/after for every fix applied

---

## Detection Patterns

### Tier 1: Almost Always AI (Remove Immediately)

These phrases are so strongly associated with AI that their presence alone suggests unedited output.

| Pattern | Example | Fix |
|---------|---------|-----|
| Delve | "Let's delve into..." | Remove or replace with direct statement |
| Game-changer | "This game-changing approach..." | Describe the actual impact |
| Revolutionary | "A revolutionary new method..." | State what it actually does |
| Unlock potential | "Unlock your potential..." | Remove entirely |
| Leverage (as verb) | "Leverage these insights..." | "Use" |
| It's worth noting | "It's worth noting that..." | Just state the thing |
| Moreover/Furthermore | "Moreover, this approach..." | Remove or use "Also" |
| Today's digital landscape | "In today's digital landscape..." | Remove |
| Cutting-edge | "Cutting-edge solutions..." | Remove |
| Pivotal moment | "Marking a pivotal moment in..." | State what happened |
| Tapestry (abstract) | "A rich tapestry of influences..." | Remove or be specific |
| Intricate/intricacies | "The intricacies of..." | "Details of" or remove |
| Showcase (as verb) | "Showcasing their commitment..." | "Shows" or describe what happened |
| Vibrant | "A vibrant community of..." | Remove or use specific detail |
| Interplay | "The interplay between X and Y..." | "How X and Y affect each other" |
| Garner | "Garnering attention from..." | "Got attention from" or be specific |
| Align with | "Aligning with broader trends..." | State the actual relationship |

Research evidence:
- Finnish study (56,878 essays): "delve" usage increased 10.45x post-ChatGPT
- Georgia Tech (168.3M articles): "delve" went from 0.31 to 7.9 per 1,000 papers in Q1 2024
- Biomedical study: co-usage of "delve," "realm," "underscore" increased up to 85x in 2023–2024

### Tier 2: Suspicious When Repeated

Problematic when overused or clustered.

| Pattern | Example | Fix |
|---------|---------|-----|
| Here's the thing | Used repeatedly | Keep first, vary subsequent |
| At the end of the day | "At the end of the day..." | Remove |
| The bottom line | "The bottom line is..." | Just state it |
| Let's dive in | "Without further ado, let's dive in" | Remove |
| Comprehensive and thorough | Paired adjectives | Pick one |
| Simple and straightforward | Paired adjectives | Pick one |
| In this post, we'll cover | Template opening | Remove |
| By the end of this article | Promise opener | Remove |

### Tier 3: Watch for Clusters

Fine individually, problematic together.

| Pattern | Example | Fix |
|---------|---------|-----|
| However/But | Every paragraph starts this way | Vary transitions |
| Firstly/Secondly/Thirdly | Enumerated points | Use natural flow |
| Moving forward | "Moving forward, we'll..." | Remove |
| Robust/Seamless/Scalable | Corporate buzzwords | Use specific terms |
| Stakeholder | "Key stakeholders..." | Name them or say "people" |

---

## Content Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | Significance inflation | "marking a pivotal moment in the evolution of..." | "was established in 1989 to collect statistics" |
| 2 | Notability name-dropping | "cited in NYT, BBC, FT, and The Hindu" | "In a 2024 NYT interview, she argued..." |
| 3 | Superficial -ing analyses | "symbolizing... reflecting... showcasing..." | Remove or expand with actual sources |
| 4 | Promotional language | "nestled within the breathtaking region" | "is a town in the Gonder region" |
| 5 | Vague attributions | "Experts believe it plays a crucial role" | "according to a 2019 survey by..." |
| 6 | Formulaic challenges | "Despite challenges... continues to thrive" | Specific facts about actual challenges |
| 7 | Outline-like conclusions | "Challenges" section ending with optimistic outlook | Remove or replace with actual analysis |

---

## Language Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 8 | Copula avoidance | "serves as... features... boasts..." | "is... has..." |
| 9 | Negative parallelisms | "It's not just X, it's Y" | State the point directly |
| 10 | Rule of three | "innovation, inspiration, and insights" | Use natural number of items |
| 11 | Synonym cycling | "protagonist... main character... central figure..." | "protagonist" (repeat when clearest) |
| 12 | False ranges | "from the Big Bang to dark matter" | List topics directly |
| 13 | Clinical formality | "individuals" / "utilize" / "implement" | "people" / "use" / "do" |

---

## Style Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 14 | Em dash overuse | "institutions--not the people--yet this continues--" | Use commas or periods |
| 15 | Boldface overuse | "**OKRs**, **KPIs**, **BMC**" | "OKRs, KPIs, BMC" |
| 16 | Emoji headers | "🎯 Target Goal / 💡 Key Insight" | Remove emojis |
| 17 | Title Case Headings | "Strategic Negotiations And Partnerships" | "Strategic negotiations and partnerships" |
| 18 | List addiction | Everything becomes bullets | Convert to prose where appropriate |
| 19 | Unnecessary tables | 3-row table that should be a sentence | Convert to prose |

---

## Structural Patterns (Critical)

These bypass phrase-based detection but are major tells.

### Staccato Fragment Spam

Three or more consecutive short declarative sentences stating facts in parallel structure.

Before:
> The model is impressive. Complex code ships fast. Documentation writes itself. Problems get solved quickly.

After:
> The model is impressive — complex code ships in a single session, documentation practically writes itself, and problems that would have taken a weekend now take an afternoon.

Detection rule: 3+ consecutive sentences, all under 10 words, all declarative, parallel structure, could be bullet points.

### Sentence Uniformity

Every sentence 10–15 words. Short. Punchy. Exhausting. Real writing has rhythm — mix 5-word sentences for impact with 25-word sentences that explore implications.

### Comparator Sentences

Before:
> This isn't theoretical. It's practical.
> It's not about X. It's about Y.

After: Just state what it is.

AI loves this rhetorical pattern. It sounds punchy but wastes words telling you what something isn't.

### Over-Balanced Sections

Every section same length. All paragraphs 3–4 sentences. AI doesn't have opinions, so it gives balanced coverage to everything. Real writing reflects priorities.

---

## Communication Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 20 | Chatbot artifacts | "I hope this helps! Let me know if..." | Remove entirely |
| 21 | Cutoff disclaimers | "While details are limited in available sources..." | Find sources or remove |
| 22 | Sycophantic tone | "Great question! You're absolutely right!" | Respond directly |
| 23 | Flattery sandwiches | "While traditional methods have merit, modern approaches offer..." | State your actual position |

---

## Advanced Structural Tells

### Manufactured Personality

Before:
> Five services. Five tabs. Five headaches. That got old fast.

After:
> I use five different services for my workflow. They're solid platforms, but like most SaaS tools, each means another dashboard, another context switch.

### Self-Promotional Framing

Before:
> I shipped 11 projects over the holidays. Here's what I learned.

After:
> Most developers aren't aware that [observation about the reader's situation].

The author's experience is evidence, not the story.

### Explanatory Header Templates

Headers that promise insight but deliver template structure:
- "Why This Actually Works"
- "What This Means For You"
- "The Real Reason..."
- "Here's What's Really Going On"

Fix: Replace with descriptive headers that summarize actual content.

---

## Filler and Hedging

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 24 | Filler phrases | "In order to" / "Due to the fact that" | "To" / "Because" |
| 25 | Excessive hedging | "could potentially possibly" | "may" |
| 26 | Generic conclusions | "The future looks bright" | Specific plans or facts |

---

## Scoring System

| Pattern Type | Points |
|--------------|--------|
| Each Tier 1 phrase | +3 |
| Each Tier 2 phrase (repeated) | +2 |
| Tier 3 cluster (3+ in section) | +2 |
| Failed horoscope test | +5 |
| Staccato fragment spam (per instance) | +4 |
| Sentence uniformity detected | +3 |
| Comparator sentences (per instance) | +2 |
| Manufactured personality | +4 |
| Self-promotional framing | +5 |
| Template headers (per instance) | +2 |

Score interpretation:
- 0–5: Low risk (minor edits)
- 6–12: Medium risk (significant editing required)
- 13+: High risk (likely unedited AI output)

---

## Editor Mode (Default)

This skill is an editor, not a critic. After detection:

1. Apply all fixes directly using the Edit tool
2. Report changes made with before/after examples
3. Save the cleaned file in place

Fix priority:
1. Remove all Tier 1 phrases
2. Deduplicate Tier 2 phrases (keep first, vary subsequent)
3. Break up staccato fragments (combine with em-dashes, commas, conjunctions)
4. Fix comparator sentences (just state what it is)
5. Vary sentence lengths where uniformity detected

To audit without editing, user must explicitly request "audit only."

---

## Output Format

```
## AntiSlop Report

**Horoscope Test:** [PASS/FAIL] — [reason]
**Slop Score:** [X] → [Y] — [Risk Level]

### Fixes Applied

| Location | Before | After |
|----------|--------|-------|
| Line 3 | "Let's delve into the details" | "Here are the details" |

### Remaining Considerations
- [Any issues requiring human judgment]

### The Core Principle
Your voice is in the specificity, the opinions, the rough edges, and the rhythm. Protect those.
```

---

## Pattern Refresh Protocol

Patterns go stale as AI models evolve. Check `last-refreshed` in frontmatter. If >30 days old, refresh first.

Refresh workflow:

1. Fetch latest patterns from Wikipedia:

```bash
curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=Wikipedia:Signs_of_AI_writing&prop=wikitext&format=json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data['parse']['wikitext']['*'][:30000])
" > /tmp/antislop-signs.txt

curl -s "https://en.wikipedia.org/w/api.php?action=parse&page=Wikipedia:WikiProject_AI_Cleanup&prop=wikitext&format=json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data['parse']['wikitext']['*'][:30000])
" > /tmp/antislop-cleanup.txt
```

2. Read output and diff against patterns already in this skill
3. For genuinely new patterns not already covered: classify into Tier 1/2/3, add to appropriate table with example and fix, update pattern count
4. Update `last-refreshed` date in frontmatter
5. Report what was added (if anything)

Don't add duplicates — many Wikipedia patterns are already covered here under different names.

---

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- Finnish study on "delve" usage (56,878 essays)
- Georgia Tech analysis (168.3M articles)

---

## Core Principle

AI slop isn't about individual words — it's about patterns.

One "moreover" doesn't make content AI-generated. But "moreover" + "it's worth noting" + "delve into" + uniform sentences + emoji headers = obvious slop.

The goal is writing that sounds like a specific human with specific opinions, not a very polite committee trying not to offend anyone.
