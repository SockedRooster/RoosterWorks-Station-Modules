"""Ensure the common caps fit all original mating planes and face outward."""
from pathlib import Path
import sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_hab250 as h
from station_endcaps import face_mesh,add_endcap
faces=face_mesh()
for plane in (2,1.98,.86):
    for sign in (-1,1):
        meshes={key:h.Mesh() for key in h.TEXTURES};add_endcap(meshes,sign,plane)
        for mat,mesh in meshes.items():
            assert mesh.triangles==faces[mat].triangles and mesh.uvs==faces[mat].uvs
            assert all(plane-.09<sign*y<=plane+.000001 for x,y,z in mesh.vertices),'cap protrudes or is too deep'
            assert all(math.hypot(x,z)<=1.225001 for x,y,z in mesh.vertices)
            for tri in mesh.triangles:
                a,b,c=[mesh.vertices[i] for i in tri]
                u=tuple(b[q]-a[q] for q in range(3));v=tuple(c[q]-a[q] for q in range(3))
                n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
                assert sum(n[q]*mesh.normals[tri[0]][q] for q in range(3))>0
print('PASS shared cap: identical geometry/UVs, both ends, HUB/HAB/LAB/CMD planes, outward winding, recessed hardware')
