# v0.12.0-dev.1 — Greenhouse light fix and nine 3.75 m modules

User reported no greenhouse lighting and requested fixing it, then producing
3.75 versions of the 2.5 station modules. Read source kit and installed stock
KSP light configuration; read prior ModuleManager cache, without editing the
installation. Prior GRN had only emissive geometry, no native Light. Default
removes its cosmetic grow-light toggle, and sets grow emission according to
artificial light demand. A surface glow cannot light real plant meshes.

Add four native warm-white point lights above crop tiers at Y=-0.74,-0.15,0.44,1.03 m, intensity 1.4, range 2.2 m each,
and separate inspection-strip renderer, RW_GreenhouseInspectionLamps. Stock
ModuleLight uses RW_GreenhouseInspectionLight; default on, manual switch in
editor/flight, no animation dependency, no added resource draw. Existing crop
renderer RW_GreenhouseLamps and Default crop support are unchanged. Cosmetic
inspection lighting is independent from growth, and remains available with
Kerbalism; production still requires normal inputs/power/environment. MU Light
record type 23 follows the io_object_mu format documentation. Native parser
extended to read it. No new plugin or modified hatch runtime needed. Small GRN
40764 visual triangles (64 added inspection-strip triangles), previous collision
hull, glazing and 192 plants retained. Actual Unity switch/lighting tests pending.

Added HAB/LAB/CMD/HUB/CUP/LOG/AIR/PWR/GRN-375. Full 1.5 geometry scaling includes
axial length, native colliders, trigger size/position and attach coordinates;
size-3 stack nodes, rescaleFactor=1. Surface 2.25 and volume/dry mass/storage 3.375,
slots double. Crew counts/IVAs retained exactly: HAB4, LAB2, CMD2, HUB0, CUP1,
LOG0, AIR2, PWR0, GRN0. No invented new seats. Command/science behavior retained;
CMD reaction wheel torque/EC scale by 3.375. Original renderer, variant and hatch
trigger names deliberately retained so stock controllers and original runtime
bind correctly. EVA fixed 0.5 m ray-origin offset checked against exported large
HAB and AIR solid hulls, rather than scaling the offset. Hub rounded profile
and all other accepted shapes are proportional; no new boxy hub.

Large labels are new PNGs, original shared cladding/artwork retained. Individual
native MU and scaled editable OBJ/MTL provided; rebuild source uses actual
maintained small exports with strict typed serialization, plus ordered ConfigNode
cloning. Large-specific Kerbalism/VABOrganizer files use new IDs only, inherited
conditions/modules, scaled volume/surface/resources; GRN-375 rates are 1.6875
times installed standard greenhouse. Original adapter already spans these sizes;
no unrequested 5 m adapter. Total 19 parts. All unrelated small GameData hashes
protected by Tools/large_family_baseline.json; original runtime DLL unchanged.

Tools/validate_family375.py checks all nine exports, source-sized triangles/UVs/
normals/materials, colliders, native lights, nodes, IVA/crew roles and ray origins.
Entire historical suite retained; greenhouse validator now requires an actual
Light, stock switch and separate lamp renderer. Canonical build/packaging support
19 parts. Optional Source/Blender/create_family375.py uses --part and --variant;
Blender was not executed. Native CPU overview and dark inspection views include
point-light attenuation as an approximation; no claim of KSP rendering/testing.

First large family is a development candidate. User has not accepted its fit,
appearance, lighting, balance or gameplay yet. No save edits, installation,
GitHub commits, tags or release performed. Earlier source archives preserved.
