import argparse
import os
import multiprocessing as mp
from utils.ImageConverter import ImageConverter

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to the directory containing the images")
args = vars(ap.parse_args())

old_path = "%sjpg/" % args["directory"]
new_path = "%stiff/" % args["directory"]

images = {}
for (dirpath, _, filenames) in os.walk(old_path):

    for file in filenames:
        _ , extension =  os.path.splitext(file)
        if extension in [".jpg", ".JPG", ".jpeg"]:
            name = file
            path = "%s%s" % (dirpath, file)
            images[name] = path

    break

def convert(image_path, file_format, path):
    ImageConverter.convert_format(image_path=image_path, file_format=file_format, new_path=path)

pool = mp.Pool(processes=4)
# Convert the images to tiff images before starting working on them
for index, (image_name, image_path) in enumerate(images.iteritems()):
    pool.apply(convert, args=(image_path, "tiff", new_path))
    print "%i = %s" % (index + 1, image_name)
