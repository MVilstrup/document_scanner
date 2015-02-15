import argparse

from skimage.filter import threshold_adaptive
import cv2
import numpy as np
from transform import four_point_transform
from utils import imutils
from utils.ImageConverter import ImageConverter
from hughes import compute_skew

class ImageScanner:

    def __init__(self):
        pass

    def deskew(self, image):

        (h, w) = image.shape[:2]
        moments = cv2.moments(image, binaryImage=1)

        skew = moments["mu11"] / moments["mu02"]

        matrix = np.float32([
                [1, skew, -0.5 * w * skew],
                [0, 1, 0]])

        image = cv2.warpAffine(image, matrix, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)

        (height, width) = image.shape[:2]
        image = image[20:height - 10, 60:width - 80]
        image= cv2.copyMakeBorder(image,200,200,200,200,cv2.BORDER_CONSTANT,value=(255, 255, 255))

        return image

    # Function used to scan images, and extract the receipts from them
    # If the scan is successful it returns true, and the scanned image
    # Otherwise it returns false and the original image
    def scan_reciept(self, image):
        # Load the image and compute the ratio of the old height to
        # the new height, clone the image and resize it
        ratio = image.shape[0] / 700.0
        original = image.copy()

        # initiate value to judge if the image could be scanned or not
        scanned = False

        image = imutils.resize(image, height=700)

        # Convert the image to greyscale, blur it, and find edges
        # in the image
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grey = cv2.GaussianBlur(grey, (5, 5), 0)
        edged = cv2.Canny(grey, 30, 220)

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
            return (scanned, image)

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(original, screen_contour.reshape(4, 2) * ratio)

        # Convert the warped image to greyscale, then threshold it
        # to give it that "black and white" paper effect


        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

        warped = threshold_adaptive(warped, 210, offset=19)
        warped = warped.astype("uint8") * 255
        #rotated = compute_skew(warped)
        rotated = self.deskew(warped)
        #rotated  = ImageConverter.deskew(warped)

        scanned = True

        return (scanned, rotated)



