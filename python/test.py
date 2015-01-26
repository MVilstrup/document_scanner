import argparse
import cv2
from utils import imutils
from scan import scan_reciept
# import cv2.cv as cv
# import tesseract

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

warped = scan_reciept(image)

cv2.imshow("Original",  imutils.resize(image, height=650))
cv2.imshow("Scanned",  imutils.resize(warped, height=650))

cv2.imwrite("../images/scanned.png", warped)

# api = tesseract.TessBaseAPI()
# api.Init(".", "dan", tesseract.OEM_DEFAULT)
# api.SetPageSegMode(tesseract.PSM_AUTO)
#
# image = cv.LoadImage("../images/scanned.png", cv.CV_LOAD_IMAGE_GRAYSCALE)
# tesseract.SetCvImage(image, api)
# text = api.GetUTF8Text()
# conf = api.MeanTextConf()
# print text
# api.End()

cv2.waitKey(0)