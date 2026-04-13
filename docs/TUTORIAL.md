# llm-wiki-skill Tutorial

**Language:** [English](TUTORIAL.md) | [한국어](TUTORIAL.ko.md) | [简体中文](TUTORIAL.zh-CN.md)

This tutorial walks through a realistic scenario:

1. Install `llm-wiki-skill`
2. Add it to a project
3. Check that Copilot can use it
4. Create and grow a wiki while working
5. Learn the habits that make the workflow pay off

---

## Scenario

Imagine you are evaluating AI coding tools for your team. You want more than a
chat log. You want a reusable knowledge base that keeps:

- source material in one place
- summaries and comparisons in durable pages
- an audit trail of what changed
- a quick stats view for whether the wiki is actually growing

That is the job of `llm-wiki-skill`.

This tutorial exists because the workflow was first proven inside Hermes Agent,
then split out into this standalone repository so it can be reused in Copilot,
Codex, Claude Code, Gemini, and similar runtimes without Hermes-specific setup.

---

## 1. Install the skill

### Project-level install for Copilot CLI

From your repository root:

```bash
mkdir -p .github/skills/llm-wiki
cp SKILL.md .github/skills/llm-wiki/SKILL.md
```

```powershell
New-Item -ItemType Directory -Force .github\skills\llm-wiki | Out-Null
Copy-Item SKILL.md .github\skills\llm-wiki\SKILL.md
```

Use this when the skill should travel with the repository.

### User-level install for Copilot CLI

```bash
mkdir -p ~/.copilot/skills/llm-wiki
cp SKILL.md ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
New-Item -ItemType Directory -Force $HOME\.copilot\skills\llm-wiki | Out-Null
Copy-Item SKILL.md $HOME\.copilot\skills\llm-wiki\SKILL.md
```

Use this when you want the skill available in every session.

### Other runtimes

```bash
# Claude Code
cp SKILL.md ~/.claude/skills/llm-wiki/SKILL.md

# Codex CLI
cp SKILL.md ~/.codex/skills/llm-wiki/SKILL.md

# Gemini CLI
gemini skills install github:drvoss/llm-wiki-skill
```

---

## 2. Reflect it into your project

Choose a wiki location for the project.

```powershell
$env:LLM_WIKI_PATH = "$HOME\wiki\ai-coding-tools"
```

Common patterns:

- **One wiki per repository**: good for codebase knowledge
- **One wiki per domain**: good for market research or long-running investigations
- **One shared team wiki**: good when the same area is revisited across projects

If you want this to be automatic, add `LLM_WIKI_PATH` to your shell profile or
project bootstrap script.

---

## 3. Confirm Copilot sees the skill

There is no special "installed skills" dashboard in this repository, so confirm
it the practical way:

1. Start Copilot CLI in the repository.
2. Ask it to use the skill directly.

Example prompts:

```text
Initialize a new llm-wiki at $env:LLM_WIKI_PATH about AI coding tools.
```

```text
What is the llm-wiki workflow you have available in this session?
```

If the skill is loaded, Copilot should respond in terms of the wiki workflow:
orientation, ingest, query, lint, SCHEMA/index/log, and markdown pages.

Also confirm the file is in the expected place:

```bash
ls .github/skills/llm-wiki/SKILL.md
```

```powershell
Get-Item .github\skills\llm-wiki\SKILL.md
```

or for a user install:

```bash
ls ~/.copilot/skills/llm-wiki/SKILL.md
```

```powershell
Get-Item $HOME\.copilot\skills\llm-wiki\SKILL.md
```

Use this quick checklist:

- Copilot responds in terms of **SCHEMA / index / log**
- Copilot refers to **ingest / query / lint** rather than a generic note-taking workflow
- The installed skill file exists in the expected path

---

## 4. Initialize the wiki

If you are working from a local clone of this repository, you can bootstrap the
directory before asking Copilot to work with it:

```bash
python3 scripts/wiki-init.py ~/wiki/ai-coding-tools --template tech-stack --domain "AI coding tools used by our platform team"
```

Then ask Copilot to continue from there, or ask it to initialize the wiki itself.

Ask Copilot:

```text
Initialize a new llm-wiki at $env:LLM_WIKI_PATH about AI coding tools used by our platform team.
```

After initialization, your wiki should look roughly like this:

```text
ai-coding-tools/
|- SCHEMA.md
|- index.md
|- log.md
|- raw/
|  |- articles/
|  |- papers/
|  |- transcripts/
|  \- assets/
|- entities/
|- concepts/
|- comparisons/
\- queries/
```

What each file is for:

| File | Purpose |
|------|---------|
| `SCHEMA.md` | Domain boundaries, conventions, tag taxonomy |
| `index.md` | Catalog of pages with one-line summaries |
| `log.md` | Append-only record of ingest/query/lint actions |
| `raw/` | Immutable source material |
| `entities/`, `concepts/`, `comparisons/`, `queries/` | Agent-maintained knowledge pages |

---

## 5. Ingest the first source

Now give the agent something real:

```text
Ingest this article into the wiki: https://example.com/article-about-coding-agents
```

or paste text directly:

```text
Ingest this transcript into the wiki and focus on agent orchestration trade-offs:
[paste text here]
```

After one good ingest, you should expect:

```text
ai-coding-tools/
|- raw/
|  \- articles/
|     \- article-about-coding-agents-2026-04.md
|- entities/
|  \- github-copilot.md
|- concepts/
|  |- agentic-coding.md
|  \- tool-orchestration.md
|- index.md
\- log.md
```

Typical changes:

- the raw source is saved under `raw/`
- one or more entity/concept pages are created or updated
- `index.md` gains new entries
- `log.md` records what changed

The important point is that the source and the synthesis are separate.

---

## 5A. Check the wiki pulse

Use `wiki-lint.py` when you want problems. Use `wiki-stats.py` when you want a
fast summary of what exists.

```bash
python3 scripts/wiki-stats.py ~/wiki/ai-coding-tools
python3 scripts/wiki-stats.py --json ~/wiki/ai-coding-tools
```

This is useful for checking page balance, raw-source growth, and recent activity.

---

## 6. Query the wiki

Once a few sources are ingested, ask a question:

```text
What does the wiki say about the difference between Copilot CLI and Codex CLI?
```

Good behavior looks like this:

- Copilot reads `index.md` first
- it finds the relevant entity and concept pages
- it synthesizes from the compiled wiki rather than re-reading everything from scratch
- if the answer is especially valuable, it can be filed under `queries/` or `comparisons/`

Example result:

```text
ai-coding-tools/
|- comparisons/
|  \- copilot-cli-vs-codex-cli.md
\- queries/
   \- when-to-use-agentic-cli-tools.md
```

---

## 7. Run lint to keep the wiki healthy

Use the included script:

```bash
python3 scripts/wiki-lint.py
```

or point it at a specific wiki:

```bash
python3 scripts/wiki-lint.py ~/wiki/ai-coding-tools
```

Useful flags:

- `--strict` to fail on warnings
- `--json` for machine-readable output
- `--fix` to update safe metadata such as the `index.md` header

Use lint when:

- a large ingest touched many pages
- links start breaking
- tags begin to drift
- the wiki feels harder to navigate

---

## 8. What the wiki should feel like over time

### After day 1

- a handful of raw sources
- a few concept/entity pages
- a small but useful index

### After a few sessions

- repeated topics stop needing full re-explanation
- comparisons become easier to maintain
- contradictions get recorded instead of forgotten
- the agent starts from the compiled wiki instead of from zero

### After sustained use

- `queries/` becomes a library of hard-won answers
- `comparisons/` becomes a decision record
- `SCHEMA.md` becomes the contract that keeps the wiki coherent

---

## 9. How to get better results

### Pick a narrow domain first

Good:

- "AI coding tools for our platform team"
- "This codebase's ingestion pipeline"
- "Research on agent memory patterns"

Bad:

- "all software"
- "everything about AI"

### Keep raw sources immutable

Never edit `raw/` after ingest. Fix understanding in the wiki pages, not in the source copy.

### Make the schema specific

A vague `SCHEMA.md` leads to vague pages. Tight domains and tight tag taxonomies
produce better pages.

### Ingest in batches when the sources are related

If you have 5 related articles, ingesting them as a batch gives better entity and
concept clustering than processing them one at a time.

### File only durable answers

Do not save every trivial response. Save answers that would be painful to re-derive.

### Run lint regularly

The wiki is only useful if links, tags, and navigation stay healthy.

### Add extensions only when they help

- use `extensions/arxiv` for paper-heavy research
- use `extensions/obsidian` if you want a visual vault and graph view

---

## 10. Suggested first workflow

1. Install the skill into Copilot CLI.
2. Initialize one wiki with a narrow scope.
3. Ingest 3-5 meaningful sources.
4. Ask 2-3 real questions against the wiki.
5. Run lint.
6. Refine `SCHEMA.md` after you notice which tags and page types you actually need.

That is usually enough to tell whether the pattern fits your work.

For the day-2 workflow after setup, see [docs/OPERATIONS.md](OPERATIONS.md).
