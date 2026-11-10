# Hub Fix 05

Targeted follow-up to Uniformity 04. Only the three six-way hub models and their affected color-selector geometry records change. The other 44 models, textures, part configurations and plugin binaries are preserved byte-for-byte.

The axial handrails and blue/yellow cable pairs now follow the rounded hub skin with frequent seated supports. Old short graphite/bronze shoulder looms are removed. All four radial necks receive matching service lanes extending to their attachment planes, using the shortest rotation from module +Y to the port normal without additional roll. Side runs turn into seated terminal pads on the shoulders rather than crossing the axial routes. Hub colliders, structural shell, ports and gameplay are unchanged.

## Install

For an existing **Uniformity 04** installation, extract the **Patch** archive over the KSP folder and allow its included files to overwrite. Do not remove the mod folder when applying this small patch.

The **Install** archive is the complete mod: back up and replace `GameData/RoosterWorksStationModules` with its included folder. Retain the external dependencies used by dev.11. No installed game or saves were modified during this work.

## Checks and editable source

`Reports/HUB_FIX_05.json` records export checks for all three sizes, surface contact at mounts, mesh validity, non-degenerate new triangles, terminal positions and rotation, preserved colliders, color selectors and hashes of unaffected runtime files. Studio renders show before, after and an assembled stack with a radial module. KSP visual and EVA acceptance remains pending; no in-game performance claim is made.

The editable review scenes are in `Source/Blender/RW_HubFix05.blend`. The reproducible Uniformity 04 hub input models and geometry selectors are bundled in `Source/Study05Baseline`. With Blender 5.2, NumPy and Pillow available:

```
blender --background --python Tools/build_hub_fix.py
blender --background --python Tools/validate_hub_fix.py
blender --background --python Tools/render_hub_fix.py
python Tools/package_hub_fix.py
```

Earlier revision documents are retained as history. Use these commands for this hub correction, rather than rerunning the older whole-family builders.
