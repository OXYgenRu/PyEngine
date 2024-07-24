from PIL import Image
import os

folder_path = input()
files = [f for f in os.listdir(folder_path)]
images = [Image.open(os.path.join(folder_path, f)) for f in files]
widths, heights = zip(*(i.size for i in images))
total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGBA', (total_width, max_height))

x_offset = 0
for im in images:
    new_im.paste(im, (x_offset, 0))
    x_offset += im.size[0]

new_im.save('combined.png')
