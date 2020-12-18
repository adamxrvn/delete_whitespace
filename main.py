from PIL import Image, ImageChops
import requests


# Removes borders
def trim(im, color: tuple):
    bg = Image.new(im.mode, im.size, color)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)


# takes either filename or url
print('Input file name or url: ', end="")
filename = input()

# checks is it file name or url
if 'http' in filename:
    result = requests.get(filename)
    with open("picture.png", 'wb') as fp:
        fp.write(result.content)
    im = Image.open("picture.png")
    filename = "picture.png"

else:
    im = Image.open(filename)

# Take colors in 4 corners
border_colors = [im.getpixel((0, 0)), im.getpixel((im.width - 1, 0)),
                 im.getpixel((im.width - 1, im.height - 1)), im.getpixel((0, im.height - 1))]

# Check 4 corners and if they are close to white - > trim it
if border_colors[0][0] >= 242 and border_colors[0][1] >= 242 and \
        border_colors[0][2] >= 242:
    im = trim(im, border_colors[0])

if border_colors[1][0] >= 242 and border_colors[1][1] >= 242 and \
        border_colors[1][2] >= 242:
    im = trim(im, border_colors[1])

if border_colors[2][0] >= 242 and border_colors[2][1] >= 242 and \
        border_colors[2][2] >= 242:
    im = trim(im, border_colors[2])

if border_colors[3][0] >= 242 and border_colors[3][1] >= 242 and \
        border_colors[3][2] >= 242:
    im = trim(im, border_colors[3])
# save file with a new name
im.save(f'{filename.split(".")[0]}_new.{filename.split(".")[-1]}')
print(f'Saved! Filename: {filename.split(".")[0]}_new.{filename.split(".")[-1]}')
