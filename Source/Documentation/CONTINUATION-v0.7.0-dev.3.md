# v0.7.0-dev.3 — Rounded HUB revision

User feedback: "I don't like the boxyness of the hub" after the dev.2 family
detail pass. Built from a separate copy of the dev.2 source, leaving earlier
source and archives intact. The HUB now uses a radius-1.8 m central spherical
pressure shell, tiled as six matching face patches. Circular apertures at local
Y=1.3 m transition via a tangent Hermite profile to radius-1.204 m collars at
Y=1.6 m. Smooth normals continue across the shared spherical seams. Existing
thermal petals, service conduits and collar/endcap detail follow the new surface.

Node positions remain ±2 m on all three axes; the part remains crewless and all
part/compatibility CFGs, Kerbalism balance and runtime DLL are unchanged. All
textures and the other five native models are byte-identical to dev.2, checked
against separately recorded baseline hashes in Tools/hub_revision_baseline.json.

HUB collider preservation is intentionally superseded for this authorized shape
revision. Replaced central box with an inscribed 224-triangle convex sphere;
six conservative neck frustums and six collar cylinders retain 13 solid convex
colliders. The validator reads actual exported MU collider records, compares to
procedural geometry, checks outward winding/watertightness/convexity, samples
collider surface containment, and checks spherical seams and tangent neck ends.
The five other collider sets remain protected by authentic dev.1 hashes.

Latest previews: Media/RW-HUB-250-v0.7.0-dev.3-Rounded-Review.png and
Media/RoosterWorks-v0.7.0-dev.3-Family.png. Actual exported geometry and shipped
textures are shown using the existing CPU diffuse renderer. Dev.2 review/detail
images for the five unchanged modules remain applicable; all older images are
historical. Build/validate/package remain Tools/build_appearance.py,
Tools/validate.py and Tools/package_appearance.py; Tools/render_rounded_hub.py
regenerates the current HUB sheet (comparison uses adjacent dev.2 if available).
Editable OBJ/MTL regenerated; optional Blender reconstruction not executed.

Offline validation and package integrity checks passed. This candidate has no
user visual acceptance or KSP runtime confirmation yet. In particular, check
radial attachments and station assembly because HUB collision geometry changed.
No KSP install, GitHub commit/tag/release or save modification performed.
