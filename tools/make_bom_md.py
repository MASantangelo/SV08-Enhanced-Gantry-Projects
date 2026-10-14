"""Build BOM.md from the BOM spreadsheet.

Usage: python make_bom_md.py <variant folder> <xlsx name> <title>
Section rows = only column A filled. Data rows = Category, Qty, Description, Link, Notes.
Made parts (printed parts, plates) link to their STL preview when one with a matching name
exists in the variant's Base Components (Print Ready or flat) or in Shared Components.
"""
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote, urlparse

variant, xlsx_name, title = sys.argv[1], sys.argv[2], sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__))
rows = json.loads(subprocess.check_output(
    [sys.executable, "-I", os.path.join(here, "read_xlsx.py"), os.path.join(variant, xlsx_name), "--json"]))

def norm(s):
    s = re.sub(r"^\d+x\s+", "", s)
    s = re.sub(r"\s*-\s*For Printing$", "", s)
    return s.strip().lower()


# STL preview folders, as path parts relative to the variant folder; earlier entries win.
STL_DIRS = [
    ("Base Components", "Print Ready", "For Viewing"),
    ("Base Components", "For Viewing"),
    ("..", "Shared Components", "Print Ready", "For Viewing"),
]
stl_by_name = {}
for parts in STL_DIRS:
    d = os.path.join(variant, *parts)
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if f.lower().endswith(".stl"):
            stl_by_name.setdefault(norm(os.path.splitext(f)[0]), parts + (f,))
has_shared = os.path.isdir(os.path.join(variant, "..", "Shared Components"))


def rel(*parts):
    return "/".join(quote(p) for p in parts)


def cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def buy(url):
    url = (url or "").strip()
    if not url.startswith("http"):
        return ""
    host = urlparse(url).netloc.lower()
    stores = {"amazon.": "Amazon", "aliexpress.": "AliExpress", "mouser.": "Mouser", "mcmaster.": "McMaster-Carr"}
    label = next((v for k, v in stores.items() if k in host), host.removeprefix("www."))
    return f"[{label}]({url})"


out = [f"# {title}: Bill of Materials", ""]
out.append(f"Generated from [`{xlsx_name}`]({rel(xlsx_name)}). If the two disagree, the spreadsheet is correct.")
out.append("")
out.append("Links are plain product pages with no affiliate or tracking codes. Where a listing has multiple "
           "options, the **Notes** column says which one to pick.")
out.append("")

header = None
section = None
toc = []
body = []
for r in rows:
    r = (r + [""] * 5)[:5]
    if header is None:
        if r[0] == "Category":
            header = r
        continue
    if r[0] and not any(r[1:]):
        section = r[0]
        anchor = re.sub(r"[^\w\- ]", "", section.lower()).strip().replace(" ", "-")
        toc.append(f"- [{section}](#{anchor})")
        body += ["", f"## {section}", ""]
        if section.startswith("Xol"):
            body += ["*Optional: only needed if you're building the Xol carriage.*", ""]
        if section == "Printed Parts":
            where = []
            if os.path.isdir(os.path.join(variant, "Base Components", "Print Ready")):
                where.append(f"[`Base Components/Print Ready`]({rel('Base Components', 'Print Ready')})")
            if has_shared:
                where.append(f"[`Shared Components/Print Ready`]({rel('..', 'Shared Components', 'Print Ready')}) "
                             f"(parts common to every version)")
            body += [f"Print files are in {' and '.join(where)}. Click a part name to preview it in 3D.", ""]
        elif section.endswith("Plates"):
            verb = "Machining" if section.startswith("Metal") else "Cutting"
            body += [f"{verb} files are in [`Base Components`]({rel('Base Components')}). "
                     f"Click a part name to preview it in 3D.", ""]
        body += ["| Qty | Part | Buy | Notes |", "|---:|---|---|---|"]
        continue
    if not r[2]:
        continue
    part = cell(r[2])
    if section == "Printed Parts" or section.endswith("Plates"):
        stl = stl_by_name.get(norm(r[2]))
        if not stl:  # BOM and file names can differ; fall back to a unique leading-words match
            lead = " ".join(norm(r[2]).split()[:3])
            hits = [v for k, v in stl_by_name.items() if k.startswith(lead + " ")]
            stl = hits[0] if len(hits) == 1 else None
            if stl:
                print(f"fuzzy: {r[2]!r} -> {stl[-1]!r}")
        if stl:
            part = f"[{part}]({rel(*stl)})"
    notes = cell(r[4])
    if notes == "Check Repo":
        notes = ""
    body.append(f"| {cell(r[1])} | {part} | {buy(r[3])} | {notes} |")

out += ["## Contents", ""] + toc + body + [""]
dst = os.path.join(variant, "BOM.md")
with open(dst, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))

print(f"wrote {dst}: {sum(1 for l in body if l.startswith('| ') and not l.startswith('| Qty'))} parts, {len(toc)} sections")
