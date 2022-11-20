from PIL import Image
import glob

frames = []
imgs = sorted(glob.glob("*.png"))

for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

frames[0].save('test.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=300, loop=0)