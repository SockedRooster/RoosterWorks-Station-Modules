"""Native exported greenhouse review; alpha blending and lamp-on studio view."""
from PIL import Image,ImageDraw
import render_appearance as r
sheet=Image.new('RGB',(2280,1020),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((26,18),'RW-GRN-250 / HYDROPONIC GREENHOUSE',font=r.font(34,True),fill=(235,234,220))
d.text((28,63),'v0.11.0-dev.1 / exported MU + PNG / alpha glazing, static crops, lamps shown on / in-game tests pending',font=r.font(20),fill=(156,178,185))
for j,(title,t,e) in enumerate((('GLAZED BAYS + CROP TIERS',.34,.25),('SERVICE DECKS + GROW RACKS',1.13,.33),('UPPER STACK INTERFACE',.42,1.1))):
    photo=r.render('GRN',t,e,4.65,size=(1520,1680),emissive=1).resize((760,840),Image.Resampling.LANCZOS)
    sheet.paste(photo,(j*760,140));d.text((j*760+25,110),title,font=r.font(20,True),fill=(225,226,214))
sheet.save(r.OUT/'RW-GRN-250-v0.11.0-dev.1-Review.png')
print('Greenhouse native preview saved',flush=True)
