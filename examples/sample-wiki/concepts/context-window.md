---
title: Context Window
created: 2026-01-15
updated: 2026-04-13
type: concept
tags: [llm, context-window, trend]
sources: [raw/articles/context-window-notes.md]
---

# Context Window

The amount of text and structured context a model can work with in one pass.
In AI coding workflows, this often determines whether the agent can reason over
an entire task without repeatedly rebuilding context.

## Why It Matters

Larger context windows help tools like [[github-copilot]] and [[claude-code]] keep
more repository state, prior decisions, and source material active in one turn.
That makes them more useful for sustained [[agentic-coding]] sessions.

## Tradeoffs

- Larger windows do not automatically guarantee better judgment
- More context can increase cost and latency
- Teams still need structure, which is why the [[karpathy-llm-wiki-pattern]] matters

## See Also

- [[best-tool-for-agentic-coding]]
- [[github-copilot-vs-claude-code]]
