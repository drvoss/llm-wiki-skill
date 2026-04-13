# Wiki Schema — Codebase Intelligence

> Copy this file to `$wiki/SCHEMA.md` and fill in the Domain section with your
> project name and key concerns. Delete this comment block when done.

## Domain

[Project name] codebase — modules, patterns, architectural decisions, and
known constraints as understood by the team.

This wiki tracks *why* the code is the way it is, not *what* the code does
(that belongs in inline comments and docstrings).

## Conventions

- File names: lowercase, hyphens (e.g., `auth-service.md`, `event-sourcing.md`)
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
sources: [raw/transcripts/meeting-2026-01-15.md]
---
```

## Tag Taxonomy

### Module & Layer Tags
- module
- service
- api
- database
- frontend
- backend
- worker
- infrastructure

### Pattern & Design Tags
- pattern
- architecture
- event-sourcing
- cqrs
- repository-pattern
- dependency-injection
- microservice
- monolith

### Status Tags
- active
- legacy
- deprecated
- in-progress
- planned

### Decision & Knowledge Tags
- adr
- tech-debt
- constraint
- workaround
- known-issue
- onboarding

## Page Thresholds

- **Create a page** for any module, service, or pattern that appears in 2+ conversations
  OR that a new team member would need to understand the system
- **Update** when code changes or new understanding is gained
- **Do not create** pages for individual functions or classes — those belong in code comments
- **Split** pages over 200 lines into focused sub-topics

## Entity Pages (modules, services, external dependencies)

Include:
- Purpose and responsibility boundary
- Key files and entry points (with line references where helpful)
- Dependencies on other modules (`[[wikilinks]]`)
- Configuration options and environment variables
- Known constraints or gotchas

## Concept Pages (patterns, decisions, techniques in use)

Include:
- What the pattern is and why this project uses it
- Where it's applied (link to entity pages)
- Trade-offs that led to this choice
- What to watch out for when changing it

## Comparison Pages

Use for: "why we chose X over Y", "old architecture vs new architecture".
Include the date of the decision — comparisons become stale.

## ADR Pages (Architecture Decision Records)

Store in `concepts/adr-NNN-slug.md`. Include:
- Status: Proposed | Accepted | Deprecated | Superseded by [[adr-NNN]]
- Context and problem
- Decision and rationale
- Consequences (positive and negative)

## Update Policy

When implementation changes:
1. Update the relevant entity or concept page
2. Bump `updated` date
3. If an ADR is superseded, update its status and link to the new one
4. Log the update in `log.md`
