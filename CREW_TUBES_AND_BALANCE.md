# v0.16.0-dev.2 — elbow artwork UV fix

User's in-game screenshot showed logos and nameplates repeated six times across the bend. The elbow panel helper subdivided geometry for curvature but restarted texture V=0..1 on every strip. It now maps each strip to its corresponding fraction of the complete panel. Both 250/375 elbows have single continuous nameplates, logos and cladding texture coverage. UVs alone change; exact geometry, normals, indices, materials, textures, colliders, stack nodes, gameplay and the straight tube models are preserved.

New exported-model regression checks sum UV area to require one artwork instance per physical plaque/logo and one texture per cladding tile, and check shared plaque UV edges. The old winding-only test detected mirroring but not repeated artwork; that coverage gap is corrected. The native MU, OBJ/MTL and procedural source agree. Live KSP oblique/close-up visual confirmation remains pending.

Balance and science storage from dev.1 are unchanged. The roadmap includes ground-base modules, adjustable legs and selectable ring colors on each module. Close KSP before replacing the TEST folder. No installation, save edits, GitHub action or release was performed.

## Prior development notes

# RoosterWorks v0.16.0-dev.1 — crew passages and requested balance

## Electrical storage

Cuts are applied once to the v0.15.0-dev.3 capacities, then changed base EC is rounded to the nearest ten (half up), retaining the user's rounding preference. HAB loses 30%; PWR battery-only loses 15%; PWR nuclear loses 20%. Reactor output, uranium use/storage, waste storage, dry hardware mass/cost, cooling, selection and the dev.3 resource-menu refresh behavior remain unchanged.

| Part / configuration | Previous base EC | New base EC |
|---|---:|---:|
| HAB-250 | 420 | 290 |
| HAB-375 | 787.5 | 550 |
| PWR-250 Battery only | 3500 | 2980 |
| PWR-375 Battery only | 6750 | 5740 |
| PWR-250 Integrated nuclear | 3060 | 2450 |
| PWR-375 Integrated nuclear | 5910 | 4730 |

These are base config values. Under the reference Kerbalism crewed-part x2.8 patch, HAB should show **812 / 1540 EC**. Crewless PWR retains the table values. Earlier one-of-eight-bay storage ratios are superseded by these independent balance cuts; the reactor still exchanges a battery bay. Other parts' battery capacities are unchanged. The hidden historical reactor IDs receive the same current nuclear limits through a late patch; saved vessel resource records are not directly migrated or edited.

## Science storage

CMD-250/CMD-375 and LAB-250/LAB-375 receive **2500 MB (2.5 GB)** maximum Kerbalism data storage. LAB-250/LAB-375 receive **100 sample slots** maximum. Both editor expansion factors are capped at 1, and effective configured capacities match the ceilings, preventing the normal drive multiplier from exceeding the requested limits. CMD sample storage is preserved. Research processing, experiments, acquisition rates and EC usage remain unchanged.

Kerbalism uses decimal MB/GB (1000 MB per GB), verified against its primary [Lib source](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Lib.cs). sampleCapacity is a slot count, not a universal count of differently sized experiments. Science limits are applied after the Default/global drive patches under Kerbalism FeatureScience. Stock-only research behavior remains unchanged. Test newly placed parts: serialized existing craft or stored vessel drive state can retain earlier settings until explicitly reconfigured in the editor.

## Four new passage parts

| Part | Diameter | Shape / length | Dry mass | Stack nodes |
|---|---:|---|---:|---|
| RW-TUB-250 | 2.5 m | Straight, 2.0 m | 0.55 t | +/-1.0 m Y, size 2 |
| RW-TUB-375 | 3.75 m | Straight, 3.0 m | 1.85625 t | +/-1.5 m Y, size 3 |
| RW-ELB-250 | 2.5 m | 90-degree bend; 1.8 m centreline radius + 0.3 m tangent collars | 0.85 t | (-0.9,-1.2,0) toward -Y; (1.2,0.9,0) toward +X, size 2 |
| RW-ELB-375 | 3.75 m | 90-degree bend; 2.7 m centreline radius + 0.45 m tangent collars | 2.86875 t | (-1.35,-1.8,0) toward -Y; (1.8,1.35,0) toward +X, size 3 |

All four are **crewless pressurized passages**, with no seats, IVA, EVA hatch, built-in battery, food/oxygen stores or phantom gameplay equipment. Connected-vessel crew transfer follows KSP's normal behavior; optional Connected Living Space support explicitly marks them passable. Conditional Kerbalism Habitat supplies the internal pressure volume. Structural category, advConstruction technology, fuel crossfeed and unchanged RoosterWorks diameter interfaces.

Straight bodies use 16 curved panel sectors and sealed shared interface caps. Elbows use a true quarter-circle skin with straight tangent collars, curved panel rows, reinforcing bands, continuous service rail sections and readable logos/role-specific IDs. White and grey shell finishes reuse the accepted finish module, existing metal trim and diffuse textures. No existing model or glass mesh is changed. Large passages are real 1.5x native exports with appropriately labelled 375 textures, not rescaleFactor-only parts.

Each straight tube has one closed convex 96-triangle collider; each elbow has 12 closed convex 96-triangle solids along the curve and tangent collars. Straight render geometry has 17460 triangles, elbow 40172. Geometry, normal winding, label UVs, collar/end planes, perpendicular interface directions, native scale and pressure/CLS guards are checked offline. Physics, assembly, crew/CLS transfer and pressure confirmation require actual KSP testing.

## Source, build and tests

Inspect this kit before future changes. Canonical Tools/build_appearance.py rebuilds the original family and new tubes. Tools/build_ec_balance.py rebuilds balance/options/new passages and manifests without regenerating old models. Source/build_crew_tubes.py emits native MU, OBJ/MTL, role/size textures and conditional pressure/CLS patches. Source/Blender/create_crew_tubes.py optionally reconstructs an exact shipped passage in Blender; Blender was not run for this build. Source/build_storage_balance.py emits the late science/current legacy-EC limits. Source/Balancing/power_capacity_policy.json freezes independent PWR cuts; electric_charge_policy.json carries HAB/base-PWR overrides.

The original hatch and accepted finish DLLs remain byte-identical. Power controller behavior remains byte-identical at source level except its GetInfo wording to reflect the new independent balance; the DLL is rebuilt against installed KSP APIs. Existing native models, glass, lights, textures, other resources, mass, costs, crew and compatibility gameplay are fingerprint-checked. Historical EC-only audits restore only capacities using immutable before snapshots; a dedicated v0.16 audit validates current cuts and new limits. The shared old test suite and new tube/balance validators form Tools/validate.py.

## In-game checklist

- Close KSP, replace GameData/RoosterWorksStationModules with this TEST folder and restart. No game files or saves have been edited by the build.
- Newly placed HAB: verify base/current Kerbalism EC values; keep existing hatch, crew, supplies and lighting behavior.
- On each PWR, keep the part menu open while switching Battery/Nuclear. Verify the new maxima, fuel-row removal, finite nuclear generation, save/reload and background behavior.
- CMD/LAB: confirm one active archive, 2.5 GB ceiling; LAB 100 sample slots ceiling. Check data collection, transfer, persistence, existing research processing and inability to select a larger drive.
- Assemble straight tube and elbow chains in both sizes; verify diameters, stack planes, 90-degree orientation, collar seals, collision and crossfeed.
- Switch every new passage between White/Grey and inspect logos, detailed panels, rails and ring seams. Test Kerbalism pressure and optional CLS crew routing through them.

ROADMAP.md records requested **Ground-base modules** and **Adjustable legs** as planned, with specifications to be decided. They are not implemented in this build. No release, GitHub change, installation or save edit was performed. Offline checks and ZIP integrity do not establish live KSP acceptance of the new passages or limits.
