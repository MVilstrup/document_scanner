import argparse
import os
import multiprocessing as mp
import cv2

from utils import imutils
from utils.ImageConverter import ImageConverter
from scan import ImageScanner


images_not_scanned = {}
def scan_image(image_name, image_path):
    image = cv2.imread(image_path)
    scanner = ImageScanner()
    scanned, warped = scanner.scan_reciept(image)
    if scanned:
        new_image_path = "%s%s" % (new_path, image_name)
        cv2.imwrite(new_image_path, warped)
        ImageConverter.convert_dpi(new_image_path)
        print "%s has been scanned" % image_name
    else:
        images_not_scanned[image_name] = image_path
        print "%s could not be scanned" % image_name


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

pool = mp.Pool(processes=4)
threads = []

# Convert the images to tiff images before starting working on them
for image_name, image_path in images.iteritems():
    threads.append(pool.apply_async(scan_image, args=(image_name, image_path)))

for thread in threads:
    thread.wait()

print "Number of images that could not be scanned = %i" % len(images_not_scanned)

if len(images_not_scanned) > 0:
    print "\n Images not scanned are: \n"
    for (image_name, _) in images_not_scanned.iteritems():
        print image_name