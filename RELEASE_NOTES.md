# RoosterWorks Station Modules v0.6.0-dev.1 — Development Test

**Do not publish as a stable release.** The separately preserved v0.5.3-rc.1 remains the current prepared prerelease candidate.

This development build adds an original RW-CUP-250 2.5 m terminal observation cupola with eight sloped glass bays, circular overhead window, bronze/ivory service collar, original RoosterWorks brand details, one crew position, stock `cupolaInternal` provisional IVA, exterior lighting toggle, 300 ElectricCharge, and conditional Kerbalism supplies/habitat. Bottom stack interface at Y=-0.860 m, no upper node. All prior four stations' native models/configurations and runtime code remain unchanged.

The model's `.mu` is generated from the same RoosterWorks Python geometry and includes a watertight 96-triangle convex collision mesh; editable OBJ/MTL and Blender builder are packaged in the developer source. The cupola has no EVA hatch, reaction wheel, antenna, command controls or integrated docking. This is a visual terminal station module, not a standalone vessel controller. Glass remains the current dark-tinted material; no custom IVA has been made.

Offline native/config/geometry validation passed, as did the prior four station modules' regression suite. In-game VAB mounting, Kerbalism, crew transfer, window lighting, hub assembly and actual flight behavior remain to be tested. `TEST_CHECKLIST-v0.6.0.md` details the checks. Do not imply that v0.5.3 hub/endcap flight acceptance has occurred.
