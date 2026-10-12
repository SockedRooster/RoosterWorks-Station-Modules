"""Render actual HAB/LAB/CMD meshes from above to review matching endcaps."""
from pathlib import Path
from types import SimpleNamespace
import sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_hab250 as hab, build_lab250 as lab, build_cmd250 as cmd
import render_window_comparison as renderer
groups=hab.generate_groups()
parts=[('HAB-250',hab.combine_meshes(groups['Base'],groups['SideHatch']),1.98),
       ('LAB-250',lab.geometry(),1.98),('CMD-250',cmd.geometry(),.86)]
sheet=Image.new('RGB',(1650,335),(20,27,34));draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
for i,(name,mesh,plane) in enumerate(parts):
    wrapper=SimpleNamespace(generate_geometry=lambda variant,m=mesh:m,MODELS=hab.MODELS,
                            point=lambda radius,theta,y,p=plane:(0,p,0))
    renderer.load=lambda root,name,w=wrapper:w
    img=renderer.render(ROOT,name,span=3.0,elevation=2.3)
    sheet.paste(img.resize((550,295)),(i*550,40))
    draw.text((i*550+20,5),name+' — matching endcaps',font=font,fill=(237,242,246))
sheet.save(ROOT/'Media/Station-endcaps-v053.png')
print(ROOT/'Media/Station-endcaps-v053.png')
