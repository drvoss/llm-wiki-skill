# llm-wiki Operations Guide

**Language:** [English](OPERATIONS.md) | [한국어](OPERATIONS.ko.md) | [简体中文](OPERATIONS.zh-CN.md)

This guide covers the day-2 workflow for a real wiki: cleanup, batch updates,
lint discipline, and when to archive or file material.

---

## 1. Operating model

Use the wiki as a maintained knowledge base, not as a dumping ground.

- `raw/` is immutable source material
- layer-2 pages (`entities/`, `concepts/`, `comparisons/`, `queries/`) are curated synthesis
- `SCHEMA.md` is the contract
- `index.md` and `log.md` are the navigation backbone

Good operating rhythm:

1. Ingest or update a few related sources
2. Update the relevant pages in one pass
3. Run `wiki-lint.py`
4. Fix navigation or taxonomy drift immediately

---

## 2. Duplicate page cleanup

Duplicate pages are one of the easiest ways for a wiki to decay.

Use this rule of thumb:

- **Merge** when two pages cover the same entity or concept
- **Keep separate** when the pages represent different scopes
- **Archive** when one page is fully superseded

Suggested cleanup sequence:

1. Choose the surviving page
2. Move unique facts into that page
3. Replace important links in other pages
4. Remove the old page from `index.md`
5. Add an `archive` or `update` entry to `log.md`

---

## 3. Schema drift management

Schema drift usually appears as:

- too many near-duplicate tags
- pages with mixed scopes
- inconsistent naming

When this happens:

1. Tighten the tag taxonomy in `SCHEMA.md`
2. Rename tags in pages to match the new taxonomy
3. Revisit page titles and file names
4. Run `wiki-lint.py --strict`

If you keep finding the same off-taxonomy idea, add it to `SCHEMA.md` first,
then start using it on pages.

---

## 4. Batch ingest strategy

When several sources are about the same topic, do not process them one by one.

Use this order:

1. Read all related sources
2. Make one list of recurring entities and concepts
3. Check the wiki once for what already exists
4. Update or create pages in one pass
5. Update `index.md` once
6. Write one log entry for the batch

This keeps the wiki cleaner and reduces duplicate page creation.

---

## 5. Query filing rules

Not every answer belongs in `queries/`.

Good candidates:

- answers that synthesize several pages
- answers you expect to ask again
- answers that support a recurring decision

Bad candidates:

- simple lookups
- one-line factual answers
- questions that are trivial to re-derive

If in doubt, file only the answers that would be annoying to rebuild from scratch.

---

## 6. Stale page review

A stale page is not always a bad page. It may simply describe a stable concept.

Review stale pages with this decision tree:

- **Still accurate and useful?** Keep it, maybe bump `updated` after review
- **Partly outdated but still relevant?** Update it
- **Fully superseded?** Archive it

Use stale review to improve quality, not to create churn for its own sake.

---

## 7. Archiving workflow

Archive when a page is replaced, obsolete, or outside the wiki's active scope.

Recommended steps:

1. Move the page under `_archive/`
2. Remove it from `index.md`
3. Replace critical wikilinks where needed
4. Add a log entry describing what replaced it

Do not archive raw sources. Raw files are your provenance layer.

---

## 8. Lint workflow

Use `wiki-lint.py` as your routine guardrail.

```bash
python3 scripts/wiki-lint.py ~/wiki/my-domain
python3 scripts/wiki-lint.py --strict ~/wiki/my-domain
python3 scripts/wiki-lint.py --json ~/wiki/my-domain
python3 scripts/wiki-lint.py --fix ~/wiki/my-domain
```

Suggested usage:

- regular local maintenance: plain lint
- CI or shared repos: `--strict`
- automation and reporting: `--json`
- safe metadata repair: `--fix`

---

## 9. Stats workflow

Use `wiki-stats.py` when you want a quick positive snapshot instead of a fault report.

```bash
python3 scripts/wiki-stats.py ~/wiki/my-domain
python3 scripts/wiki-stats.py --json ~/wiki/my-domain
```

Good uses:

- checking that the wiki is actually growing
- reviewing the balance between page types
- seeing whether raw sources and curated pages are moving together

---

## 10. Suggested maintenance cadence

### After each meaningful ingest

- update affected pages
- update index/log
- run lint

### After a batch of sources

- do one cleanup pass for naming and tags
- file 1-2 durable queries if needed

### Periodically

- review stale pages
- review tag sprawl
- archive obsolete pages

This is enough to keep a wiki healthy without turning it into ceremony.
