# RoosterWorks — Detail Study 02

This is the second exterior art candidate, based on Visual Development 01 and the original v0.7.5-dev.11 gameplay build. It responds to the supplied in-game comparison: substantial material relief and structural depth visible at normal viewing distances. The reference is used as visual direction; no assets from the other mod were copied.

## Changes

- Both habitat lengths (HAB and HABS), in 2.5/3.75/5 m sizes: gently padded hull covers, deeper stepped window bezels around the existing glass, bevelled segmented metal shoulders and supported perimeter grab handles. Six native models receive geometry changes.
- All 47 models receive normal-mapped insulation/foil materials where used. Woven, wrinkled thermal covers have stitched hems and sparse inspection markings. Gold endcap foil has irregular folded relief and smoothly shaded underlying geometry.
- Two shared 1024-square DXT5nm maps, with full 11-level normalized mip chains and exported tangent frames, drive stock KSP/Bumped Specular shading. No additional plugin dependency is introduced. Five albedo/specular textures are reauthored, including the existing grey finish alternatives.
- The first pass's service hardware remains. Glass shapes and emissive materials, hatch identities, attachment transforms, collider geometry, gameplay configs and binaries remain unchanged. Ring-color selection keeps its original vertex counts and triangle ranges. New shoulder metal has a fixed structural finish.

## Install

Close KSP. Back up your existing `GameData/RoosterWorksStationModules` folder, then replace that folder with the folder from **RoosterWorks-Detail-Study-02-Install.zip**. Keep other mods unchanged. Restore the backup to roll back. The full install package includes the preceding detail pass; it does not require installing Pass 01 first.

This work only changes the workspace copy. No installed game or save was modified. The gameplay version file remains dev.11; the archive name and this document identify the art candidate.

## Preview and acceptance

`Media/DetailStudy02/Comparison.png` contains matched-lighting views against Pass 01, including the compact habitat shown in the supplied comparison. The renderer imports the shipped MU files and decodes the actual runtime DDS maps. `Source/Blender/RW_DetailStudy02.blend` contains the packed editable scenes. Blender uses an approximation of the stock KSP specular shader, so these images establish geometry and texture appearance, not exact in-game lighting.

`Reports/DETAIL_STUDY_02.json` is the current offline validation report. Historical reports elsewhere in the source describe earlier builds. Checks cover native mesh limits and indices, tangent frames, texture references, complete DDS mip chains, preserved glass/colliders and original ring-selector mappings, and byte-identical gameplay files.

KSP acceptance remains pending. In a test save, review the compact and long habitats at all three sizes, white/grey finishes, each ring color, both hatch options, cabin lights, EVA access, and stacked/docked end clearances. Inspect the texture response under VAB and directional flight lighting and while zooming out. Performance has not been measured in KSP.

## Reproduce

Python requires numpy and Pillow (DDS DXT5 support). Blender 5.2 was used for the review scenes.

```
python Tools/build_detail_study.py --baseline ../RoosterWorks-Visual-Development-01-Install.zip
python Tools/validate_detail_study.py
blender --background --python Tools/render_detail_study.py
python Tools/package_detail_study.py
```

The builder restores the immutable Pass 01 install before applying Study 02, so rerunning it does not accumulate geometry. Keep that input archive beside this working folder. `Source/Study02Baseline` retains the input native models and textures for review. The procedural texture authoring sources are in `Source/Textures/DetailStudy`. The older `build_visual_upgrade.py` and its validator apply only to Pass 01; they are retained as history and are not the final Study 02 build step.

Normal-map conventions were checked against the primary [MU reader/writer](https://github.com/taniwha/io_object_mu/blob/master/mu.py) and its [texture importer](https://github.com/taniwha/io_object_mu/blob/master/import_mu/textures.py): normal texture type, stock shader name, and DDS vertical-storage convention. DDS X/Y channels are packed in alpha/green and decoded for review. RGB source normals are also included for editing.
