# Wiki Schema — Technology Landscape

> Copy this file to `$wiki/SCHEMA.md` and customize the Domain and Tag Taxonomy
> sections for your specific technology area. Delete this comment block when done.

## Domain

[What this wiki covers — be specific. Examples:
"AI coding tools and agent frameworks as of 2026",
"Frontend state management libraries",
"Cloud infrastructure tooling for TypeScript projects"]

## Conventions

- File names: lowercase, hyphens, no spaces (e.g., `github-copilot.md`, `flux-pattern.md`)
- Every wiki page starts with YAML frontmatter (see Frontmatter section below)
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
sources: [raw/articles/source-file.md]
---
```

## Tag Taxonomy

Define 10–20 top-level tags. Add new tags here **before** using them on pages.
Every tag on a page must appear in this list.

### Tool & Platform Tags
- tool
- cli
- ide
- agent
- api
- library
- framework
- platform

### Technology Tags
- ai
- llm
- inference
- fine-tuning
- rag
- vector-db

### Status & Meta Tags
- experimental
- stable
- deprecated
- comparison
- benchmark
- trend
- controversy

### Organization Tags
- company
- open-source
- research-lab

## Page Thresholds

- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Update an existing page** when a source adds new information about something already covered
- **Do not create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages

One page per notable tool, product, company, or person. Include:
- What it is and who makes it
- Key capabilities and differentiators
- Pricing / licensing model (if relevant)
- Relationships to other entities via `[[wikilinks]]`
- Source references

## Concept Pages

One page per technique, pattern, or idea. Include:
- Clear definition
- Why it matters
- Current state and limitations
- Related concepts via `[[wikilinks]]`

## Comparison Pages

Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis as of the page's `updated` date
- Sources for each claim

## Update Policy

When new information conflicts with existing content:
1. Check dates — newer primary sources generally supersede older ones
2. If genuinely contradictory, record both positions with their dates and sources
3. Add `contradictions: [other-page]` to frontmatter
4. Flag for user review in the next lint report
