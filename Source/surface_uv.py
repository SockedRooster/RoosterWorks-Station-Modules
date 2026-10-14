"""Readable outward labels in Unity's left-handed camera convention.

Keep this in source geometry so MU, OBJ and Blender all agree. PNG artwork
stays unchanged. Atlas covers reverse U within each island at atlas_uv().
"""
def finish(meshes):
    for material,mesh in meshes.items():
        if material=='crest' or 'label' in material or material.startswith('cladding'):
            mesh.uvs=[(1-u,v) for u,v in mesh.uvs]
    return meshes
