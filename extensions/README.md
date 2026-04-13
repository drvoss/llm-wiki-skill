# Extensions

Optional skill modules that add capabilities to `llm-wiki`.
The core `SKILL.md` has no external dependencies — these are opt-in.

| Extension | Adds | Dependency |
|-----------|------|------------|
| [`arxiv/`](arxiv/SKILL.md) | Search and ingest arXiv papers | `curl`, `python3` (stdlib only) |
| [`github/`](github/SKILL.md) | Ingest issues, PRs, releases, READMEs, and discussions | `gh` or GitHub API access |
| [`obsidian/`](obsidian/SKILL.md) | Obsidian vault integration + headless sync | `obsidian-headless` (optional) |

## Using Extensions

Extensions are standalone skill files — load them alongside the main skill when needed:

```
# In Copilot CLI: load both the main skill and the extension
# (reference both SKILL.md paths in your session context)

# Gemini CLI
gemini skills install github:drvoss/llm-wiki-skill
gemini skills install github:drvoss/llm-wiki-skill/extensions/arxiv
gemini skills install github:drvoss/llm-wiki-skill/extensions/github

# Claude Code — copy to ~/.claude/skills/
cp -r extensions/arxiv ~/.claude/skills/llm-wiki-arxiv
cp -r extensions/github ~/.claude/skills/llm-wiki-github
cp -r extensions/obsidian ~/.claude/skills/llm-wiki-obsidian
```

## Adding Extensions

To contribute a new extension:

1. Create `extensions/<name>/SKILL.md`
2. Set `requires: llm-wiki` in frontmatter metadata
3. Document the dependency clearly — the core skill must work without it
4. Add a row to the table above
