# Build guides

> [!NOTE]
> The layout of these guides and the FAQ is modeled after the documentation of the [Monolith Gantry](https://github.com/Monolith3D/Monolith_Gantry) by Monolith3D. The text and pictures here are our own, written for the SV08 Enhanced Gantry.

Step-by-step guides for building the SV08 Enhanced Gantry, one sub-assembly at a time. They apply to all three versions (printed, carbon fiber and metal); where a version differs, the step says so.

## Start here

1. **Pick your version.** The [comparison on the main page](../README.md#pick-your-version) and the [FAQ](../FAQ.md#which-version-should-i-build) cover the differences.
2. **Make the parts.** Print them, cut them from carbon fiber, or machine them. Each version's README covers its fits and tolerances.
3. **Buy the hardware.** Each version has its own BOM with purchase links: [Printed](../Printed%20Version/BOM.md) · [Carbon fiber](../CF%20Version/BOM.md) · [Metal](../Metal%20Version/BOM.md).
4. **Build the sub-assemblies** with the guides below.
5. **Fit them to the printer, then tension and tune.**

## Guides

| Guide | Status |
|---|---|
| [Installing the gantry](Installation.md): bench prep, the frame and all four motor corners | Ready |
| XY joints | Draft: [bench assembly](XY%20Joint.md), to be reworked into the installation order |
| Tensioning the belts | Coming |

## How the pictures are made

Every step image is rendered from the project's STEP files, so the pictures match the current CAD. The steps for each guide are listed in [`Docs/steps`](steps), and `tools/build-steps.ps1` regenerates the images (see [tools/README.md](../tools/README.md)).
