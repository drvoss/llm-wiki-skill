#!/usr/bin/env python3
"""
wiki-lint.py - Health checker for LLM Wiki (Karpathy pattern)

Usage:
    python3 wiki-lint.py [wiki_path]
    python3 wiki-lint.py --strict [wiki_path]
    python3 wiki-lint.py --json [wiki_path]
    python3 wiki-lint.py --fix [wiki_path]
    python3 wiki-lint.py                   # uses LLM_WIKI_PATH env var

Exit codes:
    0 - no errors (warnings/info may exist unless --strict is used)
    1 - one or more errors found, or warnings found with --strict
    2 - wiki directory not found
"""

import argparse
import io
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output on all platforms (Windows cmd/PowerShell default to cp1252)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

LAYER2_DIRS = ["entities", "concepts", "comparisons", "queries"]
REQUIRED_FRONTMATTER = ["title", "created", "updated", "type", "tags", "sources"]
PAGE_SIZE_WARN = 200
STALE_DAYS = 90
LOG_ROTATION_THRESHOLD = 500
MIN_OUTBOUND_WIKI_LINKS = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint an llm-wiki directory.")
    parser.add_argument("wiki_path", nargs="?", help="Path to the wiki directory")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", dest="json_output", action="store_true", help="Emit JSON output")
    parser.add_argument("--fix", action="store_true", help="Fix safe metadata issues such as index header counts")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def find_wiki_path(args: argparse.Namespace) -> Path:
    if args.wiki_path:
        return Path(args.wiki_path).expanduser()
    env = os.environ.get("LLM_WIKI_PATH")
    if env:
        return Path(env).expanduser()
    return Path.home() / "wiki"


def collect_pages(wiki: Path) -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for directory in LAYER2_DIRS:
        layer_dir = wiki / directory
        if layer_dir.exists():
            for file_path in layer_dir.glob("*.md"):
                pages[file_path.stem] = file_path
    return pages


def extract_wikilinks(content: str) -> list[str]:
    raw_matches = re.findall(r"\[\[([^\]]+)\]\]", content)
    cleaned: list[str] = []
    for match in raw_matches:
        target = match.split("|")[0].split("#")[0].strip()
        if target:
            cleaned.append(target)
    return cleaned


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def parse_list_field(raw: str) -> list[str]:
    if not raw:
        return []
    value = raw.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    items: list[str] = []
    for part in value.split(","):
        item = part.strip().strip("'\"")
        if item:
            items.append(item)
    return items


def parse_tags(frontmatter: dict[str, str]) -> list[str]:
    return parse_list_field(frontmatter.get("tags", ""))


def parse_sources(frontmatter: dict[str, str]) -> list[str]:
    return parse_list_field(frontmatter.get("sources", ""))


def parse_contradictions(frontmatter: dict[str, str]) -> list[str]:
    return parse_list_field(frontmatter.get("contradictions", ""))


def parse_updated_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        normalized = value
        if len(normalized) == 10:
            normalized += "T00:00:00"
        return datetime.fromisoformat(normalized).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def load_schema_tags(wiki: Path) -> set[str] | None:
    schema_path = wiki / "SCHEMA.md"
    if not schema_path.exists():
        return None

    content = read_text(schema_path)
    in_taxonomy = False
    tags: set[str] = set()

    for line in content.split("\n"):
        if re.match(r"^##\s+Tag\s+Taxonomy", line, re.IGNORECASE):
            in_taxonomy = True
            continue
        if in_taxonomy and re.match(r"^##\s+", line):
            break
        if in_taxonomy and line.strip().startswith("- "):
            tag_part = line.strip()[2:].split(":")[0].split("(")[0].strip()
            for tag in tag_part.split(","):
                normalized = tag.strip().lower()
                if normalized:
                    tags.add(normalized)

    return tags if tags else None


def check_broken_links(pages: dict[str, Path], all_links: dict[str, list[str]]) -> list[str]:
    issues: list[str] = []
    for source, links in all_links.items():
        for link in links:
            if link not in pages:
                issues.append(f"  [{source}.md] broken link -> [[{link}]]")
    return issues


def check_orphans(pages: dict[str, Path], inbound: dict[str, list[str]]) -> list[str]:
    return [
        f"  {name}.md: orphan page (0 inbound wiki links)"
        for name in sorted(pages)
        if len(inbound.get(name, [])) == 0
    ]


def check_index_completeness(wiki: Path, pages: dict[str, Path]) -> list[str]:
    index_path = wiki / "index.md"
    if not index_path.exists():
        return ["  index.md not found - run 'init' or create it manually"]

    content = read_text(index_path)
    missing: list[str] = []
    for name in sorted(pages):
        if f"[[{name}]]" not in content and f"[{name}](" not in content:
            missing.append(f"  {name}.md not in index.md")
    return missing


def check_frontmatter(pages: dict[str, Path]) -> list[str]:
    issues: list[str] = []
    for name, path in sorted(pages.items()):
        content = read_text(path)
        if not re.match(r"^---", content):
            issues.append(f"  {name}.md: no frontmatter block")
            continue
        frontmatter = parse_frontmatter(content)
        for field in REQUIRED_FRONTMATTER:
            if field not in frontmatter or not frontmatter[field]:
                issues.append(f"  {name}.md: missing '{field}'")
    return issues


def check_tag_taxonomy(pages: dict[str, Path], schema_tags: set[str] | None) -> list[str]:
    if schema_tags is None:
        return []

    issues: list[str] = []
    for name, path in sorted(pages.items()):
        frontmatter = parse_frontmatter(read_text(path))
        for tag in parse_tags(frontmatter):
            if tag.lower() not in schema_tags:
                issues.append(f"  {name}.md: unknown tag '{tag}' (not in SCHEMA.md taxonomy)")
    return issues


def check_sources_exist(pages: dict[str, Path], wiki: Path) -> list[str]:
    issues: list[str] = []
    for name, path in sorted(pages.items()):
        frontmatter = parse_frontmatter(read_text(path))
        for source in parse_sources(frontmatter):
            if not (wiki / source).exists():
                issues.append(f"  {name}.md: source not found -> {source}")
    return issues


def check_min_outbound_links(pages: dict[str, Path], all_links: dict[str, list[str]]) -> list[str]:
    issues: list[str] = []
    for name, links in sorted(all_links.items()):
        valid_links = sorted({link for link in links if link in pages and link != name})
        if len(valid_links) < MIN_OUTBOUND_WIKI_LINKS:
            issues.append(
                f"  {name}.md: only {len(valid_links)} outbound wiki link(s) "
                f"(min {MIN_OUTBOUND_WIKI_LINKS})"
            )
    return issues


def check_contradictions_targets(pages: dict[str, Path]) -> list[str]:
    issues: list[str] = []
    for name, path in sorted(pages.items()):
        frontmatter = parse_frontmatter(read_text(path))
        for target in parse_contradictions(frontmatter):
            if target not in pages:
                issues.append(f"  {name}.md: contradiction target not found -> {target}")
    return issues


def check_index_header(
    wiki: Path, pages: dict[str, Path], fix: bool
) -> tuple[list[str], list[str]]:
    index_path = wiki / "index.md"
    if not index_path.exists():
        return [], []

    content = read_text(index_path)
    match = re.search(
        r"^> Last updated:\s*(\d{4}-\d{2}-\d{2})\s*\|\s*Total pages:\s*(\d+)\s*$",
        content,
        re.MULTILINE,
    )
    if not match:
        return ["  index.md: missing or malformed 'Last updated | Total pages' header"], []

    updated_dates = []
    for path in pages.values():
        frontmatter = parse_frontmatter(read_text(path))
        parsed = parse_updated_date(frontmatter.get("updated", ""))
        if parsed is not None:
            updated_dates.append(parsed)

    expected_date = (
        max(updated_dates).strftime("%Y-%m-%d")
        if updated_dates
        else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    expected_count = len(pages)

    current_date = match.group(1)
    current_count = int(match.group(2))

    if current_date == expected_date and current_count == expected_count:
        return [], []

    if fix:
        updated_content = re.sub(
            r"^> Last updated:\s*\d{4}-\d{2}-\d{2}\s*\|\s*Total pages:\s*\d+\s*$",
            f"> Last updated: {expected_date} | Total pages: {expected_count}",
            content,
            count=1,
            flags=re.MULTILINE,
        )
        if updated_content != content:
            write_text(index_path, updated_content)
            return [], [f"  index.md: updated header to {expected_date} / {expected_count} page(s)"]

    return [
        f"  index.md: header mismatch (expected Last updated {expected_date} | Total pages {expected_count})"
    ], []


def check_page_sizes(pages: dict[str, Path]) -> list[str]:
    issues: list[str] = []
    for name, path in sorted(pages.items()):
        line_count = read_text(path).count("\n")
        if line_count > PAGE_SIZE_WARN:
            issues.append(f"  {name}.md: {line_count} lines (>{PAGE_SIZE_WARN} - consider splitting)")
    return issues


def check_stale_pages(pages: dict[str, Path]) -> list[str]:
    issues: list[str] = []
    now = datetime.now(timezone.utc)
    for name, path in sorted(pages.items()):
        frontmatter = parse_frontmatter(read_text(path))
        updated = parse_updated_date(frontmatter.get("updated", ""))
        if updated is None:
            continue
        age = (now - updated).days
        if age > STALE_DAYS:
            issues.append(f"  {name}.md: last updated {age} days ago")
    return issues


def check_log_size(wiki: Path) -> str | None:
    log_path = wiki / "log.md"
    if not log_path.exists():
        return None
    count = len(re.findall(r"^## \[", read_text(log_path), re.MULTILINE))
    if count > LOG_ROTATION_THRESHOLD:
        year = datetime.now().year - 1
        return f"  log.md has {count} entries - rename to log-{year}.md and start fresh"
    return None


def section(title: str, items: list[str], icon: str) -> int:
    if not items:
        return 0
    print(f"{icon}  {title} ({len(items)}):")
    for item in items:
        print(item)
    print()
    return len(items)


def emit_json(
    wiki: Path,
    page_count: int,
    errors: list[str],
    warnings: list[str],
    info: list[str],
    strict: bool,
    exit_code: int,
) -> None:
    payload = {
        "wiki": str(wiki),
        "page_count": page_count,
        "strict": strict,
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "exit_code": exit_code,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    args = parse_args()
    wiki = find_wiki_path(args)

    if not wiki.exists():
        if args.json_output:
            emit_json(wiki, 0, ["  wiki directory not found"], [], [], args.strict, 2)
        else:
            print(f"❌  Wiki not found: {wiki}")
            print("    Set LLM_WIKI_PATH or pass the path as an argument.")
        sys.exit(2)

    pages = collect_pages(wiki)
    if not pages:
        if args.json_output:
            emit_json(wiki, 0, [], [], ["  no pages found in layer-2 directories"], args.strict, 0)
        else:
            print(f"🔍  Linting wiki: {wiki}\n")
            print("⚠️   No pages found in entities/, concepts/, comparisons/, or queries/.")
            print("    Start by ingesting a source.")
        sys.exit(0)

    all_links: dict[str, list[str]] = {}
    inbound: dict[str, list[str]] = defaultdict(list)
    for name, path in pages.items():
        links = extract_wikilinks(read_text(path))
        all_links[name] = links
        for link in links:
            inbound[link].append(name)

    schema_tags = load_schema_tags(wiki)

    errors = check_broken_links(pages, all_links) + check_sources_exist(pages, wiki)
    warnings = (
        check_orphans(pages, inbound)
        + check_index_completeness(wiki, pages)
        + check_frontmatter(pages)
        + check_tag_taxonomy(pages, schema_tags)
        + check_min_outbound_links(pages, all_links)
        + check_contradictions_targets(pages)
    )
    index_header_warnings, index_header_info = check_index_header(wiki, pages, args.fix)
    warnings += index_header_warnings
    info = check_page_sizes(pages) + check_stale_pages(pages) + index_header_info

    log_warning = check_log_size(wiki)
    if log_warning:
        info.append(log_warning)

    exit_code = 1 if errors or (args.strict and warnings) else 0

    if args.json_output:
        emit_json(wiki, len(pages), errors, warnings, info, args.strict, exit_code)
        sys.exit(exit_code)

    print(f"🔍  Linting wiki: {wiki}\n")
    print(f"    {len(pages)} page(s) found\n")

    section("Errors - fix before committing", errors, "❌")
    section("Warnings - should fix", warnings, "⚠️ ")
    section("Info - consider fixing", info, "ℹ️ ")

    print("─" * 48)
    if not errors and not warnings and not info:
        print("✅  Wiki is healthy - no issues found.\n")
    else:
        print(f"    {len(errors)} error(s)  {len(warnings)} warning(s)  {len(info)} info\n")

    if args.strict and warnings and not errors:
        print("    Strict mode promoted warnings to a failing exit code.\n")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
