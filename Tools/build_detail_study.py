"""Second art study: tactile blankets, tangent-space normals and structural depth.

Input is the immutable Visual Development 01 Install.zip, not an installed game.
Uses stock KSP/Bumped Specular; DXT5nm stores X in alpha and Y in green.
"""
from pathlib import Path
import sys,math,json,zipfile,argparse,copy,io,struct
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'.build-deps'),str(R/'Source'),str(R/'Tools')]
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from native_model import load,walk
from native_derivatives import write
from appearance_textures import font
import build_hab250 as h
M=R/'GameData/RoosterWorksStationModules/Models'
ART=R/'Source/Textures/DetailStudy';ART.mkdir(parents=True,exist_ok=True)
BASE=R/'Source/Study02Baseline';BASE.mkdir(exist_ok=True)

def noise(n,seed):
    rng=np.random.default_rng(seed);out=np.zeros((n,n))
    for grid,weight in ((10,1),(23,.48),(49,.23),(113,.08)):
        a=rng.integers(0,256,(grid,grid),dtype=np.uint8)
        im=Image.fromarray(a).resize((n,n),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(n/grid*.08))
        out+=(np.asarray(im,dtype=float)/255-.5)*weight
    return out

def save_normal_dds(rgb,path):
    # Full normalized mip chain avoids sparkling textile detail at VAB distances.
    # DDS uses the vertically inverted storage convention relative to KSP PNGs.
    image=Image.fromarray(rgb[::-1].copy());blocks=[];header=None
    while True:
        xyz=np.asarray(image,dtype=float)/127.5-1
        xyz/=np.maximum(np.linalg.norm(xyz,axis=-1,keepdims=True),1e-9)
        packed=np.full((*xyz.shape[:2],4),255,dtype=np.uint8)
        packed[:,:,1]=np.uint8(np.clip(xyz[:,:,1]*.5+.5,0,1)*255)
        packed[:,:,3]=np.uint8(np.clip(xyz[:,:,0]*.5+.5,0,1)*255)
        buf=io.BytesIO();Image.fromarray(packed).save(buf,format='DDS',pixel_format='DXT5');data=buf.getvalue()
        if header is None:header=bytearray(data[:128])
        blocks.append(data[128:])
        if image.width==1:break
        image=image.resize((max(1,image.width//2),max(1,image.height//2)),Image.Resampling.BOX)
    struct.pack_into('<I',header,8,struct.unpack_from('<I',header,8)[0]|0x20000)
    struct.pack_into('<I',header,28,len(blocks));struct.pack_into('<I',header,108,0x401008)
    path.write_bytes(header+b''.join(blocks))

def maps():
    n=1024;y,x=np.mgrid[:n,:n]/n
    grain=noise(n,811);fine=noise(n,519)
    edge=np.minimum.reduce([x,1-x,y,1-y])
    # Warped crumple ridges; wavelengths in centimetres, never checkerboard grain.
    wrinkle=.30*grain+.055*np.sin(x*180+grain*17)*np.sin(y*124+fine*13)
    rim=np.exp(-((edge-.037)/.005)**2)
    seam=np.exp(-((edge-.053)/.0028)**2)
    height=wrinkle*(1-np.exp(-edge*70))+.09*rim-.055*seam
    # Thin double sewn hem with intermittent stitch depressions.
    stitch=np.exp(-((edge-.046)/.0022)**2)*(np.sin((x+y)*math.tau*92)>.25)
    height-=stitch*.032
    for kind in ('quilt','foil'):
        ht=height if kind=='quilt' else .7*grain+.05*np.sin(x*40+grain*24)*np.sin(y*27+fine*18)
        # Image rows run downward; tangent V runs upward.
        strength=34 if kind=='quilt' else 22
        dy,dx=np.gradient(ht);normal=np.stack((-dx*strength,dy*strength,np.ones_like(dx)),axis=-1)
        normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
        rgb=np.uint8(np.clip(normal*.5+.5,0,1)*255)
        Image.fromarray(rgb).save(ART/f'rwm_{kind}_normal_rgb.png')
        # DXT5nm bypasses PNG loader conversion and is directly sampled by UnpackNormal.
        save_normal_dds(rgb,M/f'rwm_{kind}_NRM.dds')
        Image.fromarray(np.uint8(np.clip(ht+.5,0,1)*255)).save(ART/f'{kind}_height.png')
    for name,base in [('cladding',(204,207,199)),('cladding_white',(223,225,216)),('cladding_grey',(118,130,136)),('cladding_white_grey',(139,148,151))]:
        shade=grain*12-rim*7+seam*5+wrinkle*9
        a=np.uint8(np.clip(np.array(base)[None,None,:]+shade[:,:,None],0,255))
        im=Image.fromarray(a);d=ImageDraw.Draw(im)
        # Sparse inspection printing on stitched covers, away from high relief.
        d.rounded_rectangle((83,801,385,884),radius=8,fill=tuple(int(v*.92) for v in base),outline=tuple(int(v*.68) for v in base),width=2)
        ink=tuple(int(v*.42) for v in base)
        d.text((98,816),'RW  /  MLI-07',font=font(23,True),fill=ink)
        d.text((98,851),'THERMAL COVER',font=font(14),fill=ink)
        for px in (48,976):
            for py in (48,976):
                d.ellipse((px-9,py-9,px+9,py+9),fill=(109,119,117),outline=(221,224,211),width=2)
                d.line((px-4,py,px+4,py),fill=(49,59,60),width=2)
        spec=np.uint8(np.clip(38+grain*12+rim*22,20,80))
        if 'grey' in name:spec=np.uint8(np.clip(80+grain*20+rim*25,35,120))
        im.putalpha(Image.fromarray(spec));im.save(M/f'rwm_{name}.png',optimize=True)
    foil=np.uint8(np.clip(np.array((169,130,64))[None,None,:]+(grain*39+fine*10)[:,:,None]*np.array((1,.85,.5)),0,255))
    im=Image.fromarray(foil);im.putalpha(Image.fromarray(np.uint8(np.clip(155+grain*45,90,190))));im.save(M/'rwm_hubblanket.png',optimize=True)

def recalc(m,smooth=False):
    p=np.asarray(m['vertices']);old=np.asarray(m['normals']);tris=np.array([t for s in m['submeshes'] for t in s]);sums=np.zeros_like(p)
    cross=np.cross(p[tris[:,1]]-p[tris[:,0]],p[tris[:,2]]-p[tris[:,0]])
    for j in range(3):np.add.at(sums,tris[:,j],cross)
    keys=np.round(p if smooth else np.concatenate((p,old),axis=1),5);_,ids=np.unique(keys,axis=0,return_inverse=True)
    accum=np.zeros((ids.max()+1,3));np.add.at(accum,ids,sums);sums=accum[ids]
    lens=np.linalg.norm(sums,axis=1);good=lens>1e-12;sums[good]/=lens[good,None];sums[~good]=old[~good]
    m['normals']=sums.tolist()

def tangents(m):
    p=np.asarray(m['vertices']);uv=np.asarray(m['uvs']);n=np.asarray(m['normals']);t=np.array([t for s in m['submeshes'] for t in s])
    e1=p[t[:,1]]-p[t[:,0]];e2=p[t[:,2]]-p[t[:,0]];d1=uv[t[:,1]]-uv[t[:,0]];d2=uv[t[:,2]]-uv[t[:,0]]
    det=d1[:,0]*d2[:,1]-d1[:,1]*d2[:,0];inv=np.zeros_like(det);mask=abs(det)>1e-12;inv[mask]=1/det[mask]
    tx=(e1*d2[:,1,None]-e2*d1[:,1,None])*inv[:,None]
    ty=(e2*d1[:,0,None]-e1*d2[:,0,None])*inv[:,None]
    sx=np.zeros_like(p);sy=np.zeros_like(p)
    for j in range(3):np.add.at(sx,t[:,j],tx);np.add.at(sy,t[:,j],ty)
    sx-=n*np.sum(n*sx,axis=1)[:,None];length=np.linalg.norm(sx,axis=1);bad=length<1e-8
    fallback=np.cross(n[bad],np.where((abs(n[bad,0])<.9)[:,None],(1,0,0),(0,1,0)))
    sx[bad]=fallback;length=np.linalg.norm(sx,axis=1);sx/=np.maximum(length[:,None],1e-9)
    hand=np.where(np.sum(np.cross(n,sx)*sy,axis=1)<0,-1.,1.)
    m['tangents']=np.column_stack((sx,hand)).tolist()

def pillow(m,scale):
    # Existing per-rectangle UV islands provide consistent closed hem boundaries.
    assert len(m['vertices'])%4==0
    dest=h.Mesh()
    for i in range(0,len(m['vertices']),4):
        p=np.array(m['vertices'][i:i+4]);uv=np.array(m['uvs'][i:i+4]);norm=np.array(m['normals'][i:i+4])
        steps=max(1,min(7,math.ceil(abs(p[3,1]-p[0,1])/scale/.065)))
        for j in range(steps):
            pts=[];uvs=[];norms=[]
            for u,v in ((0,j/steps),(1,j/steps),(1,(j+1)/steps),(0,(j+1)/steps)):
                pt=(p[0]*(1-u)+p[1]*u)*(1-v)+(p[3]*(1-u)+p[2]*u)*v
                coord=(uv[0]*(1-u)+uv[1]*u)*(1-v)+(uv[3]*(1-u)+uv[2]*u)*v
                no=(norm[0]*(1-u)+norm[1]*u)*(1-v)+(norm[3]*(1-u)+norm[2]*u)*v
                bulge=.008*scale*max(0,math.sin(math.pi*coord[0])*math.sin(math.pi*coord[1]))**.65
                radial=np.array((pt[0],0,pt[2]));radial/=np.linalg.norm(radial)
                pts.append(tuple(pt+radial*bulge));uvs.append(tuple(coord));norms.append(tuple(no))
            dest.quad(pts,norms,uvs)
    out=dict(vertices=dest.vertices,normals=dest.normals,uvs=dest.uvs,submeshes=[dest.triangles]);recalc(out);return out

def windows(m,path,short,scale):
    if 'Glass' in path:return 0
    centres=[(math.tau*(col+1)/12,-1.730+(row+.5)*3.460/8) for row,col in h.BAYS] if not short else [(a,0) for a in (math.pi/3,math.pi,5*math.pi/3)]
    if '/SideHatch/' in path:return 0
    count=0
    for i,(x,y,z) in enumerate(m['vertices']):
        rr=math.hypot(x,z)/scale;theta=math.atan2(x,z)%math.tau
        if not 1.2005<rr<1.208:continue
        fits=any(abs(y/scale-cy)<=.2401 and abs((theta-(ct+off)+math.pi)%math.tau-math.pi)<=.197 for ct,cy in centres for off in (-.421,0,.421))
        if not fits:continue
        # Outer painted rim rises 30mm; inward bevel falls into the preserved glass.
        pairs=[(1.201,.006),(1.202,.015),(1.204,.026),(1.2048,.019),(1.207,.033)]
        depth=min(pairs,key=lambda a:abs(a[0]-rr))[1]
        m['vertices'][i]=(x*(1+depth/rr),y,z*(1+depth/rr));count+=1
    if count:recalc(m)
    return count

def shoulders(scale,half):
    meshes={k:h.Mesh() for k in ('steel','rail','graphite')}
    # Segmented bevelled shoulder jackets and supported circumferential grab rails.
    for sign in (-1,1):
        profile=[(half-.241,1.207),(half-.214,1.235),(half-.105,1.235),(half-.074,1.218)]
        for j in range(12):
            a=math.tau*j/12+.004;b=math.tau*(j+1)/12-.004
            for q in range(3):
                y0,r0=profile[q];y1,r1=profile[q+1]
                for k in range(4):
                    t0=a+(b-a)*k/4;t1=a+(b-a)*(k+1)/4
                    pts=[h.point(r0,t0,sign*y0),h.point(r0,t1,sign*y0),h.point(r1,t1,sign*y1),h.point(r1,t0,sign*y1)]
                    if sign<0:pts.reverse()
                    no=np.cross(np.subtract(pts[1],pts[0]),np.subtract(pts[2],pts[0]));no/=np.linalg.norm(no)
                    meshes['steel'].quad(pts,[tuple(no)]*4)
        # Low-profile U-shaped grabs; all below the mating plane and inside 2.5m envelope.
        for j in range(12):
            t=math.tau*(j+.5)/12;y=sign*(half-.065)
            path=[h.point(1.218,t-.065,y),h.point(1.243,t-.055,y),h.point(1.243,t+.055,y),h.point(1.218,t+.065,y)]
            for p,q in zip(path,path[1:]):h.tube(meshes['rail'],p,q,r=.006,sides=8)
    for mesh in meshes.values():mesh.vertices=[tuple(v*scale for v in p) for p in mesh.vertices]
    return meshes

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);args=ap.parse_args()
    with zipfile.ZipFile(args.baseline) as z:
        for entry in z.namelist():
            if entry.startswith('GameData/') and not entry.endswith('/'):(R/entry).write_bytes(z.read(entry))
    maps();audit=[]
    for path in sorted(M.glob('*.mu')):
        original=path.read_bytes();(BASE/path.name).write_bytes(original)
        model=load(path);scale=int(path.stem.split('_')[-1])/250 if path.stem.split('_')[-1].isdigit() else 1
        habitat=path.stem.startswith(('RW_HAB_','RW_HABS_'));short=path.stem.startswith('RW_HABS_')
        changed_materials=[]
        for i,mat in enumerate(model.materials):
            tex=model.textures[mat['properties']['_MainTex']['index']]['name']
            kind='quilt' if tex in ('rwm_cladding','rwm_cladding_white') else 'foil' if tex=='rwm_hubblanket' else None
            if kind:
                normal='rwm_'+kind+'_NRM';index=next((j for j,t in enumerate(model.textures) if t['name']==normal),None)
                if index is None:index=len(model.textures);model.textures.append(dict(name=normal,type=1))
                mat['shader']='KSP/Bumped Specular';mat['properties'].update(_BumpMap=dict(index=index,scale=(1.,1.),offset=(0.,0.)),_SpecColor=(.28,.28,.28,1.) if kind=='quilt' else (.70,.56,.30,1.),_Shininess=.18 if kind=='quilt' else .30)
                changed_materials.append(i)
        moved=0;inflated=0
        for address,n in walk(model.root):
            if 'mesh' not in n:continue
            tex=model.textures[model.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']
            if tex=='rwm_hubblanket':recalc(n['mesh'],smooth=True)
            if habitat:
                moved+=windows(n['mesh'],address,short,scale)
                tex=model.textures[model.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']
                if tex in ('rwm_cladding','rwm_cladding_white'):
                    n['mesh']=pillow(n['mesh'],scale);inflated+=1
            if any(i in changed_materials for i in n['materials']):tangents(n['mesh'])
        if habitat:
            for key,mesh in shoulders(scale,.990 if short else 1.980).items():
                if not mesh.vertices:continue
                index=next(i for i,m in enumerate(model.materials) if model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_'+key)
                model.root['children'].append(dict(name='RW_Study02_Shoulder_'+key,position=(0,0,0),rotation=(0,0,0,1),scale=(1,1,1),children=[],materials=[index],shadows=(1,1),mesh=dict(vertices=mesh.vertices,normals=mesh.normals,uvs=mesh.uvs,submeshes=[mesh.triangles])))
        if changed_materials or habitat:
            write(model,path);audit.append(dict(model=path.name,normal_mapped_materials=len(changed_materials),window_vertices_shaped=moved,padded_meshes=inflated))
    (R/'Reports/DETAIL_STUDY_02.json').write_text(json.dumps(dict(models=audit,status='Built; validation pending'),indent=2)+'\n')
    print('Built',len(audit),'models with tactile surface shading; 6 habitat models receive structural depth',flush=True)

if __name__=='__main__':main()
