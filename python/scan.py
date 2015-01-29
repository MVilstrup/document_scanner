import argparse

from skimage.filter import threshold_adaptive
import cv2
import numpy as np
from transform import four_point_transform
from utils import imutils
from hughes import compute_skew

class ImageScanner:

    def __init__(self):
        pass

    def deskew(self, image, width):

        (h, w) = image.shape[:2]
        moments = cv2.moments(image)

        skew = moments["mu11"] / moments["mu02"]

        matrix = np.float32([
                [1, skew, -0.5 * w * skew],
                [0, 1, 0]])

        image = cv2.warpAffine(image, matrix, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)

        image = imutils.resize(image, width=width)

        return image

    def scan_reciept(self, image):
        # Load the image and compute the ratio of the old height to
        # the new height, clone the image and resize it
        ratio = image.shape[0] / 700.0
        original = image.copy()

        image = imutils.resize(image, height=700)

        # Convert the image to greyscale, blur it, and find edges
        # in the image
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grey = cv2.GaussianBlur(grey, (5, 5), 0)
        edged = cv2.Canny(grey, 30, 200)

        # Find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        (contours, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        # loop over the contours
        screen_contour = None
        for c in contours:
            # Approximate the contour
            perimiter = cv2.arcLength(c, True)
            approximation = cv2.approxPolyDP(c, 0.02 * perimiter, True)

            # If our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approximation) == 4:
                screen_contour = approximation
                break

        # show the contour (outline) of the piece of paper
        if screen_contour is None:
            print "No contours could be found"
            return

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(original, screen_contour.reshape(4, 2) * ratio)

        # Convert the warped image to greyscale, then threshold it
        # to give it that "black and white" paper effect


        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        width = warped.shape[1]
        warped = threshold_adaptive(warped, 210, offset=13)

        warped = warped.astype("uint8") * 255
        rotated = compute_skew(warped)

        return rotated



