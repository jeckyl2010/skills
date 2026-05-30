---
name: senior-ui-ux
description: Apply senior UI/UX judgment to interfaces, user flows, interaction details, and product usability decisions.
version: "1.0.3"
tags: [ux, ui, accessibility, wcag, usability, copywriting, consultancy-sites]
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []
---

# Senior UI/UX

Use this skill when evaluating pages, forms, navigation, dashboards, onboarding, interaction flows, information architecture, or visual/interaction polish.

## Goals
- Optimize for clarity, trust, speed of comprehension, and task completion.
- Reduce friction, ambiguity, and cognitive load.
- Balance aesthetics with accessibility and usability.
- Treat UX as part of product strategy, not just visual styling.

## Default lens
1. Start from user goals, not UI components.
2. Identify the primary action on each screen.
3. Remove unnecessary choices, fields, and distractions.
4. Make system status, feedback, and next steps obvious.
5. Design for mobile, accessibility, and edge cases by default.
6. Protect trust with clear language, consistent behavior, and predictable interactions.

## Review checklist
- Is the user's primary task obvious?
- Is the visual hierarchy clear in under 5 seconds?
- Are labels and copy plain, specific, and action-oriented?
- Are calls to action distinguishable and appropriately prioritized?
- Are spacing, alignment, and grouping supporting comprehension?
- Is error prevention better than error recovery?
- Is the experience accessible: contrast, focus, keyboard use, semantics, target size?
- Does the flow minimize user effort and unnecessary decisions?

## Output structure
When useful, structure responses as:
- User goal
- Friction points
- Recommended UX changes
- Visual hierarchy / content notes
- Accessibility concerns
- Mobile / responsive concerns
- Expected impact

## Accessibility — WCAG contrast audits

When working on dark-background design systems, run a contrast audit before shipping. The WCAG AA thresholds are 4.5:1 for normal text and 3.0:1 for large text (18pt+ or 14pt bold).

Use `scripts/wcag-contrast-check.py` — paste in the colour tokens and get a pass/fail table.

### CSS token strategy for dark surfaces

Keep two accent tokens when the brand accent is a mid-range blue/purple (e.g. `#5352cc`):

```css
--accent:       #5352cc;   /* backgrounds, borders, focus rings — never as text */
--accent-text:  #7c7bef;   /* text and icons on dark surfaces — lighter, passes AA */
```

`#5352cc` on near-white nav passes (5.78), but on a dark background (#0d0d10) it's 3.18 — fails normal text. The lighter `#7c7bef` gives 5.49 on dark. Never use `--accent` for text on dark backgrounds.

`--dark-text-3` (metadata, secondary labels on dark surfaces) must be at least `#7c7c7c` on `#0d0d10` to clear 4.65. The naive default of `#52525b` is 2.51 — hard fail.

### Programmatic audit workflow

1. Extract all colour token pairs (text colour + background it appears on)
2. Run the WCAG formula: linearize each channel, compute luminance, ratio = (L1+0.05)/(L2+0.05)
3. Flag anything below 4.5 on normal-sized text, below 3.0 on large text
4. Adjust token values until all pass — favour adjusting the text token, not the background
5. Check that accent-as-background (buttons, borders) is not affected by the text token change

See `scripts/wcag-contrast-check.py` for the ready-to-run script.

## Strong defaults
- One primary action per view or section.
- Short headings and concrete labels.
- Progressive disclosure over overwhelming density.
- Consistent spacing and typography scales.
- Immediate feedback for user actions.
- Accessible interactions and resilient layouts.

## Trust-heavy marketing and consultancy pages

When working on consultancy, portfolio, or other trust-led marketing pages:
- Optimize first for fast scanning, then for depth.
- Do not open with walls of testimonial text when shorter proof signals establish credibility faster.
- Prefer an editorial proof structure: short signal cards or pull quotes first, fuller recommendations second, complete source text behind progressive disclosure.
- Frame pages by job-to-be-done: homepage = value proposition, services = when to hire, about = working style and credibility, testimonials = proof, contact = low-friction next step.
- When a user expresses a clear preference for concrete homepage wording, preserve it instead of replacing with something more abstract.
- For Danish/Nordic professional-services pages, prefer language that is calm, credible, and craftsmanship-led before it is clever.
- A restrained memorable twist is welcome when it sharpens recall without lowering trust. Understated wit, not campaign theatrics.
- Place the twist in supporting copy, proof framing, or CTA context before the main value proposition; headlines and service naming usually need to stay more sober.
- Treat metaphor and motif language as a limited budget. One or two related lines add recall; repeating across multiple pages starts to feel self-conscious.
- If a line feels showy, salesy, or performing for attention, dial it back until it reads like quiet confidence.
- For cautious professional-services buyers, a CTA frame like "When to reach out" can work better than generic invitation copy.
- On a one-person consultancy, keep the founder's name in secondary CTAs ("Contact Anders", not just "Contact"). The name is a differentiator — it signals a real person, not a form routed to a team. Generic CTA labels erode this. Only shorten if the button is in a context where the name is already visually present directly above it.
- To express that a consultant "listens" without stating it: use specificity of problem description. Name the frustrations clients actually have. Precise, recognisable pain points read as earned experience. Vague positioning reads as defensive.
- Distinguish "good practices" from "best practices" in copy. "Best practice" ends thinking. "Good practice" keeps judgment alive. This signals seniority and independence from methodology sales.
- When rewriting a strength/value card that currently states what you don't do, rewrite it to state what you actually do and why. Negative framing is weaker than affirmative framing.
- On multi-page copy passes, align homepage and proof/testimonials first, then propagate tone into about, services, and contact. This reduces drift.
- Once the site reads coherently and remaining issues are taste-level microcopy, prefer stopping over circular polishing.

## Professional-services / consultancy website reviews
When reviewing a solo consultant, boutique agency, or high-trust professional-services site:
- Judge the site first on credibility, scannability, and buyer fit — not on novelty.
- Give each page a distinct job: Home = positioning, Services = when to hire, About = working style and trust, Testimonials = proof, Contact = friction removal.
- Flag repeated positioning language across pages; repeated good messaging still weakens clarity when every page says the same thing in slightly different words.
- Treat long testimonials as a presentation problem, not a content problem: recommend excerpts, pull-quotes, and progressive disclosure before cutting proof entirely.
- Push service sections to answer "when should I hire this person?" and "what outcome do I get?", not just "what can they do?"
- Prefer conversion support for cautious buyers: concrete reasons to reach out, what to include in a first message, and what happens next.
- If the site already has a strong calm/premium tone, prefer tightening and re-sequencing over rewriting the brand voice.

## Animation and motion constraints

Anders's projects follow a strict motion policy:
- Opacity-only fades are acceptable: `initial={{ opacity: 0 }} animate={{ opacity: 1 }}`
- Y-axis slides (`y: 20`, `y: -10`, etc.) are NOT acceptable — even small ones
- Staggered list entry animations (`delay: index * 0.05`) are NOT acceptable
- Framer-motion is a large dependency that tends to get applied pervasively and with the wrong defaults. Before adding it to a project, confirm the scope is limited to a controlled wrapper component that enforces the above constraints
- If framer-motion is already in a project: audit all usages. Replace staggered-slide patterns with a single constrained wrapper or drop the library in favour of CSS `transition-opacity`
- The correct consolidation: create one `<FadeIn>` wrapper component that only ever does opacity fade (short duration, no y, no stagger), and route all motion through it

## Pitfalls to avoid
- Optimizing for visual novelty over usability
- Too many competing calls to action. Three hero CTAs is one too many — the third dilutes conversion without adding authority.
- Off-platform CTAs in the hero: any button that sends a visitor to another product (ChatGPT, LinkedIn, etc.) during initial evaluation hands over narrative control at the worst possible moment. Even well-implemented off-platform features (structured prompts, guided flows) belong lower on the page, not in the primary conversion zone.
- Vague microcopy and unlabeled states
- Hidden interactions without affordances
- Ignoring loading, empty, error, and success states
- Desktop-first thinking for broadly used interfaces
- Long testimonial pages that make strong proof hard to scan
- Repeating the same positioning message across every page until differentiation flattens
- Turning service pages into taxonomy dumps instead of decision-support pages
- Rewriting user-preferred hero copy toward something more generic or abstract
- Eyebrow label colour drift: when a page has multiple section labels using different CSS classes, they can silently get different colour tokens. Both are doing the same job so they must use the same token.
- Redundant progressive disclosure cues on the same card: one disclosure affordance per card. The action link is the one to keep; the explanatory label is the one to remove.
- Contact page metadata creep: timezone notes, response-SLA qualifiers, and operating-hours caveats add friction. A single "Usually replies within one business day." is enough.
- Defensive copy on solo-operator sites: stating what is already implied ("no account managers", "one senior point of contact") signals insecurity rather than confidence. The visitor has already inferred these from the fact it's a one-person consultancy. Any copy that explains what you don't have belongs in the bin.
- Orphaned secondary links: demoting a channel (e.g. LinkedIn) to a plain text link floating below a card creates visual orphaning. If the channel belongs at all, keep it inside the same card structure — same layout class, same row pattern — so it reads as part of the system rather than an afterthought.

## Support files

- `references/consultancy-proof-pages.md` — compact notes on presenting testimonial-heavy consultancy pages for scan-first trust building.
- `references/high-trust-consultancy-sites.md` — review framework for professional-services sites.
- `scripts/wcag-contrast-check.py` — paste in colour token pairs, get a WCAG AA pass/fail table.
