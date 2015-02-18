import cv2.cv as cv
import tesseract


def read_receipt(image_path):
    api = tesseract.TessBaseAPI()
    api.Init(".", "dan", tesseract.OEM_DEFAULT)
    api.SetPageSegMode(tesseract.PSM_AUTO)
    image = cv.LoadImage(image_path)
    tesseract.SetCvImage(image, api)
    text = api.GetUTF8Text()
    conf = api.MeanTextConf()
    print text
    api.End()
