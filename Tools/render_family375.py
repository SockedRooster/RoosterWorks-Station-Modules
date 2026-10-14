"""Native family overview and greenhouse lighting comparison; CPU, not KSP."""
from PIL import Image,ImageDraw
import render_appearance as r
roles=('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN')
spans={'HAB':7.2,'LAB':7.2,'CMD':5.25,'HUB':8.7,'CUP':4.72,'LOG':6.15,'AIR':5.18,'PWR':5.18,'GRN':6.98}
sheet=Image.new('RGB',(1800,2050),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((30,18),'ROOSTERWORKS / 3.75 M STATION FAMILY',font=r.font(34,True),fill=(235,234,220))
d.text((32,64),'v0.12.0-dev.1 / nine native large modules / exported geometry + textures / in-game acceptance pending',font=r.font(20),fill=(156,178,185))
for j,role in enumerate(roles):
    photo=r.render(role,.60,.38,spans[role],diameter=375,size=(900,975),variant='SideHatch' if role=='HAB' else 'Standard',point_lights=role=='GRN',emissive={'rwm_grninspection':1}).resize((600,650),Image.Resampling.LANCZOS)
    x=j%3*600;y=100+j//3*650;sheet.paste(photo,(x,y));d.text((x+24,y+10),'RW-'+role+'-375',font=r.font(24,True),fill=(235,234,220))
sheet.save(r.OUT/'RoosterWorks-3.75m-v0.12.0-dev.1-Family.png')
sheet=Image.new('RGB',(2280,1020),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((26,18),'GREENHOUSE / WARM-WHITE INSPECTION LIGHTING FIX',font=r.font(32,True),fill=(235,234,220))
d.text((28,64),'v0.12.0-dev.1 / actual native point-light positions and ranges / CPU illumination approximation, not KSP',font=r.font(20),fill=(156,178,185))
for j,(title,diameter,dark) in enumerate((('2.5 M / DAYLIGHT',250,False),('2.5 M / DARK INSPECTION VIEW',250,True),('3.75 M / DARK INSPECTION VIEW',375,True))):
    photo=r.render('GRN',.34,.25,4.65*(1.5 if diameter==375 else 1),diameter=diameter,dark=dark,point_lights=True,emissive={'rwm_grninspection':1},size=(1520,1680)).resize((760,840),Image.Resampling.LANCZOS)
    sheet.paste(photo,(j*760,140));d.text((j*760+25,110),title,font=r.font(20,True),fill=(225,226,214))
sheet.save(r.OUT/'Greenhouse-Lighting-v0.12.0-dev.1-Review.png')
print('Large family and greenhouse lighting previews saved',flush=True)
