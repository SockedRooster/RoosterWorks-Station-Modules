# v0.16.0-dev.3 — VAB categories and straight-tube loading fix

The user requested category placement and reported missing straight crew tubes. LOG placement was explicitly clarified as **Station Utility**, superseding the conflicting Supply Containers request for that same current part. Future selectable logistics contents are on the roadmap; resource switching is not implemented by this catalogue pass.

| Assets (both sizes where available) | VABOrganizer group |
|---|---|
| HAB | Habitation |
| CUP | Cupolas |
| CMD | Station Cores |
| TUB straight crew tubes / ELB 90-degree elbows | Station Connectors |
| HUB | Station Hubs |
| ADP 2.5-to-3.75 adapter | Station Adapters |
| AIR | Airlocks |
| LOG | Station Utility |
| GRN | Greenhouses |
| LAB | Labs |
| PWR (existing Battery/Nuclear variant choice) | Batteries |

`Compatibility/StationCatalogue.cfg` applies exact part-ID assignments in a final VABOrganizer pass, removing older duplicate organizer nodes. Group IDs match the installed VABOrganizer / SSPXr definitions: crewHabitation, cupolas, station, crewTubes, crewHubs, crewAdapters, airlocks, crewUtility, greenhouses, labs and batteries. Cupolas use the Pods editor tab and greenhouses Science, matching their installed category counterparts. Group fallbacks are included for the SSPXr-specific categories if VABOrganizer is installed without SSPXr. Flight roles, science/life support, stock module capabilities and all storage numbers are unchanged; editor placement does not add command capabilities to cupolas.

## Why straight tubes were missing

The installed KSP.log showed both straight-tube files present but failing in KSPCommunityFixes.Library.MuParser.ReadMaterials with an out-of-range index. PartCompiler consequently could not clone either model. This was a model-load failure rather than an absent config or research/category-only issue.

The shared passage palette included the unused elbow-label material last. Straight tube renderers referenced materials only through index 14, but their exported material table contained 16 entries. The KSPCF fast loader's renderer-binding range did not cover that trailing unused entry. The writer now trims unused trailing material/texture entries, so tube material count matches the highest referenced index + 1. Renderer indices, shaders and active textures remain unchanged. Elbows already referenced the last material and retain byte-identical models, including the corrected dev.2 UVs. Straight tube geometry, normals, UVs and collision are also identical; only the unused trailing material/texture records disappear.

## Source and evidence

Source/build_catalogue.py emits editor placement from a maintained mapping. Source/build_options.py includes it in the canonical and per-asset option builds. Source/build_family375.py excludes the all-size catalogue patch from large-family derivation. Source/build_crew_tubes.py prevents trailing unused materials in future exports.

Tools/validate_crew_tubes.py now checks the material-table/renderer-index contract as well as native geometry, UVs and collider checks. Tools/validate_catalogue.py verifies the 23 mappings, final/conditional patch nodes, fallbacks and exact prior GameData fingerprints, allowing only version and the precisely constrained tube material-table delta. Tools/tube_material_regression.py proves no tube geometry/UV/physics change. The original gameplay, balancing, elbow-UV and source tests remain in Tools/validate.py.

No game installation or saves were edited. Close KSP, replace GameData/RoosterWorksStationModules with the TEST folder and restart. Confirm both RW-TUB entries load and appear in Station Connectors; inspect the category table above and both elbow UVs. New live model loading and menu placement confirmation remain pending; offline validation does not constitute an in-game test.

The roadmap now also includes **selectable logistics contents** for Food, Water, Oxygen, Ammonia, Waste and other supplies, alongside ground-base modules, adjustable legs and ring colors. Current LOG remains Station Utility as confirmed; dedicated future supply-container placement is left to that future work.
