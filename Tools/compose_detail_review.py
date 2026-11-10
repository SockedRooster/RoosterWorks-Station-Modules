from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'.build-deps'))
from PIL import Image,ImageDraw,ImageFont
OUT=R/'Media/DetailStudy02'
bold=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',38)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',27)
sheet=Image.new('RGB',(2200,2440),(15,22,28));d=ImageDraw.Draw(sheet)
d.text((35,24),'ROOSTERWORKS / MATERIAL DEPTH + STRUCTURAL DETAIL',font=bold,fill=(238,236,219))
d.text((35,80),'Same exported compact habitat, same lighting. Blender preview; KSP acceptance pending.',font=small,fill=(167,185,195))
for row,view in enumerate(('Overall','Surface')):
    for col,state in enumerate(('Before','After')):
        x=col*1100;y=185+row*1120
        photo=Image.open(OUT/f'HABS_{view}_{state}.png').convert('RGB')
        sheet.paste(photo,(x,y));d.text((x+35,y-45),('PASS 01 / BEFORE' if col==0 else 'STUDY 02 / AFTER')+' — '+view.upper(),font=small,fill=(226,201,150))
sheet.save(OUT/'Comparison.png')
