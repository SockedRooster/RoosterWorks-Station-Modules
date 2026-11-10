# Roadmap 0.65 — ring colors and logistics contents

Development build: **v0.6.5-dev.1**. The roadmap's 0.65 milestone is represented as 0.6.5 in machine-readable version metadata. Local TEST and source packages; no release publication or game installation is implied.

## Ring color

All 23 current native models have an independent **Ring color** editor selector: Original, Steel, White, Charcoal, Blue, Green, Red and Gold. Both diameters, adapter, straight tubes and elbows are supported; hidden historical reactor IDs also use their existing PWR model maps. White/Grey exterior finish, HAB hatch/window variants and PWR Battery/Nuclear variants remain independent.

The option colors complete structural/interface rings and circular metal trim, retaining texture weathering. Small fasteners, rectangular cargo accents, badges, window frames, glass and warm-white lamps retain their established materials. Original restores each ring's original material and follows White/Grey shell changes where applicable. Color is saved with the part and applied on flight load; editor symmetry and copied parts are supported. Color has no mass, cost, resource or collider effect.

The 23 native .mu files are byte-identical to 0.6.0. Generated RingGeometry.cfg records exact triangle ranges from those files. The plugin clones only the visual mesh instance and partitions existing triangles into body and ring submeshes, without changing vertices, normals, UVs, winding or colliders. Runtime copies with an already partitioned visual mesh are supported. New color PNGs are generated from existing surface textures by build_ring_options.py; no new model or external plugin dependency is required.

## Logistics contents

With Kerbalism Default and Community Resource Pack, both LOG parts expose **Logistics contents** in the editor: Mixed supplies, Food, Water, Oxygen, Nitrogen, Ammonia, Waste and WasteWater. Mixed supplies retains the exact accepted six-resource capacities and initial fills. Dedicated options replace that mixed payload with one resource. LOG stays in **Station Utility**.

Dedicated tank volume is 520 L for LOG-250 and 1755 L for LOG-375 (3.375 times larger), conservatively below the original mixed payload's total effective storage volume. Oxygen, Nitrogen and Ammonia use the installed Kerbalism Default tank pressures of 200, 180 and 35 bar respectively. The volume remains fixed across choices; gas units represent compressed quantities rather than extra bay space.

| Dedicated contents | LOG-250 capacity | LOG-375 capacity | Initial fill |
|---|---:|---:|---|
| Food | 520 | 1755 | Full |
| Water | 520 | 1755 | Full |
| Oxygen | 104000 | 351000 | Full |
| Nitrogen | 93600 | 315900 | Full |
| Ammonia | 18200 | 61425 | Full |
| Waste | 520 | 1755 | Empty |
| WasteWater | 520 | 1755 | Empty |

The ordinary KSP cargo inventory is separate and unchanged: LOG-250 has 12 slots / 1400 L, LOG-375 has 24 slots / 4725 L. Dry mass, price, EC balance, pressure support and models remain unchanged. Standard resource densities still determine loaded resource mass.

Switching is editor-only. Reloading an editor part preserves existing partial fills; resources retained across a switch retain their fill fraction, while newly introduced supply tanks start full and waste tanks empty. Unselected managed resources are removed and open resource controls refreshed. Unrelated resources are untouched. A missing resource definition leaves the existing cargo intact. No resources are resized, added, removed or refilled in flight, including legacy vessels without a prior contents selection. Kerbalism retains ownership of consumption, background simulation and transfers. Unsupported profiles keep the prior behavior and do not receive an inert selector.

## Source and validation

The new RoosterWorksCustomization.dll contains RingColor.cs and LogisticsContents.cs, compiled against the actual KSP 1.12.5 assemblies. Accepted hatch, finish and reactor plugins are byte-preserved. Build scripts generate maps, textures and payload definitions after the existing options, with explicit exclusions from the 3.75 m derivation pass to avoid duplicate patches.

validate_roadmap065.py protects all 120 prior GameData files other than version metadata, audits every actual model/map/texture and LOG capacity, and executes the actual C# sources with state doubles. Cases include Original restoration, finish order, renamed Unity model roots, editor copies of partitioned meshes, saved flight colors, visual-instance cleanup, both LOG sizes, tank replacement, empty waste, partial fills, inventory/menu repair, missing resource definitions and no flight refill/migration. These checks establish source/binary/build behavior; they do not run Unity or ModuleManager.

## In-game acceptance checklist

1. Close KSP, back up saves, and replace GameData/RoosterWorksStationModules with the TEST folder. Use newly placed parts for the initial editor checks.
2. Select every ring color on a HAB and LOG in both sizes. Check Original restoration and White/Grey changes in both orders; inspect badges, glass and lamps. Repeat on HUB, CUP, GRN, adapter, straight tube and elbow.
3. Copy and symmetry-place colored parts, then change ring choices. Switch HAB hatch and PWR hardware variants; confirm ring color and independent controls still work.
4. On both LOG sizes, keep the part menu open while switching all eight loadouts. Only selected payload tanks should remain; capacities must match the table; Waste/WasteWater start empty. Mixed supplies restores the prior six tanks. Cargo inventory slots/volume remain unchanged.
5. Reduce a supply fill slider, save/reload the craft, and verify the amount. Launch each dedicated gas/liquid loadout, consume/transfer some contents, then save/reload flight; no refill or unexpected capacity change should occur. Check a copied legacy save separately: its existing inventory must remain intact.
6. Confirm normal Kerbalism life-support consumption and unloaded-vessel resource amounts. Actual VAB visuals, ModuleManager application, Unity mesh instances and flight/background behavior remain pending until tested in KSP.
