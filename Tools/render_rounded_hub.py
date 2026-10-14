"""Review the actual exported rounded HUB beside the preceding candidate."""
from pathlib import Path
import math
from PIL import Image,ImageDraw
import render_appearance as r

def main():
    sheet=Image.new('RGB',(1800,1350),(12,20,27));d=ImageDraw.Draw(sheet)
    d.text((28,18),'RW-HUB-250 / ROUNDED PRESSURE JUNCTION',font=r.font(34,True),fill=(235,234,220))
    d.text((30,66),'v0.7.0-dev.3 / exported native model + shipped textures / in-game review pending',font=r.font(20),fill=(156,178,185))
    for j,(title,t,e) in enumerate((('OBLIQUE',.70,.38),('FRONT',0,.06),('UPPER',.76,1.0))):
        photo=r.render('HUB',t,e,5.5,size=(1200,1240)).resize((600,620),Image.Resampling.LANCZOS)
        sheet.paste(photo,(j*600,115));d.text((j*600+25,93),title,font=r.font(19),fill=(169,187,188))
    current=r.MODELS
    old=current.parents[2].parent/'rw-v070dev2/GameData/RoosterWorksStationModules/Models'
    if old.exists():
        r.MODELS=old
        before=r.render('HUB',.70,.38,5.5,size=(1200,1100)).resize((600,550),Image.Resampling.LANCZOS)
        r.MODELS=current
        after=r.render('HUB',.70,.38,5.5,size=(1200,1100)).resize((600,550),Image.Resampling.LANCZOS)
        sheet.paste(before,(200,790));sheet.paste(after,(1000,790))
        d.text((225,763),'PREVIOUS / SQUARE SHOULDERS',font=r.font(21,True),fill=(169,187,188))
        d.text((1025,763),'REVISED / CURVED SHELL + NECKS',font=r.font(21,True),fill=(235,234,220))
    sheet.save(r.OUT/'RW-HUB-250-v0.7.0-dev.3-Rounded-Review.png')
    # Five family tiles remain applicable: their native models and textures are
    # verified byte-identical to dev.2 by the revision regression check.
    family_path=r.OUT/'RoosterWorks-v0.7.0-dev.2-Family.png'
    if family_path.exists():
        family=Image.open(family_path).convert('RGB');fd=ImageDraw.Draw(family)
        fd.rectangle((0,62,1800,106),fill=(12,20,27))
        fd.text((34,70),'v0.7.0-dev.3 / rounded HUB / native models + shipped textures / in-game review pending',font=r.font(21),fill=(156,178,185))
        photo=r.render('HUB',.70,.38,5.8,size=(1520,1680)).resize((570,630),Image.Resampling.LANCZOS)
        family.paste(photo,(15,801))
        fd.text((32,780),'RW-HUB-250',font=r.font(24,True),fill=(236,230,211))
        family.save(r.OUT/'RoosterWorks-v0.7.0-dev.3-Family.png')
    print('Rounded HUB preview saved',flush=True)

if __name__=='__main__':main()
