# Wiki Schema — AI Coding Tools Landscape

## Domain

AI-assisted coding tools, agent frameworks, and IDE integrations as of 2026.
Covers capabilities, pricing, runtime models, and how tools compare.

## Conventions

- File names: lowercase, hyphens (e.g., `github-copilot.md`, `agentic-coding.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages — minimum 2 outbound links per page
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [tag1, tag2]
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy

- tool
- cli
- ide
- agent
- api
- company
- open-source
- comparison
- benchmark
- trend
- agentic-coding
- llm
- mcp
- copilot
- context-window
- deprecated

## Page Thresholds

- **Create a page** when a tool/concept appears in 2+ sources OR is central to one source
- **Update an existing page** when a source adds new information
- **Do not create** pages for passing mentions or tools outside the AI coding domain
- **Split** pages over 200 lines

## Update Policy

This space moves fast. When new information conflicts with existing content:
1. Preserve the old claim with its date
2. Add the new information with its date
3. Mark `contradictions: [page]` in frontmatter if genuinely contradictory
