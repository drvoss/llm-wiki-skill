---
name: llm-wiki
description: "Build and maintain a persistent, interlinked markdown knowledge base using Karpathy's LLM Wiki pattern — compile knowledge once from sources, keep it current, and query it without re-reading raw documents every time."
version: 1.0.0
author: llm-wiki-skill contributors
license: MIT
metadata:
  category: workflow
  agent_type: general-purpose
  compatible_runtimes: [copilot-cli, claude-code, codex-cli, gemini-cli]
---

# LLM Wiki

Build a personal or team knowledge base as a directory of interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

**The key insight:** traditional AI-assisted research re-reads raw sources every session.
A wiki compiles that work once. Cross-references are already there.
Contradictions have already been flagged. Knowledge compounds across sessions.

**Division of labor:** you curate sources and direct analysis.
The agent summarizes, cross-references, files, and maintains consistency.

---

## When to Use

- You want to stop re-explaining the same domain to the AI every session
- You're researching a topic across many sources and want a synthesized view
- You need a living document about a codebase, a technology landscape, or a subject area
- You want an audit trail of what you've learned and when

## When NOT to Use

| Instead of llm-wiki | Use |
|---------------------|-----|
| One-off research question | `deep-research` or a direct web search |
| Code documentation for a specific repo | `code-tour` or `architecture-decisions` |
| Task/issue tracking | session SQL todos |
| Capturing a single meeting note | a plain markdown note |

---

## Configuration

Set the wiki path via environment variable (default: `~/wiki`):

```powershell
# PowerShell — add to your profile or session
$env:LLM_WIKI_PATH = "C:\Users\you\wiki"

# Bash equivalent
export LLM_WIKI_PATH="$HOME/wiki"
```

The wiki is just a directory of markdown files — open it in any editor.
For Obsidian integration, see [`extensions/obsidian/SKILL.md`](extensions/obsidian/SKILL.md).

---

## Architecture — Three Layers

```
$wiki/
├── SCHEMA.md        ← Layer 3: domain rules, conventions, tag taxonomy
├── index.md         ← navigation: every page listed with a one-line summary
├── log.md           ← append-only action log (rotate at 500 entries)
│
├── raw/             ← Layer 1: immutable source material (never edited)
│   ├── articles/    ← web articles, clippings
│   ├── papers/      ← PDFs, arXiv papers
│   ├── transcripts/ ← meeting notes, interviews
│   └── assets/      ← images, diagrams
│
├── entities/        ← Layer 2: people, orgs, products, tools
├── concepts/        ← Layer 2: ideas, techniques, topics
├── comparisons/     ← Layer 2: side-by-side analyses
└── queries/         ← Layer 2: filed answers worth keeping
```

**Layer 1 — Raw:** immutable. The agent reads but never modifies these.  
**Layer 2 — Wiki:** agent-owned pages. Created, updated, and cross-referenced.  
**Layer 3 — Schema:** defines structure, conventions, and tag taxonomy.

---

## Session Start — Orientation (Required)

**Every session, before any operation:**

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"

# 1. Understand the domain, conventions, and tag taxonomy
Get-Content "$wiki/SCHEMA.md"

# 2. Know what pages exist
Get-Content "$wiki/index.md"

# 3. See recent activity (last 30 entries)
Get-Content "$wiki/log.md" | Select-Object -Last 50
```

Skipping orientation causes duplicate pages, missed cross-references, and
tags outside the taxonomy. For large wikis (100+ pages), also search for the
topic at hand before creating anything new.

---

## Initializing a New Wiki

When the user asks to create or start a wiki:

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"

# Create the directory structure
New-Item -ItemType Directory -Force -Path @(
    "$wiki/raw/articles",
    "$wiki/raw/papers",
    "$wiki/raw/transcripts",
    "$wiki/raw/assets",
    "$wiki/entities",
    "$wiki/concepts",
    "$wiki/comparisons",
    "$wiki/queries"
)
```

Then:
1. Ask the user what domain the wiki covers — be specific
2. Write `SCHEMA.md` from one of the provided [templates](templates/)
3. Write initial `index.md` with section headers (Entities / Concepts / Comparisons / Queries)
4. Write initial `log.md` with a creation entry
5. Confirm the wiki is ready and suggest first sources to ingest

If this repository is available locally, you can optionally bootstrap the wiki first:

```powershell
python3 scripts/wiki-init.py $wiki --template tech-stack --domain "AI coding tools"
```

---

## Operation 1 — Ingest

When the user provides a source (URL, file, or pasted text):

**① Capture the raw source**

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"
$date = Get-Date -Format "yyyy-MM-dd"

# URL → fetch content and save (runtime-dependent web fetch tool)
# File → copy to raw/
# Pasted text → save to raw/articles/ or raw/transcripts/

# Name descriptively: raw/articles/karpathy-wiki-2026-01.md
```

**② Discuss takeaways** with the user — what's significant, what matters for the domain.
(Skip in automated/cron contexts.)

**③ Check what already exists** — prevents the most common wiki failure: duplicates.

```powershell
# Search index and existing pages for mentioned entities/concepts
Select-String -Path "$wiki/**/*.md" -Pattern "EntityName" -Recurse
Get-Content "$wiki/index.md" | Select-String "EntityName"
```

**④ Write or update wiki pages**

Apply the **Page Threshold** from `SCHEMA.md`:
- **Create** a new page when an entity/concept appears in 2+ sources OR is central to one source
- **Update** an existing page with new information — bump `updated` date
- **Don't create** pages for passing mentions or things outside the domain
- When information contradicts existing content: record both positions with dates and sources,
  add `contradictions: [page-name]` to frontmatter, flag for user review

Every page frontmatter:
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [tag-from-taxonomy]
sources: [raw/articles/source-name.md]
---
```

Every new or updated page must link to at least **2 other pages** via `[[wikilinks]]`.
Check that existing pages link back.

**⑤ Update navigation**

```powershell
# Add new pages to index.md alphabetically within their section
# Update "Total pages" count and "Last updated" date in index.md header

# Append to log.md
Add-Content "$wiki/log.md" "## [$date] ingest | Source Title`n- Created: page-a.md`n- Updated: page-b.md`n"
```

**⑥ Report** every file created or updated to the user.

A single source can touch 5–15 wiki pages. This is the compounding effect working.

---

## Operation 2 — Query

When the user asks a question about the wiki's domain:

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"
$date = Get-Date -Format "yyyy-MM-dd"

# 1. Find relevant pages
Get-Content "$wiki/index.md" | Select-String "keyword"

# 2. For large wikis (100+ pages), also search content
Select-String -Path "$wiki/**/*.md" -Pattern "keyword" -Recurse

# 3. Read the relevant pages
# 4. Synthesize: cite sources — "Based on [[page-a]] and [[page-b]]..."
# 5. File if valuable: create queries/<slug>.md or comparisons/<slug>.md
#    Only file answers that would be painful to re-derive. Skip trivial lookups.

# 6. Log the query
Add-Content "$wiki/log.md" "## [$date] query | What is X?`n- Filed: queries/what-is-x.md`n"
```

---

## Operation 3 — Lint

Run the lint script to check wiki health:

> Note: `scripts/wiki-lint.py` is only available when this repository is
> cloned locally. If you installed only `SKILL.md`, run lint by passing the
> script path explicitly or copy `scripts/wiki-lint.py` alongside your wiki.

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"
python3 scripts/wiki-lint.py $wiki

# Bash equivalent
WIKI="${LLM_WIKI_PATH:-$HOME/wiki}"
python3 scripts/wiki-lint.py "$WIKI"
```

The script checks:

| Check | Severity |
|-------|----------|
| Broken `[[wikilinks]]` (points to non-existent page) | Error |
| Missing raw source referenced in `sources:` | Error |
| Orphan pages (zero inbound wikilinks) | Warning |
| Pages missing from `index.md` | Warning |
| Missing frontmatter fields (`title`, `created`, `updated`, `type`, `tags`, `sources`) | Warning |
| Tags outside the taxonomy defined in `SCHEMA.md` | Warning |
| Pages with fewer than 2 outbound wiki links | Warning |
| Missing contradiction targets referenced in frontmatter | Warning |
| `index.md` header metadata out of sync | Warning |
| Pages over 200 lines (candidates for splitting) | Info |
| Pages not updated in 90+ days | Info |
| `log.md` over 500 entries (needs rotation) | Info |

After lint, append to `log.md`:
```
## [YYYY-MM-DD] lint | N errors, M warnings
```

---

## Working with the Wiki

### Search

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"

# By content
Select-String -Path "$wiki/**/*.md" -Pattern "transformer" -Recurse

# By filename
Get-ChildItem "$wiki" -Recurse -Filter "*transformer*"

# By tag
Select-String -Path "$wiki/**/*.md" -Pattern "tags:.*alignment" -Recurse

# Recent activity
Get-Content "$wiki/log.md" | Select-Object -Last 30
```

### Bulk Ingest (multiple sources at once)

1. Read all sources first — don't process one at a time
2. Identify all entities and concepts across all sources
3. Check existing pages for all of them in one search pass
4. Create/update pages in one pass
5. Update `index.md` once at the end
6. Write a single log entry covering the batch

### Archiving

When content is fully superseded:

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"
New-Item -ItemType Directory -Force "$wiki/_archive/entities"
Move-Item "$wiki/entities/old-page.md" "$wiki/_archive/entities/old-page.md"
# Remove from index.md
# Replace [[old-page]] links with plain text + "(archived)"
Add-Content "$wiki/log.md" "## [$date] archive | old-page.md — superseded by new-page.md`n"
```

---

## Pitfalls

- **Never modify `raw/`** — sources are immutable. Corrections go in wiki pages.
- **Always orient first** — SCHEMA + index + recent log before any operation in a new session.
- **Always update `index.md` and `log.md`** — skipping this makes the wiki degrade over time.
- **Don't create pages for passing mentions** — follow the Page Threshold in `SCHEMA.md`.
- **Don't create pages without cross-references** — every page needs ≥ 2 `[[wikilinks]]`.
- **Tags must come from the taxonomy** — freeform tags turn into noise. Add new tags to `SCHEMA.md` first.
- **Ask before mass-updating** — if an ingest would touch 10+ pages, confirm scope with the user first.
- **Rotate the log** — when `log.md` exceeds 500 entries, rename to `log-YYYY.md` and start fresh.

---

## Extensions

| Extension | What it adds |
|-----------|-------------|
| [`extensions/arxiv`](extensions/arxiv/SKILL.md) | Search arXiv papers during ingest (no API key) |
| [`extensions/github`](extensions/github/SKILL.md) | Ingest GitHub issues, PRs, releases, and README material |
| [`extensions/obsidian`](extensions/obsidian/SKILL.md) | Use an Obsidian vault as the wiki directory |

## See Also

- [templates/](templates/) — ready-made `SCHEMA.md` for tech-stack, codebase, product-intelligence, and research wikis
- [templates/pages/](templates/pages/) — starter page skeletons for entity, concept, comparison, and query pages
- [docs/OPERATIONS.md](docs/OPERATIONS.md) — day-2 operating guidance for keeping a wiki healthy over time
- [scripts/wiki-init.py](scripts/wiki-init.py) — bootstrap a new wiki skeleton from repository templates
- [scripts/wiki-stats.py](scripts/wiki-stats.py) — lightweight wiki summary for page, source, and activity counts
- [examples/sample-wiki/](examples/sample-wiki/) — a working example wiki to reference
- [scripts/wiki-lint.py](scripts/wiki-lint.py) — standalone lint script
