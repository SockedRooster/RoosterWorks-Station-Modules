# Ring selector hotfix — v0.7.5-dev.3

User reported that ring colors change initially but stop responding after
clicking away and reopening the part menu. Surface colors continue working.

The previous code had two independently reproducible stale-state gaps: an
unchanged B9 subtype name didn't resynchronize a restored ringColor field,
and a cached ring Material was still painted after the displayed renderer
materials were recreated. Regression tests failed against dev2 for both gaps.
This simulates editor rebuild conditions; the exact live KSP trigger has not
been traced in-game.

The menu now compares the live persisted choice with the swatch every editor
frame. Ring binding detects replaced meshes and reconnects live body/ring
materials before applying color. Detached owned meshes/materials are released;
cleanup avoids overwriting another controller's replacement mesh/materials.
The polling fallback survives recreated UI callback delegates.

Only RoosterWorksEditor.dll, RoosterWorksCustomization.dll and version metadata
change in GameData. All models, textures, other plugins, part configs, science
tiers, finish options, resource capacities and reactor logic remain identical
to dev2. Historic source/runtime snapshots and exact hotfix digest policy are
embedded for portable regression validation. The logistics source in the
recompiled customization DLL is unchanged and its tests still run.

## Installation and live confirmation

Close KSP. Replace the RoosterWorksStationModules folder with the TEST package's
GameData folder contents. Do not overlay only source files; both runtime DLLs
must update. No automatic game installation or save changes were performed.

In VAB/SPH, select a ring color, click away, reopen the menu, and select several
other colors. Repeat close/reopen cycles and test Original. Switch surface
White/Grey between ring choices, test HAB hatch and PWR hardware variants,
symmetry copies and editor save/reload. Existing flight appearance and science
archives should remain intact. Offline regressions pass; actual reported
in-game sequence remains pending user confirmation. This is a development
test build, not a publication or release-status claim.
