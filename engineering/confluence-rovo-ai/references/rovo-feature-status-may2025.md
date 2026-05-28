# Rovo Feature Status — May 2025 Research

Source: Atlassian Community + Atlassian Support docs, verified May 2025.

## /rovochat macro (beta)
- Announced in Atlassian Community thread qaq-p/2916987
- Atlassian Team (Liam C, Apr 2025): "scoped to a particular space, label, or ancestor page. Looking at releasing in beta Q2 2025."
- Atlassian Team (Matt B, May 2025): "currently in beta and available to a limited number of customers. Expect to gradually expand access."
- NOT GA as of May 2025. No firm GA date.
- Invoke via /rovochat or /rovo chat in Confluence editor (when available).

## Space Agent (GA)
- Official docs: https://support.atlassian.com/confluence-cloud/docs/set-up-a-rovo-agent-for-your-confluence-space/
- Space Settings > Space agent > Assign agent
- Agent appears as button on space homepage + top of agents list on all pages in space
- Requires: published agent + space admin rights
- Available to all users in space including guests

## Rovo Agent builder
- Rovo Studio: https://team.atlassian.com
- Natural language "What are we building?" prompt bootstraps the config
- Must Publish before agent is assignable or visible in Rovo Chat
- Actions (skills): only relevant for agents that need to take action, not pure Q&A

## Rovo Chat scoping behaviour
- Default: searches all spaces user has read access to
- Soft-scoping: conversational prompt "Only answer from [Space Name]"
- Hard-scoping: only achievable via custom RAG build outside Atlassian stack
- Space Agent config influences default context but is not a hard restriction
