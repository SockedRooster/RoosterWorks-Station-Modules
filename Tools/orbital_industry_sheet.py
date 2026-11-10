from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];folder=R/'Media/OrbitalIndustry'
out=Image.new('RGB',(1600,490),(21,30,42));draw=ImageDraw.Draw(out)
for i,(role,title) in enumerate([('ISRU','Orbital Ore Refinery'),('NST','Nuclear Materials Vault'),('CEN','Fuel Centrifuge'),('NSM','Nuclear Smelter')]):
 draw.text((i*400+18,14),role+'-250',font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',25),fill=(237,193,97))
 draw.text((i*400+18,49),title,font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',19),fill=(230,235,240))
 im=Image.open(folder/(role+'.png')).convert('RGB').resize((400,340),Image.Resampling.LANCZOS);out.paste(im,(i*400,85))
draw.text((20,453),'ROOSTERWORKS  /  ORBITAL INDUSTRY  /  2.5 m  /  dev.11 TEST — actual model previews',font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18),fill=(183,198,214))
out.save(folder/'Family.png');print('PASS assembled orbital industry family preview')
