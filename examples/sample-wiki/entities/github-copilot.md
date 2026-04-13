---
title: GitHub Copilot
created: 2026-01-15
updated: 2026-04-13
type: entity
tags: [tool, copilot, ide, cli, company]
sources: [raw/articles/github-copilot-product-page.md]
---

# GitHub Copilot

GitHub's AI coding assistant, developed by GitHub (Microsoft) and launched in 2021.
Available as an IDE extension (VS Code, JetBrains, Neovim) and as a CLI (`gh copilot`).

## Key Capabilities

- Inline code completion and multi-line generation
- Chat interface for code explanation and refactoring
- **Agent Mode (CLI)**: autonomous multi-step coding via Plan, Autopilot, and Fleet modes
- Built-in GitHub MCP: native access to Issues, PRs, and Actions
- Background agents: delegate long-running tasks to cloud agents via `&` or `/delegate`
- Fleet mode: parallel execution of the same task across many files

## Models Available (2026)

- GPT-4.1, GPT-4.1-mini (OpenAI)
- Claude Sonnet 4.6, Claude Opus 4.6 (Anthropic)
- Gemini 3 Pro (Google)

## Pricing (as of 2026-01-15)

- Individual: $10/month (2,000 completions, 50 chat messages)
- Business: $19/user/month (unlimited, admin controls)
- Enterprise: $39/user/month (fine-tuning, compliance)

## Relationships

Part of the broader [[agentic-coding]] trend. Competes with tools like [[claude-code]]
and follows patterns described in the [[karpathy-llm-wiki-pattern]] for knowledge
management. In CLI-heavy work, the practical trade-off often comes down to
[[github-copilot-vs-claude-code]] and how much available [[context-window]] matters.

## Notes

- Copilot CLI reads `.github/copilot-instructions.md` automatically at session start
- Session SQL: built-in SQLite per session for todo tracking
- Cross-session memory via `session_store`
