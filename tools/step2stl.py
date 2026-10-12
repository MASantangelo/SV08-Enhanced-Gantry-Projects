"""Convert every STEP file in a folder to STL in <folder>/For Viewing.

Run with FreeCAD's freecadcmd (see update-previews.ps1). freecadcmd doesn't
pass argv to scripts reliably, so the folder comes from the STEP2STL_DIR env
var. Optional STEP2STL_ONLY limits to one file name.

Single parts (one solid) are meshed uniformly fine. Assemblies use size-aware
settings instead: uniform fine settings blow full assemblies up to 500+ MB
because the McMaster-style hardware is all B-spline surfaces, so small
hardware is meshed coarse and big parts fine. That keeps the 1092-solid P6
assembly at ~38 MB for GitHub's viewer.
"""
import glob
import os

import Import  # noqa: F401  (registers STEP importer)
import Mesh
import MeshPart
import Part

SRC = os.environ["STEP2STL_DIR"]
ONLY = os.environ.get("STEP2STL_ONLY")
OUT = os.path.join(SRC, "For Viewing")
os.makedirs(OUT, exist_ok=True)

PART_SETTINGS = (0.02, 0.0872665)  # linear mm, angular rad (5 deg)
ASSEMBLY_SETTINGS = [  # (max bbox dim mm, linear mm, angular rad)
    (25, 0.3, 0.8),
    (80, 0.1, 0.35),
    (1e9, 0.05, 0.17),
]


def mesh(shape, lin, ang):
    return MeshPart.meshFromShape(Shape=shape, LinearDeflection=lin, AngularDeflection=ang, Relative=False)


files = sorted(glob.glob(os.path.join(SRC, "*.step")) + glob.glob(os.path.join(SRC, "*.stp")))
if ONLY:
    files = [f for f in files if os.path.basename(f) == ONLY]
fails = 0
for path in files:
    name = os.path.splitext(os.path.basename(path))[0]
    dst = os.path.join(OUT, name + ".stl")
    try:
        shape = Part.Shape()
        shape.read(path)
        if len(shape.Solids) <= 1:
            out = Mesh.Mesh(mesh(shape, *PART_SETTINGS))
        else:
            out = Mesh.Mesh()
            for s in shape.Solids:
                size = max(s.BoundBox.XLength, s.BoundBox.YLength, s.BoundBox.ZLength)
                _, lin, ang = next(t for t in ASSEMBLY_SETTINGS if size < t[0])
                out.addMesh(Mesh.Mesh(mesh(s, lin, ang)))
        out.write(dst)
        print(f"OK   {name}.stl  solids={len(shape.Solids)}  facets={out.CountFacets}  {os.path.getsize(dst)/1e6:.1f}MB")
    except Exception as e:  # keep going on bad files
        fails += 1
        print(f"FAIL {name}: {e}")
print(f"DONE {len(files) - fails}/{len(files)}")
