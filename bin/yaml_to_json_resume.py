#!/usr/bin/env python3
"""
Convert assets/json/resume.yaml -> assets/json/resume.json

Usage:
  python3 bin/yaml_to_json_resume.py --in assets/json/resume.yaml --out assets/json/resume.json

This script is conservative: it maps the `cv` structure from your YAML into a JSON
structure compatible with the website's existing `resume.json` layout.
"""

from pathlib import Path
import argparse
import json
import sys
import re

try:
    import yaml
except Exception as e:
    print("PyYAML is required. Install with: python3 -m pip install pyyaml", file=sys.stderr)
    raise


def convert(yaml_data: dict) -> dict:
    cv = yaml_data.get("cv", {})
    out = {}

    def strip_md_link(s):
        """Extract plain text from markdown link: [text](url) -> text"""
        if not s:
            return s
        m = re.match(r"^\[([^\]]+)\]\(([^)]+)\)$", s.strip())
        if m:
            return m.group(1)
        return s

    def strip_md_italic(s):
        """Strip markdown italic markers: _text_ -> text"""
        if not s:
            return s
        return re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", s)

    def md_to_html(s):
        """Convert minimal markdown (bold, links) to HTML.

        This is conservative: it converts **bold** -> <strong> and [text](url) -> <a href="url">text</a>.
        If the input already contains HTML tags it will still perform substitutions but common cases are safe.
        """
        if not s:
            return s

        # convert markdown links [text](url) -> <a href="url">text</a>
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: '<a href="' + m.group(2) + '">' + m.group(1) + '</a>', s)
        # convert bold ***text*** -> <strong>text</strong>
        s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong>\1</strong>", s)
        # if leftover bold with ***text***, convert to <strong>text</strong>
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return s

    def map_degree(deg):
        if not deg:
            return deg
        mapping = {
            "M.Sc.": "Master of Science",
            "MSc": "Master of Science",
            "M.Sc": "Master of Science",
            "B.Sc.": "Bachelor of Science",
            "B.Sc": "Bachelor of Science",
            "BSc": "Bachelor of Science",
            "H.S.": "High School Diploma",
            "H.S": "High School Diploma",
            "H.S": "High School Diploma",
            "H.S.D": "High School Diploma",
        }
        return mapping.get(deg, deg)

    # basics
    basics = {}
    basics["name"] = cv.get("name")
    basics["email"] = cv.get("email")
    basics["phone"] = cv.get("phone")
    basics["url"] = cv.get("website")
    # put the location string into a simple object for compatibility
    basics["location"] = {"city": cv.get("location", "")}
    # summary is stored under sections.summary as a list of paragraphs
    sections = cv.get("sections", {})
    summary_list = sections.get("summary") or []
    basics["summary"] = md_to_html("\n\n".join(summary_list)) if isinstance(summary_list, list) else md_to_html(summary_list or "")
    out["basics"] = basics

    # work / experience
    out["work"] = []
    for e in sections.get("experience", []) or []:
        it = {}
        it["name"] = strip_md_link(e.get("company"))
        it["position"] = e.get("position")
        it["location"] = e.get("location")
        it["url"] = e.get("link")
        it["startDate"] = e.get("start_date")
        it["endDate"] = e.get("end_date")
        it["summary"] = md_to_html(e.get("summary")) if e.get("summary") else e.get("summary")
        if e.get("highlights"):
            it["highlights"] = [md_to_html(h) for h in e.get("highlights")]
        out["work"].append(it)

    # education
    out["education"] = []
    for ed in sections.get("education", []) or []:
        it = {}
        it["institution"] = strip_md_link(ed.get("institution"))
        it["area"] = ed.get("area")
        it["studyType"] = ed.get("degree")
        it["startDate"] = ed.get("start_date")
        it["endDate"] = ed.get("end_date")
        it["url"] = ed.get("link")
        if ed.get("highlights"):
            it["courses"] = [md_to_html(h) for h in ed.get("highlights")]
        # normalize degree naming
        it["studyType"] = map_degree(it.get("studyType"))
        if ed.get("transcript"):
            it["transcript"] = ed.get("transcript")
        out["education"].append(it)

    # publications
    out["publications"] = []
    for p in sections.get("publications", []) or []:
        it = {}
        raw_title = p.get("title") or p.get("name")
        # Extract URL from markdown link in title if present
        title_link = re.match(r"^\[([^\]]+)\]\(([^)]+)\)$", (raw_title or "").strip())
        it["name"] = title_link.group(1) if title_link else raw_title
        it["publisher"] = strip_md_italic(p.get("journal"))
        it["releaseDate"] = p.get("date")
        it["url"] = (title_link.group(2) if title_link else None) or p.get("url") or p.get("link")
        # authors -> summary or keep as list under summary
        if p.get("authors"):
            if isinstance(p.get("authors"), list):
                it["summary"] = ", ".join(p.get("authors"))
            else:
                it["summary"] = p.get("authors")
        # convert title/journal fields and summary from markdown to HTML
        if it.get("name"):
            it["name"] = md_to_html(it.get("name"))
        if it.get("publisher"):
            it["publisher"] = md_to_html(it.get("publisher"))
        if it.get("summary"):
            it["summary"] = md_to_html(it.get("summary"))
        out["publications"].append(it)

    # volunteer
    out["volunteer"] = []
    for v in sections.get("volunteer", []) or []:
        it = {}
        it["organization"] = strip_md_link(v.get("company") or v.get("organization"))
        it["position"] = v.get("position")
        it["url"] = v.get("link")
        it["startDate"] = v.get("start_date")
        it["endDate"] = v.get("end_date")
        it["summary"] = md_to_html(v.get("summary")) if v.get("summary") else v.get("summary")
        out["volunteer"].append(it)

    # awards / additional_experience_and_awards
    out["awards"] = []
    for a in sections.get("additional_experience_and_awards", []) or []:
        it = {}
        it["title"] = strip_md_link(a.get("label"))
        it["summary"] = md_to_html(a.get("details")) if a.get("details") else a.get("details")
        it["url"] = a.get("link")
        it["date"] = a.get("date")
        it["awarder"] = a.get("awarder")
        out["awards"].append(it)

    # languages: support dict objects, label/details, or inline "**Lang:** Fluency | ..." strings
    # certificate files for languages (can't store in YAML sections without rendercv validation errors)
    cert_map = {"English": "english_matteo_merler.pdf"}
    out["languages"] = []
    for l in sections.get("languages", []) or []:
        if isinstance(l, dict):
            name = l.get("language") or l.get("label")
            fluency = l.get("fluency") or l.get("details")
            lang = {"language": name, "fluency": fluency}
            if isinstance(lang.get("language"), str):
                lang["language"] = md_to_html(lang.get("language"))
            if isinstance(lang.get("fluency"), str):
                lang["fluency"] = md_to_html(lang.get("fluency"))
            if l.get("certificate_file"):
                lang["certificate_file"] = l.get("certificate_file")
            out["languages"].append(lang)
        elif isinstance(l, str) and "|" in l:
            # inline format: "**Italian:** Native | **English:** C2 (...) | ..."
            for part in l.split("|"):
                part = part.strip()
                # strip markdown bold markers
                part = re.sub(r"\*\*(.+?)\*\*", r"\1", part)
                if ":" in part:
                    name, fluency = part.split(":", 1)
                    lang = {"language": name.strip(), "fluency": fluency.strip()}
                    if name.strip() in cert_map:
                        lang["certificate_file"] = cert_map[name.strip()]
                    out["languages"].append(lang)
                else:
                    out["languages"].append({"language": part, "fluency": ""})
        else:
            out["languages"].append({"language": l, "fluency": ""})

    # certificates (pass-through if present)
    out["certificates"] = sections.get("certificates", []) or []

    # pass-through for other simple sections
    for key in ("skills", "interests", "references", "projects"):
        if key in sections:
            out[key] = sections.get(key)

    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input", default="assets/json/resume.yaml")
    parser.add_argument("--out", dest="output", default="assets/json/resume.json")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    data = yaml.safe_load(input_path.read_text(encoding="utf-8"))
    result = convert(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
