from PIL import Image,ImageDraw
import numpy as np,math
from native_model import load,walk
from render_appearance import render,font,OUT,MODELS
def framed(role,size,color='Original',finish='White',pixels=(360,420),variant='Standard',span=None):
    v=np.array([p for _,n in walk(load(MODELS/f'RW_{role}_{size}.mu').root) if 'mesh' in n for p in n['mesh']['vertices']])
    view=np.array((math.sin(.65),.40,math.cos(.65)));view/=np.linalg.norm(view)
    right=-np.cross((0,1,0),view);right/=np.linalg.norm(right);up=np.cross(right,view)
    px=v@right;py=v@up;focus=(px.min()+px.max())/2*right+(py.min()+py.max())/2*up
    if span is None:span=max(py.max()-py.min(),(px.max()-px.min())*pixels[1]/pixels[0])*1.15
    return render(role,theta=.65,elevation=.40,span=span,diameter=size,size=pixels,focus=focus,finish=finish,ring_color=color,variant=variant)
family=Image.new('RGB',(1440,1500),(12,20,27));d=ImageDraw.Draw(family)
d.text((24,18),'ROOSTERWORKS / 0.7 NATIVE 5 m STATION FAMILY',font=font(30,True),fill=(232,232,218))
d.text((25,60),'Actual exported meshes and textures / offline preview / in-game acceptance pending',font=font(17),fill=(161,180,190))
roles=('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN','TUB','ELB','ADP_375')
for j,role in enumerate(roles):
    x=j%4*360;y=110+j//4*460
    image=framed(role,500,color='Blue' if j%3==1 else 'Original',finish='Grey metal' if j%2 else 'White')
    family.paste(image,(x,y+28));d.text((x+16,y),('ADP-375/500' if role=='ADP_375' else role+'-500'),font=font(21,True),fill=(231,226,208));print('Rendered 5 m',role,flush=True)
family.save(OUT/'RoosterWorks-0.7-5m-Family.png')
short=Image.new('RGB',(1440,1250),(12,20,27));d=ImageDraw.Draw(short)
d.text((25,18),'ROOSTERWORKS / 0.75 COMPACT HABITATS',font=font(31,True),fill=(232,232,218))
d.text((25,62),'Same camera scale in all six views / full HABs above, two-crew compact HABs below',font=font(18),fill=(161,180,190))
for row in (0,1):
    for j,size in enumerate((250,375,500)):
        role='HAB' if row==0 else 'HABS';x=j*480;y=120+row*550
        image=framed(role,size,color='Original' if row==0 else 'Blue',finish='White' if row==0 else 'Grey metal',pixels=(480,480),variant='Standard' if row==0 else 'SideHatch',span=10.2)
        short.paste(image,(x,y+34));length=(3.96 if row==0 else 1.98)*size/250
        d.text((x+22,y),f'{size/100:g} m / '+('Full' if row==0 else 'Compact')+f' / {length:g} m long',font=font(21,True),fill=(231,226,208))
        d.text((x+22,y+516),'4 crew' if row==0 else '2 crew / Side Hatch / Blue rings',font=font(18),fill=(161,180,190));print('Rendered comparison',role,size,flush=True)
short.save(OUT/'RoosterWorks-0.75-Compact-HABs.png')
