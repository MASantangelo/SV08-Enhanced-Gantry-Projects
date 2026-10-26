# FAQ

> [!NOTE]
> The layout of these guides and the FAQ is modeled after the documentation of the [Monolith Gantry](https://github.com/Monolith3D/Monolith_Gantry) by Monolith3D. The text and pictures here are our own, written for the SV08 Enhanced Gantry.

## Choosing a version

### Which version should I build?
All three share the same layout, hardware, bearings and belts, so the choice comes down to how you'll make the plates:

- **Printed (6 mm):** the easiest if you have a printer and no mill. Uses M3 heat-set inserts. The v2 parts print with no supports.
- **Carbon fiber (6 mm):** the design basis. The plates need a mill, because the bearing steps, counterbores and nut pockets are partial-depth features. Uses standard M3 nuts in hex pockets.
- **Metal (5 mm 6061):** machined and tapped, so there are no inserts or nuts. Thinner plates mean a few shims and one sanded screw head (see the [Metal README](Metal%20Version/README.md)).

You can start printed and move to CF or metal later without changing any other hardware.

### Can I mix versions?
Not within a corner: each sub-assembly's plates are sized for its own thickness and threaded points. Mixing whole sub-assemblies, for example printed XY joints with CF motor corners, hasn't been tested.

## Parts and sourcing

### What can I reuse from my stock SV08?
- **Linear rails and carriages:** the Y and X rails and their carriages carry over.
- **Extrusions:** the gantry Y extrusions, the gantry X extrusion and the toolhead extrusion all fit. The motor mounts and XY joints line up with the stock extrusions' existing M4 holes. The gantry X is shortened to 342 mm; to keep the stock 345 mm one, use a 6 mm OD spacer in the spot nearest each end (one per back corner), or trim 1.5 mm off each end.
- **Not the motors, unless they have a long enough shaft:** the double-shear corners need a 5 mm motor shaft about 37 mm long, so the shaft reaches the outer bearing.

### What are live idlers, and why Chicago bolts?
A live idler turns with its pulley: the pulley is fixed to a shaft, and the shaft spins in a bearing in each plate. That supports the pulley on both sides (dual shear), so it can take more belt tension without flexing.

The shafts are 304 stainless Chicago bolts: a 5 mm barrel with an M4 thread inside, closed by an M4×8 ultra-thin flat head. The barrel runs the full width of both bearings and the two heads clamp them, so the idler can't float up and down under belt tension. The BOM lists two alternatives: an M3 internally threaded spacer, sanded to fit, or a 5 mm slip-fit dowel. The dowel lets the idler float, which shows up as vibration.

### Why don't I use the screws that come with the Chicago bolts?
Their 2 mm tall heads don't fit under the front motors. The M4×8 ultra-thin flat heads (1.2 mm) do. On the metal version, sand the two front heads down to about 1.0 mm.

### Why nuts instead of PEM standoffs on the CF version?
Standard M3 nuts are cheap, available everywhere, need no epoxy and are easy to replace, while PEM standoffs are a specialist part. The nut pockets are also shallower than the PEM seats, which leaves more carbon around them.

### The threaded spacers don't fit my bearings. What now?
That only matters if you use the threaded spacer alternative instead of the Chicago bolts. The linked spacers are anodised and measure about 5.05 mm, too big for a 695 bearing (4.992–5.000 mm). Sand the whole length of each spacer in a drill with 400–600 grit until it presses into a bearing with firm thumb pressure and the pulley slides over it.

## Printing

### What print settings should I use?
The v2 test build used 0.2 mm layers, 0.4 mm line width, Arachne walls in inner/outer/inner order, 4 wall loops and 40% cubic infill, with no supports. The plates are modelled in their print orientation, so print them as the files are laid out.

### My holes print undersize or oversize
The printed plates have their holes enlarged by about 0.3 mm already. The D5 shoulder-bolt holes are modelled at 5.1 mm on purpose: run a 5 mm drill through each by hand for a snug fit.

### Any tips for the heat-set inserts?
Press the bearings in first, start each insert straight by pulling it in with an M3 screw, and set them flush or slightly deep. Then chase each one from the side the real screw doesn't come in from. The full method is in [Installing the heat-set inserts](Printed%20Version/README.md#installing-the-heat-set-inserts).

## Machining (CF and metal)

### My bearing seats or holes come out tight
The drawings are nominal size. Cutter wear and deflection make holes come out slightly undersize, and a contoured 13 mm bearing bore usually loses more than a small helically bored hole. Cut test holes and adjust with stock-to-leave in your CAM. Check the bearing seats and shoulder-bolt holes with the real bearing and bolt, not calipers alone.

### Do the left plates need special handling?
CF left plates are drawn as their right-hand plate turned over, so their pockets are on the opposite face of the file. Machine each plate pocket-side up as drawn. Metal left plates are plain mirror images.

## Assembly

### How tight should the belts be?
Aim for 6–8 lb (26.7–35.6 N) per belt span, with both belts the same. Measure by plucking a span and reading its frequency; the [tensioning section of the installation guide](Docs/Installation.md#tensioning-the-belts) has the target frequencies for each span length and the step-by-step. Don't go past the top of the range: over-tensioning broke a belt on the v2 test build.

### How far should the pulleys sit from the bearings?
About 0.5 mm. The pulley turns but the bearing's outer ring doesn't, so a pulley pushed against a bearing rubs. A folded piece of paper makes a good shim while you tighten the set screws.

### Do I need threadlocker?
Yes, on the ultra-thin flat heads that close the Chicago bolts, because those shafts spin. Use blue (medium strength); red needs heat to remove, which can damage the bearings and printed parts nearby.

### My motors don't clamp down at the front corners
The front shoulder bolts are also the motor screws. On the printed and CF versions about 4.5 mm of thread goes into the motor. If your motor's holes are only 4 mm deep, trim 0.5 mm off each bolt. The metal version uses washers or a trim; see its README.

## Other

### Will you sell parts?
Machined aluminium tensioner lever arms for all three versions will be available at some point.

### What's the license?
GPL-3.0, the same as the original [Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod) it's based on. See the [License section](README.md#license).
