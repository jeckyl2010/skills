---
name: confluence-rovo-ai
description: Configure and surface Rovo AI features in Confluence Cloud — Chat, custom Agents, Space Agent assignment, and space homepage CTA patterns.
version: "1.0.0"
tags: [confluence, rovo, atlassian, ai, documentation, rag]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Confluence Rovo AI Setup

## Triggers
Use this skill when asked about AI chat in Confluence, Rovo setup, space-scoped Q&A, or surfacing an AI assistant on a Confluence space homepage.

## Plan check
- What Confluence plan tier is the org on? Rovo requires Premium or Enterprise (or Rovo add-on).
- Does the user have space admin rights? Required for Space Agent assignment.
- Does the user have site admin rights? Required for site-level Atlassian Intelligence toggle.

## Feature map (as of May 2025)

| Feature | Status | Access |
|---|---|---|
| Rovo Chat sidebar panel | GA | All pages, right sidebar |
| Rovo Search | GA | Search bar |
| Rovo Agents (pre-built) | GA | Via Rovo Chat |
| Custom Rovo Agents | GA | Rovo Studio (team.atlassian.com) |
| Space Agent assignment | GA | Space Settings > Space agent |
| /rovochat embed macro | Limited private beta | Not yet GA |
| Atlassian Intelligence (writing, summarize) | Premium/Enterprise | Site admin toggle |

## Rovo Chat — quick scope test
Before building anything, test: open Rovo Chat and ask "What does this space say about [topic]?" If it returns relevant answers, scoping via conversation prompt is sufficient for usability. Don't build what the native tool already does.

## Custom Rovo Agent — creation steps
1. Go to Rovo Studio: team.atlassian.com > Rovo > Agents > Create agent
2. The builder opens with a natural language prompt: "What are we building?" — describe the use case in plain English.
3. Review generated config: name, avatar, description, system prompt, knowledge sources.
4. Skills (actions): only add if the agent needs to DO things beyond Q&A (create Jira issues, update pages). For pure documentation Q&A — skip skills entirely.
5. Web Search: disable for space-scoped documentation agents. Enabling it allows internet answers, defeating the scoping intent.
6. Save > Publish. Only published agents are assignable or findable in Rovo Chat.

## Space Agent — surface agent on space homepage
Requires: space admin rights + published agent.

1. Navigate to the Confluence space.
2. Space settings > Space agent > Assign agent.
3. Browse/search published agents > select yours.
4. Result: agent appears as a button on the space homepage and at the top of the agents list when any user clicks the AI icon on any page in the space.

All space users including guests can use it once assigned.

## Space homepage CTA (no macro, no admin rights needed)
If the /rovochat macro is not yet available on the instance, a Confluence Panel macro works as a lightweight CTA:

- Insert a Panel macro (blue background, #0052CC)
- Heading: "Ask the Documentation Assistant"
- Subtext: "Get instant answers from this space — powered by Rovo AI"
- Link button pointing to the agent URL or Rovo Chat

Two minutes in the editor, zero admin rights required. Visually prominent without being garish.

## Pitfalls

- The /rovochat embed macro is NOT generally available. Typing /rovochat in the editor will fail on most instances. Use the Space Agent + Panel CTA approach instead.
- Rovo features require Premium/Enterprise or a Rovo add-on. On Free/Standard the menus either don't appear or prompt for upgrade.
- Site-level Atlassian Intelligence must be enabled first by a site admin before space-level settings appear. Space admin cannot unblock this alone.
- Space Agent button on homepage is the primary discovery point — users will not naturally find an agent via the AI toolbar icon. Document the access path for your team.
- Rovo Chat by default searches ALL spaces the user has read access to. For usability scoping, rely on conversation prompts ("Only answer from [Space Name]") or the Space Agent config, not a hard technical restriction.

## References
- references/rovo-feature-status-may2025.md — feature availability research from session
