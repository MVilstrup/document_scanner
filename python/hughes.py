import math

import cv2
import numpy as np

from utils import imutils


def compute_skew(image):
    original = image.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(image, kernel, iterations=13)  # dilate
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    # for each contour found, draw a rectangle around it on original image
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # discard the biggest areas
        if h > 300 and w > 400:
            continue

        # TODO Try to find the logo on the receipt
        if h > 100 and w > 200:
            continue


        # discard areas that are too small
        if h < 40 or w < 40:
            continue

        # draw rectangle around contour on original image
        cv2.drawContours(image, contour, -1, (0, 0, 0), -1)

    edges = cv2.Canny(image, 80, 120)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 2, None, 150, 40)
    degrees = 0
    calculated_lines = 0
    for line in lines[0]:
        pt1 = (line[0], line[1])
        pt2 = (line[2], line[3])
        dx, dy = line[2] - line[0], line[3] - line[1]

        angle = math.atan2(dy, dx)
        degree = math.degrees(angle)
        if -10 < degree < 10:
            degrees += math.sqrt(degree * degree)
            calculated_lines += 1
            cv2.line(image, pt1, pt2, (0, 0, 255), 3)

    degrees /= lines.size
    print "Image rotated = %f degrees" % degrees
    rotated = imutils.rotate(original, degrees)
    (height, width) = rotated.shape[:2]
    rotated = rotated[20:height - 20, 20:width - 20]

    return rotated