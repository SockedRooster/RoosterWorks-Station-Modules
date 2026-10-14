"""Native MU label and recess review with Unity's camera handedness."""
import math
from PIL import Image,ImageDraw
import render_appearance as r

def main():
    sheet=Image.new('RGB',(1800,1460),(12,20,27));d=ImageDraw.Draw(sheet)
    d.text((25,20),'ROOSTERWORKS / BADGE + END-RIM FIXES',font=r.font(32,True),fill=(235,234,220))
    d.text((27,67),'v0.7.0-dev.4 / exported native models / Unity camera orientation / KSP review pending',font=r.font(20),fill=(156,178,185))
    for j,(label,t,y,rad) in enumerate((('HAB',math.pi,0,1.245),('LAB',0,-.98,1.237),('CMD',math.pi,-.06,1.238),('CUP',math.pi,-.57,1.235),('LOG',math.pi/4,0,1.268))):
        focus=(rad*math.sin(t),y,rad*math.cos(t))
        photo=r.render(label,t,.02,.80,focus=focus,size=(1200,650)).resize((600,325),Image.Resampling.LANCZOS)
        x=(j%3)*600;yy=112+(j//3)*365
        sheet.paste(photo,(x,yy+26));d.text((x+22,yy),f'RW-{label}-250 / BADGE',font=r.font(22,True),fill=(231,226,208))
    photo=r.render('HUB',0,.02,.8,focus=(0,1.756,1.225),size=(1200,650)).resize((600,325),Image.Resampling.LANCZOS)
    sheet.paste(photo,(1200,503));d.text((1222,477),'RW-HUB-250 / COLLAR ID',font=r.font(22,True),fill=(231,226,208))
    for j,(label,t,e,focus,span) in enumerate((('HAB',.4,1.3,(0,1.92,0),3.0),('LOG',.4,.16,(0,1.49,-1.12),.40),('HUB',.4,.15,(0,1.995,-1.12),.40))):
        photo=r.render(label,t,e,span,focus=focus,size=(1200,1050)).resize((600,525),Image.Resampling.LANCZOS)
        sheet.paste(photo,(j*600,890));d.text((j*600+22,857),f'RW-{label}-250 / CLOSED RECESS',font=r.font(21,True),fill=(231,226,208))
    sheet.save(r.OUT/'RoosterWorks-v0.7.0-dev.4-Surface-Fixes.png')
    print('Native badge and rim review saved',flush=True)

if __name__=='__main__':main()
