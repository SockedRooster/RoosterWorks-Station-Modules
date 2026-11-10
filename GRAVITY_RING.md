Current corrections: v0.7.5-dev.8 — see GRAVITY_RING_FIXES.md. Includes two pressure-access tubes and their wider, slightly angled stow geometry (5 m fairing recommended), corrected color-map format and dedicated window emission mask. Previous design notes below.

# GRAV-250 folding gravity habitat — v0.7.5-dev.7 TEST

New four-crew station part with a fixed 2.5 m axial hub and two stack nodes.
Eight hinged spokes unfold alternating packed pressure sections, then inflate
to form a roughly 9.84 m ring (plus seam hardware). Recommend a 5 m fairing.
Review Media/GravityRing/Stowed.png, Unfolding.png and Deployed.png.

In orbit, choose Deploy Gravity Ring, wait for inflation, then Start Ring
Rotation. Speed adjusts 1–8 rpm, default 6 rpm; Stop Ring Rotation coasts down.
Before folding, stop completely and transfer crew to another station module.
Deploy/fold/start/stop have action-group bindings. VAB previews are supported.
White/Grey finish and hub ring colors retain the standard station controls.
Eight window banks have a stock Ring Lights switch.

The rotor is animated geometry on one fixed part. Attached modules and the
axial attachment nodes do not rotate. This does not generate physical gravity,
spin momentum, gyroscopic forces or a rotating walkable IVA. The calculated
acceleration display is informational: 6 rpm at 4.2 m is approximately 0.17 g.
No automatic Kerbalism gravity/comfort bonus is added. Conservative Kerbalism
support counts only the 12 m³ fixed hub. Inflated ring space is not counted
yet; crew use the stock four-seat cabin IVA. There is no exterior hatch: use
crew transfer through the hub. Advanced gravity effects/IVA are future work.

Mass 8 t; cost 48,000; 900 EC; inventory 8 slots/600 L. Deployment uses
0.25 EC/s, rotation 0.75 EC/s, only while loaded/unpacked at normal time rate.
Power loss pauses deployment and coasts the rotor down; operation resumes
when power returns. Physics warp/high time warp pause the controller, with
no background EC processing. Folding is blocked while crewed or spinning.
Give the deployed ring clear space from solar panels and station structures.

Stock research uses specializedConstruction; Community Tech Tree overrides
to longTermHabitation. The part is under Utility / Habitation when VABOrganizer
is present. All dev.6 logistics changes and previous station assets/plugins
remain byte-identical, except the version. This adds six assets/configs only.

Close KSP; replace only GameData/RoosterWorksStationModules. The separate
ground addon remains installed. Try deployment, lighting, rotation/stop, power
loss, saving/reloading and crew-transfer/fold interlocks in a test station.
In-game acceptance is pending; the installed game and saves were not changed.

Current native builder: Source/build_gravity_ring.py. Editable packed geometry:
Source/Blender/RW_GRAV_250.blend. Runtime: Source/GravityRing.cs and
Tools/build-gravity-runtime.ps1. Source-aware tests: Tools/test-gravity-ring.ps1.
Native/preservation gate: Tools/validate_gravity_ring.py. Runtime compiled with
KSP 1.12.5; 1,788 controller assertions pass with doubles, including interlocks,
power, ramping, saved phase, warp, editor controls and intermediate poses. These
do not replace full ModuleManager, collision or in-game visual testing.
Earlier builders/reports remain historical. Previews use exact native geometry
under illustrative Blender lighting. Both install and developer archives verify
CRC, checksums and identical GameData payloads.
