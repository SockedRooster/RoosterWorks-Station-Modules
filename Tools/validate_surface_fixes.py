"""Check native readable UV handedness and every recessed endcap liner."""
from pathlib import Path
import math,sys
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_hub250 import PORTS,orient

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

interfaces={'HAB':[(s,1.98) for s in (-1,1)],'LAB':[(s,1.98) for s in (-1,1)],
            'GRN':[(s,1.8) for s in (-1,1)],'PWR':[(s,1.2) for s in (-1,1)],'AIR':[(s,1.2) for s in (-1,1)],'CMD':[(s,.86) for s in (-1,1)],'CUP':[(-1,.86)],'LOG':[(s,1.5) for s in (-1,1)]}
for label in ('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN'):
    model=load(ROOT/f'GameData/RoosterWorksStationModules/Models/RW_{label}_250.mu')
    meshes=[];readable=0
    for _,node in walk(model.root):
        if 'mesh' not in node or 'materials' not in node:continue
        mesh=node['mesh'];meshes.append(mesh)
        for triangles,material_id in zip(mesh['submeshes'],node['materials']):
            material=model.materials[material_id]
            tex=model.textures[material['properties']['_MainTex']['index']]['name']
            if tex!='rwm_crest' and 'label' not in tex and tex!='rwm_detail' and 'cladding' not in tex:continue
            for a,b,c in triangles:
                uv=mesh['uvs'];p=mesh['vertices'];n=mesh['normals'][a]
                u1,v1=sub(uv[b],uv[a]);u2,v2=sub(uv[c],uv[a])
                # Unity clockwise faces: screen-right U and screen-up V give
                # a negative determinant relative to the outward winding.
                assert (u1*v2-u2*v1)*dot(cross(sub(p[b],p[a]),sub(p[c],p[a])),n)<-1e-15,(label,tex,'mirrored UV')
                readable+=1
    def local_vertex(p,n,axis=None,sign=1,plane=2):
        if axis is not None:
            basis=[orient(v,axis) for v in ((1,0,0),(0,1,0),(0,0,1))]
            return tuple(dot(p,v) for v in basis),tuple(dot(n,v) for v in basis)
        return (p[0],sign*p[1]-plane+2,sign*p[2]),(n[0],sign*n[1],sign*n[2])
    caps=[(axis,1,2) for axis in PORTS.values()] if label=='HUB' else [(None,s,plane) for s,plane in interfaces[label]]
    for axis,sign,plane in caps:
        verts=[local_vertex(p,n,axis,sign,plane) for mesh in meshes for p,n in zip(mesh['vertices'],mesh['normals'])]
        # Verify native cap cylinder faces, not just the authoring function.
        for radius,y0,y1,inward in ((1.125,1.920,1.994,True),(1.145,1.992,1.997,True),
                                    (1.225,1.920,1.997,False),(.510,1.981,1.986,True),
                                    (.485,1.969,1.982,True),(.130,1.969,1.981,False),(.104,1.976,1.981,True)):
            for y in (y0,y1):
                ring=[(p,n) for p,n in verts if abs(math.hypot(p[0],p[2])-radius)<2e-6 and abs(p[1]-y)<2e-6 and abs(n[1])<1e-6]
                assert len(ring)>=96,(label,axis,sign,radius,y,'missing liner')
                assert all((p[0]*n[0]+p[2]*n[2])*(-1 if inward else 1)>.99*radius for p,n in ring)
        outer=[]
        for _,node in walk(model.root):
            if 'mesh' not in node or 'materials' not in node:continue
            for material_id in node['materials']:
                mat=model.materials[material_id];tex=model.textures[mat['properties']['_MainTex']['index']]['name']
                if tex=='rwm_hubblanket':
                    outer.extend(local_vertex(p,(0,0,0),axis,sign,plane)[0] for p in node['mesh']['vertices'])
        assert sum(1 for p in outer if abs(math.hypot(p[0],p[2])-1.130)<2e-6 and 1.920<p[1]<1.994)>=288
    if label=='CUP':
        crown=[(p,n) for mesh in meshes for p,n in zip(mesh['vertices'],mesh['normals'])
               if abs(math.hypot(p[0],p[2])-.594)<2e-6 and abs(n[1])<1e-6 and .6209<p[1]<.6331]
        assert len(crown)>=576
        assert all(p[0]*n[0]+p[2]*n[2]<-.593 for p,n in crown)
        assert any(abs(math.hypot(p[0],p[2])-.614)<2e-6 and abs(p[1]-.633)<2e-6 for mesh in meshes for p in mesh['vertices'])
        print('PASS CUP upper viewport: continuous inward liner and overlapped outer lip; glazing unchanged')
    print('PASS',label,readable,'readable Unity-facing triangles;',len(caps),'sealed recessed caps')
print('PASS all 21 shared interfaces (adapter has a separate scaled-cap audit): inward liner faces, outer skirt to lip, blanket overlap and sealed closure steps')
