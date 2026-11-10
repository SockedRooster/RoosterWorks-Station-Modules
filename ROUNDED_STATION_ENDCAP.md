# Rounded station endcap — v0.7.5-dev.10 TEST

Adds RW-END-250/125 to Station Modules: a 0.9 m-long rounded transition from
the 2.5 m station interface to a 1.25 m nose, matching the accepted ground
endcap shell. All four underside hose runs (104 individual segments) are
removed. Grab rails, small routed shoulder lines, trim, recessed faces and
upright badges remain. The label now identifies Station Systems.

The model is Y-axial like the station family: large size2 structural base at
Y=-0.45 m, small size1 docking nose at Y=+0.45 m. It weighs 0.30 t and costs
1,250 funds, with 350 connection force/torque thresholds. The large end has
no docking module. The small end uses stock docking with crossfeed enabled
and staging disabled. It retains the ground endcap's acquisition settings.
Docking uses stock controls; no Ground Modules docking controller is required.

White/Grey metal finishes and all existing independent ring colors use the
unchanged station appearance plugins. Both end windows have working emissive
materials controlled by Module Lights, including the Lights action group.
No crew, IVA, exterior EVA hatch, habitat, shielding, fuel or ground equipment
is added. Optional Connected Living Space marks it passable. With VAB
Organizer, it appears in Station Adapters (crewAdapters).

This part is self-contained in Station Modules. It does not require Ground
Modules, and no ground files are changed. All existing dev.9 Station Modules
models, textures, configurations and plugin binaries are byte-for-byte
preserved; only the version and new endcap files are added. The accepted
compact gravity ring and working ring lights remain unchanged.

Close KSP, replace only GameData/RoosterWorksStationModules and restart.
The part is named RoosterWorks RW-END-250/125 Rounded Station Endcap. Find it
under Structural / Station Adapters or search END-250. Test the two attachment
sizes, the nose docking port, White/Grey finish, ring colors after reopening
the menu and Module Lights. Flight physics/full mod-load acceptance is pending.
No installed game files, craft or saves are modified by this package.

Checks cover Y-axis attachment/port orientation, outward normals/winding,
finite UVs/geometry, ten convex collision sections within PhysX limits,
emission mask/alpha, ring-map bounds, dependencies, hashes and preservation.
3,728 actual-source color assertions cover exact body/ring partitions, all
colors, repeated menu polling and native reset/rebinding with the real new map.
The copied dev.9 gravity/color tests remain relevant to unchanged assets;
the current validation entry point is Tools/validate_station_endcap.py.

Builder: Tools/build_station_endcap.py. Editable packed native-equivalent
model: Source/Blender/RW_END_250_125.blend. Preview tool:
Tools/create_station_endcap_blend.py. Previews: Media/StationEndcap/.
Building the derivative requires the protected adjacent ground-hotpatch-v23
source; installation does not. All build inputs are read-only.
