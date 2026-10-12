"""Dump an .xlsx (first sheet) as tab-separated rows using only the stdlib."""
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
path = sys.argv[1]
z = zipfile.ZipFile(path)

shared = []
if "xl/sharedStrings.xml" in z.namelist():
    for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
        shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))


def col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group()
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


rows = []
sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
for r in sheet.iter(f"{{{NS['m']}}}row"):
    row = {}
    for c in r.findall("m:c", NS):
        t = c.get("t")
        v = c.find("m:v", NS)
        f = c.find("m:f", NS)
        if t == "s" and v is not None:
            val = shared[int(v.text)]
        elif t == "inlineStr":
            val = "".join(x.text or "" for x in c.iter(f"{{{NS['m']}}}t"))
        else:
            val = v.text if v is not None else ""
        if f is not None and f.text:
            val = f"{val}  [formula: {f.text}]"
        row[col_index(c.get("r"))] = val
    width = max(row) + 1 if row else 0
    rows.append([row.get(i, "") for i in range(width)])

if "--json" in sys.argv:
    print(json.dumps(rows))
else:
    for row in rows:
        print("\t".join(row))
    print("---- core.xml ----")
    print(z.read("docProps/core.xml").decode("utf-8", "replace"))
