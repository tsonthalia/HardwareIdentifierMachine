# Importing Image class from PIL module
from PIL import Image
import os
import numpy as np
import cv2

import sys

hardwarePath = "images/" + sys.argv[1] + "/"
uncroppedImages = hardwarePath + "uncroppedImages"

os.mkdir(hardwarePath + "croppedImages")
os.mkdir(hardwarePath + "resizedImages")
os.mkdir(hardwarePath + "edgeDetectionCroppedImages")
os.mkdir(hardwarePath + "edgeDetectionUncroppedImages")
os.mkdir(hardwarePath + "edgeDetectionResizedImages")

# os.mkdir(hardwarePath + "croppedImages")
# os.mkdir(hardwarePath + "resizedImages")

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

for currPic in os.listdir(uncroppedImages):
    if ("jpeg" in currPic):
        # Opens a image in RGB mode
        im = Image.open(uncroppedImages + "/" + currPic)

        # Size of the image in pixels (size of orginal image)
        # (This is not mandatory)
        width, height = im.size

        # Setting the points for cropped image
        left = 600
        top = 50
        right = 1000
        bottom = 1200

        # Cropped image of above dimension
        # (It will not change orginal image)
        image = cv2.imread(uncroppedImages + "/" + currPic,0)
        croppedImage = image[top:bottom, left:right]
        resizedImage = cv2.resize(croppedImage, (224, 224))
        edgeDetectionUncroppedImage = auto_canny(image)
        edgeDetectionCroppedImage = edgeDetectionUncroppedImage[top:bottom, left:right]
        edgeDetectionResizedImage = cv2.resize(edgeDetectionCroppedImage, (224, 224))

        cv2.imwrite(hardwarePath + "croppedImages/" + currPic,croppedImage)
        cv2.imwrite(hardwarePath + "resizedImages/" + currPic,resizedImage)
        cv2.imwrite(hardwarePath + "edgeDetectionUncroppedImages/" + currPic,edgeDetectionUncroppedImage)
        cv2.imwrite(hardwarePath + "edgeDetectionCroppedImages/" + currPic,edgeDetectionCroppedImage)
        cv2.imwrite(hardwarePath + "edgeDetectionResizedImages/" + currPic,edgeDetectionResizedImage)
        # auto.save(hardwarePath + "edgeDetectionCroppedImages/" + currPic, "JPEG")
        # im1.save(hardwarePath + "croppedImages/" + currPic, "JPEG")
        # im2.save(hardwarePath + "resizedImages/" + currPic, "JPEG")

        # Shows the image in image viewer
