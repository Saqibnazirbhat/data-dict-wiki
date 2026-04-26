"""Detect drift between wiki pages and their cited raw/ sources.

Each wiki page lists its sources in frontmatter. This tool computes a SHA-256
of every cited source and compares to a `source_hashes:` map stored alongside.

Usage:
    python tools/check-drift.py            # report only; exit 1 on drift
    python tools/check-drift.py --update   # write current hashes back to frontmatter
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
HASH_LEN = 16  # truncated sha256 — 8 bytes is plenty for drift detection


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:HASH_LEN]


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Return (frontmatter_block, body) or None if no frontmatter."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end], text[end + 5 :]


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [v.strip() for v in inner.split(",")]
    return []


def parse_inline_map(value: str) -> dict[str, str]:
    value = value.strip()
    if value.startswith("{") and value.endswith("}"):
        inner = value[1:-1].strip()
        if not inner:
            return {}
        out: dict[str, str] = {}
        for pair in inner.split(","):
            if ":" not in pair:
                continue
            k, v = pair.split(":", 1)
            out[k.strip()] = v.strip()
        return out
    return {}


def extract_field(frontmatter: str, key: str) -> tuple[int, int, str] | None:
    """Return (line_start, line_end, value) for a top-level scalar/inline field.

    Handles inline form only (`key: value` on one line). Block lists/maps
    aren't used in this wiki yet; if they appear we fall back to no-op.
    """
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*?)$", re.MULTILINE)
    m = pattern.search(frontmatter)
    if not m:
        return None
    return m.start(), m.end(), m.group(1)


def get_sources(frontmatter: str) -> list[str]:
    field = extract_field(frontmatter, "sources")
    if not field:
        return []
    return parse_inline_list(field[2])


def get_source_hashes(frontmatter: str) -> dict[str, str]:
    field = extract_field(frontmatter, "source_hashes")
    if not field:
        return {}
    return parse_inline_map(field[2])


def format_hash_map(hashes: dict[str, str]) -> str:
    if not hashes:
        return "{}"
    pairs = ", ".join(f"{k}: {v}" for k, v in hashes.items())
    return "{" + pairs + "}"


def write_source_hashes(text: str, new_hashes: dict[str, str]) -> str:
    """Insert or replace `source_hashes:` line in frontmatter."""
    fm = split_frontmatter(text)
    if not fm:
        return text
    frontmatter, body = fm

    line = f"source_hashes: {format_hash_map(new_hashes)}"
    field = extract_field(frontmatter, "source_hashes")
    if field:
        start, end, _ = field
        new_fm = frontmatter[:start] + line + frontmatter[end:]
    else:
        # insert right after `sources:` line, or at end of frontmatter
        sources_field = extract_field(frontmatter, "sources")
        if sources_field:
            insert_at = sources_field[1]
            new_fm = frontmatter[:insert_at] + "\n" + line + frontmatter[insert_at:]
        else:
            new_fm = frontmatter.rstrip("\n") + "\n" + line + "\n"
    return f"---\n{new_fm}\n---\n{body}"


def scan(update: bool) -> int:
    drift: list[tuple[Path, str, str, str]] = []      # (page, source, stored, current)
    missing: list[tuple[Path, str]] = []              # (page, source)
    untracked: list[tuple[Path, str]] = []            # (page, source)
    orphan: list[tuple[Path, str]] = []               # (page, source) — hash but no longer cited
    updated: list[Path] = []

    for page in sorted(WIKI_DIR.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        fm = split_frontmatter(text)
        if not fm:
            continue
        frontmatter, _ = fm

        sources = get_sources(frontmatter)
        stored = get_source_hashes(frontmatter)
        if not sources:
            continue

        current: dict[str, str] = {}
        for src in sources:
            src_path = REPO_ROOT / src
            if not src_path.exists():
                missing.append((page, src))
                continue
            cur_hash = sha(src_path)
            current[src] = cur_hash
            if src not in stored:
                untracked.append((page, src))
            elif stored[src] != cur_hash:
                drift.append((page, src, stored[src], cur_hash))

        for src in stored:
            if src not in sources:
                orphan.append((page, src))

        if update and current != stored:
            new_text = write_source_hashes(text, current)
            if new_text != text:
                page.write_text(new_text, encoding="utf-8")
                updated.append(page)

    rel = lambda p: p.relative_to(REPO_ROOT).as_posix()

    if update:
        if updated:
            print(f"Updated source_hashes in {len(updated)} page(s):")
            for p in updated:
                print(f"  - {rel(p)}")
        else:
            print("No frontmatter changes needed.")
        if missing:
            print(f"\nWARNING: {len(missing)} page(s) cite missing sources:")
            for p, src in missing:
                print(f"  - {rel(p)}: {src}")
        return 0

    print(f"Scanned {sum(1 for _ in WIKI_DIR.rglob('*.md'))} wiki page(s).\n")
    issues = 0

    if drift:
        issues += len(drift)
        print(f"DRIFT — {len(drift)} source(s) changed since wiki was written:")
        for p, src, old, new in drift:
            print(f"  - {rel(p)}")
            print(f"      source:  {src}")
            print(f"      stored:  {old}")
            print(f"      current: {new}")

    if missing:
        issues += len(missing)
        print(f"\nMISSING SOURCE — {len(missing)} cited source file(s) not on disk:")
        for p, src in missing:
            print(f"  - {rel(p)}: {src}")

    if untracked:
        # untracked is a soft warning, not a failure — bootstrap with --update
        print(f"\nUNTRACKED — {len(untracked)} source(s) lack a stored hash (run --update):")
        for p, src in untracked:
            print(f"  - {rel(p)}: {src}")

    if orphan:
        print(f"\nORPHAN HASH — {len(orphan)} stored hash(es) for sources no longer cited:")
        for p, src in orphan:
            print(f"  - {rel(p)}: {src}")

    if not (drift or missing or untracked or orphan):
        print("Clean. All wiki pages are in sync with their cited sources.")

    return 1 if issues else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--update", action="store_true",
                    help="Write current source hashes back into wiki frontmatter.")
    args = ap.parse_args()
    return scan(update=args.update)


if __name__ == "__main__":
    sys.exit(main())
