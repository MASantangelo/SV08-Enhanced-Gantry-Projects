# SV08 Metal Gantry (5 mm)

**Work in progress.** The plates are designed and checked; the assemblies, bill of materials and renders are still to come.

The metal variant: every gantry plate is machined from 5 mm 6061 aluminium, with tapped M3 holes in place of the heat-set inserts (printed) and PEM standoffs (CF).

## Plates (available now)

[`Base Components`](Base%20Components) has all 13 parts as STEP files, with 3D previews in [`Base Components/For Viewing`](Base%20Components/For%20Viewing):

- 4 front corner plates, 4 back corner plates and 4 XY live idler plates, in mirrored left/right pairs
- the 5 mm XY live idler spacer

The spacers and tensioner lever arms that every version shares are in [`Shared Components`](../Shared%20Components).

### Hole guide for machining

| Hole | Size | Notes |
|---|---|---|
| **M3 tapped** | Ø2.5 tap drill | Tap M3×0.5. Some are tapped from the bottom of a shallow pocket. |
| **M2 tapped** | Ø1.6 tap drill | On the back top plates (endstop mount). Use cutting fluid and back the tap out often; M2 taps break easily. |
| **M3 / M4 / M5 clearance** | Ø3.2 / Ø4.3 / Ø5.3 | Close fit |
| **Shoulder-bolt holes** | Ø5.00 | Locating fit for the D5 shoulder bolts. For the best fit, drill Ø4.8 and ream to Ø5 H7. |
| **Bearing seats** | Ø13.00 bore, Ø16.20 × 1.6 mm step | Locating fit for F695 flanged bearings |
| **Motor boss** | Ø22.00 | Locates the NEMA 17 boss on the front top plates |
| **Tensioner slot** | 5.3 mm wide | Clearance, so the tensioner shaft can slide |

The pockets and steps (bearing seats, countersunk screw seats, the pulley-clearance relief on the back top plates) need a mill; a waterjet or laser can't cut partial-depth features.

Every plate passes [`tools/plate-check.ps1`](../tools), which checks thickness, hole sizes, minimum wall thickness (1.5 mm) and left/right mirror symmetry.
