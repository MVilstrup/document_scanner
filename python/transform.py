import numpy as np
import cv2


def order_points(points):
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rectangle = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = points.sum(axis=1)
    rectangle[0] = points[np.argmin(s)]
    rectangle[2] = points[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    difference = np.diff(points, axis=1)
    rectangle[1] = points[np.argmin(difference)]
    rectangle[3] = points[np.argmax(difference)]

    # return the ordered points
    return rectangle


def four_point_transform(image, points):
    # Obtain a consistent order of the points and unpack them
    # individually
    rectangle = order_points(points)
    (top_left, top_right, bottom_left, bottom_right) = rectangle

    # Compute the width of the new image, which will be the
    # maximum distance between the top-right and top-left coordinates
    # x-coordinates or the bottom-right and bottom-left
    width_top = np.sqrt(((top_right[0] - top_left[0]) ** 2 + (top_right[0] - top_left[0]) ** 2))
    width_bottom = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2 + (bottom_right[0] - bottom_left[0]) ** 2))
    max_width = max(int(width_top), int(width_bottom))

    # Compute the height of the new image, which will be the maximum
    # distance between the top-right and bottom-right y-coordinates
    # or the top-left and bottom-left y-coordinates
    height_right = np.sqrt(((top_right[1] - bottom_right[1]) ** 2 + (top_right[1] - bottom_right[1]) ** 2))
    height_left = np.sqrt(((top_left[1] - bottom_left[1]) ** 2 + (top_left[1] - bottom_left[1]) ** 2))
    max_height = max(int(height_right), int(height_left))

    # Not that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i. e top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, bottom-left order
    destination = np.array([
                               [0, 0],
                               [max_width - 1, 0],
                               [max_width - 1, max_height - 1],
                               [0, max_height - 1]], dtype="float32")

    # Compute the perspective transform matrix and the apply it to the image
    matrix = cv2.getPerspectiveTransform(rectangle, destination)
    warped = cv2.warpPerspective(image, matrix, (max_width, max_height))

    return warped

