"""Build the landing-page image: the same render of each variant, split into labelled regions.

Usage (FreeCAD's python.exe):  python tools/landing_composite.py
Writes Renders/Landing - Front Right.png at the repo root.

Uses <variant>/Renders/Full Gantry - Front Right.png for each variant in REGIONS that has one.
With three variants the image is split in a "Y" from its centre: seams run to the top-left
corner, the top-right corner and the bottom middle, giving a left, a top and a right region.
With two, a single vertical seam splits it down the middle. Each region gets its variant's label.
Each render was auto-cropped (and scaled to a fixed width) separately, so parts that stick out
in one variant, like the CF version's top-mounted motors, shift and scale its frame. The renders
are registered to the first one on their dark pixels (mostly the black extrusions): a search over
scale, with FFT cross-correlation for the shift, so the gantries line up across the seams.
Like render.py, it writes pixels only and skips unchanged output.
"""
import os
import sys

import numpy as np
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


def dark_mask(img, step=1, threshold=60):
    """Float array, 1 where the pixel is dark (the extrusions), sampled every step pixels."""
    w, h = img.width(), img.height()
    a = np.frombuffer(img.constBits(), np.uint8, img.bytesPerLine() * h)
    a = a.reshape(h, img.bytesPerLine() // 4, 4)[:, :w, :3]
    return (a.mean(axis=2) < threshold).astype(float)[::step, ::step]


def resized(m, s):
    h, w = m.shape
    yi = np.minimum((np.arange(int(round(h * s))) / s).astype(int), h - 1)
    xi = np.minimum((np.arange(int(round(w * s))) / s).astype(int), w - 1)
    return m[yi][:, xi]


def best_shift(ref, mov):
    """(score, dx, dy): the shift of mov that best overlaps ref."""
    H, W = ref.shape[0] + mov.shape[0], ref.shape[1] + mov.shape[1]
    c = np.fft.irfft2(np.fft.rfft2(ref, (H, W)) * np.conj(np.fft.rfft2(mov, (H, W))), (H, W))
    dy, dx = np.unravel_index(np.argmax(c), c.shape)
    return c[dy, dx], (dx - W if dx > W // 2 else dx), (dy - H if dy > H // 2 else dy)


def register(ref_img, img):
    """(scale, dx, dy) that maps img onto ref_img: coarse search on a quarter-size mask, then refine."""
    ref4, mov4 = dark_mask(ref_img, 4), dark_mask(img, 4)
    _, _, _, s = max(best_shift(ref4, resized(mov4, s)) + (s,) for s in np.arange(0.90, 1.10, 0.005))
    ref1, mov1 = dark_mask(ref_img), dark_mask(img)
    _, dx, dy, s = max(best_shift(ref1, resized(mov1, t)) + (t,) for t in np.arange(s - 0.005, s + 0.0051, 0.001))
    return float(s), int(dx), int(dy)


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
    # Map every image onto the first one's frame; the output is the first image's size.
    transforms = [(1.0, 0, 0)] + [register(regions[0][4], r[4]) for r in regions[1:]]
    for r, (sc, dx, dy) in zip(regions[1:], transforms[1:]):
        print(f"     {r[0]}: scale {sc:.3f}, shift {dx:+d}, {dy:+d} px")
    w, h = regions[0][4].width(), regions[0][4].height()

    out = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
    out.fill(QtCore.Qt.white)
    p = QtGui.QPainter(out)
    p.setRenderHint(QtGui.QPainter.Antialiasing)
    p.setRenderHint(QtGui.QPainter.TextAntialiasing)
    polys, seams = region_polygons(w, h, [r[2] for r in regions])
    if len(regions) == 2:  # two variants: first on the left, second on the right
        regions = [regions[0][:2] + ("left",) + regions[0][3:], regions[1][:2] + ("right",) + regions[1][3:]]

    for r, (sc, dx, dy) in zip(regions, transforms):
        path = QtGui.QPainterPath()
        path.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x, y) for x, y in polys[r[2]]]))
        path.closeSubpath()
        p.save()
        p.setClipPath(path)
        p.translate(dx, dy)
        p.scale(sc, sc)
        p.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        p.drawImage(0, 0, r[4])
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
