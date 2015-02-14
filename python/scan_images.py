import argparse
import os

import cv2

from utils import imutils
from utils.ImageConverter import ImageConverter
from scan import ImageScanner


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to the directory containing the images")
args = vars(ap.parse_args())

images = {}

for (dirpath, _, filenames) in os.walk(args["directory"]):

    for file in filenames:
        _ , extension =  os.path.splitext(file)
        if extension in [".tiff", ".TIFF"]:
            name = file
            path = "%s%s" % (dirpath, file)
            images[name] = path

    break

new_path = "%s../scanned_images/" % args["directory"]

images_not_scanned = {}

# Convert the images to tiff images before starting working on them
for (image_name, image_path) in images.iteritems():
    image = cv2.imread(image_path)
    scanner = ImageScanner()
    scanned, warped = scanner.scan_reciept(image)
    if scanned:
        new_image_path = "%s%s" % (new_path, image_name)
        print new_image_path
        cv2.imwrite(new_image_path, warped)
    else:
        images_not_scanned[image_name] = image_path

print "Number of images that could not be scanned = %i\n" % len(images_not_scanned)
print "Images not scanned are: \n"

for (image_name, _) in images.iteritems():
    print image_name