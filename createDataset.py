from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np

import cv2

from picamera import PiCamera

from PIL import Image

import tflite_runtime.interpreter as tflite # TF2

# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program

import os
import sys

GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

camera = PiCamera()
camera.color_effects = (128,128)

# Set up pin 11 for PWM
GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


# Move the servo back and forth
count = 0

print(count)

empty = False

hardware = "Machine Flat Allen 10-32 0.75in"

os.mkdir("images/New/" + hardware)
os.mkdir("images/New/" + hardware + "/uncroppedImages")
os.mkdir("images/New/" + hardware + "/edgeDetectionUncroppedImages")
os.mkdir("images/New/" + hardware + "/edgeDetectionCroppedImages")
os.mkdir("images/New/" + hardware + "/edgeDetectionResizedImages")

while not empty:
    p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
    sleep(2)                 # Wait 1 second
    p.ChangeDutyCycle(8)    # Changes the pulse width to 12 (so moves the servo)
    sleep(1)
    camera.capture('picture.jpeg')

    if __name__ == '__main__':
      # Setting the points for cropped image
      left = 600
      top = 50
      right = 1000
      bottom = 1200

      image = cv2.imread('picture.jpeg')
      croppedImage = image[top:bottom, left:right]
      resizedImage = cv2.resize(croppedImage, (224, 224))
      edgeDetectionUncroppedImage = auto_canny(image)
      edgeDetectionCroppedImage = edgeDetectionUncroppedImage[top:bottom, left:right]
      edgeDetectionResizedImage = cv2.resize(edgeDetectionCroppedImage, (224, 224))

      cv2.imwrite("images/New/" + hardware + "/uncroppedImages/picture" + str(count) + ".jpeg",image)
      cv2.imwrite("images/New/" + hardware + "/edgeDetectionUncroppedImages/picture" + str(count) + ".jpeg",edgeDetectionUncroppedImage)
      cv2.imwrite("images/New/" + hardware + "/edgeDetectionCroppedImages/picture" + str(count) + ".jpeg",edgeDetectionCroppedImage)
      cv2.imwrite("images/New/" + hardware + "/edgeDetectionResizedImages/picture" + str(count) + ".jpeg",edgeDetectionResizedImage)

      print(count)

      count=count+1
      p.ChangeDutyCycle(12)
      sleep(1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults
