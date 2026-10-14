"""CPU views of shipped native models and exact optional grey textures."""
from PIL import Image,ImageDraw
from render_appearance import render,font,OUT
ROLES=('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN')
SPANS={'HAB':4.8,'LAB':4.8,'CMD':3.5,'HUB':5.8,'CUP':3.15,'LOG':4.1,'AIR':3.5,'PWR':3.5,'GRN':4.6,'ADP':4.8}
for size in (250,375):
    sheet=Image.new('RGB',(1500,1050),(12,20,27));d=ImageDraw.Draw(sheet)
    d.text((25,15),f'ROOSTERWORKS / GREY METAL / {size/100:g} m',font=font(26,True),fill=(234,232,220))
    d.text((25,52),'Native model + shipped textures / CPU preview / in-game confirmation pending',font=font(16),fill=(159,179,188))
    labels=list(ROLES)+(['ADP'] if size==250 else [])
    for i,role in enumerate(labels):
        x=(i%5)*300;y=85+(i//5)*465
        photo=render(role,span=SPANS[role]*(1.5 if size==375 else 1),diameter='250_375' if role=='ADP' else size,size=(300,390),finish='Grey metal',variant='SideHatch' if role=='HAB' else 'Standard',emissive=.5)
        sheet.paste(photo,(x,y+30));d.text((x+15,y),f'RW-{role}-{size}' if role!='ADP' else '2.5 > 3.75 adapter',font=font(18,True),fill=(232,228,212))
        print('Rendered',role,size,flush=True)
    sheet.save(OUT/f'Grey-Metal-{size}-Family.png')
comparison=Image.new('RGB',(1600,930),(12,20,27));d=ImageDraw.Draw(comparison)
d.text((25,15),'EXTERIOR FINISH / WHITE + GREY METAL',font=font(30,True),fill=(235,232,220))
for i,(role,finish) in enumerate((('HUB','White'),('HUB','Grey metal'),('PWR','White'),('PWR','Grey metal'))):
    image=render(role,span=SPANS[role],size=(400,770),finish=finish)
    comparison.paste(image,(400*i,110));d.text((400*i+20,80),role+' / '+finish,font=font(22,True),fill=(223,224,216))
comparison.save(OUT/'White-Grey-Metal-Comparison.png')
