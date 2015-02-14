import argparse
import os

import cv2

from utils import imutils
from utils.ImageConverter import ImageConverter
from scan import ImageScanner

# Ensure the image has a resolution of 300 Dots Per Inch (DPI) and is Tiff file format
from os import walk

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to the directory containing the images")
args = vars(ap.parse_args())

old_path = "%sjpg/" % args["directory"]
new_path = "%stiff/" % args["directory"]
print new_path

images = []
for (dirpath, _, filenames) in walk(old_path):

    for file in filenames:
        _, extension =  os.path.splitext(file)
        if extension in [".jpg", ".jpeg", ".JPG"]:
            image = "%s%s" % (dirpath, file)
            images.append(image)

    break

# Convert the images to tiff images before starting working on them
for image in images:
    image_path = ImageConverter.convert_format_and_dpi(image, file_format="tiff", new_path=new_path, dpi=300)