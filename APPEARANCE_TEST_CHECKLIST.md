# v0.7.0-dev.4 appearance test — KSP 1.12.5

This is a six-module development candidate. Offline checks passed; actual
KSP shading, texture loading, seams, performance and gameplay need confirmation.

- [ ] Inspect HAB, LAB, CMD, HUB, CUP and LOG at near and normal VAB zoom, then in sunlight and shadow in flight.
- [ ] New cladding has crisp cover edges, fasteners, MMOD/service stencils and restrained grain; no texture smearing or shimmering.
- [ ] All HAB/LAB/CMD/CUP/LOG nameplates read ROOSTERWORKS left-to-right in VAB and flight. HUB IDs, endcap plaques, crests and service/hull stencils have correct orientation. Original rooster branding remains present on the whole family.
- [ ] Inspect every exposed endcap at shallow/grazing angles: no background slits between the bronze blanket, inner rim, stepped lip or central pressure closure. Check both ends of HAB/LAB/CMD/LOG, all six HUB faces and CUP bottom; inspect CUP upper skylight trim too.
- [ ] Common endcaps fit flush when stacked. New metal lip and circuit plates stay inside the old mating planes.
- [ ] LOG's white shoulder collars no longer show dark/white flicker; cargo ID plates and supply panels are clear of paired handrails.
- [ ] HUB has a rounded central body and smooth curved necks from all six sides; no gaps or shading creases at shared spherical seams.
- [ ] Stack parts on all six HUB ports and check symmetry, radial attachment fit and collision clearance in VAB/flight. HUB colliders were revised in dev.3 and are unchanged in dev.4.
- [ ] HUB shoulder looms look continuous and properly attached on all six sides, without crowded intersections.
- [ ] CUP's accepted mullion/header joins still have no daylight gaps; panes and overhead window have unchanged size and geometry.
- [ ] Toggle warm-white cabin lights on/off for HAB/LAB/CMD/CUP; the hull and diagnostic plates remain unlit.
- [ ] Both HAB variants look correct; perform EVA, grab/climb and boarding from Side Hatch. Standard Windows still disallows EVA.
- [ ] Test stock inventory and Kerbalism storage/pressure on LOG using TEST_CHECKLIST-v0.7.0.md.
- [ ] Verify CMD signal/control/SAS, LAB science and station crew transfers with the same mods used for the prior baseline.
- [ ] Compare load time/frame rate on a representative station. The detail pass increases visual geometry; the rounded HUB adds curved subdivisions. Other modules' colliders are preserved; HUB colliders follow the new shape.

Record screenshots and KSP.log for failures. Decorative panels, ports, conduits,
cassettes and endcap pressure closures do not add functional doors or equipment.
