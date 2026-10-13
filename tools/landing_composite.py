"""Build the landing-page image: the same render of each variant, split on diagonals.

Usage (FreeCAD's python.exe):  python tools/landing_composite.py
Writes Renders/Landing - Front Right.png at the repo root.

Uses <variant>/Renders/Full Gantry - Front Right.png for each variant that has one, in the
order Printed, CF, Metal. With two variants the image is split on the diagonal from top right
to bottom left (first variant upper left, second lower right). With three, two parallel
diagonals give three bands. Renders are aligned on the top-left of their content, since each
was auto-cropped separately. Like render.py, it writes pixels only and skips unchanged output.
"""
import math
import os
import sys

from PySide2 import QtCore, QtGui

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIANTS = ["Printed Version", "CF Version", "Metal Version"]
VIEW = "Full Gantry - Front Right.png"
OUT = os.path.join(ROOT, "Renders", "Landing - Front Right.png")
SEAM = QtGui.QColor(200, 200, 200)


def content_origin(img, step=2, threshold=248):
    xs, ys = [], []
    for y in range(0, img.height(), step):
        for x in range(0, img.width(), step):
            if QtGui.qGray(img.pixel(x, y)) < threshold:
                xs.append(x)
                ys.append(y)
    return QtCore.QPoint(min(xs), min(ys))


def main():
    app = QtGui.QGuiApplication(sys.argv[:1])  # noqa: F841 (needed for QPainter)
    srcs = [(v, os.path.join(ROOT, v, "Renders", VIEW)) for v in VARIANTS]
    imgs = [(v, QtGui.QImage(p).convertToFormat(QtGui.QImage.Format_RGB32)) for v, p in srcs if os.path.exists(p)]
    if len(imgs) < 2:
        print(f"Only {len(imgs)} variant render(s) found; nothing to composite.")
        return
    origins = [content_origin(img) for _, img in imgs]
    # Shift every image so its content's top-left lands where the first image's does.
    shifts = [origins[0] - o for o in origins]
    w = max(img.width() + s.x() for (_, img), s in zip(imgs, shifts))
    h = max(img.height() + s.y() for (_, img), s in zip(imgs, shifts))

    out = QtGui.QImage(w, h, QtGui.QImage.Format_RGB32)
    out.fill(QtCore.Qt.white)
    p = QtGui.QPainter(out)
    p.setRenderHint(QtGui.QPainter.Antialiasing)
    n = len(imgs)
    # Diagonal bands parallel to the top-right -> bottom-left diagonal. Band boundary k is the
    # line x/w + y/h = 2k/n, so with two variants the single seam runs corner to corner.
    def seam_ends(t):
        """Where the line x/w + y/h = t meets the image edges."""
        if t <= 1:
            return (w * t, 0.0), (0.0, h * t)
        return (float(w), h * (t - 1)), (w * (t - 1), float(h))

    def band(k):
        a, b = 2.0 * k / n, 2.0 * (k + 1) / n  # region between x/w + y/h = a and = b
        pts = list(seam_ends(a)) + list(seam_ends(b))
        pts += [(x, y) for x, y in ((0, 0), (w, 0), (w, h), (0, h)) if a <= x / w + y / h <= b]
        cx = sum(x for x, _ in pts) / len(pts)
        cy = sum(y for _, y in pts) / len(pts)
        pts.sort(key=lambda q: math.atan2(q[1] - cy, q[0] - cx))  # convex region: sort around its centre
        path = QtGui.QPainterPath()
        path.addPolygon(QtGui.QPolygonF([QtCore.QPointF(x, y) for x, y in pts]))
        return path

    for k, ((_, img), s) in enumerate(zip(imgs, shifts)):
        p.save()
        p.setClipPath(band(k))
        p.drawImage(s, img)
        p.restore()
    p.setPen(QtGui.QPen(SEAM, 3))
    for k in range(1, n):
        (x1, y1), (x2, y2) = seam_ends(2.0 * k / n)
        p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))
    p.end()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT) and QtGui.QImage(OUT).convertToFormat(QtGui.QImage.Format_RGB32) == out:
        print(f"SAME {os.path.relpath(OUT, ROOT)}")
        return
    out.save(OUT)
    print(f"OK   {os.path.relpath(OUT, ROOT)}  {w}x{h}  ({', '.join(v for v, _ in imgs)})")


if __name__ == "__main__":
    main()
