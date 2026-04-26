"""Mechanical lint for the wiki — implements the six checks from CLAUDE.md.

Checks:
  1. Broken links     — `[[target]]` with no matching wiki file (ERROR)
  2. Missing fields   — frontmatter must have type/name/status/last_updated (ERROR)
  3. Orphan pages     — zero inbound links from any other wiki page (WARN)
  4. Stub debt        — `status: stub` older than 7 days (WARN)
  5. Stale pages      — `last_updated` older than 90 days (WARN)
  6. Contradictions   — `CONTRADICTION:` marker present (WARN)

Exit code: 1 if any ERROR, else 0. WARN-only runs still pass CI.
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

REQUIRED_FIELDS = ("type", "name", "status", "last_updated")
ROOT_PAGES = {"index.md", "log.md"}  # exempt from orphan check

STUB_DAYS = 7
STALE_DAYS = 90

# Match [[target]] or [[target|alias]] or [[target#anchor|alias]].
# Capture the target only (basename used for Obsidian resolution).
LINK_RE = re.compile(r"\[\[([^\]|#\n]+?)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\]")


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end], text[end + 5 :]


def parse_simple_fields(frontmatter: str) -> dict[str, str]:
    """Pull top-level `key: value` pairs. Values kept as raw strings."""
    out: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def parse_date(s: str) -> date | None:
    s = s.strip().strip("'\"")
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def collect_pages() -> list[Path]:
    return sorted(WIKI_DIR.rglob("*.md"))


def collect_link_targets(pages: list[Path]) -> dict[str, list[Path]]:
    """Files that wiki links can resolve to.

    Includes everything under wiki/ plus any markdown at the repo root
    (CLAUDE.md, README.md, etc.) — Obsidian resolves links by basename
    across the whole vault, and the vault root is the repo root.
    """
    idx: dict[str, list[Path]] = {}
    for p in pages:
        idx.setdefault(p.stem, []).append(p)
    for p in REPO_ROOT.glob("*.md"):
        idx.setdefault(p.stem, []).append(p)
    return idx


def extract_links(text: str) -> list[str]:
    # Markdown tables escape `|` as `\|` inside cells. Unescape before parsing
    # so `[[target\|alias]]` is treated as `[[target|alias]]`.
    text = text.replace("\\|", "|")
    return [m.group(1).strip() for m in LINK_RE.finditer(text)]


def main() -> int:
    pages = collect_pages()
    if not pages:
        print(f"No wiki pages found under {WIKI_DIR.relative_to(REPO_ROOT)}.")
        return 1

    index = collect_link_targets(pages)
    today = date.today()

    rel = lambda p: p.relative_to(REPO_ROOT).as_posix()

    broken_links: list[tuple[Path, str]] = []
    missing_fields: list[tuple[Path, list[str]]] = []
    stub_debt: list[tuple[Path, int]] = []
    stale: list[tuple[Path, int]] = []
    contradictions: list[Path] = []
    inbound: dict[str, int] = {p.stem: 0 for p in pages}

    # Collision check: only flag duplicates *within* wiki/. Root-level
    # vault files (CLAUDE.md etc.) sharing a basename with a wiki page
    # would be a problem too, but that case is rare and not present here.
    wiki_basenames: dict[str, list[Path]] = {}
    for p in pages:
        wiki_basenames.setdefault(p.stem, []).append(p)
    collisions: list[tuple[str, list[Path]]] = [
        (k, v) for k, v in wiki_basenames.items() if len(v) > 1
    ]

    for page in pages:
        text = page.read_text(encoding="utf-8")
        fm = split_frontmatter(text)
        body = text
        fields: dict[str, str] = {}
        if fm:
            frontmatter, body = fm
            fields = parse_simple_fields(frontmatter)

        # Check 2: required frontmatter fields
        if page.name not in ROOT_PAGES:
            missing = [f for f in REQUIRED_FIELDS if f not in fields]
            if missing:
                missing_fields.append((page, missing))

        # Check 1 + inbound counts: links
        # Scan the whole file (frontmatter included — owner: [[...]] counts as a link).
        for target in extract_links(text):
            if target in index:
                if target != page.stem:  # don't count self-links
                    inbound[target] = inbound.get(target, 0) + 1
            else:
                broken_links.append((page, target))

        # Check 4: stub debt
        if fields.get("status") == "stub":
            d = parse_date(fields.get("last_updated", ""))
            if d:
                age = (today - d).days
                if age > STUB_DAYS:
                    stub_debt.append((page, age))
            else:
                stub_debt.append((page, -1))  # unknown age

        # Check 5: stale pages
        d = parse_date(fields.get("last_updated", ""))
        if d:
            age = (today - d).days
            if age > STALE_DAYS:
                stale.append((page, age))

        # Check 6: contradictions
        if "CONTRADICTION:" in body:
            contradictions.append(page)

    # Check 3: orphans (zero inbound links, excluding root pages)
    orphans = [
        p for p in pages
        if p.name not in ROOT_PAGES and inbound.get(p.stem, 0) == 0
    ]

    errors = 0
    warns = 0

    print(f"Linted {len(pages)} wiki page(s).\n")

    if broken_links:
        errors += len(broken_links)
        print(f"ERROR — broken links ({len(broken_links)}):")
        for p, target in broken_links:
            print(f"  - {rel(p)}: [[{target}]]")
        print()

    if missing_fields:
        errors += len(missing_fields)
        print(f"ERROR — missing required frontmatter fields ({len(missing_fields)}):")
        for p, fields in missing_fields:
            print(f"  - {rel(p)}: missing {', '.join(fields)}")
        print()

    if collisions:
        errors += len(collisions)
        print(f"ERROR — basename collisions (Obsidian links resolve by basename) ({len(collisions)}):")
        for name, paths in collisions:
            print(f"  - {name}: {', '.join(rel(p) for p in paths)}")
        print()

    if stub_debt:
        warns += len(stub_debt)
        print(f"WARN — stub debt ({len(stub_debt)}, threshold {STUB_DAYS} days):")
        for p, age in stub_debt:
            label = f"{age} days" if age >= 0 else "unknown age"
            print(f"  - {rel(p)} ({label})")
        print()

    if stale:
        warns += len(stale)
        print(f"WARN — stale pages ({len(stale)}, threshold {STALE_DAYS} days):")
        for p, age in stale:
            print(f"  - {rel(p)} ({age} days)")
        print()

    if orphans:
        warns += len(orphans)
        print(f"WARN — orphan pages ({len(orphans)}, no inbound links):")
        for p in orphans:
            print(f"  - {rel(p)}")
        print()

    if contradictions:
        warns += len(contradictions)
        print(f"WARN — unresolved CONTRADICTION markers ({len(contradictions)}):")
        for p in contradictions:
            print(f"  - {rel(p)}")
        print()

    if errors == 0 and warns == 0:
        print("Clean. No issues found.")
    else:
        print(f"Summary: {errors} error(s), {warns} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
