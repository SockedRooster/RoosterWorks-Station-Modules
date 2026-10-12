from render_window_comparison import render,ROOT
image=render(ROOT,'hatch_rails',variant='SideHatch',focus_y=-.72,angle_offset=.2,span=1.8)
image.save(ROOT/'Media/HAB-grab-rails-v046.png')
print(ROOT/'Media/HAB-grab-rails-v046.png')
