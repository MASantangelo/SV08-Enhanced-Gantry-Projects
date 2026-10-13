"""Render STEP files to PNG with their CAD colours, using FreeCAD's GUI. Quits when done.

Launched by render.ps1 as:  FreeCAD.exe tools\\render.py
FreeCAD doesn't pass script arguments through reliably, so settings come from env vars:
  RENDER_CONFIG  path to a JSON job file (see render.ps1 for the format it writes)
  RENDER_LOG     path to a log file (the GUI has no usable stdout)

Each view is a camera direction: azimuth (degrees around the vertical axis: 0 = from the
front, i.e. from -Y; 45 = front right; 315 = front left) and elevation (degrees above the
horizon; avoid 90, since the camera-mounted light washes out faces seen head-on).
Azimuth "outside" views a sub-assembly from its outside corner of the machine.
Images are rendered at 2x, cropped to the parts plus a margin, then scaled down, which
gives smooth edges without relying on FreeCAD's anti-aliasing settings.
"""
import json
import os
import traceback

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui

LOG = os.environ["RENDER_LOG"]


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def quit_freecad():
    QtCore.QTimer.singleShot(500, lambda: FreeCADGui.getMainWindow().close())


try:
    # utf-8-sig: PowerShell 5.1 writes the job file with a byte-order mark
    CFG = json.load(open(os.environ["RENDER_CONFIG"], encoding="utf-8-sig"))
except Exception:
    log("ERROR reading job file: " + traceback.format_exc())
    log("DONE")
    quit_freecad()
    raise


def camera(azimuth, elevation):
    # Start from FreeCAD's top view (looking down -Z), tilt toward the front, then spin around Z.
    tilt = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), 90 - elevation)
    spin = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), azimuth)
    return spin.multiply(tilt)


def outside_corner_azimuth(doc):
    """For a sub-assembly placed in machine coordinates: the 45-degree diagonal that looks
    at it from outside the machine (from the direction of its centre, seen from the origin)."""
    import math
    boxes = [o.Shape.BoundBox for o in doc.Objects
             if hasattr(o, "Shape") and not o.Shape.isNull() and o.Shape.BoundBox.isValid()]
    cx = sum((b.XMin + b.XMax) / 2 for b in boxes) / len(boxes)
    cy = sum((b.YMin + b.YMax) / 2 for b in boxes) / len(boxes)
    az = math.degrees(math.atan2(cx, -cy)) % 360  # camera direction (sin az, -cos az)
    return min((45, 135, 225, 315), key=lambda d: min(abs(az - d), 360 - abs(az - d)))


def shade_without_edges(doc):
    for obj in doc.Objects:
        vo = getattr(obj, "ViewObject", None)
        if vo is not None and "Shaded" in vo.listDisplayModes():
            vo.DisplayMode = "Shaded"


def content_box(img, step=4, threshold=248):
    """Bounding box of non-white pixels, found on a downscaled copy for speed."""
    small = img.scaled(img.width() // step, img.height() // step,
                       QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation)
    xs, ys = [], []
    for y in range(small.height()):
        for x in range(small.width()):
            if QtGui.qGray(small.pixel(x, y)) < threshold:
                xs.append(x)
                ys.append(y)
    if not xs:
        return QtCore.QRect(0, 0, img.width(), img.height())
    return QtCore.QRect(min(xs) * step, min(ys) * step,
                        (max(xs) - min(xs) + 1) * step, (max(ys) - min(ys) + 1) * step)


def without_metadata(img):
    """Pixel-only copy. FreeCAD embeds a creation time and the full local file path as PNG
    text chunks, which would leak the path and make every render differ byte-wise."""
    img = img.convertToFormat(QtGui.QImage.Format_RGB32)
    bits = bytes(img.constBits())
    return QtGui.QImage(bits, img.width(), img.height(), img.bytesPerLine(), QtGui.QImage.Format_RGB32).copy()


def crop_and_scale(src, dst, width, margin):
    """Crop to the parts, scale down, and write only if the pixels changed. Returns (w, h, written)."""
    img = QtGui.QImage(src)
    box = content_box(img)
    pad = int(max(box.width(), box.height()) * margin)
    box = box.adjusted(-pad, -pad, pad, pad).intersected(img.rect())
    out = without_metadata(img.copy(box).scaledToWidth(width, QtCore.Qt.SmoothTransformation))
    if os.path.exists(dst):
        old = QtGui.QImage(dst).convertToFormat(QtGui.QImage.Format_RGB32)
        if old == out and not old.textKeys():
            return out.width(), out.height(), False
    out.save(dst)
    return out.width(), out.height(), True


def render_all():
    try:
        import ImportGui
        width = CFG.get("width", 1600)
        margin = CFG.get("margin", 0.04)
        for job in CFG["jobs"]:
            doc = FreeCAD.newDocument("render")
            ImportGui.insert(job["step"], doc.Name)
            shade_without_edges(doc)
            view = FreeCADGui.ActiveDocument.ActiveView
            # Camera moves animate by default, and saveImage would catch them mid-move.
            view.setAnimationEnabled(False)
            os.makedirs(job["out_dir"], exist_ok=True)
            for v in job["views"]:
                az = outside_corner_azimuth(doc) if v["azimuth"] == "outside" else v["azimuth"]
                view.setCameraType("Perspective" if v.get("perspective") else "Orthographic")
                view.setCameraOrientation(camera(az, v["elevation"]))
                view.fitAll()
                QtGui.QApplication.processEvents()
                dst = os.path.join(job["out_dir"], f"{job['name']} - {v['name']}.png")
                tmp = dst + ".2x.png"
                view.saveImage(tmp, width * 2, int(width * 2 * 0.75), "White")
                w, h, written = crop_and_scale(tmp, dst, width, margin)
                os.remove(tmp)
                state = "OK  " if written else "SAME"
                log(f"{state} {os.path.basename(dst)}  {w}x{h}  (azimuth {az}, elevation {v['elevation']})")
            FreeCAD.closeDocument(doc.Name)
    except Exception:
        log("ERROR " + traceback.format_exc())
    finally:
        log("DONE")
        quit_freecad()


QtCore.QTimer.singleShot(1500, render_all)  # let the main window finish starting
