"""Three views of the actual exported adapter; never a concept proxy."""
from PIL import Image,ImageDraw
import render_appearance as r
original=r.render
def render(theta,elevation):
    # Existing renderer expects RW_<label>_250. ADP filename is a two-size ID.
    from native_model import load as real_load
    r.load=lambda path:real_load(r.MODELS/'RW_ADP_250_375.mu')
    try:return original('ADP',theta,elevation,4.1,size=(1520,1680))
    finally:r.load=real_load
sheet=Image.new('RGB',(2280,1020),(12,20,27));d=ImageDraw.Draw(sheet)
d.text((26,18),'RW-ADP-250-375 / STATION SIZE TRANSITION',font=r.font(34,True),fill=(235,234,220))
d.text((28,63),'v0.10.0-dev.1 / 2.5 m top to 3.75 m bottom / native model / in-game fit pending',font=r.font(22),fill=(156,178,185))
for j,(title,t,e) in enumerate((('TAPER + SERVICE DETAIL',.50,.25),('SMALL 2.5 M INTERFACE',.50,1.1),('LARGE 3.75 M INTERFACE',.50,-1.1))):
    photo=render(t,e).resize((760,840),Image.Resampling.LANCZOS)
    sheet.paste(photo,(j*760,140));d.text((j*760+25,110),title,font=r.font(20,True),fill=(225,226,214))
sheet.save(r.OUT/'RW-ADP-250-375-v0.10.0-dev.1-Review.png')
print('Adapter native preview saved',flush=True)
