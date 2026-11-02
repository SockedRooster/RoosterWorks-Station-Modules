# Roadmap 0.7 / 0.75 station expansion

0.7 adds native 5 m HAB, LAB, CMD, HUB, CUP, LOG, AIR, PWR, GRN, straight crew tube and 90-degree elbow, plus a correctly tapered 3.75-to-5 m adapter. Geometry, collision, triggers, lights and node positions use real metres; rescaleFactor stays 1. The full family retains the matching 2.5 m roles, seats, stock IVA, equipment and variant IDs. OBJ/MTL exports and the native serializer are included in Source/Blender and Source/native_derivatives.py.

The adapter has a 3.75 m upper interface, 5 m lower interface and 2.1 m length. Its taper uses an analytic transform with inverse-Jacobian normals; uniformly scaling the older adapter would have produced a wrong 3.33 m small end. Three closed convex collision sections and sealed endcap detail are retained.

## Electrical and gameplay balance

5 m base EC: HAB 370, CMD 630, CUP 525, PWR battery 10200, PWR nuclear 8410; other passive roles remain zero. HAB uses the installed SSPX 5 m habitation reference (500 EC), +5%, then the established -30% reduction, rounded to tens. Command uses the 600 EC 5 m core reference +5%; cupola uses the 500 EC 5 m cupola reference +5%. PWR uses an area proxy from accepted 3.75 m balances, rounded to tens. These are base values; Kerbalism Default applies its crewed-part multiplier. Larger geometry does not multiply command batteries by volume.

The 5 m PWR nuclear variant extends the prior 1.1 / 1.2 size sequence to 1.3: 6.5 EC/s, 1.95 units fuel and retained waste capacity, +0.0507 t dry hardware. Includes fixed cooling, starts off, does not refill in flight, and uses the existing tested controller. Battery/Nuclear and exterior/ring choices remain separate. Kerbalism Default/CRP is required for the current nuclear selector.

CMD/LAB data stays capped at 2500 MB (2.5 GB) and LAB at 100 sample slots. Habitat/supply volume scales by 8 and surface by 4 relative to 2.5 m. 5 m LOG has 36 stock item slots / 11200 L, independent of its fixed-volume 4160 L dedicated supply payload. Mixed supplies and all seven dedicated content choices are retained, with waste tanks initially empty and no flight inventory migration.

## Compact HABs — 0.75 package only

| Part | Diameter | Length | Crew | Base EC | Dry mass |
|---|---:|---:|---:|---:|---:|
| RW-HAB-S-250 | 2.5 m | 1.98 m | 2 | 150 | 1.75 t |
| RW-HAB-S-375 | 3.75 m | 2.97 m | 2 | 280 | 5.90625 t |
| RW-HAB-S-500 | 5 m | 3.96 m | 2 | 190 | 14 t |

Each compact HAB is a new one-course procedural model, with complete shared endcaps and a centered full-proportion hatch/window bank. No axial squashing of viewports, door hardware or badges. Two-seat stock mk1CabinInternal is temporary; it is not a custom IVA. Standard / Side Hatch groups, tagged exit/ladder triggers, a closed 96-triangle convex solid, centered handrails/footholds and warm-white cabin lamps are retained. Compact supply and internal volume are half the corresponding full HAB; half dry mass/cost and rounded half battery capacity. Surface uses the same endcaps and half the cylindrical wall. White/Grey finish and ring control apply in all three sizes.

## Ground-base plans — concept only

0.8: horizontal habitation/science/service modules on mounting cradles, and a vertical ground module with a real side entry, fold-out landing, hinged stair sections and folding handrails. The stairs should stow against the hull for transport and deploy to a clear walkable ground path. Exact hinge positions, stair dimensions, collider treatment and animation timing will be prototyped before a playable part is added.

0.9: adjustable telescopic legs with wide swivel footpads and brace supports; consider a wheel option for mobile bases. Independent travel/leveling, loads, terrain contact, deployment, retraction and save persistence need testing. Ground concepts shown in Media are design illustrations, not exported KSP models or functional animations. The 0.8/0.9 parts are not included in these TEST packages.

## Acceptance checklist

1. Close KSP and replace the RoosterWorksStationModules folder with the desired TEST package. 0.75 contains the complete 0.7 family plus compact HABs.
2. Attach every 5 m part through size-4 nodes. Test all six HUB faces, both elbow interfaces, tube loading and the adapter's size-3/4 ends. Check seams, orientation, clipping and collision. Size-4 is a fifth metre interface, not a second copy of the 3.75 m geometry.
3. Check labels, glass, lamp controls, White/Grey and every ring color. Repeat after copying parts, symmetry, switching HAB variants, and loading craft/flight saves.
4. On 5 m PWR, switch Battery/Nuclear while the part menu stays open. Check 10200/8410 EC, finite fuel, empty waste and output 6.5 EC/s; Battery must remove nuclear inventory. Validate Kerbalism loaded/background operation and no external radiator requirement.
5. Check 5 m LOG mixed/dedicated contents and the separate stock item inventory. Save partial fills and verify flight reload does not refill. Check command/lab 2.5 GB and lab 100 slots after ModuleManager processing.
6. On each compact HAB, verify two crew portraits, stock IVA, Standard exit gating, Side Hatch EVA, automatic ladder grab/climb/boarding, internal crew transfer and Kerbalism pressure. Inspect all cap/ring seams and window/hatch curvature closely. Existing full HABs and old vessels should remain unchanged.

Offline tests audit new native geometry, normals, UVs, material binding, closure, stack nodes, actual variant/trigger names, saved inventory logic and preservation of prior assets. Unity, ModuleManager, IVA placement, flight interaction and visuals remain pending in-game confirmation.
