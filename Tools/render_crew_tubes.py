from PIL import Image,ImageDraw
from render_appearance import render,font,OUT
import numpy as np,math
from native_model import load,walk
from render_appearance import MODELS
sheet=Image.new('RGB',(1600,740),(12,20,27));draw=ImageDraw.Draw(sheet)
draw.text((25,20),'ROOSTERWORKS / CREW TUBES + 90 DEGREE ELBOWS',font=font(30,True),fill=(235,232,220))
draw.text((25,62),'Shipped native models and textures / CPU preview / KSP confirmation pending',font=font(18),fill=(159,179,188))
for j,(role,size,finish) in enumerate((('TUB',250,'White'),('TUB',375,'Grey metal'),('ELB',250,'White'),('ELB',375,'Grey metal'))):
    model=load(MODELS/f'RW_{role}_{size}.mu')
    vertices=np.array([v for _,n in walk(model.root) if 'mesh' in n for v in n['mesh']['vertices']])
    view=np.array((math.sin(.70),.48,math.cos(.70)));view/=np.linalg.norm(view)
    right=-np.cross((0,1,0),view);right/=np.linalg.norm(right);up=np.cross(right,view)
    px=vertices@right;py=vertices@up
    focus=(px.min()+px.max())/2*right+(py.min()+py.max())/2*up
    span=max(py.max()-py.min(),(px.max()-px.min())*550/400)*1.12
    image=render(role,theta=.70,elevation=.48,span=span,diameter=size,size=(400,550),finish=finish,focus=focus)
    sheet.paste(image,(j*400,145));draw.text((j*400+20,112),f'RW-{role}-{size} / '+finish,font=font(20,True),fill=(230,229,211))
    print('Rendered',role,size,flush=True)
sheet.save(OUT/'Crew-Tubes-and-Elbows-v0.16.0-dev.2.png')
