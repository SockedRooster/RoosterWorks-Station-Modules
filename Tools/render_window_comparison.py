"""Software render the real model triangles and textures at an oblique angle."""
from pathlib import Path
import importlib.util,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]

def load(root,name):
    spec=importlib.util.spec_from_file_location(name,root/'Source/build_hab250.py')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module

def render(root,name,variant='Standard',focus_y=.64875,angle_offset=.67,span=1.18,elevation=.27):
    b=load(root,name)
    mesh=b.generate_geometry(variant)
    width,height=1100,590
    rgb=np.full((height,width,3),(20,27,34),dtype=np.uint8)
    depth=np.full((height,width),-np.inf)
    theta=np.pi/3+angle_offset
    view=np.array((np.sin(theta),elevation,np.cos(theta)));view/=np.linalg.norm(view)
    right=np.cross((0,1,0),view);right/=np.linalg.norm(right)
    up=np.cross(view,right)
    focus=np.array(b.point(1.12,np.pi/3,focus_y))
    light=np.array((.65,.6,.75));light/=np.linalg.norm(light)
    scale=height/span
    for material,m in mesh.items():
        if not m.triangles:continue
        verts=np.array(m.vertices);normals=np.array(m.normals);uvs=np.array(m.uvs)
        texture=np.array(Image.open(b.MODELS/f'rwm_{material}.png').convert('RGB'))
        rel=verts-focus
        projected=np.column_stack((width/2+rel@right*scale,height/2-rel@up*scale,rel@view))
        for tri in m.triangles:
            idx=list(tri);xyz=verts[idx];p=projected[idx]
            if np.dot(np.cross(xyz[1]-xyz[0],xyz[2]-xyz[0]),view)<=0:continue
            x0=max(0,int(np.floor(p[:,0].min())));x1=min(width-1,int(np.ceil(p[:,0].max())))
            y0=max(0,int(np.floor(p[:,1].min())));y1=min(height-1,int(np.ceil(p[:,1].max())))
            if x1<x0 or y1<y0:continue
            yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
            den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
            if abs(den)<1e-9:continue
            a=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
            c=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den
            d=1-a-c
            z=a*p[0,2]+c*p[1,2]+d*p[2,2]
            mask=(a>=-1e-6)&(c>=-1e-6)&(d>=-1e-6)&(z>depth[y0:y1+1,x0:x1+1])
            if not mask.any():continue
            weights=np.stack((a[mask],c[mask],d[mask]),axis=1)
            uv=weights@uvs[idx]
            normal=weights@normals[idx];normal/=np.linalg.norm(normal,axis=1)[:,None]
            shade=.44+.56*np.clip(normal@light,0,1)
            u=np.clip((uv[:,0]*(texture.shape[1]-1)).astype(int),0,texture.shape[1]-1)
            v=np.clip(((1-uv[:,1])*(texture.shape[0]-1)).astype(int),0,texture.shape[0]-1)
            pixels=np.clip(texture[v,u]*shade[:,None],0,255).astype(np.uint8)
            rgb[y0:y1+1,x0:x1+1][mask]=pixels
            depth[y0:y1+1,x0:x1+1][mask]=z[mask]
    return Image.fromarray(rgb)

if __name__=='__main__':
    before=render(Path(sys.argv[1]),'hab_before') if len(sys.argv)>1 else None
    after=render(ROOT,'hab_after')
    sheet=Image.new('RGB',(1140,1310 if before else 660),(20,27,34));draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',25)
    panels=[(15,'v0.4.4 — raised frame, overlapping hull panels',before)] if before else []
    panels.append((665 if before else 15,'v0.4.5 — seated trim, hull cutouts, curved glazing',after))
    for y,title,img in panels:
        draw.text((20,y),title,font=font,fill=(237,242,246))
        sheet.paste(img,(20,y+42))
    out=ROOT/'Media/HAB-window-fit-v045.png';sheet.save(out);print(out)
