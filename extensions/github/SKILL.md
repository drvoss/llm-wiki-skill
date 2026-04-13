---
name: llm-wiki-github
description: "Extension for llm-wiki: ingest GitHub repository context such as issues, pull requests, releases, and README material into the wiki."
version: 1.0.0
metadata:
  category: workflow
  agent_type: general-purpose
  requires: llm-wiki
---

# GitHub Extension for llm-wiki

Use GitHub repository material as first-class source input for `llm-wiki`.
This extension is useful when your wiki tracks a codebase, product space,
roadmap, or ecosystem where GitHub itself is a primary source of truth.

## Sources This Extension Covers

| GitHub source | Typical wiki output |
|---------------|---------------------|
| README / docs | Entity or concept page updates |
| Release notes | Timeline updates, comparisons, product shifts |
| Issues | Problem statements, constraints, decisions |
| Pull requests | Change rationale, implementation trade-offs |
| Discussions | Open questions, community signals |

## Authentication

Prefer GitHub CLI with an authenticated session:

```bash
gh auth status
```

or use an environment token:

```bash
export GH_TOKEN=ghp_your_token_here
```

Do not hardcode tokens into wiki files.

## Quick Reference

| Action | Command |
|--------|---------|
| List recent issues | `gh issue list --repo OWNER/REPO --limit 10` |
| View issue details | `gh issue view 123 --repo OWNER/REPO --comments` |
| List recent PRs | `gh pr list --repo OWNER/REPO --limit 10` |
| View PR details | `gh pr view 456 --repo OWNER/REPO --comments --files` |
| View releases | `gh release list --repo OWNER/REPO --limit 10` |

## Ingest Workflow

### 1. Capture raw GitHub material

Save the GitHub material under `raw/articles/` or `raw/transcripts/`:

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"
$slug = "owner-repo-release-2026-04"

Set-Content "$wiki/raw/articles/$slug.md" "# Release notes`n`n..."
```

Suggested naming:

- `raw/articles/repo-readme-2026-04.md`
- `raw/articles/owner-repo-release-2026-04.md`
- `raw/transcripts/issue-123-discussion.md`
- `raw/transcripts/pr-456-review-thread.md`

### 2. Extract the signal

Focus on:

- what changed
- why it changed
- who the change is for
- what trade-offs or constraints were stated
- whether the result belongs in an entity, concept, comparison, or query page

### 3. Update the wiki

Use normal `llm-wiki` rules:

- create pages only when the content meets the page threshold
- link each new or updated page to at least 2 other wiki pages
- update `index.md` and `log.md`
- preserve contradictions instead of silently overwriting earlier claims

## Good Patterns

### Release note ingest

Use for:

- pricing changes
- packaging changes
- roadmap signals
- new integrations

Typical output:

- update an entity page
- update a comparison page
- file a durable query if the release changes a recurring decision

### Issue / PR ingest

Use for:

- known constraints
- implementation rationale
- product feedback themes
- repeated user pain points

Typical output:

- update a codebase concept page
- update a product intelligence entity page
- file a query if the answer will be reused

## Tips

- Prefer official release notes and merged PRs over speculative issues
- Keep comments as raw provenance instead of rewriting them as settled fact
- Use release dates and merge dates in wiki updates
- If GitHub material is noisy, summarize it into `raw/` first, then ingest from that cleaner source
