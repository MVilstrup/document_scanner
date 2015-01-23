import argparse
import cv2
import tesseract
from scan import scan_reciept

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
cv2.imshow("Original", image)

warped = scan_reciept(image)

# Read the scanned image with tesseract
api = tesseract.TessBaseAPI()
api.Init(".", "dan", tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)

tmp = cv2.cv.fromarray(warped)
cv2.cv.SaveImage("saved.png", tmp)
image = cv2.cv.LoadImage("./saved.png", cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)
tesseract.SetCvImage(image, api)
text = api.GetUTF8Text()
conf = api.MeanTextConf()
print text

api.End()

cv2.waitKey(0)