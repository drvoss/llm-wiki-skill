#!/usr/bin/env python3
"""
wiki-stats.py - Lightweight summary for an llm-wiki directory.
"""

import argparse
import io
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

LAYER2_DIRS = ["entities", "concepts", "comparisons", "queries"]
RAW_DIRS = ["articles", "papers", "transcripts", "assets"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show summary stats for an llm-wiki directory.")
    parser.add_argument("wiki_path", nargs="?", help="Path to the wiki directory")
    parser.add_argument("--json", dest="json_output", action="store_true", help="Emit JSON")
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


def parse_updated(path: Path) -> datetime | None:
    match = re.search(r"^updated:\s*(.+)$", read_text(path), re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    try:
        if len(value) == 10:
            return datetime.fromisoformat(value)
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_wikilinks(content: str) -> list[str]:
    links = re.findall(r"\[\[([^\]]+)\]\]", content)
    cleaned: list[str] = []
    for link in links:
        target = link.split("|")[0].split("#")[0].strip()
        if target:
            cleaned.append(target)
    return cleaned


def count_log_entries(log_path: Path) -> int:
    if not log_path.exists():
        return 0
    return len(re.findall(r"^## \[", read_text(log_path), re.MULTILINE))


def last_log_date(log_path: Path) -> str | None:
    if not log_path.exists():
        return None
    matches = re.findall(r"^## \[(\d{4}-\d{2}-\d{2})\]", read_text(log_path), re.MULTILINE)
    return matches[-1] if matches else None


def collect_stats(wiki: Path) -> dict:
    pages_by_type: dict[str, list[Path]] = {}
    all_pages: list[Path] = []
    link_count = 0
    updated_dates: list[datetime] = []

    for directory in LAYER2_DIRS:
        layer_dir = wiki / directory
        files = sorted(layer_dir.glob("*.md")) if layer_dir.exists() else []
        pages_by_type[directory] = files
        all_pages.extend(files)

    for page in all_pages:
        content = read_text(page)
        link_count += len(extract_wikilinks(content))
        updated = parse_updated(page)
        if updated:
            updated_dates.append(updated)

    raw_counts = Counter()
    raw_root = wiki / "raw"
    if raw_root.exists():
        for directory in RAW_DIRS:
            dir_path = raw_root / directory
            if dir_path.exists():
                raw_counts[directory] = len([p for p in dir_path.iterdir() if p.is_file()])

    page_count = len(all_pages)
    return {
        "wiki": str(wiki),
        "pages": {
            "total": page_count,
            "entities": len(pages_by_type["entities"]),
            "concepts": len(pages_by_type["concepts"]),
            "comparisons": len(pages_by_type["comparisons"]),
            "queries": len(pages_by_type["queries"]),
        },
        "links": {
            "total": link_count,
            "average_per_page": round(link_count / page_count, 1) if page_count else 0.0,
        },
        "raw": {
            "total": sum(raw_counts.values()),
            "articles": raw_counts["articles"],
            "papers": raw_counts["papers"],
            "transcripts": raw_counts["transcripts"],
            "assets": raw_counts["assets"],
        },
        "activity": {
            "last_updated": max(updated_dates).strftime("%Y-%m-%d") if updated_dates else None,
            "last_log_entry": last_log_date(wiki / "log.md"),
            "log_entries": count_log_entries(wiki / "log.md"),
        },
    }


def print_text(stats: dict) -> None:
    print("Wiki Stats")
    print("-" * 36)
    print(
        f"Pages:     {stats['pages']['total']} total "
        f"({stats['pages']['entities']} entities, {stats['pages']['concepts']} concepts, "
        f"{stats['pages']['comparisons']} comparisons, {stats['pages']['queries']} queries)"
    )
    print(
        f"Links:     {stats['links']['total']} wikilinks, avg {stats['links']['average_per_page']} per page"
    )
    print(
        f"Sources:   {stats['raw']['total']} raw files "
        f"({stats['raw']['articles']} articles, {stats['raw']['papers']} papers, "
        f"{stats['raw']['transcripts']} transcripts, {stats['raw']['assets']} assets)"
    )
    print(
        f"Activity:  Last updated {stats['activity']['last_updated'] or 'unknown'} | "
        f"Last log {stats['activity']['last_log_entry'] or 'unknown'} | "
        f"{stats['activity']['log_entries']} log entries"
    )


def main() -> None:
    args = parse_args()
    wiki = resolve_wiki_path(args)
    if not wiki.exists():
        print(f"Wiki not found: {wiki}", file=sys.stderr)
        sys.exit(2)

    stats = collect_stats(wiki)
    if args.json_output:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print_text(stats)


if __name__ == "__main__":
    main()
