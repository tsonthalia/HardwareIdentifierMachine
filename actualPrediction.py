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

def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

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
# for folder in os.listdir("images/All/"):
#     count+=len(os.listdir("images/All/" + folder + "/uncroppedImages"))

print(count)

empty = False

while not empty:
    p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
    sleep(2)                 # Wait 1 second
    p.ChangeDutyCycle(8)    # Changes the pulse width to 12 (so moves the servo)
    sleep(1)
    camera.capture('picture.jpeg')

    if __name__ == '__main__':

      interpreter = tflite.Interpreter(model_path='models/modelEdgeDetectionResized/model.tflite')
      interpreter.allocate_tensors()

      input_details = interpreter.get_input_details()
      output_details = interpreter.get_output_details()

      # check the type of the input tensor
      floating_model = input_details[0]['dtype'] == np.float32

      # NxHxWxC, H:1, W:2
      height = input_details[0]['shape'][1]
      width = input_details[0]['shape'][2]

      # print(width)
      # print(height)

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

      cv2.imwrite("picture.jpeg", edgeDetectionResizedImage)

      img = Image.open('picture.jpeg')

      # add N dim
      input_data = np.expand_dims(img, axis=0)
      input_data2 = []

      for i in range(len(input_data)):
          input_data2.append([])
          for j in range(len(input_data[i])):
              input_data2[i].append([])
              for k in range(len(input_data[i][j])):
                  input_data2[i][j].append([input_data[i][j][k], input_data[i][j][k], input_data[i][j][k]])
      

      if floating_model:
        input_data = (np.float32(input_data))

      interpreter.set_tensor(input_details[0]['index'], input_data2)

      interpreter.invoke()

      output_data = interpreter.get_tensor(output_details[0]['index'])
      results = np.squeeze(output_data)

      top_k = results.argsort()[-5:][::-1]
      labels = load_labels('models/modelEdgeDetectionResized/dict.txt')
      #for i in top_k:
           #if floating_model:
               # print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
           #else:
                #print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
      #print('\n')

      prediction = labels[top_k[0]]
      predictionResult = results[top_k[0]]
      
      print(prediction + ": " + str(predictionResult/255.0))
      if (prediction == "empty"):
          empty = True
      #cv2.imwrite("images/All/uncroppedImages/picture" + str(count) + ".jpeg",image)
      #cv2.imwrite("images/All/edgeDetectionUncroppedImages/picture" + str(count) + ".jpeg",edgeDetectionUncroppedImage)
      #cv2.imwrite("images/All/edgeDetectionCroppedImages/picture" + str(count) + ".jpeg",edgeDetectionCroppedImage)
      #cv2.imwrite("images/All/edgeDetectionResizedImages/picture" + str(count) + ".jpeg",edgeDetectionResizedImage)
      
      #cv2.imwrite("images/All/" + prediction + "/uncroppedImages/picture" + str(count) + ".jpeg",image)
      #cv2.imwrite("images/All/" + prediction + "/edgeDetectionUncroppedImages/picture" + str(count) + ".jpeg",edgeDetectionUncroppedImage)
      #cv2.imwrite("images/All/" + prediction + "/edgeDetectionCroppedImages/picture" + str(count) + ".jpeg",edgeDetectionCroppedImage)
      #cv2.imwrite("images/All/" + prediction + "/edgeDetectionResizedImages/picture" + str(count) + ".jpeg",edgeDetectionResizedImage)
      
      print(count)

      
      # cv2.imwrite("images/All/" + prediction + "/uncroppedImages/picture" + str(count),image)
      # cv2.imwrite("images/All/" + prediction + "/croppedImages/picture" + str(count),croppedImage)
      # cv2.imwrite("images/All/" + prediction + "/resizedImages/picture" + str(count),resizedImage)
      # cv2.imwrite("images/All/" + prediction + "/edgeDetectionUncroppedImages/picture" + str(count),edgeDetectionUncroppedImage)
      # cv2.imwrite("images/All/" + prediction + "/edgeDetectionCroppedImages/picture" + str(count),edgeDetectionCroppedImage)
      # cv2.imwrite("images/All/" + prediction + "/edgeDetectionResizedImages/picture" + str(count),edgeDetectionResizedImage)

      count=count+1
      p.ChangeDutyCycle(12)
      sleep(1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults

