#!/usr/bin/env python3
"""
Sync the `publications:` section of rendercv/resume.yaml from _bibliography/papers.bib.

papers.bib is the single source of truth for publications. This script regenerates
the `publications:` block of the RenderCV YAML so that both the CV PDF (rendered from
the YAML) and the website's resume.json (converted from the YAML by
bin/yaml_to_json_resume.py) stay in sync. You only ever add new papers to papers.bib.

Usage:
  python3 bin/bib_to_publications.py --bib _bibliography/papers.bib --resume rendercv/resume.yaml

The publications block is AUTO-GENERATED: do not hand-edit it in resume.yaml, edit the
.bib instead. Only the `publications:` block is touched; the rest of resume.yaml is left
byte-for-byte identical.

Mapping rules (BibTeX -> RenderCV publication entry):
  title    <- title
  authors  <- author, normalized to "First Last", the owner (default "Matteo Merler")
              wrapped in **bold**, and equal-contribution markers (`*`) shown as a
              trailing dagger (†).
  journal  <- cv_venue if present, else "arXiv preprint" for arXiv @misc entries,
              else booktitle / journal (rendered italic in the CV).
  date     <- cv_date if present, else derived from year (+ month) as YYYY-MM-01.
  url      <- cv_url if present, else the arXiv PDF link for arXiv entries, else the
              url / pdf / html field.

Optional per-entry override / control fields you can add to any .bib entry (al-folio
ignores unknown fields, so they don't affect the publications page):
  cv_venue = {...}   exact venue string to show on the CV
  cv_date  = {YYYY-MM-DD}   exact date for CV ordering and display
  cv_url   = {...}   exact link for the CV title
  cv_hide  = {true}  exclude this paper from the CV while keeping it on the website
"""

from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
except Exception:
    print(
        "bibtexparser is required. Install with: python3 -m pip install bibtexparser",
        file=sys.stderr,
    )
    raise

OWNER_DEFAULT = "Matteo Merler"

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def strip_braces(s: str) -> str:
    return (s or "").replace("{", "").replace("}", "")


def yaml_dq(s: str) -> str:
    """Escape a string for use inside a YAML double-quoted scalar."""
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')


def is_truthy(v) -> bool:
    return str(v).strip().lower() in {"true", "1", "yes"}


def parse_month(raw) -> int | None:
    if not raw:
        return None
    key = collapse_ws(strip_braces(str(raw))).lower()[:3]
    return MONTHS.get(key)


def normalize_author(token: str, owner: str) -> str:
    """Turn a raw BibTeX author token into the CV display form.

    "Dainese*, Nicola" -> "Nicola Dainese†"
    "Merler, Matteo"   -> "**Matteo Merler**"
    "Matteo Merler*"   -> "**Matteo Merler**†"
    """
    token = collapse_ws(strip_braces(token))
    has_dagger = "*" in token
    name = token.replace("*", "").strip()
    if "," in name:
        last, first = name.split(",", 1)
        name = f"{collapse_ws(first)} {collapse_ws(last)}".strip()
    if name == owner:
        name = f"**{name}**"
    if has_dagger:
        name += "†"  # †
    return name


def split_authors(author_field: str) -> list[str]:
    field = collapse_ws(author_field)
    return [a for a in re.split(r"\s+and\s+", field) if a.strip()]


def is_arxiv(entry: dict) -> bool:
    return (
        "arxiv" in (entry.get("archiveprefix", "").lower())
        or bool(entry.get("eprint"))
    )


def derive_venue(entry: dict) -> str:
    if entry.get("cv_venue"):
        return collapse_ws(strip_braces(entry["cv_venue"]))
    if entry.get("ENTRYTYPE", "").lower() == "misc" and is_arxiv(entry):
        return "arXiv preprint"
    for key in ("booktitle", "journal", "publisher"):
        if entry.get(key):
            return collapse_ws(strip_braces(entry[key]))
    return ""


def derive_date(entry: dict) -> str | None:
    if entry.get("cv_date"):
        return collapse_ws(strip_braces(entry["cv_date"]))
    year = collapse_ws(strip_braces(entry.get("year", "")))
    if not year:
        return None
    month = parse_month(entry.get("month"))
    return f"{year}-{month:02d}-01" if month else f"{year}-01-01"


def derive_url(entry: dict) -> str | None:
    if entry.get("cv_url"):
        return collapse_ws(strip_braces(entry["cv_url"]))
    if is_arxiv(entry) and entry.get("eprint"):
        return f"https://arxiv.org/pdf/{collapse_ws(strip_braces(entry['eprint']))}"
    if entry.get("url"):
        return collapse_ws(strip_braces(entry["url"]))
    pdf = collapse_ws(strip_braces(entry.get("pdf", "")))
    if pdf.startswith("http"):
        return pdf
    if entry.get("html"):
        return collapse_ws(strip_braces(entry["html"]))
    return None


def entry_to_pub(entry: dict, owner: str) -> dict:
    title = collapse_ws(strip_braces(entry.get("title", "")))
    return {
        "title": title,
        "authors": [normalize_author(a, owner) for a in split_authors(entry.get("author", ""))],
        "venue": derive_venue(entry),
        "date": derive_date(entry),
        "url": derive_url(entry),
    }


def load_publications(bib_path: Path, owner: str) -> list[dict]:
    text = bib_path.read_text(encoding="utf-8")
    # Strip the leading Jekyll front matter (--- ... ---) al-folio prepends.
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]

    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    db = bibtexparser.loads(text, parser=parser)

    pubs = []
    for entry in db.entries:
        if is_truthy(entry.get("cv_hide", "")):
            continue
        pub = entry_to_pub(entry, owner)
        if not pub["title"]:
            continue
        pubs.append(pub)

    # Most recent first; stable for equal dates so .bib order breaks ties.
    pubs.sort(key=lambda p: p["date"] or "", reverse=True)
    return pubs


def render_block(pubs: list[dict]) -> list[str]:
    """Render the publications block as a list of lines (4-space base indent)."""
    lines = ["    publications:"]
    lines.append(
        "      # AUTO-GENERATED from _bibliography/papers.bib by "
        "bin/bib_to_publications.py -- do not edit by hand."
    )
    for p in pubs:
        url = p["url"] or ""
        title_md = f"[{p['title']}]({url})" if url else p["title"]
        lines.append(f'      - title: "{yaml_dq(title_md)}"')
        if p["date"]:
            lines.append(f'        date: "{yaml_dq(p["date"])}"')
        lines.append("        authors:")
        for a in p["authors"]:
            lines.append(f'          - "{yaml_dq(a)}"')
        if p["venue"]:
            lines.append(f'        journal: "{yaml_dq("_" + p["venue"] + "_")}"')
        if url:
            lines.append(f'        url: "{yaml_dq(url)}"')
    return lines


def splice_publications(resume_text: str, block_lines: list[str]) -> str:
    lines = resume_text.split("\n")
    start = next(
        (i for i, ln in enumerate(lines) if ln.rstrip() == "    publications:"),
        None,
    )
    if start is None:
        raise SystemExit("Could not find a `    publications:` key in the resume YAML.")
    # The block ends at the next sibling mapping key at the same (4-space) indent.
    end = next(
        (i for i in range(start + 1, len(lines)) if re.match(r"^    [A-Za-z_]", lines[i])),
        len(lines),
    )
    new_lines = lines[:start] + block_lines + lines[end:]
    return "\n".join(new_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", default="_bibliography/papers.bib")
    parser.add_argument("--resume", default="rendercv/resume.yaml")
    parser.add_argument("--owner", default=OWNER_DEFAULT, help="Author name to bold")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if resume.yaml would change (don't write).",
    )
    args = parser.parse_args()

    bib_path = Path(args.bib)
    resume_path = Path(args.resume)
    for p in (bib_path, resume_path):
        if not p.exists():
            print(f"Not found: {p}", file=sys.stderr)
            sys.exit(2)

    pubs = load_publications(bib_path, args.owner)
    block_lines = render_block(pubs)

    original = resume_path.read_text(encoding="utf-8")
    updated = splice_publications(original, block_lines)

    if updated == original:
        print(f"resume.yaml already up to date ({len(pubs)} publications).")
        return

    if args.check:
        print("resume.yaml is OUT OF SYNC with papers.bib (run without --check to fix).", file=sys.stderr)
        sys.exit(1)

    resume_path.write_text(updated, encoding="utf-8")
    print(f"Synced {len(pubs)} publications from {bib_path} into {resume_path}.")


if __name__ == "__main__":
    main()
