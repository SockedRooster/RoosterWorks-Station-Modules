"""Check exported tapered geometry, both sealed caps, attachment and prior files."""
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Source'))
from electric_charge_balance import check_preserved
from collections import Counter
import math,json,hashlib,sys,re
import numpy as np
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_adp250375 as b
from station_endcaps import face_mesh
def sub(a,c):return tuple(x-y for x,y in zip(a,c))
def dot(a,c):return sum(x*y for x,y in zip(a,c))
def cross(a,c):return (a[1]*c[2]-a[2]*c[1],a[2]*c[0]-a[0]*c[2],a[0]*c[1]-a[1]*c[0])
def key(p):return tuple(round(x,5) for x in p)
model=load(b.MODELS/(b.PART+'.mu'));solids={};visual={};count=0
for _,node in walk(model.root):
    assert node['tag']=='Untagged' and node['layer']==0
    if 'collider' in node:
        c=node['collider'];assert c['trigger']==0 and c['convex']==1
        solids[node['name']]=c['mesh']
    if 'mesh' not in node:continue
    m=node['mesh'];count+=sum(len(t) for t in m['submeshes'])
    assert len(m['vertices'])<65535 and len(m['vertices'])==len(m['normals'])==len(m['uvs'])
    assert all(math.isfinite(x) for p in m['vertices']+m['normals']+m['uvs'] for x in p)
    assert all(abs(p[1])<=.900001 and math.hypot(p[0],p[2])<1.88 for p in m['vertices'])
    for tris,mid in zip(m['submeshes'],node['materials']):
        mat=model.materials[mid];assert mat['shader']=='KSP/Diffuse'
        tex=model.textures[mat['properties']['_MainTex']['index']]['name'];visual[tex]=m
        for a,c,d in tris:
            p,q,r=[m['vertices'][i] for i in (a,c,d)]
            assert dot(cross(sub(q,p),sub(r,p)),m['normals'][a])>1e-15,'Inverted visual face'
            if tex in ('rwm_crest','rwm_adplabel','rwm_detail','rwm_cladding','rwm_cladding_white'):
                u1,v1=sub(m['uvs'][c],m['uvs'][a]);u2,v2=sub(m['uvs'][d],m['uvs'][a])
                assert u1*v2-u2*v1<0,('Mirrored UV',tex)
assert count==16356 and len(solids)==3
expected={'AdapterLargeCollar':(-.9,-.72,1.806,1.806),'AdapterTaper':(-.72,.72,1.806,1.204),'AdapterSmallCollar':(.72,.9,1.204,1.204)}
assert solids.keys()==expected.keys()
for name,m in solids.items():
    y0,y1,r0,r1=expected[name];vs=m['vertices'];center=(0,(y0+y1)/2,0);edges=Counter()
    assert len(m['submeshes'][0])==96
    assert abs(min(v[1] for v in vs)-y0)<1e-6 and abs(max(v[1] for v in vs)-y1)<1e-6
    for v in vs:
        y=v[1];r=r0+(r1-r0)*(y-y0)/(y1-y0)
        assert math.hypot(v[0],v[2])<=r+1e-6
        assert math.hypot(v[0],v[2])<=b.radius(y)+1e-6
    for tri in m['submeshes'][0]:
        p,q,r=[vs[i] for i in tri];n=cross(sub(q,p),sub(r,p))
        assert dot(n,sub(p,center))>0,'Inverted collider'
        assert max(dot(n,sub(v,p)) for v in vs)<1e-6,'Nonconvex collider'
        points=[key(v) for v in (p,q,r)]
        for i in range(3):edges[tuple(sorted((points[i],points[(i+1)%3])))]+=1
    assert set(edges.values())=={2},'Open collider'
for a,c,y in (('AdapterLargeCollar','AdapterTaper',-.72),('AdapterTaper','AdapterSmallCollar',.72)):
    rings=[{key(v) for v in solids[n]['vertices'] if abs(v[1]-y)<1e-6} for n in (a,c)]
    assert rings[0]==rings[1],'Gap between collision sections'
# Every shared cap vertex must survive export at both radial scales. This
# includes inward reveal walls, overlapping blanket edge and stepped center.
for mat,m in face_mesh().items():
    if not m.vertices:continue
    exported=visual['rwm_'+mat];actual={key(v) for v in exported['vertices']};points=np.array(exported['vertices'])
    for sign,scale in ((1,1),(-1,1.5)):
        for x,y,z in m.vertices:
            target=(x*scale,sign*(b.HALF+y-2),sign*z*scale)
            assert key(target) in actual or np.min(np.max(np.abs(points-target),axis=1))<2e-7,('Cap geometry missing',mat,sign)
for tex in model.textures:assert (b.MODELS/(tex['name']+'.png')).exists()
cfg=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_ADP_250_375.cfg').read_text()
assert not re.search(r'\b(MODULE|INTERNAL|RESOURCE)\s*\{',cfg)
for field in ('CrewCapacity = 0','mass = 1.1','category = Structural','bulkheadProfiles = size2, size3','attachRules = 1,0,1,1,0','node_stack_top = 0, 0.9, 0, 0, 1, 0, 2','node_stack_bottom = 0, -0.9, 0, 0, -1, 0, 3'):
    assert field in cfg,field
golden=json.loads((ROOT/'Tools/adapter_baseline.json').read_text())
for path,digest in golden.items():check_preserved(ROOT,path,digest)
print('PASS ADP: 16356 outward visual triangles; readable UVs; both scaled closed shared caps retained; all textures present')
print('PASS ADP: three watertight convex solids follow taper with coincident joint rings; size-2/3 stack nodes at +/-0.9m')
print('PASS ADP: passive crewless structure; prior eight modules preserved except authorized EC balance; in-game fit/appearance pending')
