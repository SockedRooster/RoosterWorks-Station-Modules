"""Native greenhouse geometry, glazing aperture, light/controller, prior assets."""
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Source'))
from electric_charge_balance import check_preserved
from collections import Counter
import math,json,hashlib,sys,re
import numpy as np
from PIL import Image
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_grn250 as b
def sub(a,c):return tuple(x-y for x,y in zip(a,c))
def dot(a,c):return sum(x*y for x,y in zip(a,c))
def cross(a,c):return (a[1]*c[2]-a[2]*c[1],a[2]*c[0]-a[0]*c[2],a[0]*c[1]-a[1]*c[0])
def key(p):return tuple(round(x,6) for x in p)
model=load(b.MODELS/(b.PART+'.mu'));solids=[];visual={};count=0;lamp_nodes=[]
for _,node in walk(model.root):
    assert node['tag']=='Untagged' and node['layer']==0
    if 'collider' in node:
        c=node['collider'];assert c['trigger']==0 and c['convex']==1
        solids.append(c['mesh'])
    if 'mesh' not in node:continue
    m=node['mesh'];count+=sum(len(t) for t in m['submeshes'])
    assert len(m['vertices'])<65535 and len(m['vertices'])==len(m['normals'])==len(m['uvs'])
    assert all(math.isfinite(x) for p in m['vertices']+m['normals']+m['uvs'] for x in p)
    assert all(abs(p[1])<=1.800001 and math.hypot(p[0],p[2])<1.30 for p in m['vertices'])
    for tris,mid in zip(m['submeshes'],node['materials']):
        mat=model.materials[mid];tex=model.textures[mat['properties']['_MainTex']['index']]['name'];visual[tex]=m
        expected='KSP/Alpha/Translucent' if tex=='rwm_grnglass' else 'KSP/Emissive/Diffuse' if tex in ('rwm_grnlamp','rwm_grninspection') else 'KSP/Diffuse'
        assert mat['shader']==expected
        if tex=='rwm_grnlamp':
            lamp_nodes.append(node['name']);assert '_Emissive' in mat['properties'] and '_EmissiveColor' in mat['properties']
        for a,c,d in tris:
            p,q,r=[m['vertices'][i] for i in (a,c,d)]
            assert dot(cross(sub(q,p),sub(r,p)),m['normals'][a])>1e-15,('Face/normal mismatch',tex)
            if tex=='rwm_crest' or 'label' in tex or 'cladding' in tex or tex=='rwm_detail':
                u1,v1=sub(m['uvs'][c],m['uvs'][a]);u2,v2=sub(m['uvs'][d],m['uvs'][a])
                assert u1*v2-u2*v1<0,('Mirrored UV',tex)
assert count==40764 and len(solids)==1 and lamp_nodes==['RW_GreenhouseLamps']
lights=[n for _,n in walk(model.root) if 'light' in n]
assert len(lights)==4 and all(n['name']=='RW_GreenhouseInspectionLight' for n in lights)
assert all(n['light']['type']==2 and n['light']['intensity']>0 and n['light']['range']>2 for n in lights)
assert np.allclose([n['position'][1] for n in lights],np.array(b.TIERS)+.25)
mesh=solids[0];vs=mesh['vertices'];edges=Counter();assert len(mesh['submeshes'][0])==96
for tri in mesh['submeshes'][0]:
    p,q,r=[vs[i] for i in tri];n=cross(sub(q,p),sub(r,p));assert dot(n,p)>0
    assert max(dot(n,sub(v,p)) for v in vs)<1e-6
    ks=[key(v) for v in (p,q,r)]
    for i in range(3):edges[tuple(sorted((ks[i],ks[(i+1)%3])))]+=1
assert set(edges.values())=={2}
assert abs(min(v[1] for v in vs)+1.8)<1e-6 and abs(max(v[1] for v in vs)-1.8)<1e-6
glass=visual['rwm_grnglass'];assert sum(len(t) for t in glass['submeshes'])==512
alpha=Image.open(b.MODELS/'rwm_grnglass.png');assert alpha.mode=='RGBA' and alpha.getextrema()[3]==(36,36)
for p,n in zip(glass['vertices'],glass['normals']):
    assert abs(p[1])<=1.215001 and abs(n[1])<1e-6
    radius=math.hypot(p[0],p[2]);assert min(abs(radius-r) for r in (1.197,1.198))<1e-6
assert b.FRAME_HALF>b.GLASS_EDGE
# Check pane center rays at several heights for opaque geometry covering glass.
# Test triangles at pressure-wall radius; the narrow brace ring is deliberately
# excluded. Interior plants/racks and neighboring frame legs are allowed.
for bay in range(8):
    center=math.tau*(bay+.5)/8
    for tex,m in visual.items():
        if tex=='rwm_grnglass':continue
        for tris in m['submeshes']:
            for tri in tris:
                ps=[m['vertices'][i] for i in tri]
                if not all(math.hypot(p[0],p[2])>1.17 and abs(p[1])<1.18 for p in ps):continue
                if all(abs(p[1])<.14 for p in ps):continue
                angles=[math.atan2(p[0],p[2]) for p in ps]
                diff=[math.atan2(math.sin(a-center),math.cos(a-center)) for a in angles]
                assert not (max(diff)-min(diff)<math.pi and min(diff)<-.02 and max(diff)>.02),'Opaque wall behind pane'
for tex in ('rwm_grnleaf','rwm_grnleaflight','rwm_grnroot'):
    assert all(math.hypot(p[0],p[2])<1.11 and abs(p[1])<1.24 for p in visual[tex]['vertices'])
# A representative closed leaf has positive signed volume and every edge shared.
leaf=b.h.Mesh();b.leaf(leaf,(0,0,0),.4,.12,.055,.08)
volume=sum(dot(leaf.vertices[a],cross(leaf.vertices[c],leaf.vertices[d]))/6 for a,c,d in leaf.triangles)
assert volume>0,'Leaf winding points inward'
for tex in model.textures:assert (b.MODELS/(tex['name']+'.png')).exists()
cfg=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_GRN_250.cfg').read_text()
for field in ('CrewCapacity = 0','mass = 2.75','maxAmount = 0','includedRenderer = RW_GreenhouseLamps','node_stack_top = 0, 1.8, 0, 0, 1, 0, 2','node_stack_bottom = 0, -1.8, 0, 0, -1, 0, 2'):
    assert field in cfg,field
for field in ('name = ModuleLight','lightName = RW_GreenhouseInspectionLight','lightMeshRendererName = RW_GreenhouseInspectionLamps','isOn = true','useResources = false'):assert field in cfg
assert not re.search(r'\b(INTERNAL)\s*\{',cfg) and 'name = ModuleCommand' not in cfg
patch=(ROOT/'GameData/RoosterWorksStationModules/Compatibility/GreenhouseKerbalism.cfg').read_text()
assert '#@PART[kerbalism-greenhouse]/MODULE[Greenhouse] {}' in patch
assert ':HAS[@MODULE[Greenhouse]]:NEEDS[Kerbalism,ProfileDefault]' in patch
for field in ('@crop_size *= 0.5','@ec_rate *= 0.5','@INPUT_RESOURCE,*','@OUTPUT_RESOURCE,*','%lamps = RW_GreenhouseLamps','%shutters =','%plants =','!MODULE[ModuleColorChanger] {}','name = ProcessController','resource = _PressureControl',':NEEDS[Kerbalism,FeatureHabitat]'):
    assert field in patch,field
assert '@crop_rate' not in patch and patch.count('@rate *= 0.5')==2
assert patch.index('#@PART')<patch.index(':HAS[@MODULE[Greenhouse]]')<patch.index('!MODULE[ModuleColorChanger]')
# Generic ConfigNode brace structure and exactly one resource per new part patch.
for text in (cfg,patch):
    text=re.sub(r'//[^\n]*','',text);depth=0
    for char in text:
        depth+=(char=='{')-(char=='}');assert depth>=0
    assert depth==0
for name in ('Food','Water','Ammonia','CarbonDioxide','Nitrogen','Oxygen'):
    assert len(re.findall(r'RESOURCE\s*\{\s*name = '+name+r'\s',patch))==1,name
golden=json.loads((ROOT/'Tools/greenhouse_baseline.json').read_text())
for path,digest in golden.items():check_preserved(ROOT,path,digest)
print('PASS GRN: 40764 consistent visual triangles; readable UVs; 8 unobstructed low-alpha glass bays, contained crops and one closed convex solid')
print('PASS GRN: four native warm-white point lights and separate inspection renderer/stock switch; crop controller remains independent')
print('PASS GRN: one emissive lamp renderer; Default template copy/half-rate patch, controller separation, pressure support, guarded resources and stock fallback')
print('PASS GRN: prior nine GameData preserved except authorized EC balance; actual MM application, production, alpha sorting and flight tests pending')
