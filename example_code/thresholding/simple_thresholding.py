import argparse

import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imshow("Image", image)

# This way of doing thresholding is not optimal since threshvalue has to be defined by the developer (in this case 155)
# This code works on the coins.png image to select the coins and not the table
(_, thresh) = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY)
cv2.imshow("Threshold Binary", thresh)

(_, thresh_inv) = cv2.threshold(blurred, 155, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Threshold Inverse", thresh_inv)

cv2.imshow("Coins", cv2.bitwise_and(image, image, mask=thresh_inv))  # Select only the coins

cv2.waitKey(0)
