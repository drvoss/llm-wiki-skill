# Wiki Schema — Research & Literature

> Copy this file to `$wiki/SCHEMA.md` and fill in the Domain section.
> Delete this comment block when done.

## Domain

[Research area — be specific. Examples:
"Reinforcement learning from human feedback (RLHF) and alignment techniques",
"Protein structure prediction methods",
"Distributed systems consensus protocols"]

## Conventions

- File names: lowercase, hyphens (e.g., `attention-mechanism.md`, `yann-lecun.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages — minimum 2 outbound links per page
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- arXiv IDs in frontmatter when applicable: `arxiv: "2310.01234"`

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [tag1, tag2]
sources: [raw/papers/attention-is-all-you-need.md]
arxiv: "NNNN.NNNNN"   # optional, for paper-derived pages
---
```

## Tag Taxonomy

### Research Type Tags
- paper
- survey
- benchmark
- dataset
- model
- algorithm
- framework

### Status & Quality Tags
- seminal
- sota
- reproducible
- retracted
- preprint
- peer-reviewed

### Topic Tags
[Add 10–15 domain-specific topic tags here]
- training
- inference
- alignment
- evaluation
- efficiency
- interpretability

### Organization Tags
- deepmind
- openai
- anthropic
- meta-ai
- academic
- independent

### Meta Tags
- open-question
- controversy
- timeline
- comparison
- prediction

## Page Thresholds

- **Create a paper page** when a paper is cited in 2+ sources you've ingested, OR when it's the
  primary contribution being analyzed
- **Create a person/org page** when they appear across multiple papers or are a key actor
- **Create a concept page** when a technique or idea recurs across multiple papers
- **Do not create** a page for every paper you skim — only papers that materially inform the wiki's domain
- **Split** pages over 200 lines

## Paper Pages

One page per significant paper. Include:
- Full title, authors, year, venue
- arXiv ID (if available)
- Core contribution in 2–3 sentences
- Key results and numbers
- Limitations and open questions
- Connections to other work via `[[wikilinks]]`

## Concept Pages

One page per technique, algorithm, or idea. Include:
- Precise definition (not vague)
- Where it was introduced (link to paper page)
- Current understanding and open debates
- Empirical results if available
- Related concepts via `[[wikilinks]]`

## Person/Organization Pages

One page per major researcher or lab. Include:
- Affiliation(s) and focus area
- Key contributions (linked to paper pages)
- Notable positions or controversies (with sources)

## Comparison Pages

Use for: "RLHF vs DPO", "GPT-4 vs Claude-3 on benchmark X". Include:
- Precise dimensions of comparison
- Source for each data point
- Date — benchmarks move fast

## Update Policy

Research moves fast. When a new paper supersedes or contradicts existing content:
1. Update the concept page with the new finding — preserve the old claim with its date
2. Add `contradictions: [page]` to frontmatter if there's a genuine disagreement
3. Update any comparison pages affected
4. Log the update
