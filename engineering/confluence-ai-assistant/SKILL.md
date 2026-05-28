---
name: confluence-ai-assistant
description: Advise on Confluence Cloud AI — Atlassian Intelligence, Rovo Chat, Rovo Chat macro, plan tier detection, and space-level AI scoping.
version: "1.0.0"
# Last verified: May 2025 — re-check Rovo Chat macro GA status in future sessions
tags: [confluence, atlassian, rovo, ai, rag, knowledge-management]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Confluence AI Assistant — Advisory Skill

## Trigger conditions
- User asks about adding AI chat to Confluence
- User asks about RAG over a Confluence space
- User asks about Atlassian Intelligence or Rovo
- User asks how to scope AI answers to a specific space

---

## Landscape (as of May 2025)

### Atlassian Intelligence
Built into Confluence Cloud Premium and Enterprise. Gives an "Ask AI" sidebar. Zero setup if already on that tier.
Check: Site Settings > Atlassian Intelligence. If the menu item is absent, the org is on Free or Standard.

### Rovo
Atlassian's broader AI product — Rovo Chat, Rovo Search, Rovo Agents. Available on Premium/Enterprise and as an add-on. Presence of a "Rovo" entry in the Confluence nav/sidebar is a reliable signal the org has it enabled.

Rovo Chat is available as a **sidebar panel** on all Confluence pages (GA). It can be scoped to the current page or space during a conversation via soft-prompting: "Answer only from the [Space Name] space."

### Rovo Chat macro (/rovochat) — Beta
An embeddable chat widget that drops onto a Confluence page via `/rovochat` in the editor.
- Scoped to: space, label, or ancestor page
- Status: limited private beta as of May 2025; gradual rollout, no firm GA date
- Source: Atlassian Community thread + Atlassian team member confirmation (see references/)
- To test: type `/rovo` in the Confluence editor — if the macro appears, the instance is in the rollout

---

## Detecting plan tier without admin rights

Non-admins cannot see billing directly. Indirect signals in order of reliability:

1. Look for a Rovo icon or "Rovo" menu entry anywhere in the UI — presence = Premium or Enterprise
2. Look for an AI sparkle icon in the editor toolbar or page actions
3. Try https://admin.atlassian.com — if you can see billing, you have org admin rights
4. Settings gear > Billing — usually blocked for non-admins, but worth checking

Fastest: ask the IT contact or Atlassian admin directly.

---

## Scoping strategy

| Goal | Approach |
|---|---|
| Hard scope (only one space, no leakage) | Custom RAG build — only option that guarantees it |
| Soft scope (usability, not confidentiality) | Rovo Chat sidebar + prompt: "Only from [Space Name]" |
| Embedded page chat | Wait for Rovo Chat macro GA, or try /rovochat if beta available |

For usability-only scoping: the soft-prompt approach is pragmatic. Validate empirically — run representative questions and check for cross-space noise before building anything.

---

## Custom RAG path (if needed)

Source of truth already in two places:
- Markdown in git (clean, cheap to embed)
- Confluence via REST API

Stack outline:
1. Chunk markdown files
2. Embed (OpenAI, local model)
3. Store in vector DB (Qdrant, Chroma, pgvector)
4. Wrap a retrieval + generation API
5. Surface in Confluence via Forge app or iframe macro

Realistic effort: 1-2 focused weeks. Only warranted if hard scoping or data sovereignty is required.

---

## References
- `references/rovo-chat-macro-beta.md` — Atlassian Community thread excerpts and team member confirmation of Rovo Chat macro beta status
