---
title: Karpathy LLM Wiki Pattern
created: 2026-01-15
updated: 2026-04-13
type: concept
tags: [tool, llm, trend]
sources: [raw/articles/karpathy-llm-wiki-gist.md]
---

# Karpathy LLM Wiki Pattern

A knowledge management approach where an AI agent maintains a persistent, interlinked
markdown knowledge base instead of re-reading raw sources every session.
Described by Andrej Karpathy in a GitHub gist.

## The Core Insight

Traditional RAG re-discovers knowledge from raw documents on every query.
A compiled wiki keeps cross-references, contradiction flags, and synthesis already built.
Knowledge compounds across sessions rather than starting over.

## Architecture

Three layers:
1. **Raw sources** — immutable ingested material (articles, PDFs, transcripts)
2. **Wiki pages** — agent-maintained entities, concepts, comparisons, queries
3. **Schema** — domain conventions, tag taxonomy, structural rules

## Operations

- **Ingest**: save raw source → discuss with user → find existing pages → create/update → update index + log
- **Query**: read index → find relevant pages → synthesize → optionally file the answer
- **Lint**: detect orphans, broken links, index gaps, stale content, tag violations

## Tradeoffs

**vs. RAG**: Wiki requires upfront curation. RAG works on any unstructured corpus.
Wiki scales better for recurring queries in a stable domain; RAG for ad-hoc wide-scope research.

**vs. plain notes**: Wiki enforces cross-references and consistency checks. Plain notes
are faster to start but degrade into disconnected files over time.

## See Also

[[agentic-coding]] — related trend: AI that maintains state across sessions  
[[github-copilot]] — one runtime where this pattern can be applied via llm-wiki-skill  
[[best-tool-for-agentic-coding]] — example of a durable answer filed back into the wiki
