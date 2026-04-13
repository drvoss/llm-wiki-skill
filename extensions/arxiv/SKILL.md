---
name: llm-wiki-arxiv
description: "Extension for llm-wiki: search arXiv papers and ingest them into the wiki. No API key required. Combines with llm-wiki's ingest operation."
version: 1.0.0
metadata:
  category: workflow
  agent_type: general-purpose
  requires: llm-wiki
---

# arXiv Extension for llm-wiki

Search and retrieve academic papers from arXiv's free REST API, then pipe them
into the llm-wiki ingest workflow. No API key, no registration required.

## When to Use

- During llm-wiki ingest when the source is an arXiv paper
- When the user asks "what papers exist on X" during a research session
- As a step in `deep-research` before filing results into the wiki

## Quick Reference

| Action | Command |
|--------|---------|
| Search by keyword | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
| Search by author | `curl "https://export.arxiv.org/api/query?search_query=au:karpathy&max_results=5"` |
| Fetch specific paper | `curl "https://export.arxiv.org/api/query?id_list=2310.01234"` |
| Sort by date | append `&sortBy=submittedDate&sortOrder=descending` |

## Search and Parse

```powershell
# Search and display results (requires Python 3)
$query = "transformer+attention+mechanism"
curl -s "https://export.arxiv.org/api/query?search_query=all:$query&max_results=5&sortBy=submittedDate&sortOrder=descending" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for i, entry in enumerate(root.findall('a:entry', ns), 1):
    title     = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id  = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    published = entry.find('a:published', ns).text[:10]
    authors   = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns)[:3])
    summary   = entry.find('a:summary', ns).text.strip()[:250].replace('\n', ' ')
    print(f'{i}. [{arxiv_id}] {title}')
    print(f'   {authors} — {published}')
    print(f'   {summary}...')
    print(f'   PDF: https://arxiv.org/pdf/{arxiv_id}')
    print()
"
```

## Query Syntax

| Prefix | Searches | Example |
|--------|----------|---------|
| `all:` | All fields | `all:GRPO+reinforcement` |
| `ti:` | Title | `ti:large+language+models` |
| `au:` | Author | `au:vaswani` |
| `abs:` | Abstract | `abs:chain+of+thought` |
| `cat:` | Category | `cat:cs.AI` |
| `co:` | Comment | `co:NeurIPS+2024` |

Boolean: `all:GPT+OR+all:BERT`, `all:language+ANDNOT+all:vision`

## Common arXiv Categories

| Category | Field |
|----------|-------|
| `cs.AI` | Artificial Intelligence |
| `cs.LG` | Machine Learning |
| `cs.CL` | Computation and Language (NLP) |
| `cs.CV` | Computer Vision |
| `cs.SE` | Software Engineering |
| `stat.ML` | Statistics — Machine Learning |

## Ingest Workflow (with llm-wiki)

After finding a relevant paper:

```powershell
$wiki = $env:LLM_WIKI_PATH ?? "$HOME/wiki"
$date = Get-Date -Format "yyyy-MM-dd"
$arxivId = "2310.01234"
$slug = "attention-is-all-you-need"

# 1. Save the abstract/metadata as a raw source
$meta = "# Attention Is All You Need`n`narXiv: $arxivId`nDate: $date`n..."
Set-Content "$wiki/raw/papers/$slug.md" $meta

# 2. Now run the standard llm-wiki ingest operation
#    (check index, create/update entity and concept pages, update index.md and log.md)
```

The standard llm-wiki ingest rules apply:
- Create a page only if the paper meets the Page Threshold (2+ source mentions or central to one)
- Link to ≥ 2 existing pages
- Update `index.md` and `log.md`

## Tips

- Use `abs:` prefix to find papers discussing a specific technique even when it's not in the title
- Combine with `cat:cs.AI` to avoid unrelated results in other fields
- For the most recent work: always add `&sortBy=submittedDate&sortOrder=descending`
- For a known paper: fetch by ID (`id_list=NNNN.NNNNN`) rather than keyword search
