# RoosterWorks visual development build 01

Based on v0.7.5-dev.11. This is a cosmetic development candidate, not a new gameplay release.

## Artwork

HAB, LAB, CMD, CUP and LOG at 2.5, 3.75 and 5 metres receive chamfered captive panel latches and recessed, bridged quick-disconnect collars. Added hardware shares the existing steel, bronze and graphite materials, in three additional meshes per model. The small hardware is most visible in close inspection.

Thirteen shared surface maps receive restrained manufactured detail: shallow cladding edge relief, inspection witness marks, laser-etched lot codes, brushed-metal grain and softly folded thermal quilting. Existing UV layouts, texture resolution and finish variants are retained. Other parts using these shared maps also receive the surface treatment. Gravity-ring, industrial, adapter and other model geometry is unchanged.

Original mesh nodes, materials, collisions, hatch variants, attachment transforms, shaders, emissions, plugins, configurations and gameplay values are retained. Existing customization paths and triangle ranges still address the original geometry. Added hardware uses fixed metal finishes. No normal maps, new shaders or extra texture dependencies are introduced.

## Install and rollback

Close KSP. Back up the existing `GameData/RoosterWorksStationModules` folder, then replace it with the folder from the Install zip. Keep all other mods as they are. Restore the backed-up folder to roll back. This work does not modify an installed game or saves.

## Review

`Media/VisualUpgrade/Review.png` shows matched-lighting before/after habitat views, detail views, and four upgraded module families. These are Blender renders of the exported native MU assets; Blender lighting and material interpretation are not a KSP screenshot. `Source/Blender/RW_VisualUpgrade_Review.blend` contains packed editable review scenes.

The original source archive remains unchanged. `Reports/VISUAL_UPGRADE.json` records the changed assets, added triangle budgets and offline checks. All unmodified runtime files are compared byte-for-byte with the supplied dev.11 archive. The historical `validate_appearance.py` passes its geometry checks but deliberately fails its old texture fingerprint check on the newly authored bronze texture; use `validate_visual_upgrade.py` for this art candidate.

In-game acceptance remains pending: inspect all three sizes, both habitat hatch options, white/grey and ring-color selectors, lighting, EVA access and docking clearances in a test save. No FPS claim is made without running KSP.

## Rebuild

Use Python with numpy and Pillow:

```
python Tools/build_visual_upgrade.py --archive /path/to/original-dev.11-source.zip
python Tools/validate_visual_upgrade.py
blender --background --python Tools/render_visual_upgrade.py
```

The upgrade builder reads original assets from the archive on every run and adds only this pass. Rebuilding historical part generators afterward will replace its added hardware; rerun the visual builder last. The `.build-deps` folder used locally is not included in either distribution.
