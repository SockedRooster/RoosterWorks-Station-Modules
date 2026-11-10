"""Reproducible additive art pass over the dev.11 archive. No gameplay edits.

Run with Python + numpy + Pillow, passing --archive ORIGINAL_SOURCE.zip.
"""
from pathlib import Path
import sys, math, json, zipfile, argparse, hashlib, copy
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'.build-deps'),str(R/'Source'),str(R/'Tools')]
import numpy as np
from PIL import Image, ImageDraw
from native_model import load,walk
from native_derivatives import write
import build_hab250 as h
from appearance_textures import font
M=R/'GameData/RoosterWorksStationModules/Models'
B=R/'Source/VisualBaseline'; B.mkdir(exist_ok=True)

def solid_pad(mesh,t,y,r,hw,hh,depth):
    outline=[(-hw*.65,-hh),(hw*.65,-hh),(hw,-hh*.8),(hw,hh*.8),(hw*.65,hh),(-hw*.65,hh),(-hw,hh*.8),(-hw,-hh*.8)]
    def p(u,v,d):return h.point(r+d,t+u/r,y+v)
    bottom=[p(u,v,0) for u,v in outline]
    shoulder=[p(u,v,depth*.65) for u,v in outline]
    top=[p(u*.82,v*.93,depth) for u,v in outline]
    def face(points):
        normal=np.cross(np.array(points[1])-points[0],np.array(points[2])-points[0]);normal/=np.linalg.norm(normal)
        if len(points)==3:mesh.triangle(points,(tuple(normal),)*3,((.5,.5),(0,0),(1,1)))
        else:mesh.quad(points,(tuple(normal),)*4)
    center=p(0,0,depth);base=p(0,0,0)
    for j in range(8):
        k=(j+1)%8
        face((center,top[j],top[k]));face((base,bottom[k],bottom[j]))
        face((bottom[j],bottom[k],shoulder[k],shoulder[j]))
        face((shoulder[j],shoulder[k],top[k],top[j]))

def latch(meshes,t,y,r):
    # Three stepped hull-conforming layers, seated on the existing panel edge.
    for mat,hw,hh,depth in [('graphite',.012,.037,.003),('steel',.009,.030,.008),('bronze',.004,.019,.012)]:
        solid_pad(meshes[mat],t,y,r,hw,hh,depth)
    for dy in (-.024,.024):
        h.radial_fastener(meshes['steel'],t,y+dy,radius=r+.009,head=.0035)

def socket(meshes,t,y,r):
    # Closed chamfered collar on the pre-existing quick-disconnect cap.
    tangent=(math.cos(t),0,-math.sin(t));normal=(math.sin(t),0,math.cos(t))
    def p(a,rad,depth):
        c=h.point(r+depth,t,y)
        return tuple(c[k]+rad*math.cos(a)*tangent[k]+(rad*math.sin(a) if k==1 else 0) for k in range(3))
    for k in range(24):
        a=math.tau*k/24;b=math.tau*(k+1)/24
        for mat,ri,ro,di,do in [('steel',.021,.029,.029,.023),('bronze',.017,.021,.029,.029)]:
            pts=(p(a,ri,di),p(a,ro,do),p(b,ro,do),p(b,ri,di))
            meshes[mat].quad(pts,(normal,)*4)
    # Protective bridge through the black center, leaving a visible recess.
    h.tube(meshes['steel'],p(0,.013,.030),p(math.pi,.013,.030),r=.0025,sides=6)

def hardware(role):
    m={name:h.Mesh() for name in ('steel','bronze','graphite')}
    panels=[];sockets=[]
    if role=='HAB':
        for t in (.10,math.pi-.64,math.pi+.64):
            for y in (-1.30,1.26):
                a=3.40 if t>math.pi and y>0 else t
                panels.append((a,y,.26,.30,1.235));sockets.append((a+.21,y,1.235))
    elif role=='LAB':
        for t in (.72*math.pi,1.28*math.pi):panels.append((t,1.30,.27,.36,1.235))
        for t in (math.pi-.26,math.pi+.26):
            for y in (-.34,.02):sockets.append((t,y,1.235))
    elif role=='CMD':
        for t in (-1.32,1.32):panels.append((t,-.36,.28,.32,1.243));sockets.append((t,.52,1.235))
    elif role=='CUP':
        for t in (-1.72,1.72):panels.append((t,-.555,.31,.30,1.237));sockets.append((t+.23,-.535,1.235))
    elif role=='LOG':
        for bank in range(4):
            t=math.tau*(bank+.5)/4+.235
            for y in (-.65,.65):panels.append((t,y,.26,.35,1.246));sockets.append((t,y-.27,1.239))
    for t,y,w,ht,r in panels:
        for sign in (-1,1):latch(m,t+sign*w*.47/r,y,r-.001)
    for t,y,r in sockets:socket(m,t,y,r)
    return m

def texture(name,original):
    im=original.convert('RGB');a=np.asarray(im).astype(float);n,w=a.shape[:2]
    yy,xx=np.mgrid[:n,:w];u=xx/w;v=yy/n
    rng=np.random.default_rng(1948+sum(map(ord,name)))
    if 'cladding' in name:
        # Pressed panel dish, shallow edge grime and subtle ceramic grain.
        edge=np.minimum.reduce([u,1-u,v,1-v])
        relief=-10*np.exp(-edge*55)+3*np.exp(-((edge-.045)/.016)**2)
        relief+=1.1*np.sin(u*math.tau)*np.sin(v*math.tau)+rng.normal(0,.5,(n,w))
        a+=relief[:,:,None]
    elif 'hubblanket' in name:
        fu=(u*8)%1;fv=(v*8)%1
        folds=7*np.sin(fu*math.pi)*np.sin(fv*math.pi)-8*np.exp(-np.minimum.reduce([fu,1-fu,fv,1-fv])*35)
        folds+=2*np.sin((u+v)*110)*np.sin(fu*math.pi)*np.sin(fv*math.pi)
        a+=folds[:,:,None]
    elif any(s in name for s in ('steel','bronze','rail')):
        a+=(rng.normal(0,1.1,(n,1))+rng.normal(0,.45,(n,w)))[:,:,None]
    else:
        a+=(rng.normal(0,.55,(n,w))+.7*np.sin(u*math.tau)*np.cos(v*math.tau))[:,:,None]
    out=Image.fromarray(np.uint8(np.clip(a,0,255)))
    if 'cladding' in name:
        d=ImageDraw.Draw(out);s=w/1024
        def line(points,color,width=1):d.line([(int(x*s),int(y*s)) for x,y in points],fill=color,width=max(1,int(width*s)))
        # Paired edge witness ticks and laser-etched lot marks, away from label islands.
        for x in (117,873):
            for y in (290,734):
                line([(x,y),(x+24,y)],(114,129,128),2)
                line([(x+12,y-8),(x+12,y+8)],(160,171,163),1)
        d.text((int(165*s),int(896*s)),'RW / SHIELD   •   LOT 07-12',font=font(max(8,int(17*s))),fill=(116,131,127))
    if original.mode=='RGBA':out.putalpha(original.getchannel('A'))
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',required=True);args=p.parse_args()
    report={'models':[],'textures':[],'protected_files_verified':0}
    with zipfile.ZipFile(args.archive) as z:
        prefix='GameData/RoosterWorksStationModules/Models/'
        for role in ('HAB','LAB','CMD','CUP','LOG'):
            for size in (250,375,500):
                name=f'RW_{role}_{size}.mu';(B/name).write_bytes(z.read(prefix+name))
                model=load(B/name);before=copy.deepcopy(model.root);meshes=hardware(role)
                count=0
                for mat,mesh in meshes.items():
                    idx=next(i for i,m in enumerate(model.materials) if model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_'+mat)
                    scale=size/250
                    node=dict(name='RW_Visual12_'+mat,position=(0,0,0),rotation=(0,0,0,1),scale=(1,1,1),children=[],shadows=(1,1),materials=[idx],mesh=dict(vertices=[tuple(x*scale for x in v) for v in mesh.vertices],normals=mesh.normals,uvs=mesh.uvs,submeshes=[mesh.triangles]))
                    model.root['children'].append(node);count+=len(mesh.triangles)
                write(model,M/name)
                check=load(M/name);old=copy.deepcopy(check.root);old['children']=[n for n in old['children'] if not n['name'].startswith('RW_Visual12_')]
                assert old==before, name+' altered original geometry or transforms'
                for _,node in walk(check.root):
                    if 'mesh' not in node:continue
                    mesh=node['mesh'];assert np.isfinite(mesh['vertices']).all()
                    assert all(0<=i<len(mesh['vertices']) for sub in mesh['submeshes'] for tri in sub for i in tri)
                report['models'].append(dict(file=name,added_triangles=count,original_nodes_unchanged=True))
        names=['cladding','cladding_white','cladding_grey','cladding_white_grey','ceramic','ceramic_grey','white','white_grey','steel','bronze','rail','graphite','hubblanket']
        for name in names:
            filename='rwm_'+name+'.png';data=z.read(prefix+filename);(B/filename).write_bytes(data)
            with Image.open(B/filename) as original:texture(name,original).save(M/filename,optimize=True)
            report['textures'].append(filename)
        changed={prefix+x['file'] for x in report['models']}|{prefix+x for x in report['textures']}
        for entry in z.namelist():
            if not entry.startswith('GameData/') or entry.endswith('/') or entry in changed:continue
            assert (R/entry).read_bytes()==z.read(entry),entry
            report['protected_files_verified']+=1
    (R/'Reports/VISUAL_UPGRADE.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
