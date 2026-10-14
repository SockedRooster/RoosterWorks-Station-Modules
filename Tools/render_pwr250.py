"""Actual exported PWR geometry and textures, Unity camera orientation."""
from PIL import Image,ImageDraw
import math
import render_appearance as r
sheet=Image.new('RGB',(2280,1020),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((26,18),'RW-PWR-250 / BATTERY + ELECTRICAL SERVICE CORE',font=r.font(34,True),fill=(235,234,220))
d.text((28,63),'v0.9.0-dev.1 / native MU + shipped textures / 15,000 EC / in-game testing pending',font=r.font(22),fill=(156,178,185))
for j,(title,t,e) in enumerate((('CELL CABINETS + POWER BUS',.56,.28),('SERVICE TRUNKS + MOUNTING AREAS',math.pi+.87,.24),('UPPER INTERFACE',.65,1.05))):
    photo=r.render('PWR',t,e,3.45,size=(1520,1680)).resize((760,840),Image.Resampling.LANCZOS)
    sheet.paste(photo,(j*760,140));d.text((j*760+25,110),title,font=r.font(20,True),fill=(225,226,214))
sheet.save(r.OUT/'RW-PWR-250-v0.9.0-dev.1-Review.png')
print('PWR native preview saved',flush=True)
