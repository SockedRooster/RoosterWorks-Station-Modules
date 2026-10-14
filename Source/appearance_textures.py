"""Deterministic, originally drawn exterior textures for the whole family.

Diffuse textures deliberately retain the established stock KSP shaders.
The original rooster and warm-white emissive texture are preserved.
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'

def font(size,bold=False):
    candidates=[Path('C:/Windows/Fonts')/('segoeuib.ttf' if bold else 'segoeui.ttf'),
                Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for path in candidates:
        if path.exists():return ImageFont.truetype(str(path),size)
    return ImageFont.load_default(size=size)

def label(part,role):
    import build_hab250 as h
    im=Image.new('RGB',(1024,512),(232,234,224));d=ImageDraw.Draw(im)
    d.rounded_rectangle((9,9,1014,502),radius=21,fill=(39,53,61),outline=(165,119,70),width=12)
    d.rounded_rectangle((28,28,995,483),radius=12,fill=(230,233,224))
    d.rectangle((47,47,976,86),fill=(48,64,70))
    d.text((65,49),'ORBITAL SYSTEMS   /   PRESSURE-RATED ASSEMBLY',font=font(23,True),fill=(229,232,221))
    d.text((58,123),'ROOSTERWORKS',font=font(71,True),fill=(37,52,61))
    im.paste(h.rooster_crest_image(110),(844,111))
    d.line((60,225,959,225),fill=(167,115,61),width=6)
    d.text((60,257),part+' / '+role,font=font(48,True),fill=(43,59,67))
    d.text((62,338),'RW  /  250 SERIES     •     SERVICE ACCESS',font=font(25),fill=(94,103,99))
    for j in range(52):
        x=63+j*5
        d.rectangle((x,405,x+1+(j%3==0),443),fill=(65,77,80))
    d.text((369,400),'ASSEMBLY  '+part+'   /   REV 02',font=font(24),fill=(87,91,84))
    for x in (47,976):
        for y in (107,461):
            d.ellipse((x-7,y-7,x+7,y+7),fill=(109,122,125))
            d.line((x-4,y+3,x+4,y-3),fill=(43,57,64),width=2)
    return im

def surface(name,base,seed):
    n=1024;rng=np.random.default_rng(seed)
    yy,xx=np.mgrid[:n,:n]
    # Fine restrained finish; no broad periodic stripes stretched by hull UVs.
    grain=rng.normal(0,.65,(n,n))
    if name in ('steel','rail','bronze'):
        grain+=rng.normal(0,.40,(n,1))+.25*np.sin(yy*.7)
    if name in ('ceramic','white'):
        grain+=.55*np.sin(xx*math.tau/n)*np.cos(yy*math.tau/n)
    values=np.clip(np.array(base)[None,None,:]+grain[:,:,None],0,255).astype('uint8')
    im=Image.fromarray(values)
    if name=='hubblanket':
        # Fine quilt stitching over restrained insulation folds.
        d=ImageDraw.Draw(im)
        for x in range(0,n,128):
            d.line((x,0,x,n-1),fill=(136,103,65),width=3)
            for y in range(5,n,13):d.line((x+4,y,x+4,y+5),fill=(190,152,96),width=1)
        for y in range(0,n,128):
            d.line((0,y,n-1,y),fill=(136,103,65),width=3)
            for x in range(5,n,13):d.line((x,y+4,x+5,y+4),fill=(190,152,96),width=1)
    return im

def grille(name):
    im=Image.new('RGB',(1024,1024),(31,44,50));d=ImageDraw.Draw(im)
    d.rounded_rectangle((20,20,1004,1004),radius=32,fill=(68,85,91),outline=(135,146,141),width=8)
    d.rounded_rectangle((51,82,973,923),radius=22,fill=(25,35,41))
    for y in range(104,897,32):
        d.rounded_rectangle((68,y,956,y+15),radius=5,fill=(40,54,60))
        d.line((81,y+1,943,y+1),fill=(118,132,132),width=2)
        for x in (205,512,819):d.rectangle((x,y+3,x+5,y+13),fill=(29,43,49))
    d.text((85,947),'RW / '+('CARGO INSERT' if name=='logpanel' else 'THERMAL CASSETTE'),font=font(26,True),fill=(190,192,169))
    for x in (40,984):
        for y in (40,984):
            d.ellipse((x-9,y-9,x+9,y+9),fill=(172,126,72))
            d.line((x-5,y+4,x+5,y-4),fill=(44,53,55),width=3)
    return im

def cladding(white=False):
    # Dedicated hull material: never map busy plate art onto narrow window ribs.
    base=(233,234,221) if white else (214,220,215)
    im=surface('white' if white else 'ceramic',base,70341+white)
    d=ImageDraw.Draw(im)
    dark=(144,158,155);light=(243,244,231);ink=(76,95,99)
    outer=[(38,17),(985,17),(1006,38),(1006,985),(985,1006),(38,1006),(17,985),(17,38),(38,17)]
    d.line(outer,fill=dark,width=4,joint='curve')
    d.line([(43,25),(979,25),(998,43)],fill=light,width=5)
    d.line([(30,57),(30,968)],fill=light,width=4)
    # An offset etched gasket line and inspection witness marks.
    d.line([(63,104),(63,914),(110,961),(914,961)],fill=(178,190,184),width=2)
    for x in (49,975):
        for y in (52,970):
            d.ellipse((x-12,y-12,x+12,y+12),fill=(119,136,137),outline=(230,233,219),width=3)
            d.line((x-5,y+4,x+5,y-4),fill=(58,77,82),width=3)
    d.text((91,58),'RW  /  MMOD',font=font(23,True),fill=ink)
    d.text((92,88),'THERMAL SHIELD / 250',font=font(17),fill=(113,132,132))
    d.line((738,64,929,64),fill=(167,119,65),width=6)
    d.line((850,82,929,82),fill=(92,111,111),width=2)
    for x in (84,909):
        d.line((x,911,x+27,911),fill=ink,width=3)
        d.line((x+13,899,x+13,922),fill=ink,width=3)
    # Low-contrast shallow stamping distinguishes a manufactured cover.
    d.rounded_rectangle((132,162,891,853),radius=29,outline=(197,208,201) if not white else (215,220,207),width=3)
    d.line((150,172,873,172),fill=light,width=2)
    return im

def atlas():
    atlas=Image.new('RGB',(1024,1024),(35,48,57))
    titles=['LIFE SUPPORT','DATA BUS','THERMAL','OPTICAL SYS','CARGO BAY','PRESSURE','SERVICE','SUPPLY BANK']
    codes=['LS-04','AV-02','HX-01','OS-08','SEALED','2.5 M','ACCESS','ST-12']
    for k in range(8):
        tile=Image.new('RGB',(256,512),(43,58,65));d=ImageDraw.Draw(tile)
        d.rounded_rectangle((10,10,246,502),radius=12,fill=(51,66,71),outline=(124,137,136),width=3)
        d.rectangle((24,25,231,31),fill=(179,128,70))
        d.text((25,49),titles[k],font=font(20,True),fill=(227,228,214))
        d.text((25,85),codes[k],font=font(33,True),fill=(189,194,181))
        d.line((25,134,230,134),fill=(104,119,118),width=2)
        if k in (0,3,7):
            for j in range(3):
                y=159+j*73
                d.rounded_rectangle((27,y,229,y+52),radius=5,fill=(25,38,45),outline=(102,124,126),width=2)
                d.text((36,y+9),['FILTER / A','SENSOR / B','FLOW / C'][j] if k==0 else ['CHANNEL 01','CHANNEL 02','CHANNEL 03'][j],font=font(16),fill=(185,196,184))
                for q in range(5):d.rectangle((162+q*10,y+34,167+q*10,y+40),fill=(145+q*6,161,125))
        elif k in (1,2):
            for j in range(13):
                y=155+j*15
                d.rectangle((27,y,229,y+8),fill=(21,33,41))
                d.line((29,y+10,227,y+10),fill=(112,133,137),width=2)
            d.text((31,369),'ISOLATE BEFORE',font=font(17),fill=(189,195,182))
            d.text((31,391),'SERVICE',font=font(22,True),fill=(193,149,86))
        else:
            d.rounded_rectangle((27,155,229,372),radius=5,fill=(33,47,53),outline=(117,135,129),width=2)
            for j in range(7):d.line((42,179+j*22,207-(j%3)*19,179+j*22),fill=(130,149,146),width=3)
        d.rectangle((26,435,229,475),fill=(34,47,51))
        d.text((36,445),'RW • '+codes[k]+' / 02',font=font(17,True),fill=(202,184,139))
        for x in (18,238):
            for y in (18,494):
                d.ellipse((x-4,y-4,x+4,y+4),fill=(176,187,183))
        if k in (4,5,6):
            # Dedicated wide-format plaque island sampled by atlas_uv.
            d.rectangle((12,212,244,300),fill=(42,58,63),outline=(163,119,65),width=3)
            d.text((24,221),titles[k],font=font(24,True),fill=(231,230,212))
            d.text((24,255),codes[k]+' / RW-250',font=font(21),fill=(179,190,177))
        atlas.paste(tile,((k%4)*256,(k//4)*512))
    return atlas

def finish():
    MODELS.mkdir(parents=True,exist_ok=True)
    surfaces={'ceramic':(214,220,215),'white':(233,234,221),'steel':(122,139,145),
              'graphite':(43,58,65),'bronze':(174,125,73),'black':(23,33,40),
              'rail':(192,204,199),'hubblanket':(164,126,78)}
    for i,(name,base) in enumerate(surfaces.items()):
        surface(name,base,70320+i).save(MODELS/f'rwm_{name}.png',optimize=True)
    for name in ('instrument','logpanel','display'):
        grille(name).save(MODELS/f'rwm_{name}.png',optimize=True)
    for name,white in (('cladding',False),('cladding_white',True)):
        cladding(white).save(MODELS/f'rwm_{name}.png',optimize=True)
    atlas().save(MODELS/'rwm_detail.png',optimize=True)
    for name,part,role in [('label','HAB-250','HABITAT'),('lablabel','LAB-250','RESEARCH'),
                            ('cmdlabel','CMD-250','COMMAND'),('hublabel','HUB-250','JUNCTION'),
                            ('cuplabel','CUP-250','OBSERVE'),('loglabel','LOG-250','SUPPLY')]:
        label(part,role).save(MODELS/f'rwm_{name}.png',optimize=True)
    # Do not regenerate crest, glass or cabin emissive from this detail pass.
    print('Built original satin finishes, stitched insulation, service atlas and family labels')

if __name__=='__main__':finish()
