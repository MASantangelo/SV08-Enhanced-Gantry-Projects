"""Build the landing-page image: the same render of each variant, split into labelled regions.

Usage (FreeCAD's python.exe):  python tools/landing_composite.py
Writes Renders/Landing - Front Right.png at the repo root.

Uses <variant>/Renders/Full Gantry - Front Right.png for each variant in REGIONS that has one.
With three variants the image is split in a "Y" from its centre: seams run to the top-left
corner, the top-right corner and the bottom middle, giving a left, a top and a right region.
With two, a single vertical seam splits it down the middle. Each region gets its variant's label.
Renders are aligned on the top-left of their content, since each was auto-cropped separately.
Like render.py, it writes pixels only and skips unchanged output.
"""
import os
import sys

from PySide2 import QtCore, QtGui

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# (variant folder, label, region, label centre as fractions of the image)
REGIONS = [
    ("Printed Version", "Printed 6mm", "left", (0.13, 0.92)),
    ("Metal Version", "Aluminum 5mm", "top", (0.50, 0.06)),
    ("CF Version", "Carbon Fiber 6mm", "right", (0.85, 0.92)),
]
VIEW = "Full Gantry - Front Right.png"
OUT = os.path.join(ROOT, "Renders", "Landing - Front Right.png")
SEAM = QtGui.QColor(200, 200, 200)
TEXT = QtGui.QColor(40, 40, 40)
LABEL_BG = QtGui.QColor(255, 255, 255, 225)
LABEL_EDGE = QtGui.QColor(190, 190, 190)


def content_origin(img, step=2, threshold=248):
    xs, ys = [], []
    for y in range(0, img.height(), step):
        for x in range(0, img.width(), step):
            if QtGui.qGray(img.pixel(x, y)) < threshold:
                xs.append(x)
                ys.append(y)
    return QtCore.QPoint(min(xs), min(ys))


def region_polygons(w, h, names):
    """Polygons (lists of points) for each region name, plus the seam segments."""
    c = (w / 2, h / 2)
    if len(names) == 3:
        polys = {
            "left": [c, (0, 0), (0, h), (w / 2, h)],
            "top": [c, (0, 0), (w, 0)],
            "right": [c, (w, 0), (w, h), (w / 2, h)],
        }
        seams = [(c, (0, 0)), (c, (w, 0)), (c, (w / 2, h))]
    else:
        polys = {"left": [(0, 0), (w / 2, 0), (w / 2, h), (0, h)], "right": [(w / 2, 0), (w, 0), (w, h), (w / 2, h)]}
        polys["top"] = polys["right"]
        seams = [((w / 2, 0), (w / 2, h))]
    return polys, seams


def main():
    app = QtGui.QGuiApplication(sys.argv[:1])  # noqa: F841 (needed for QPainter)
    regions = []
    for folder, label, where, centre in REGIONS:
        path = os.path.join(ROOT, folder, "Renders", VIEW)
        if os.path.exists(path):
            regions.append((folder, label, where, centre, QtGui.QImage(path).convertToFormat(QtGui.QImage.Format_RGB32)))
    if len(regions) < 2:
        print(f"Only {len(regions)} variant render(s) found; nothing to composite.")
        return
    origins = [content_origin(r[4]) for r in regions]
    # Shift every image so its content's top-left lands where the first image's does.
    shifts = [origins[0] - o for o in origins]
    w = max(r[4].width() + s.x() for r, s in zip(regions, shifts))
    h = max(r[4].height() + s.y() for r, s in zip(regions, shifts))

    out = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
    out.fill(QtCore.Qt.white)
    p = QtGui.QPainter(out)
    p.setRenderHint(QtGui.QPainter.Antialiasing)
    p.setRenderHint(QtGui.QPainter.TextAntialiasing)
    polys, seams = region_polygons(w, h, [r[2] for r in regions])
    if len(regions) == 2:  # two variants: first on the left, second on the right
        regions = [regions[0][:2] + ("left",) + regions[0][3:], regions[1][:2] + ("right",) + regions[1][3:]]

    for r, s in zip(regions, shifts):
        path = QtGui.QPainterPath()
        path.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x, y) for x, y in polys[r[2]]]))
        path.closeSubpath()
        p.save()
        p.setClipPath(path)
        p.drawImage(s, r[4])
        p.restore()
    p.setPen(QtGui.QPen(SEAM, 3))
    for (x1, y1), (x2, y2) in seams:
        p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))

    font = QtGui.QFont("Segoe UI")
    font.setPixelSize(max(18, int(h * 0.038)))
    font.setBold(True)
    p.setFont(font)
    fm = QtGui.QFontMetrics(font)
    pad_x, pad_y = int(font.pixelSize() * 0.55), int(font.pixelSize() * 0.3)
    for folder, label, where, (fx, fy), _ in regions:
        tw, th = fm.horizontalAdvance(label) + 2 * pad_x, fm.height() + 2 * pad_y
        box = QtCore.QRectF(fx * w - tw / 2, fy * h - th / 2, tw, th)
        p.setPen(QtGui.QPen(LABEL_EDGE, 2))
        p.setBrush(LABEL_BG)
        p.drawRoundedRect(box, th * 0.25, th * 0.25)
        p.setPen(TEXT)
        p.drawText(box, QtCore.Qt.AlignCenter, label)
    p.end()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT) and QtGui.QImage(OUT).convertToFormat(QtGui.QImage.Format_RGB32) == out:
        print(f"SAME {os.path.relpath(OUT, ROOT)}")
        return
    out.save(OUT)
    print(f"OK   {os.path.relpath(OUT, ROOT)}  {w}x{h}  ({', '.join(r[0] for r in regions)})")


if __name__ == "__main__":
    main()
