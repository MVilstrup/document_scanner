import os
from PIL import Image
import math

import cv2


class ImageConverter:

    def __init__(self):
        pass

    # Method used to convert the DPI of an Image, to ensure the best reading resolution
    @staticmethod
    def convert_format(image_path, file_format="tiff", new_path=None):

        # Extract the relevant information about the image
        image_folder = os.path.dirname(image_path)

        # Create a new path, with a new file extension
        if new_path is None:
            image_name, _ =  os.path.splitext(image_path)
            new_path = "%s/%s.%s" % (image_folder, image_name, file_format)
        else:
            image_name, file_extension =  os.path.splitext(os.path.basename(image_path))
            new_path = "%s%s.%s" % (new_path, image_name, file_format)

        im = Image.open(image_path)
        im.save(new_path)

        return new_path

    @staticmethod
    def convert_dpi(image_path, dpi=300):
        im = Image.open(image_path)
        im.save(image_path, dpi=(dpi, dpi))



    @staticmethod
    def deskew(image):

        (height, width) = image.shape
        print "Height: %d\nWidth: %d" % (height, width)
        inverted = cv2.bitwise_not(image)
        minLineLength = width / 5
        maxLineGap = 20
        lined_image = image.copy()

        lines = cv2.HoughLinesP(inverted, 1, math.pi / 180, minLineLength, maxLineGap)
        for line in lines[0]:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])
            #print "(%d, %d) -> (%d, %d) " % (line[0], line[1], line[2], line[3])
            cv2.line(image, pt1, pt2, (0, 0, 255), 3)

        #cv2.imshow("Linned", imutils.resize(lined_image, height=650))
        #cv2.waitKey(0)
        return lined_image
