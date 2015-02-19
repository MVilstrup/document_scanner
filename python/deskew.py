import argparse
import os
import math

import cv2
import numpy as np

from utils import imutils


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to the directory containing the images")
args = vars(ap.parse_args())


def pre_process(image):
    tresh = image.clone
    _, tresh = cv2.adaptiveThreshold(tresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)
    canvas = np.zeros(image.shape[:2], dtype="uint8")

    for x in range(image.shape[0]):  # loop over columns
        for y in range(image.shape[1]):
            top_row_black = tresh[y - 1, x] == 0 or tresh[y - 1, x - 1] == 0 or tresh[y - 1, x + 1] == 0
            bot_row_black = tresh[y + 1, x] == 0 or tresh[y + 1, x - 1] == 0 or tresh[y + 1, x + 1] == 0

            px = tresh[y, x]

            if not top_row_black and px == 255 and bot_row_black:
                canvas[y, x] = 255

    return canvas

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


def find_squares(image_path):
    image = cv2.imread(image_path)
    original = image.copy()
    (height, width) = original.shape[:2]
    image_folder = os.path.dirname(image_path)
    image_name, file_extension = os.path.splitext(os.path.basename(image_path))
    canvas = np.zeros((height, width, 3), dtype="uint8")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)  # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)  # dilate
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    height = 0
    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)
        height += h
        # discard areas that are too large
        if w > (width / 2):
            continue

        # discard areas that are too small
        if h < 40 or w < 40:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (255, 0, 255), 2)

    height /= len(contours)
    print "Average height of text = %i" % height
    # write original image with added contours to disk
    dilated_path = "%s/%s-dilated.jpg" % (image_folder, image_name)
    final_path = "%s/%s-squared.jpg" % (image_folder, image_name)
    # cv2.imwrite(dilated_path, dilated)
    cv2.imwrite(final_path, canvas)
    calculate_angle(canvas)


def calculate_angle(image):
    minLineLength = image.shape[1] / 5
    maxLineGap = 20
    angle = 0.0
    calculated_lines = 0
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lines = cv2.HoughLinesP(image, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    for x1, y1, x2, y2 in lines[0]:
        if abs(x2 - x1) > 10:
            calculated_lines += 1
            angle += math.atan2(abs(y2 - y1), abs(x2 - x1))

    degrees = (angle / len(lines[0])) * 180 / math.pi
    print "Calculated lines: %i" % calculated_lines
    print "Image rotated = %f degrees" % degrees


def calculate_average_character_height(image):
    (height, width) = image.shape[:2]
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)  # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)  # dilate
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours
    height = 0
    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)
        height += h
        # discard areas that are too large
        if w > (width / 2):
            continue

        # discard areas that are too small
        if h < 40 or w < 40:
            continue

    height /= len(contours)

    return height * 0.8


def make_horisontal_profile(image):
    image = cv2.bitwise_not(image)
    counter = []
    for i in range(image.shape[0]):  # loop over columns
        counter.append(sum(image[i, j] for j in range(image.shape[1])))

    return counter


def cut_horizontal_image_segment(image_path, start, end):
    image = cv2.imread(image_path)
    width = image.shape[1]
    segment = image[start:end, 0:width]
    return segment


def divide_into_segments(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    line = False
    segments = []
    start = 0
    average_height = calculate_average_character_height(image)
    profile = make_horisontal_profile(image)

    for row, count in enumerate(profile):
        if count > 0 and not line:
            start = row
            line = True
        elif count == 0 and line:
            line = False
            segment_height = row - start
            if segment_height > average_height:
                segments.append(cut_horizontal_image_segment(image_path, start, row))

    return segments


def deskew_segment(image):
    image = cv2.copyMakeBorder(image, 20, 20, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    original = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the colors so we can use erosion and convert the letters into dots
    image = cv2.bitwise_not(image)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    image = cv2.dilate(image, kernel, iterations=9)

    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    minLineLength = image.shape[1] / 5
    maxLineGap = 20
    angle = 0.0
    degrees = 0.0
    calculated_lines = 0
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    if lines is not None:
        for x1, y1, x2, y2 in lines[0]:
            if abs(x2 - x1) > 10:
                calculated_lines += 1
                angle += math.atan2(y2 - y1, x2 - x1)

        degrees = (angle / len(lines[0])) * 180 / math.pi
    rotated_segment = imutils.rotate(original, -degrees)
    return rotated_segment


def rename_image(image_path, new_name, file_extension=".jpg"):
    image_folder = os.path.dirname(image_path)
    new_path = "%s/%s%s" % (image_folder, new_name, file_extension)

    return new_path


images = {}

for (dirpath, _, filenames) in os.walk(args["directory"]):

    for file in filenames:
        _, extension = os.path.splitext(file)
        if extension in [".tiff", ".TIFF"]:
            name = file
            path = "%s%s" % (dirpath, file)
            images[name] = path

    break

# Convert the images to tiff images before starting working on them
for image_name, image_path in images.iteritems():
    print "Deskewing image: %s" % image_name
    image = cv2.imread(image_path)
    width = image.shape[1]

    segments = divide_into_segments(image_path)
    image = np.zeros((1, width, 3), dtype="uint8")
    image[:] = (255, 255, 255)

    for segment in segments:
        image = np.concatenate((image, deskew_segment(segment)), axis=0)

    new_name = "rotated-%s" % image_name

    new_path = rename_image(image_path, new_name)

    cv2.imwrite(new_path, image)






