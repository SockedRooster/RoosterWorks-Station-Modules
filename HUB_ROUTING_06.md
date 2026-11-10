# Hub Routing 06

Supersedes Hub Fix 05. Side-port rails and blue/yellow cables no longer end on shoulder pads. Each follows the curved upper or lower shoulder around to a matching vertical stack run, with exact centerline joins and supported bends. Side-port cable offsets are reversed to match the mating orientation shown in the user's KSP screenshots. Rail endpoints at the six mating planes remain fixed.

Only the three hub models and their affected color-selector geometry records differ from Uniformity 04. The other 44 models, textures, part configurations and plugin binaries are unchanged. This is static routing: rotating an attached module about its port can change alignment.

## Install

Apply the **Patch** archive over an existing Uniformity 04 or Hub Fix 05 installation, allowing included files to overwrite. Do not remove the mod folder when applying the patch.

Alternatively, the **Install** archive contains the complete mod. Back up and replace `GameData/RoosterWorksStationModules` with its included folder. Retain external dev.11 dependencies. No game installation or saves were modified while preparing this candidate.

## Validation and source

`Reports/HUB_ROUTING_06.json` records native export validation, including every branch-to-stack centerline join, matching material/color, actual exported tube endpoints, side-port handedness, support contact, all hub colliders, geometry selectors and unaffected runtime hashes. Review images show both sides and an assembled stack; these are Blender previews. KSP acceptance and runtime performance testing remain pending.

The packed review scenes are in `Source/Blender/RW_HubRouting06.blend`. The builder uses the bundled Uniformity 04 hub models and selectors in `Source/Study05Baseline`; historical folders and notes remain available for comparison. With Blender 5.2, NumPy and Pillow available:

```
blender --background --python Tools/build_hub_fix.py
blender --background --python Tools/validate_hub_fix.py
blender --background --python Tools/render_hub_fix.py
python Tools/package_hub_fix.py
```

These current hub scripts produce revision 06. Older whole-family builders should not be rerun as a way to rebuild this revision.
