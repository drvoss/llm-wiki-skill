# Wiki Schema — Product Intelligence

> Copy this file to `$wiki/SCHEMA.md` and customize the Domain and tag taxonomy
> for the market or product space you are tracking.

## Domain

[What this wiki covers — be specific. Examples:
"AI coding tools for enterprise engineering teams in 2026",
"Observability products for cloud-native teams",
"Developer platform vendors serving mid-market SaaS companies"]

## Conventions

- File names: lowercase, hyphens, no spaces (e.g., `github-copilot.md`, `pricing-shift-q2-2026.md`)
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to connect related pages — minimum 2 outbound links per page
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- Preserve the date and source for any market claim that may change over time

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

### Competitor Tags
- direct-competitor
- indirect-competitor
- incumbent
- startup
- platform
- suite

### Product Surface Tags
- pricing
- packaging
- feature
- workflow
- integration
- launch
- deprecation

### Signal Quality Tags
- official-statement
- release-note
- analyst-report
- user-feedback
- benchmark
- rumor

### Commercial Tags
- enterprise
- smb
- self-serve
- sales-led
- open-source

### Time Tags
- q1-2026
- q2-2026
- q3-2026
- q4-2026

## Page Thresholds

- **Create a page** when a company, product, or market signal appears in 2+ sources OR is central to one source
- **Update** an existing page when pricing, positioning, roadmap, or product packaging changes
- **Do not create** pages for one-off mentions or weak rumors without follow-up evidence
- **Split** pages over 200 lines into tighter pages such as product, pricing, or roadmap subtopics

## Entity Pages

Use for companies, products, bundles, or key leaders. Include:
- What the product/company is
- Target user and market segment
- Key differentiators
- Pricing or packaging snapshot
- Links to related competitors, concepts, and comparisons

## Concept Pages

Use for recurring market themes such as "agent mode", "seat-based pricing", or "platform lock-in".
Include:
- Clear definition
- Why the concept matters commercially
- Which entities are using it
- Tensions, risks, or open questions

## Comparison Pages

Use for side-by-side evaluations such as "Copilot vs Claude Code for enterprise rollout".
Include:
- Exact comparison dimensions
- Time-bounded verdict
- Source for each claim

## Update Policy

Product intelligence changes quickly. When new information conflicts with older notes:
1. Keep the old claim with its date and source
2. Add the new claim with its date and source
3. Add `contradictions: [other-page]` to frontmatter if the disagreement matters
4. Flag the page for review in the next lint pass
