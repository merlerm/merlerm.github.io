#!/usr/bin/env python3
"""
Sync the CV summary (rendercv/resume.yaml -> sections.summary) from _pages/about.md.

_pages/about.md is the single source of truth for the bio/summary. This script
regenerates ONLY the `summary:` block of resume.yaml from the about-page body, so the
CV PDF (rendered from the YAML) and the website CV page (resume.json basics.summary,
converted by bin/yaml_to_json_resume.py) stay in sync. You only ever edit about.md.

Each paragraph of the about body becomes one summary entry. Markdown links
([text](url)) are stripped to their plain text for the CV summary; other markdown
(e.g. **bold**) is preserved.

Usage:
  python3 bin/about_to_summary.py --about _pages/about.md --resume rendercv/resume.yaml

Only the `summary:` block is touched; the rest of resume.yaml is left byte-for-byte
identical. The block carries an AUTO-GENERATED marker: edit about.md, not the YAML.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys


def strip_front_matter(text: str) -> str:
    """Drop a leading Jekyll '--- ... ---' front matter block."""
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def strip_md_links(s: str) -> str:
    """[text](url) -> text"""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)


def yaml_dq(s: str) -> str:
    """Escape a string for a YAML double-quoted scalar."""
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def get_paragraphs(body: str) -> list[str]:
    paras = []
    for block in re.split(r"\n\s*\n", body):
        text = re.sub(r"\s+", " ", strip_md_links(block)).strip()
        if text:
            paras.append(text)
    return paras


def render_block(paragraphs: list[str]) -> list[str]:
    # One list item per about.md paragraph. RenderCV emits a blank line between summary
    # entries (real Typst paragraphs); the custom Preamble sets `par(spacing: 0.8em)` so
    # they get a visible gap (the rendercv lib otherwise sets `par(spacing: 0cm)`, which
    # makes stacked summary paragraphs overlap). The web converter joins the list with
    # "\n\n" for basics.summary.
    lines = [
        "    summary:",
        "      # AUTO-GENERATED from _pages/about.md by "
        "bin/about_to_summary.py -- do not edit by hand.",
    ]
    for p in paragraphs:
        lines.append(f'      - "{yaml_dq(p)}"')
    return lines


def splice_summary(resume_text: str, block_lines: list[str]) -> str:
    lines = resume_text.split("\n")
    start = next(
        (i for i, ln in enumerate(lines) if ln.rstrip() == "    summary:"),
        None,
    )
    if start is None:
        raise SystemExit("Could not find a `    summary:` key in the resume YAML.")
    # The block ends at the next sibling mapping key at the same (4-space) indent.
    end = next(
        (i for i in range(start + 1, len(lines)) if re.match(r"^    [A-Za-z_]", lines[i])),
        len(lines),
    )
    return "\n".join(lines[:start] + block_lines + lines[end:])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--about", default="_pages/about.md")
    parser.add_argument("--resume", default="rendercv/resume.yaml")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if resume.yaml would change (don't write).",
    )
    args = parser.parse_args()

    about_path = Path(args.about)
    resume_path = Path(args.resume)
    for p in (about_path, resume_path):
        if not p.exists():
            print(f"Not found: {p}", file=sys.stderr)
            sys.exit(2)

    body = strip_front_matter(about_path.read_text(encoding="utf-8"))
    paragraphs = get_paragraphs(body)
    if not paragraphs:
        print(f"No body paragraphs found in {about_path}; nothing to sync.", file=sys.stderr)
        sys.exit(2)

    block_lines = render_block(paragraphs)
    original = resume_path.read_text(encoding="utf-8")
    updated = splice_summary(original, block_lines)

    if updated == original:
        print(f"CV summary already up to date ({len(paragraphs)} paragraph(s)).")
        return

    if args.check:
        print("resume.yaml summary is OUT OF SYNC with about.md (run without --check to fix).", file=sys.stderr)
        sys.exit(1)

    resume_path.write_text(updated, encoding="utf-8")
    print(f"Synced {len(paragraphs)} summary paragraph(s) from {about_path} into {resume_path}.")


if __name__ == "__main__":
    main()
