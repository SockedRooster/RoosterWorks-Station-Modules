"""Three native-model views of the new dedicated EVA chamber."""
from PIL import Image,ImageDraw
import math
import render_appearance as r
sheet=Image.new('RGB',(2280,1020),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((26,18),'RW-AIR-250 / DEDICATED EVA CHAMBER',font=r.font(34,True),fill=(235,234,220))
d.text((28,63),'v0.8.0-dev.1 / native MU + shipped textures / EVA and Kerbalism flight tests pending',font=r.font(22),fill=(156,178,185))
for j,(title,t,e) in enumerate((('HATCH + BOARDING RAILS',.48,.28),('SERVICE SIDE + IDENTIFICATION',math.pi+.45,.28),('UPPER INTERFACE',.48,1.05))):
    photo=r.render('AIR',t,e,3.45,size=(1520,1680)).resize((760,840),Image.Resampling.LANCZOS)
    sheet.paste(photo,(j*760,140));d.text((j*760+25,110),title,font=r.font(20,True),fill=(225,226,214))
sheet.save(r.OUT/'RW-AIR-250-v0.8.0-dev.1-Review.png')
print('AIR native preview saved',flush=True)
