---
title: Agentic Coding
created: 2026-01-15
updated: 2026-04-13
type: concept
tags: [agentic-coding, agent, trend, llm]
sources: [raw/articles/karpathy-llm-wiki-gist.md]
---

# Agentic Coding

A shift from AI-as-autocomplete to AI-as-autonomous-engineer. The agent plans a
multi-step task, writes code, runs tests, interprets errors, and iterates —
with the human reviewing and approving rather than typing every character.

## Key Characteristics

- **Multi-step execution**: the agent issues a sequence of tool calls (read, edit, run, search)
- **Self-correction**: reads test output and error messages, then revises its approach
- **Long-horizon planning**: breaks a high-level goal into subtasks before coding
- **Tool use**: accesses the filesystem, terminal, web, and external APIs

## Why It Matters

Traditional autocomplete is synchronous and single-token. Agentic coding is asynchronous
and operates at the level of features or bug fixes. This changes what skills developers
need: prompt engineering and task decomposition become more valuable than typing speed.

## Current Tools

- [[github-copilot]] — Plan Mode, Autopilot, Fleet, Background Agents
- [[claude-code]] — CLI-native agent with tool use
- Cursor — composer agent mode
- Codex CLI — OpenAI's CLI agent

## Open Questions

- Where is the right level of autonomy? Full autopilot vs. human-in-the-loop at each step
- How do agents handle ambiguous requirements?
- Cost: agentic sessions consume significantly more tokens than autocomplete

## See Also

[[karpathy-llm-wiki-pattern]] — a related idea: instead of re-reading sources every session,
compile knowledge once. Both patterns aim to reduce redundant AI work.
[[github-copilot-vs-claude-code]] — sample comparison of two CLI-capable agent tools  
[[best-tool-for-agentic-coding]] — filed answer worth keeping in the wiki
