"""Render build-guide step images from an assembly STEP, using FreeCAD's GUI. Quits when done.

Launched by build-steps.ps1 as:  FreeCAD.exe tools\\build_steps.py
Settings come from env vars (FreeCAD doesn't pass script arguments through reliably):
  STEPS_CONFIG  path to a guide's JSON step file (see Docs/steps/*.json)
  STEPS_LOG     path to a log file (the GUI has no usable stdout)

A step file names groups of parts, then lists the steps. In each step image the parts added in
that step are drawn in the accent colour, parts fitted in earlier steps of the same sequence are
grey, and everything else is hidden, so each picture shows exactly what to do next.

  {
    "step": "Printed Version/Base Assemblies/XY Joint Right Printed 6mm.step",  (relative to the repo)
    "out_dir": "Docs/Images/XY Joint",
    "width": 1200,
    "view": {"azimuth": 45, "elevation": 30},
    "groups": {
      "bottom plate": [{"label": "Bottom Plate"}],
      "bottom bearing": [{"label": "F695", "z": [-5, 10]}]          (x / y / z: ranges for the part's centre)
    },
    "steps": [
      {"name": "01 Bottom bearing", "seq": "bottom", "context": ["bottom plate"], "new": ["bottom bearing"]},
      {"name": "02 Bottom inserts", "seq": "bottom", "new": ["bottom inserts"], "view": {"azimuth": 225, "elevation": -35}}
    ]
  }

"label" is a regular expression matched against the part name (FreeCAD's copy suffixes like
"001" are ignored). "context" adds groups shown in grey from that step on; everything shown in
earlier steps with the same "seq" (context or new) stays visible in grey.
"""
import json
import math
import os
import re
import traceback

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui

LOG = os.environ["STEPS_LOG"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCENT = (0.93, 0.47, 0.10)
DONE = (0.80, 0.80, 0.82)


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def quit_freecad():
    QtCore.QTimer.singleShot(500, lambda: FreeCADGui.getMainWindow().close())


try:
    CFG = json.load(open(os.environ["STEPS_CONFIG"], encoding="utf-8-sig"))
except Exception:
    log("ERROR reading step file: " + traceback.format_exc())
    log("DONE")
    quit_freecad()
    raise

# Reuse the camera and image helpers from render.py without running its job loop.
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.py"), encoding="utf-8").read()
_helpers = _src.split("try:\n    # utf-8-sig")[0] + _src.split("    raise\n", 1)[1].split("def render_all")[0]
_ns = {"__name__": "render_helpers"}
os.environ.setdefault("RENDER_LOG", LOG)
exec(compile(_helpers, "render.py", "exec"), _ns)
camera, crop_and_scale = _ns["camera"], _ns["crop_and_scale"]


def leaves(doc):
    out = []
    for o in doc.Objects:
        if o.TypeId == "Part::Feature" and o.Shape.Solids:
            sh = o.Shape.copy()
            try:
                sh.Placement = o.getGlobalPlacement()
            except Exception:
                pass
            name = re.sub(r"\s*\d{3}$", "", o.Label)
            out.append((o, name, sh.BoundBox.Center))
    return out


def members(parts, rules):
    hit = []
    for o, name, c in parts:
        for r in rules:
            if re.search(r["label"], name) and all(a not in r or r[a][0] <= getattr(c, a) <= r[a][1] for a in ("x", "y", "z")):
                hit.append(o)
                break
    return hit


def render_all():
    try:
        import ImportGui
        width = CFG.get("width", 1200)
        out_dir = os.path.join(ROOT, CFG["out_dir"])
        os.makedirs(out_dir, exist_ok=True)
        doc = FreeCAD.newDocument("steps")
        ImportGui.insert(os.path.join(ROOT, CFG["step"]), doc.Name)
        parts = leaves(doc)
        groups = {g: members(parts, rules) for g, rules in CFG["groups"].items()}
        for g, objs in groups.items():
            if not objs:
                log(f"WARN group '{g}' matched no parts")
        view = FreeCADGui.ActiveDocument.ActiveView
        view.setAnimationEnabled(False)
        view.setCameraType("Orthographic")
        done_by_seq = {}
        for st in CFG["steps"]:
            seq = st.get("seq", "")
            done = list(done_by_seq.get(seq, [])) + list(st.get("context", []))
            new = st["new"]
            show_new = {id(o) for g in new for o in groups[g]}
            show_done = {id(o) for g in done for o in groups[g]} - show_new
            for o, _name, _c in parts:
                vo = o.ViewObject
                if id(o) in show_new:
                    vo.Visibility = True
                    vo.ShapeColor = ACCENT
                    vo.DisplayMode = "Shaded"
                elif id(o) in show_done:
                    vo.Visibility = True
                    vo.ShapeColor = DONE
                    vo.DisplayMode = "Shaded"
                else:
                    vo.Visibility = False
            v = st.get("view", CFG.get("view", {"azimuth": 45, "elevation": 30}))
            view.setCameraOrientation(camera(v["azimuth"], v["elevation"]))
            view.fitAll()
            QtGui.QApplication.processEvents()
            dst = os.path.join(out_dir, st["name"] + ".png")
            tmp = dst + ".2x.png"
            view.saveImage(tmp, width * 2, int(width * 2 * 0.75), "White")
            w, h, written = crop_and_scale(tmp, dst, width, 0.05)
            os.remove(tmp)
            log(f"{'OK  ' if written else 'SAME'} {os.path.basename(dst)}  {w}x{h}  "
                f"(new: {sum(len(groups[g]) for g in new)} parts, grey: {len(show_done)})")
            done_by_seq.setdefault(seq, [])
            done_by_seq[seq] += [g for g in list(st.get("context", [])) + new if g not in done_by_seq[seq]]
        FreeCAD.closeDocument(doc.Name)
    except Exception:
        log("ERROR " + traceback.format_exc())
    finally:
        log("DONE")
        quit_freecad()


QtCore.QTimer.singleShot(1500, render_all)
