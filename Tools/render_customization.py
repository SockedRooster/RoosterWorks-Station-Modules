from PIL import Image,ImageDraw
import numpy as np,math
from native_model import load,walk
from render_appearance import render,font,OUT,MODELS
sheet=Image.new('RGB',(1440,1230),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((26,18),'ROOSTERWORKS / 0.65 RING COLORS',font=font(31,True),fill=(233,235,226))
d.text((28,64),'Exact native triangles + shipped color maps / offline preview; live KSP test pending',font=font(17),fill=(163,185,193))
views=[('HAB',250,'White','Original'),('HAB',250,'White','Blue'),('LOG',375,'Grey metal','Red'),('CMD',250,'White','Steel'),('GRN',250,'White','Green'),('CUP',375,'Grey metal','Gold'),('HUB',250,'Grey metal','White'),('ELB',375,'Grey metal','Charcoal')]
for j,(role,size,finish,color) in enumerate(views):
    vertices=np.array([v for _,n in walk(load(MODELS/f'RW_{role}_{size}.mu').root) if 'mesh' in n for v in n['mesh']['vertices']])
    view=np.array((math.sin(.70),.48,math.cos(.70)));view/=np.linalg.norm(view)
    right=-np.cross((0,1,0),view);right/=np.linalg.norm(right);up=np.cross(right,view)
    px=vertices@right;py=vertices@up;focus=(px.min()+px.max())/2*right+(py.min()+py.max())/2*up
    span=max(py.max()-py.min(),(px.max()-px.min())*470/360)*1.14
    image=render(role,theta=.70,elevation=.48,span=span,diameter=size,size=(360,470),finish=finish,focus=focus,ring_color=color)
    x=(j%4)*360;y=116+(j//4)*560;sheet.paste(image,(x,y+34))
    d.text((x+14,y),f'{role}-{size} / {color}',font=font(20,True),fill=(225,228,216))
    d.text((x+14,y+512),finish,font=font(16),fill=(163,185,193))
    print('Rendered',role,size,color,flush=True)
sheet.save(OUT/'RoosterWorks-0.65-Ring-Colors.png')
print('Saved ring color review sheet',flush=True)
