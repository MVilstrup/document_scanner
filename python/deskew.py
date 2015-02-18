import argparse
import os
import multiprocessing as mp
import math

import cv2
import numpy as np

from utils import imutils


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to the directory containing the images")
args = vars(ap.parse_args())


def deskew_box(image_path):
    image = cv2.imread(image_path)
    original = image.copy()

    # extract path
    image_folder = os.path.dirname(image_path)
    image_name, file_extension = os.path.splitext(os.path.basename(image_path))
    new_path = "%s/%s-eroded.jpg" % (image_folder, image_name)

    # Make border around the image, so we can find a box inside it
    image = cv2.copyMakeBorder(image, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert the colors so we can use erosion and convert the letters into dots
    image = cv2.bitwise_not(image)

    # Create a kernel to specify how to erode the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    image = cv2.erode(image, kernel, iterations=2)

    # Iterate over the image to find all the white pixels
    image_array = np.asarray(image)
    points = np.argwhere(image_array == 255)

    rotated_box = cv2.minAreaRect(points)

    box = cv2.cv.BoxPoints(rotated_box)
    box = np.int0(box)

    for i, _ in enumerate(box):
        j = (i + 1) % 4
        cv2.line(image, tuple(box[j]), tuple(box[i]), (255, 0, 0), 3)

    cv2.imwrite(new_path, image)


def deskew(image_path):
    image = cv2.imread(image_path)

    # Make border around the image, so we can find a box inside it
    image = cv2.copyMakeBorder(image, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    original = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert the colors so we can use erosion and convert the letters into dots
    image = cv2.bitwise_not(image)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    image = cv2.dilate(image, kernel, iterations=9)

    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    image_lines = original.copy()

    minLineLength = image.shape[1] / 2
    maxLineGap = 20
    angle = 0.0
    print  minLineLength
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(image_lines, (x1, y1), (x2, y2), (0, 255, 0), 3)
        angle += math.atan2(y2 - y1, x2 - x1)

    degrees = (angle / len(lines[0])) * 180 / math.pi

    print "Image rotated = %f degrees" % degrees
    rotated = imutils.rotate(original, degrees)

    # extract path
    image_folder = os.path.dirname(image_path)
    image_name, file_extension = os.path.splitext(os.path.basename(image_path))
    new_path = "%s/%s-rotated.jpg" % (image_folder, image_name)
    edged_path = "%s/%s-edged.jpg" % (image_folder, image_name)
    lined_path = "%s/%s-lined.jpg" % (image_folder, image_name)



    cv2.imwrite(lined_path, image_lines)
    cv2.imwrite(new_path, rotated)
    cv2.imwrite(edged_path, edges)



images = {}

for (dirpath, _, filenames) in os.walk(args["directory"]):

    for file in filenames:
        _, extension = os.path.splitext(file)
        if extension in [".tiff", ".TIFF"]:
            name = file
            path = "%s%s" % (dirpath, file)
            images[name] = path

    break

pool = mp.Pool(processes=4)
threads = []

# Convert the images to tiff images before starting working on them
for image_name, image_path in images.iteritems():
    deskew(image_path)

for thread in threads:
    thread.wait()