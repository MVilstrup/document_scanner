import argparse

import cv2
import cv2.cv as cv
import tesseract

from utils import imutils
from scan import ImageScanner


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
scanner = ImageScanner()
warped = scanner.scan_reciept(image)

cv2.imshow("Original", imutils.resize(image, height=650))
cv2.imshow("Lines", imutils.resize(warped, height=650))

cv2.imwrite("../images/scanned.png", warped)

api = tesseract.TessBaseAPI()
api.Init(".", "dan", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)
image = cv.LoadImage("../images/scanned.png")
tesseract.SetCvImage(image, api)
text = api.GetUTF8Text()
conf = api.MeanTextConf()
print text
api.End()

cv2.waitKey(0)