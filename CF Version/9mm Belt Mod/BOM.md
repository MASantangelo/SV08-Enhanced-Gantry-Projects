# SV08-CF6 Carbon Fiber Gantry for 9mm Belts: Bill of Materials

Generated from [`SV08_CF6_9mm_BOM_from_STEP.xlsx`](SV08_CF6_9mm_BOM_from_STEP.xlsx). If the two disagree, the spreadsheet is correct.

Links are plain product pages with no affiliate or tracking codes. Where a listing has multiple options, the **Notes** column says which one to pick.

## Contents

- [Fasteners - Screws](#fasteners---screws)
- [Fasteners - Shoulder Bolts](#fasteners---shoulder-bolts)
- [Fasteners - T-Nuts](#fasteners---t-nuts)
- [Live Idler Shafts](#live-idler-shafts)
- [Fasteners - Nuts](#fasteners---nuts)
- [Washers & Shims](#washers--shims)
- [Bearings](#bearings)
- [Pulleys](#pulleys)
- [Belts](#belts)
- [Spacers (Aluminum)](#spacers-aluminum)
- [Xol Toolhead Hardware](#xol-toolhead-hardware)
- [Electronics / Endstops](#electronics--endstops)
- [Linear Rails & Sliders](#linear-rails--sliders)
- [Linear Rail Mounting Hardware](#linear-rail-mounting-hardware)
- [Motors](#motors)
- [Extrusions](#extrusions)
- [CF Plates](#cf-plates)
- [Printed Parts](#printed-parts)

## Fasteners - Screws

*The M3 screws and M3 T-nuts that mount the linear rails are listed separately under [Linear Rail Mounting Hardware](#linear-rail-mounting-hardware).*

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 28 | M4 x 16mm BHCS | [Amazon](https://amazon.com/dp/B0GJJH316Y) | T-nut bolts into the extrusions, now through the 5mm riser spacers (M4 x 10mm in the standard CF build). The tip stops 0.9mm short of the far face of the T-nut. |
| 24 | M3 x 6mm FHCS | [Amazon](https://amazon.com/dp/B01E5EOIWW) |  |
| 12 | M3 x 10mm BHCS | [Amazon](https://amazon.com/dp/B0GJK7Z9DH) |  |
| 8 | M3 x 45mm SHCS | [Amazon](https://amazon.com/dp/B0FS1PNZRY) | Back motor screws, 10mm longer than the standard CF build (M3 x 35mm) for the 30mm gap. |
| 8 | M4 x 55mm BHCS | [Amazon](https://amazon.com/dp/B0CNK8QPNX) | Z carriage bolts, 10mm longer than the standard CF build (M4 x 45mm). |
| 4 | M4x8 Ultra Thin Flat Head | [Amazon](https://amazon.com/dp/B0H61X7SWB) | Screw end of each Chicago bolt live idler shaft (1 per front motor assembly and 1 per XY joint). 1.2mm head, thin enough to clear the front motors. Use threadlocker: blue (medium, removable) recommended; red (high strength) only for a permanent build, since removing it takes heat that can damage the bearings. |
| 4 | M2 x 2mm Set Screw | [Amazon](https://amazon.com/dp/B0DDJBSF6B) | Should come with the GT2 20-Tooth Pulley - Live Idler Version (9mm Belt) (2 per pulley, 4 total). |
| 4 | M2 x 8mm SHCS | [Amazon](https://amazon.com/dp/B0D4JMPT86) |  |
| 4 | M4 x 20mm BHCS | [Amazon](https://amazon.com/dp/B0DYSQZHC9) |  |
| 4 | M5 x 60mm SHCS | [Amazon](https://amazon.com/dp/B0GHNHFYJN) | Tensioner lever bolts (front motor assemblies), each with an M5 Nut and 2 M5 Washers. Replaces the M5 x 45mm BHCS of the standard CF build. |

## Fasteners - Shoulder Bolts

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 12 | D5 M3 x 40mm Shoulder Bolt | [AliExpress](https://www.aliexpress.us/item/3256810189139611.html) | Make sure you select Size D5-M3, Length 40mm. Front motor screws and XY joint bolts (replaces the 30mm and 25mm ones of the standard CF build). |
| 4 | D5 M3 x 35mm Shoulder Bolt | [AliExpress](https://www.aliexpress.us/item/3256810189139611.html) | Make sure you select Size D5-M3, Length 35mm |

## Fasteners - T-Nuts

*The M3 screws and M3 T-nuts that mount the linear rails are listed separately under [Linear Rail Mounting Hardware](#linear-rail-mounting-hardware).*

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 32 | M4 T-Nut | [Amazon](https://amazon.com/dp/B0C9DJBG1H) |  |

## Live Idler Shafts

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 2 | M5x40 Chicago Bolt Base | [Amazon](https://amazon.com/dp/B0FLJNY14R) | Live idler shaft in the front motor assemblies (1 per side). 304 stainless Chicago screw: the 5mm x 40mm barrel runs the full width of both bearings, head at the bottom and an M4x8 Ultra Thin Flat Head at the top, 0.4mm under the motor. Pack of 20; the M4x4 screws in the pack aren't used (their 2mm heads don't clear the motor). ALTERNATIVES (not as good): an M3 internally threaded spacer, 5mm OD x 35mm (amazon.com/dp/B0D3HWQ2GF), clamped by 2x M3 x 10mm ultra-thin flat heads (amazon.com/dp/B0H61WCTBX). The anodised spacers measure about 5.05mm, so sand the whole length in a drill (400-600 grit) until it presses into a bearing with firm thumb pressure and the pulley slides over it. Or a 5mm h6/h7 slip-fit dowel / ground shaft, 40mm long: it fits, but it's held only by the pulley set screws, so the idler can float up and down under belt tension, which causes vibration. |
| 2 | M5x45 Chicago Bolt Base | [AliExpress](https://www.aliexpress.us/item/3256809059470359.html) | Make sure you select x45mm (L). Live idler shaft in the XY joints (1 per joint). 304 stainless Chicago screw: the 5mm x 45mm barrel runs the full width of both bearings, its head on one bearing and an M4x8 Ultra Thin Flat Head on the other, so the bearings are clamped and the idler can't float. ALTERNATIVES (not as good): an M3 internally threaded spacer, 5mm OD x 40mm, clamped by 2x M3 x 10mm ultra-thin flat heads (amazon.com/dp/B0H61WCTBX). The anodised spacers measure about 5.05mm, so sand the whole length in a drill (400-600 grit) until it presses into a bearing with firm thumb pressure and the pulley slides over it. Or a 5mm h6/h7 slip-fit dowel / ground shaft, 45mm long: it fits, but it's held only by the pulley set screws, so the idler can float up and down under belt tension, which causes vibration. |

## Fasteners - Nuts

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 4 | M2 Nut | [Amazon](https://amazon.com/dp/B0FGTMN5JM) |  |
| 4 | M5 Nut | [Amazon](https://amazon.com/dp/B0D1X2YBLJ) | Tensioner lever bolts (M5 x 60mm SHCS). |
| 36 | M3 Nut | [Amazon](https://amazon.com/dp/B0F9FC4563) | Standard M3 hex nuts (ISO 4032: 5.5mm across flats, up to 2.4mm thick) in hex pockets in the CF plates, in place of the PEM standoffs: bearing retainers, shoulder bolts and lever-arm screws. The pockets are 5.9mm across flats, so a dab of glue holds a nut in place while you assemble. |

## Washers & Shims

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 8 | M5 Washer (5mm ID \| 10mm OD \| 1mm Tall) | [Amazon](https://amazon.com/dp/B07WZ5WQCG) | Tensioner lever bolts only (2 per bolt). The bearing stacks use the 7mm OD M5 shims below instead. |
| 3 | M5 Shim 7mm OD 0.2mm Thick | [AliExpress](https://www.aliexpress.us/item/3256809856464997.html) | Make sure you select M5x7 and 0.2mm thick. Also sold as a set (0.1-0.5mm): amazon.com/dp/B0F2J8P3KL. 5mm ID x 7mm OD shims touch only the bearing inner race, so they set the idler height without rubbing the outer race. Fine-tunes the XY joint stacks. |
| 3 | M5 Shim 7mm OD 0.3mm Thick | [AliExpress](https://www.aliexpress.us/item/3256809856464997.html) | Make sure you select M5x7 and 0.3mm thick. Also sold as a set (0.1-0.5mm): amazon.com/dp/B0F2J8P3KL. 5mm ID x 7mm OD shims touch only the bearing inner race, so they set the idler height without rubbing the outer race. Fine-tunes the XY joint stacks. |
| 25 | M5 Shim 7mm OD 0.5mm Thick | [AliExpress](https://www.aliexpress.us/item/3256809856464997.html) | Make sure you select M5x7 and 0.5mm thick. Also sold as a set (0.1-0.5mm): amazon.com/dp/B0F2J8P3KL. 5mm ID x 7mm OD shims touch only the bearing inner race, so they set the idler height without rubbing the outer race. Above and below every corner idler stack, and in the right XY joint. |
| 4 | M5 Shim 7mm OD 1.0mm Thick | [AliExpress](https://www.aliexpress.us/item/3256809856464997.html) | Make sure you select M5x7 and 1.0mm thick. Also sold as a set (0.1-0.5mm): amazon.com/dp/B0F2J8P3KL. 5mm ID x 7mm OD shims touch only the bearing inner race, so they set the idler height without rubbing the outer race. Between the two idler stacks on each back shoulder bolt. |
| 38 | M4 Washer (4mm ID \| 9mm OD \| 1mm Tall) | [Amazon](https://amazon.com/dp/B0DK6KXB6W) | .8mm more common and acceptable swap, OD matters |
| 8 | M3 Washer (3mm ID \| 7mm OD \| .5-.6mm Tall) | [Amazon](https://amazon.com/dp/B0C3TJ7PWT) |  |
| 8 | M3 Shim (3mm ID \| 5mm OD \| .2mm Tall) | [Amazon](https://amazon.com/dp/B08ZYP1TK4) |  |

## Bearings

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 48 | 695-2RS Flanged Bearing | [Amazon](https://amazon.com/dp/B0CGXF48ZZ) | Includes the 12 loose bearings named F695-2RS Bearing Single in CAD (36 in the idler stacks + 12 loose). |
| 18 | 695-2RS Bearing (Non-Flanged) | [Amazon](https://amazon.com/dp/B0CRVKG96C) | The middle bearing of each 9mm idler: F695 + 695 + F695 = 12mm tall, 10mm between the flanges. |
| 4 | MR63ZZ Bearing 3x6x2.5mm | [Amazon](https://amazon.com/dp/B0DY11G865) |  |

## Pulleys

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 6 | GT2 20-Tooth Pulley Set-Screw Version (9mm Belt) | [Amazon](https://amazon.com/dp/B07BT6N12L) | Make sure you select the 20-tooth, 5mm bore version. One on each motor (4) and one on each front live idler shaft (2). |
| 2 | GT2 20-Tooth Pulley - Live Idler Version (9mm Belt) | [AliExpress](https://www.aliexpress.us/item/3256803833151466.html) | Make sure you select Bore 5mm Width 10mm. One per XY joint, on the Chicago bolt shaft. Uses 2x M2 x 2mm Set Screws each (4 total). |

## Belts

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 1 | Bottom Belt 2.1m (9mm) | [AliExpress](https://www.aliexpress.us/item/3256806321466333.html) | 9mm wide GT2 belt. Select a length that covers both belts (2.1m each). |
| 1 | Top Belt 2.1m (9mm) | [AliExpress](https://www.aliexpress.us/item/3256806321466333.html) | 9mm wide GT2 belt. Select a length that covers both belts (2.1m each). |

## Spacers (Aluminum)

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 17 | M5 Spacer 8mm OD 2mm Tall | [AliExpress](https://www.aliexpress.us/item/2251832865702678.html) | Make sure you select M5, OD 8mm, 10pcs, length 2mm. Between the idler stacks and the plates. Purchase preferred. Printed as alternative with same dimensions. |
| 1 | M5 Spacer 8mm OD 7mm Tall | [Amazon](https://amazon.com/dp/B0DJPQ4RYH) | Right XY joint stack. Purchase preferred. Printed as alternative with same dimensions. |
| 9 | M5 Spacer 8mm OD 15mm Tall | [AliExpress](https://www.aliexpress.us/item/3256806296320708.html) | Make sure you select M5, 10pc, length 15mm. Front idler stacks and the right XY joint. Purchase preferred. Printed as alternative with same dimensions. |
| 1 | M5 Spacer 8mm OD 20mm Tall | [Amazon](https://amazon.com/dp/B0CRL77N5C) | Left XY joint stack. Purchase preferred. Printed as alternative with same dimensions. |
| 2 | M5 Spacer 8mm OD 30mm Tall | [Amazon](https://amazon.com/dp/B0CQ53LS2B) | Front corner post without an idler (1 per side). Purchase preferred. Printed as alternative with same dimensions. |
| 2 | M5 Spacer 8mm OD 40mm Tall | [AliExpress](https://www.aliexpress.us/item/3256806296320708.html) | Make sure you select M5, 10pc, length 40mm (also on aliexpress.us/item/2251832865702678.html). Between the tensioner lever arms (1 per front motor assembly). Purchase preferred. Printed as alternative with same dimensions. |
| 8 | M3 Spacer 6mm OD 30mm Tall | [Amazon](https://amazon.com/dp/B0CQF71CJY) | Back motor standoffs. Purchase preferred. Printed as alternative with same dimensions. 6mm OD, so the stock 345mm X extrusion fits without cutting. |

## Xol Toolhead Hardware

*Optional: only needed if you're building the Xol carriage.*

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 4 | M3 x 6mm BHCS |  | Not required unless building the Xol carriage. |
| 2 | M2 x 12mm BHCS |  | Not required unless building the Xol carriage. |
| 2 | M3 x 30mm Dowel Pin |  | Only dowel used by the Xol Toolhead. Not required unless building the Xol carriage. |
| 2 | Xol 9mm Clamp |  | 9mm belt version of the Xol clamp. Not required unless building the Xol carriage. |
| 1 | D2F-L Micro Switch (Endstop) |  | Not required unless building the Xol carriage. |
| 1 | Xol-Carriage_MGN12H_MGN9H_archetype_clips |  | Not required unless building the Xol carriage. |

## Electronics / Endstops

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 2 | D2F-L Micro Switch (Endstop) | [Amazon](https://amazon.com/dp/B0DBV8XGG4) | Base machine endstops (one in each back assembly). |

## Linear Rails & Sliders

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 2 | MGN9H Linear Rail Slide |  | Re-usable from Stock |
| 2 | Y MGN9H Rail 402mm |  | Re-usable from Stock |
| 1 | MGN12H Linear Rail Slide |  | Re-usable from Stock |
| 1 | X MGN12H Rail 406mm |  | Re-usable from Stock |

## Linear Rail Mounting Hardware

*The screws and T-nuts that hold the linear rails to the 2020 extrusions: 10 per Y rail and 8 on the X rail.*

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 28 | M3 x 8mm SHCS | [Amazon](https://amazon.com/dp/B0F5Q6YYWM) | Rail mounting screws: 10 per Y rail (20) and 8 on the X rail, one per M3 T-Nut. |
| 28 | M3 T-Nut | [Amazon](https://amazon.com/dp/B0G2M7W3PL) | Rail mounting T-nuts: 10 per Y rail (20) and 8 on the X rail. |

## Motors

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 4 | 42-48 Motor 5mmx42-47mm Shaft |  | The shaft needs to stick out at least 42mm from the motor face to pass through the bearing in the bottom plate (the standard CF build uses 30-37mm). |

## Extrusions

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 2 | Gantry Y-Axis 2020 Extrusion 469mm |  | Stock extrusion works: the front and back motor-mount bolt holes line up with its existing holes. |
| 1 | Gantry X-Axis 2020 Extrusion 342mm |  | Shortened from 345mm: all tensioning now happens at the front motor mounts. The back motor-mount bolt holes line up with the stock extrusion's existing holes. The stock 345mm extrusion also fits without cutting, because the back motor standoffs are 6mm OD. If you cut a 345mm extrusion down to 342mm, take 1.5mm off each end: the stock holes are 5mm and 23mm from each end, so an even trim keeps both ends lined up with the back motor-mount holes. |
| 1 | Toolhead X-Axis 2020 Extrusion 426mm |  | Stock extrusion works: the XY joint bolt holes line up with its existing holes (5mm and 25mm from each end). |

## CF Plates

Cutting files are in [`Base Components/9mm Belt Mod`](../Base%20Components/9mm%20Belt%20Mod) and [`Base Components`](../Base%20Components). Click a part name to preview it in 3D.

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 6 | [XY Live Idler Spacer 5mm CF6mm](../Base%20Components/For%20Viewing/XY%20Live%20Idler%20Spacer%205mm%20CF6mm.stl) |  | Cut from the same 6mm carbon fiber plate and machined down to 5mm (no separate 5mm sheet needed). 3 per XY joint: the 9mm version adds one above the X beam. |
| 1 | [Back Left Bottom Plate CF6mm](../Base%20Components/For%20Viewing/Back%20Left%20Bottom%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Back Left Top Plate CF6mm](../Base%20Components/For%20Viewing/Back%20Left%20Top%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Back Right Bottom Plate CF6mm](../Base%20Components/For%20Viewing/Back%20Right%20Bottom%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Back Right Top Plate CF6mm](../Base%20Components/For%20Viewing/Back%20Right%20Top%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Front Left Bottom CF6mm](../Base%20Components/For%20Viewing/Front%20Left%20Bottom%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Front Left Top CF6mm](../Base%20Components/For%20Viewing/Front%20Left%20Top%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Front Right Bottom CF6mm](../Base%20Components/For%20Viewing/Front%20Right%20Bottom%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [Front Right Top CF6mm](../Base%20Components/For%20Viewing/Front%20Right%20Top%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [XY Live Idler Left Bottom Plate CF6mm](../Base%20Components/For%20Viewing/XY%20Live%20Idler%20Left%20Bottom%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [XY Live Idler Left Top Plate CF6mm](../Base%20Components/For%20Viewing/XY%20Live%20Idler%20Left%20Top%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [XY Live Idler Right Bottom Plate CF6mm](../Base%20Components/For%20Viewing/XY%20Live%20Idler%20Right%20Bottom%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 1 | [XY Live Idler Right Top Plate CF6mm](../Base%20Components/For%20Viewing/XY%20Live%20Idler%20Right%20Top%20Plate%20CF6mm.stl) |  | Cut from 6mm carbon fiber |
| 4 | [Back Motor 5mm Spacer for X Gantry](../Base%20Components/9mm%20Belt%20Mod/For%20Viewing/Back%20Motor%205mm%20Spacer%20for%20X%20Gantry.stl) |  | 5mm riser between the plate and the extrusion. Cut it from 6mm carbon fiber and machine it down to 5mm (like the XY spacer), or print it. |
| 4 | [Back Motor 5mm Spacer for Y Gantry](../Base%20Components/9mm%20Belt%20Mod/For%20Viewing/Back%20Motor%205mm%20Spacer%20for%20Y%20Gantry.stl) |  | 5mm riser between the plate and the extrusion. Cut it from 6mm carbon fiber and machine it down to 5mm (like the XY spacer), or print it. |
| 4 | [Front Motor 5mm Spacer for Y Gantry](../Base%20Components/9mm%20Belt%20Mod/For%20Viewing/Front%20Motor%205mm%20Spacer%20for%20Y%20Gantry.stl) |  | 5mm riser between the plate and the extrusion. Cut it from 6mm carbon fiber and machine it down to 5mm (like the XY spacer), or print it. |

## Printed Parts

Print files are in [`Shared Components/Print Ready`](../../Shared%20Components/Print%20Ready) (parts common to every version). Click a part name to preview it in 3D.

| Qty | Part | Buy | Notes |
|---:|---|---|---|
| 4 | [Tensioner Lever Arm Revised](../../Shared%20Components/Print%20Ready/For%20Viewing/4x%20Tensioner%20Lever%20Arm%20Revised%20-%20For%20Printing.stl) |  | Print it (Shared Components/Print Ready, holes enlarged for printing) or cut it from CF or metal (Shared Components/For Cutting, nominal size). |
| 4 | [Z Carriage Spacer](../../Shared%20Components/Print%20Ready/For%20Viewing/4x%20Z%20Carriage%20Spacer%20-%20For%20Printing.stl) |  |  |
| 2 | [Back Spacer Plate 30mm](../../Shared%20Components/Print%20Ready/For%20Viewing/2x%20Back%20Spacer%20Plate%2030mm%20-%20For%20Printing.stl) |  |  |
| 2 | [Front Spacer Plate 30mm](../../Shared%20Components/Print%20Ready/For%20Viewing/2x%20Front%20Spacer%20Plate%2030mm%20-%20For%20Printing.stl) |  |  |
| 2 | [Printed Back Motor Spacer](../../Shared%20Components/Print%20Ready/For%20Viewing/2x%20Printed%20Back%20Motor%20Spacer%20-For%20Printing.stl) |  |  |
| 2 | [XY Live Idler Spacer 35mm](../../Shared%20Components/Print%20Ready/For%20Viewing/2x%20XY%20Live%20Idler%20Spacer%2035mm%20-%20For%20Printing.stl) |  |  |
