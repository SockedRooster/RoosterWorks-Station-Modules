"""Render exported native MU geometry and shipped textures with a CPU z-buffer.

Deterministic orthographic inspection views; studio lighting, no invented
geometry, no specular effects absent from the preserved KSP/Diffuse shader.
"""
from pathlib import Path
import sys,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
OUT=ROOT/'Media'

def font(sz,bold=False):
    sys.path.insert(0,str(ROOT/'Source'))
    from appearance_textures import font as resolve
    return resolve(sz,bold)

def render(label,theta=.60,elevation=.42,span=4.7,variant='Standard',focus=(0,0,0),size=(760,840),emissive=0,diameter=250,dark=False,point_lights=False,finish='White'):
    model=load(MODELS/f'RW_{label}_{diameter}.mu')
    width,height=size
    rgb=np.zeros((height,width,3),dtype=np.uint8)
    gradient=np.linspace(1,0,height)[:,None,None]
    rgb[:]=np.array((14,23,30))+gradient*np.array((17,19,19))
    depth=np.full((height,width),-np.inf)
    view=np.array((math.sin(theta),elevation,math.cos(theta)));view/=np.linalg.norm(view)
    # Unity camera: outward viewing puts -local tangent on screen right.
    right=-np.cross((0,1,0),view);right/=np.linalg.norm(right);up=np.cross(right,view)
    focus=np.array(focus);scale=height/span
    light=np.array((.45,.8,.65));light/=np.linalg.norm(light)
    fill=np.array((-.7,.2,-.3));fill/=np.linalg.norm(fill)
    textures={}
    lights=[n for _,n in walk(model.root) if 'light' in n] if point_lights else []
    opaque=[];transparent=[]
    for path,node in walk(model.root):
        if 'mesh' not in node or 'materials' not in node:continue
        if label=='HAB':
            if variant=='Standard' and '/SideHatch/' in path:continue
            if variant=='SideHatch' and '/WindowBankStandard/' in path:continue
        assert node['position']==(0.,0.,0.) and node['rotation']==(0.,0.,0.,1.) and node['scale']==(1.,1.,1.)
        mesh=node['mesh'];verts=np.asarray(mesh['vertices']);normals=np.asarray(mesh['normals']);uvs=np.asarray(mesh['uvs'])
        rel=verts-focus
        p_all=np.column_stack((width/2+rel@right*scale,height/2-rel@up*scale,rel@view))
        for sub,mat_id in zip(mesh['submeshes'],node['materials']):
            mat=model.materials[mat_id];tex_name=model.textures[mat['properties']['_MainTex']['index']]['name']
            if finish=='Grey metal' and tex_name in ('rwm_ceramic','rwm_white','rwm_cladding','rwm_cladding_white'):tex_name+='_grey'
            if tex_name not in textures:textures[tex_name]=np.asarray(Image.open(MODELS/(tex_name+'.png')).convert('RGBA'))
            texture=textures[tex_name]
            tris=np.asarray(sub);xyz=verts[tris]
            visible=np.einsum('ij,j->i',np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),view)>1e-10
            if mat['shader']=='KSP/Alpha/Translucent':
                for indices in tris[visible]:
                    transparent.append((float(p_all[indices,2].mean()),p_all,verts,normals,uvs,texture,indices,mat))
            else:
                for indices in tris[visible]:opaque.append((0,p_all,verts,normals,uvs,texture,indices,mat))
    for _,p_all,verts,normals,uvs,texture,indices,mat in opaque+sorted(transparent,key=lambda item:item[0]):
                is_transparent=mat['shader']=='KSP/Alpha/Translucent'
                p=p_all[indices]
                x0=max(0,int(np.floor(p[:,0].min())));x1=min(width-1,int(np.ceil(p[:,0].max())))
                y0=max(0,int(np.floor(p[:,1].min())));y1=min(height-1,int(np.ceil(p[:,1].max())))
                if x1<x0 or y1<y0:continue
                yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
                den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
                if abs(den)<1e-9:continue
                a=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
                b=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den;c=1-a-b
                z=a*p[0,2]+b*p[1,2]+c*p[2,2]
                mask=(a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)&(z>depth[y0:y1+1,x0:x1+1])
                if not mask.any():continue
                weights=np.stack((a[mask],b[mask],c[mask]),axis=1)
                uv=weights@uvs[indices];normal=weights@normals[indices]
                normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-8)
                shade=np.full(len(normal),.10) if dark else .40+.49*np.clip(normal@light,0,1)+.11*np.clip(normal@fill,0,1)
                u=np.clip(uv[:,0],0,1)*(texture.shape[1]-1);v=(1-np.clip(uv[:,1],0,1))*(texture.shape[0]-1)
                # Bilinear filtering makes stencil edges and insulation seams readable.
                iu=u.astype(int);iv=v.astype(int);nu=np.minimum(iu+1,texture.shape[1]-1);nv=np.minimum(iv+1,texture.shape[0]-1)
                fu=(u-iu)[:,None];fv=(v-iv)[:,None]
                pixels=(texture[iv,iu]*(1-fu)+texture[iv,nu]*fu)*(1-fv)+(texture[nv,iu]*(1-fu)+texture[nv,nu]*fu)*fv
                color=pixels[:,:3]*shade[:,None]
                for lamp in lights:
                    position=weights@verts[indices];delta=np.array(lamp['position'])-position
                    distance=np.linalg.norm(delta,axis=1);direction=delta/np.maximum(distance[:,None],1e-8)
                    strength=np.maximum(1-distance/lamp['light']['range'],0)**2*lamp['light']['intensity']*2
                    strength*=np.maximum(np.sum(normal*direction,axis=1),0)
                    color+=pixels[:,:3]*strength[:,None]*np.array(lamp['light']['color'][:3])
                value=emissive.get(model.textures[mat['properties']['_MainTex']['index']]['name'],0) if isinstance(emissive,dict) else emissive
                if value and mat['shader']=='KSP/Emissive/Diffuse':
                    color=np.maximum(color,pixels[:,:3]*value)
                if is_transparent:
                    alpha=pixels[:,3:4]/255
                    color=color*alpha+rgb[y0:y1+1,x0:x1+1][mask]*(1-alpha)
                rgb[y0:y1+1,x0:x1+1][mask]=np.clip(color,0,255).astype('uint8')
                if not is_transparent:depth[y0:y1+1,x0:x1+1][mask]=z[mask]
    return Image.fromarray(rgb)

def main():
    OUT.mkdir(exist_ok=True)
    roles={'HAB':'LIFE SUPPORT / HABITAT','LAB':'RESEARCH / THERMAL HARDWARE','CMD':'AVIONICS / STATION COMMAND',
           'HUB':'SIX-WAY PRESSURE JUNCTION','CUP':'OBSERVATION / OPTICAL SYSTEMS','LOG':'CARGO / SUPPLY STORAGE'}
    overview=Image.new('RGB',(1800,1470),(12,20,27));draw=ImageDraw.Draw(overview)
    draw.text((32,18),'ROOSTERWORKS  /  EXTERIOR DETAIL PASS',font=font(38,True),fill=(235,234,220))
    draw.text((34,70),'v0.7.0-dev.4 • Native model geometry + shipped textures • KSP in-game review pending',font=font(21),fill=(156,178,185))
    for j,(label,role) in enumerate(roles.items()):
        span={'HAB':4.8,'LAB':4.8,'CMD':3.5,'HUB':5.8,'CUP':3.15,'LOG':4.1}[label]
        theta={'HAB':.82,'LAB':.6,'CMD':.55,'HUB':.70,'CUP':.55,'LOG':.65}[label]
        views=[('SIDE HATCH' if label=='HAB' else 'EXTERIOR',theta,.38,'SideHatch' if label=='HAB' else 'Standard'),('SERVICE SIDE',theta+math.pi,.33,'Standard'),('UPPER DETAIL',theta,.90,'Standard')]
        sheet=Image.new('RGB',(2280,940),(12,20,27));d=ImageDraw.Draw(sheet)
        d.text((26,16),f'RW-{label}-250  /  {role}',font=font(32,True),fill=(235,234,220))
        for k,(title,t,e,variant) in enumerate(views):
            photo=render(label,t,e,span,variant,size=(1520,1680)).resize((760,840),Image.Resampling.LANCZOS)
            sheet.paste(photo,(760*k,82))
            d.text((760*k+24,60),title,font=font(18),fill=(169,187,188))
            if k==0:
                x=(j%3)*600;y=115+(j//3)*660
                overview.paste(photo.resize((570,630),Image.Resampling.LANCZOS),(x+15,y+26))
                draw.text((x+32,y+5),f'RW-{label}-250',font=font(24,True),fill=(236,230,211))
        path=OUT/f'RW-{label}-250-v0.7.0-dev.4-Review.png';sheet.save(path);print(path,flush=True)
    overview.save(OUT/'RoosterWorks-v0.7.0-dev.4-Family.png')
    detail_sheet=Image.new('RGB',(1800,1410),(12,20,27));dd=ImageDraw.Draw(detail_sheet)
    dd.text((28,18),'ROOSTERWORKS  /  HARDWARE + SURFACE DETAIL',font=font(32,True),fill=(235,234,220))
    details=[('HAB',.10,1.26,'LIFE SUPPORT / CLADDING',.80),('LAB',math.pi,-.17,'RESEARCH MANIFOLD',.90),
             ('LOG',0,.655,'CARGO CASSETTE / ID PLATE',1.12),('CUP',1.72,-.555,'OBSERVATION SYSTEMS',.76)]
    for j,(label,t,y,title,span) in enumerate(details):
        focus=(1.235*math.sin(t),y,1.235*math.cos(t))
        photo=render(label,t,.08,span,focus=focus,size=(1800,1200)).resize((900,600),Image.Resampling.LANCZOS)
        x=(j%2)*900;yy=90+(j//2)*650
        detail_sheet.paste(photo,(x,yy+25));dd.text((x+28,yy),title,font=font(22,True),fill=(231,226,208))
    detail_sheet.save(OUT/'RoosterWorks-v0.7.0-dev.4-Details.png')
    print('Family preview saved',flush=True)

if __name__=='__main__':main()
