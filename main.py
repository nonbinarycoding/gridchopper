# Grid chopper
# Breaks apart multicolor image file into a grid
# G.L. Osborne
# Aug. 3, 2023

# I'm posting this a base to build off of, not as a
# ready-to-use program.  Unless you're using the same size images I was.

# all original images are 1800x644
# desired images are are 350x215


import os
import cv2 as cv
from PIL import Image, ImageDraw
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



# Step one: breaks the image into strips

i = 1

basepath = 'screenshots/'
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            with Image.open(basepath + entry.name) as im:
                to_crop_top = im.copy()
                to_crop_bottom = im.copy()
                (left, upper, right, lower) = (0, 0, 350, 215)
                im_crop_top = to_crop_top.crop((0, 0, 1800, 322))
                im_crop_bottom = to_crop_bottom.crop((0, 322, 1800, 644))
                filename_top = ("strip" + str(i) + "a.png")
                filename_bottom = ("strip" + str(i) + "b.png")
                im_crop_top.save(filename_top)
                im_crop_bottom.save(filename_bottom)
        i = i + 1

# Step two: split the strips into final images

basepath = 'strips/'
with os.scandir(basepath) as entries:
    for entry in entries:
        j = 1
        (left, upper, right, lower) = (0, 0, 257, 322)
        if entry.is_file():
            with Image.open(basepath + entry.name) as im:
                while j < 8:
                    im_crop = im.crop((left, upper, right, lower))
                    # OCR the color number for the filename
                    image_text = pytesseract.image_to_string(im_crop)
                    image_text = image_text.lower()
                    # If the OCR doesn't read right, save to a temp file
                    if image_text.isalnum():
                        new_filename = "colors/" + image_text[2:6] + ".png"
                    else:
                        new_filename = "colors/temp" + entry.name + str(i) + ".png"
                    im_crop.save(new_filename)
                    left = left + 257
                    right = right + 257
                    j = j + 1
