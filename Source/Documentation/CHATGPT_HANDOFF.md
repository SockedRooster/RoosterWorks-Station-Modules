# RoosterWorks Station Modules — regular ChatGPT handoff

Prepared October 12, 2026. Continue this project from the attached developer source; do not restart it from a screenshot or regenerate the tested parts from scratch.

## Current task and deliverables

The user requested release preparation and continuation in regular ChatGPT. Prepared v0.5.3-rc.1 with unchanged v0.5.3 GameData, cleaned public documentation, player/developer ZIPs, source-import workflow and release checklist. No GitHub publish, tag, source upload, game installation or live conversation conversion was performed. A Chat conversation can continue from this document and uploaded source archive; desktop paths alone are not file contents.

Latest source: developer archive named RoosterWorks-Station-Modules-v0.5.3-rc.1-Developer-Source.zip. Repository: https://github.com/SockedRooster/RoosterWorks-Station-Modules . The repository importer was read during preparation and still targets v0.4.3. Replace it with the prepared importer before uploading the new developer ZIP. It pins the archive checksum, exact entry count and safe allowed paths. Do not merely rename an older archive.

## Confirmation boundary

v0.4.6 is the last explicitly user-confirmed functional baseline: HAB Side Hatch EVA, grab/climb, boarding, Standard Windows access gating, improved windows, radial attachments, CMD control/standalone signal, and LAB science all worked. The hub and endcap changes through v0.5.3 passed static/native model checks; the user has not explicitly confirmed hub flight, six-node attachment/symmetry, through-hub crew transfer, Kerbalism atmosphere, or final endcap appearance. Publish as a prerelease until these are confirmed; do not describe them as runtime validated. The release is prepared locally, not published.

## Parts and design decisions

- HAB-250: four seats, +/-1.98 m stack planes. Standard Windows / Exterior Side Hatch variants. Side Hatch at angle 60 degrees, y=-0.64875 m, radius 1.43 m; native Airlock and overlapping inward-facing Ladder triggers on layer 21. Top/bottom endcaps are decorative; they are not additional EVA exits.
- LAB-250: two seats, +/-1.98 m stack planes, science/life-support integration. Preserve actual patched experiment/storage behavior.
- CMD-250: two seats, +/-0.86 m planes, command/SAS/reaction wheel and INTERNAL + DIRECT telemetry. All modules explicitly vesselType=Station. Temporary stock IVA retained.
- HUB-250: six 2.5 m size-2 nodes at +/-2 m X/Y/Z, four-way side-node symmetry, no seats/command/EVA/integrated docking. Separate docking ports attach to nodes. Thirteen solid colliders; Kerbalism Habitat volume 10/surface 35, initial balance. Mass 2.5 t, cost 6200, Structural/metaMaterials.
- Preserve ivory panels, bronze accents, original rooster logo, warm-white lights and Kerbalism integrations. User wanted endcaps matching the reference-informed hub: small pressure closure, broad recessed bronze insulation, thin rim, pipes/rail details. Source/station_endcaps.py now supplies the exact common cap to all four parts. Endcap fittings are decorative. Custom IVAs remain deferred.

## Established root causes and fixes

CMD no signal: parts lacked vesselType; RW-only vessels launched as Debris. Installed KSP 1.12.5 CommNetVessel destroys its connection for Debris/SpaceObject/Unknown. Explicit Station classification fixed it. Existing Debris saves are not rewritten. An obsolete CMD250_CommNet_Diagnostic_A.cfg replaced native transmitters; it was disabled and must remain disabled/removed.

HAB hatch blocked: KSP casts a clearance ray from 0.5 m behind hatch toward the hatch. Hollow thin wall-box colliders self-intersected that ray at ~0.200 m. Replaced them with one watertight convex 24-sided hull, 96 triangles; ray origin is inside with 0.227 m margin. Keep this geometry and stock external obstruction checks.

No grab point: add native Ladder-tagged box trigger at the exit, inward local Z/up local Y. Standard's invisible exit: runtime gates both colliders and cached part.airlock using ModulePartVariants.SelectedVariant.Name. Portrait EVA additionally checks part.NoAutoEVA, so controller owns/restores part.noAutoEVAAny in flight while preserving its original restriction. It does not write the temporary lock in the editor. Startup and variant-change handling are tested with actual-method state doubles. Runtime assembly/version remains 0.4.6 intentionally; do not confuse that with package version 0.5.3.

## Source and validation workflow

Python generators write native .mu and textured OBJ/MTL. Shared geometry/material helpers are Source/build_hab250.py; LAB/CMD use them. Source/build_hub250.py contains hub shell/colliders. Shared endcaps are Source/station_endcaps.py. Rebuild geometry without rerunning texture generators when preserving the exact rooster/label/blanket textures. Python/Pillow required; previews use NumPy. Runtime is C# compiled against actual KSP assemblies with Tools/build-runtime.ps1; no KSP/Unity DLLs are included.

Run Tools/validate.py and Tools/test-hatch-access.ps1. Prior independent MU reader audit confirmed unchanged HAB/LAB/CMD collider objects and glazing meshes after cap changes; hub MU unchanged from v0.5.2. All installed GameData stays identical to v0.5.3 TEST in this release candidate. Developer ZIP includes all editable sources and build/check tools, not proprietary game assemblies, saves, raw game IL, local audit caches or third-party reference assets.

Original Work continuation conversation: chatgpt-conversation://6acbd061-161c-83ea-8455-04fe2dfc20b4 (Code RW Station parts). Its cached assistant messages were opaque, so this handoff and developer files are authoritative for recovered decisions. No complete remaining-parts roadmap was recovered; do not invent agreed part names.

## Local paths (only when that computer is connected)

Workspace: C:/Users/rida6/.codex/.chatgpt-projects/g-p-6ac8f1e835cc819196ce79f44b4b0698 . Synced sources/ is read-only. Latest working model source rw-v053; release copy release-v0.5.3-rc.1/source. Preserve prior ZIPs/checksums.
Game/log: D:/SteamLibrary/steamapps/common/Kerbal Space Program/KSP.log . Cache: same game root/GameData/ModuleManager.ConfigCache . Original v0.4.3 archives are in C:/Users/rida6/Downloads.
For future failures inspect actual current KSP.log and ModuleManager.ConfigCache when provided; don't claim a speculative config fix has solved a runtime issue. Regular ChatGPT should ask for these files when it cannot access the local installation.

## Next step

Review RELEASE_CHECKLIST.md and obtain the remaining in-game confirmations. Then finalize publishing/tag/release assets with the user. Keep changelogs around final implemented behavior. Continue future parts using the existing shared assets/geometry; preserve proven systems. Do not infer approval to publish from this document alone; follow the user's direct requests in the receiving chat.
