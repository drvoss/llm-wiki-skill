# llm-wiki-skill

**Language:** [English](README.md) | [한국어](README.ko.md) | [简体中文](README.zh-CN.md)

**Tutorial:** [English](docs/TUTORIAL.md) | [한국어](docs/TUTORIAL.ko.md) | [简体中文](docs/TUTORIAL.zh-CN.md)

**Operations Guide:** [English](docs/OPERATIONS.md) | [한국어](docs/OPERATIONS.ko.md) | [简体中文](docs/OPERATIONS.zh-CN.md)

A standalone, runtime-agnostic skill for building and maintaining a persistent
markdown knowledge base - based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Compatible with GitHub Copilot CLI, Claude Code, Codex CLI, Gemini CLI, and
any [agentskills.io](https://agentskills.io)-compatible runtime.

---

## Why This Exists

`llm-wiki-skill` takes an idea proven inside
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent) and
packages it as a reusable, cross-runtime skill package.

In Hermes Agent, `llm-wiki` is one bundled skill inside a larger agent system.
This repository splits that idea into a standalone package with its own:

- `SKILL.md` for the core workflow
- `templates/` for domain-specific schemas
- `scripts/wiki-lint.py` for zero-dependency health checks
- `scripts/wiki-stats.py` for quick coverage and activity summaries
- `examples/` for a reference wiki
- `extensions/` for optional add-ons like arXiv, GitHub, and Obsidian

The result is a cleaner way to adopt the pattern in tools beyond Hermes without
bringing along Hermes-specific config and runtime assumptions.

---

## The Problem It Solves

Every AI session starts from zero. You re-explain the domain, the agent re-reads
the same sources, re-discovers the same relationships. Work doesn't compound.

**llm-wiki** flips this. The agent compiles knowledge once into interlinked markdown files.
Next session: orient in 30 seconds (SCHEMA + index + recent log), then build on
what's already there. Cross-references exist. Contradictions are flagged. Synthesis is done.

---

## Start Here

- Read the hands-on tutorial: [docs/TUTORIAL.md](docs/TUTORIAL.md)
- Keep the wiki healthy with the operations guide: [docs/OPERATIONS.md](docs/OPERATIONS.md)
- Install the skill into your runtime
- Initialize a wiki for one real domain
- Ingest a few sources before judging the workflow

---

## Installation

### GitHub Copilot CLI

```bash
# Project-level: copy SKILL.md to .github/skills/
cp SKILL.md .github/skills/llm-wiki/SKILL.md

# User-level: available in all sessions
cp SKILL.md ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
# Project-level
New-Item -ItemType Directory -Force .github\skills\llm-wiki | Out-Null
Copy-Item SKILL.md .github\skills\llm-wiki\SKILL.md

# User-level
New-Item -ItemType Directory -Force $HOME\.copilot\skills\llm-wiki | Out-Null
Copy-Item SKILL.md $HOME\.copilot\skills\llm-wiki\SKILL.md
```

### Claude Code

```bash
# User-level
cp SKILL.md ~/.claude/skills/llm-wiki/SKILL.md
```

### Codex CLI

```bash
cp SKILL.md ~/.codex/skills/llm-wiki/SKILL.md
```

### Gemini CLI

```bash
gemini skills install github:drvoss/llm-wiki-skill
```

---

## Quick Start

```powershell
# 1. Set your wiki path (add to your shell profile)
$env:LLM_WIKI_PATH = "$HOME/wiki"

# 2. If you're using this repository locally, bootstrap a wiki skeleton
python3 scripts/wiki-init.py $env:LLM_WIKI_PATH --template tech-stack --domain "AI coding tools"

# 3. Ingest your first source
# > Ingest this article into the wiki: [URL or paste text]

# 4. Query the wiki
# > What do we know about agentic coding patterns?

# 5. Run lint to check wiki health
python3 scripts/wiki-lint.py
```

For a complete scenario - including installing into a project, checking that
Copilot sees the skill, watching the wiki grow, and learning better operating
habits - use the tutorial: [docs/TUTORIAL.md](docs/TUTORIAL.md).

---

## Three Operations

| Operation | Trigger | What happens |
|-----------|---------|-------------|
| **Ingest** | "Add this to the wiki", paste a URL | Saves raw source -> checks for duplicates -> creates/updates pages -> updates index + log |
| **Query** | "What does the wiki say about X?" | Reads index -> finds relevant pages -> synthesizes -> optionally files the answer |
| **Lint** | "Check the wiki" or `python3 scripts/wiki-lint.py` | Finds orphans, broken links, index gaps, frontmatter issues, stale content |

---

## Structure

```
llm-wiki-skill/
|- SKILL.md              <- main skill (load this into your AI tool)
|- scripts/
|  |- wiki-init.py       <- bootstrap a wiki skeleton from local templates
|  |- wiki-lint.py       <- standalone lint script (Python 3, no dependencies)
|  \- wiki-stats.py      <- lightweight wiki coverage and activity summary
|- templates/            <- ready-made SCHEMA.md for different domains
|  |- SCHEMA-tech-stack.md
|  |- SCHEMA-codebase.md
|  |- SCHEMA-product-intelligence.md
|  |- SCHEMA-research.md
|  \- pages/             <- starter templates for entity/concept/comparison/query pages
|- docs/                 <- tutorial and operations guides (EN / KO / ZH-CN)
|- examples/
|  \- sample-wiki/       <- working example wiki to explore
\- extensions/           <- optional add-ons (opt-in, separate dependencies)
   |- arxiv/SKILL.md     <- arXiv paper search (curl + python3 stdlib)
   |- github/SKILL.md    <- GitHub issues, PRs, releases, README ingest
   \- obsidian/SKILL.md  <- Obsidian vault + headless sync
```

---

## Wiki Structure (created in your `$LLM_WIKI_PATH`)

```
~/wiki/
|- SCHEMA.md        <- domain rules and tag taxonomy (from templates/)
|- index.md         <- one-line summary for every page
|- log.md           <- append-only action log
|- raw/             <- immutable sources (articles, papers, transcripts)
|- entities/        <- people, orgs, tools, products
|- concepts/        <- ideas, techniques, patterns
|- comparisons/     <- side-by-side analyses
\- queries/         <- filed answers worth keeping
```

---

## Extensions

Core `SKILL.md` has no external dependencies. Extensions are opt-in:

| Extension | What it adds |
|-----------|-------------|
| [`extensions/arxiv`](extensions/arxiv/SKILL.md) | Search arXiv during ingest (no API key) |
| [`extensions/github`](extensions/github/SKILL.md) | Ingest GitHub issues, PRs, releases, and README material |
| [`extensions/obsidian`](extensions/obsidian/SKILL.md) | Obsidian vault + headless sync |

---

## Lint Script

```bash
# Bootstrap a new wiki from a repository template
python3 scripts/wiki-init.py ~/wiki/ai-coding-tools --template tech-stack --domain "AI coding tools"

# Check wiki health
python3 scripts/wiki-lint.py                      # uses LLM_WIKI_PATH
python3 scripts/wiki-lint.py ~/my-project-wiki    # explicit path
python3 scripts/wiki-lint.py --strict ~/my-project-wiki
python3 scripts/wiki-lint.py --json ~/my-project-wiki
python3 scripts/wiki-lint.py --fix ~/my-project-wiki

# Get a lightweight wiki summary
python3 scripts/wiki-stats.py ~/my-project-wiki

# CI example for GitHub-hosted wikis
cat examples/github-actions/wiki-lint.yml
```

Checks: broken wikilinks, missing source files, orphan pages, index gaps, missing frontmatter,
unknown tags, minimum outbound wiki links, contradiction targets, index header metadata,
oversized pages, stale content, log rotation.

`wiki-stats.py` complements lint by giving a fast summary of page counts, link density,
raw source counts, and recent activity without framing everything as a problem.

Exit code 0 = no errors. Exit code 1 = errors found. Exit code 2 = wiki not found.

---

## Relationship to Hermes Agent and everything-copilot-cli

This repository started from the `llm-wiki` skill in
[`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent), then
expanded it into a standalone package for multiple runtimes.

It was also deliberately kept separate from
[everything-copilot-cli](https://github.com/drvoss/everything-copilot-cli) to
avoid scope creep. `llm-wiki-skill` is cross-runtime and includes its own
templates, lint tooling, tutorials, examples, and extensions - more than a
single `SKILL.md` file.

---

## License

MIT
