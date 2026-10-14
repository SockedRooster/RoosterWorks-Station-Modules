# v0.16.0-dev.2 — elbow artwork UV fix

User's in-game screenshot showed logos and nameplates repeated six times across the bend. The elbow panel helper subdivided geometry for curvature but restarted texture V=0..1 on every strip. It now maps each strip to its corresponding fraction of the complete panel. Both 250/375 elbows have single continuous nameplates, logos and cladding texture coverage. UVs alone change; exact geometry, normals, indices, materials, textures, colliders, stack nodes, gameplay and the straight tube models are preserved.

New exported-model regression checks sum UV area to require one artwork instance per physical plaque/logo and one texture per cladding tile, and check shared plaque UV edges. The old winding-only test detected mirroring but not repeated artwork; that coverage gap is corrected. The native MU, OBJ/MTL and procedural source agree. Live KSP oblique/close-up visual confirmation remains pending.

Balance and science storage from dev.1 are unchanged. The roadmap includes ground-base modules, adjustable legs and selectable ring colors on each module. Close KSP before replacing the TEST folder. No installation, save edits, GitHub action or release was performed.

## Prior development notes

