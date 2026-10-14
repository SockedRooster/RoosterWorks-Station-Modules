"""Preview actual exported MU meshes at the same camera scale."""
from PIL import Image,ImageDraw
from render_appearance import render,font,OUT
image=Image.new('RGB',(1440,1180),(12,20,27));d=ImageDraw.Draw(image)
d.text((25,16),'ROOSTERWORKS / 0.75 LONG CREW TUBES',font=font(31,True),fill=(232,232,218))
d.text((25,60),'Actual native models and shipped textures / same scale / in-game acceptance pending',font=font(18),fill=(161,180,190))
for row,role in enumerate(('TUB','TUBL')):
    for col,size in enumerate((250,375,500)):
        x=col*480;y=110+row*510
        picture=render(role,diameter=size,size=(480,450),span=9.8,theta=.65,elevation=.3,ring_color='Original' if row==0 else 'Blue',finish='White' if row==0 else 'Grey metal')
        image.paste(picture,(x,y+35))
        d.text((x+22,y),f'{size/100:g} m / '+('Standard' if row==0 else 'Long')+f' / {(2 if row==0 else 4)*size/250:g} m length',font=font(22,True),fill=(231,226,208))
        print('Rendered',role,size,flush=True)
image.save(OUT/'RoosterWorks-0.75-Long-Crew-Tubes.png')
