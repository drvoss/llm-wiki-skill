#!/usr/bin/env python3
"""
wiki-init.py - Bootstrap a new llm-wiki directory from repository templates.

Usage:
    python3 wiki-init.py [wiki_path]
    python3 wiki-init.py ~/wiki/my-domain --template tech-stack --domain "AI coding tools"
    python3 wiki-init.py --template blank --overwrite
"""

import argparse
import io
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

WIKI_DIRS = [
    "raw/articles",
    "raw/papers",
    "raw/transcripts",
    "raw/assets",
    "entities",
    "concepts",
    "comparisons",
    "queries",
    "_archive/entities",
    "_archive/concepts",
    "_archive/comparisons",
    "_archive/queries",
]

TEMPLATE_MAP = {
    "tech-stack": "templates/SCHEMA-tech-stack.md",
    "codebase": "templates/SCHEMA-codebase.md",
    "research": "templates/SCHEMA-research.md",
    "product-intelligence": "templates/SCHEMA-product-intelligence.md",
}

BLANK_SCHEMA = """# Wiki Schema

## Domain

[Describe the domain this wiki covers.]

## Conventions

- File names: lowercase, hyphens, no spaces
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to connect related pages
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md`
- Every action must be appended to `log.md`

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [tag1, tag2]
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy

- tool
- concept
- comparison
- note

## Page Thresholds

- Create a page when an entity or concept appears in 2+ sources OR is central to one source
- Update existing pages when new information arrives
- Do not create pages for passing mentions
- Split pages over 200 lines
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a new llm-wiki directory.")
    parser.add_argument("wiki_path", nargs="?", help="Path for the wiki directory")
    parser.add_argument(
        "--template",
        choices=["blank", "tech-stack", "codebase", "research", "product-intelligence"],
        default="blank",
        help="Schema template to seed into SCHEMA.md",
    )
    parser.add_argument("--domain", help="Domain text to place in the SCHEMA.md Domain section")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing wiki skeleton")
    return parser.parse_args()


def resolve_wiki_path(args: argparse.Namespace) -> Path:
    if args.wiki_path:
        return Path(args.wiki_path).expanduser()
    env = os.environ.get("LLM_WIKI_PATH")
    if env:
        return Path(env).expanduser()
    return Path.home() / "wiki"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def load_schema_template(repo_root: Path, template_name: str) -> str:
    if template_name == "blank":
        return BLANK_SCHEMA
    template_path = repo_root / TEMPLATE_MAP[template_name]
    return read_text(template_path)


def replace_domain_section(content: str, domain: str) -> str:
    pattern = re.compile(r"(?ms)^## Domain\s*\n.*?(?=^##\s|\Z)")
    replacement = f"## Domain\n\n{domain}\n\n"
    if pattern.search(content):
        return pattern.sub(replacement, content, count=1)
    return content


def seed_index(domain: str, date: str) -> str:
    title = f"# Wiki Index - {domain}" if domain else "# Wiki Index"
    return (
        f"{title}\n\n"
        "> Content catalog. Every wiki page listed under its type with a one-line summary.\n"
        "> Read this first to find relevant pages before searching or creating.\n"
        f"> Last updated: {date} | Total pages: 0\n\n"
        "## Entities\n\n"
        "*(none yet)*\n\n"
        "## Concepts\n\n"
        "*(none yet)*\n\n"
        "## Comparisons\n\n"
        "*(none yet)*\n\n"
        "## Queries\n\n"
        "*(none yet)*\n"
    )


def seed_log(domain: str, date: str) -> str:
    domain_text = domain or "[fill in the domain]"
    return (
        "# Wiki Log\n\n"
        "> Chronological record of all wiki actions. Append-only.\n"
        "> Format: `## [YYYY-MM-DD] action | subject`\n"
        "> Actions: init, ingest, update, query, lint, archive\n"
        "> Rotate when this file exceeds 500 entries: rename to log-YYYY.md and start fresh.\n\n"
        f"## [{date}] init | Wiki initialized\n"
        f"- Domain: {domain_text}\n"
        "- Structure created: SCHEMA.md, index.md, log.md, raw/, entities/, concepts/, comparisons/, queries/\n"
    )


def has_existing_wiki_content(wiki: Path) -> bool:
    expected_paths = [
        wiki / "SCHEMA.md",
        wiki / "index.md",
        wiki / "log.md",
        wiki / "raw",
        wiki / "entities",
        wiki / "concepts",
        wiki / "comparisons",
        wiki / "queries",
    ]
    return any(path.exists() for path in expected_paths)


def main() -> None:
    args = parse_args()
    wiki = resolve_wiki_path(args)
    repo_root = Path(__file__).resolve().parents[1]

    if has_existing_wiki_content(wiki) and not args.overwrite:
        print(f"Wiki already appears to exist at: {wiki}", file=sys.stderr)
        print("Use --overwrite to replace the skeleton files.", file=sys.stderr)
        sys.exit(1)

    try:
        wiki.mkdir(parents=True, exist_ok=True)
        for relative_dir in WIKI_DIRS:
            (wiki / relative_dir).mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"Failed to create wiki directories: {exc}", file=sys.stderr)
        sys.exit(2)

    date = datetime.now().strftime("%Y-%m-%d")
    domain = args.domain or ""
    schema_content = load_schema_template(repo_root, args.template)
    if domain:
        schema_content = replace_domain_section(schema_content, domain)

    try:
        write_text(wiki / "SCHEMA.md", schema_content.rstrip() + "\n")
        write_text(wiki / "index.md", seed_index(domain, date))
        write_text(wiki / "log.md", seed_log(domain, date))
    except OSError as exc:
        print(f"Failed to write wiki seed files: {exc}", file=sys.stderr)
        sys.exit(2)

    print(f"Initialized llm-wiki at: {wiki}")
    print(f"Template: {args.template}")
    if domain:
        print(f"Domain: {domain}")
    print("Next steps:")
    print("  1. Review SCHEMA.md and tighten the tag taxonomy.")
    print("  2. Ingest a first source into raw/.")
    print("  3. Run wiki-lint.py after a few page updates.")


if __name__ == "__main__":
    main()
