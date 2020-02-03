from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np

from time import sleep

from PIL import Image

import tensorflow as tf # TF2

import os

def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

modelName = 'modelEdgeDetectionResized'

if __name__ == '__main__':

  interpreter = tf.lite.Interpreter(model_path='models/' + modelName + '/model.tflite')
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  # other = input_details[0]['shape'][0]
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]

  # print(other)
  # print(width)
  # print(height)

  # Setting the points for cropped image
  # left = 270
  # top = 50
  # right = 420
  # bottom = 470

  # Setting the points for cropped image
  # left = 600
  # top = 50
  # right = 1000
  # bottom = 1200

  img = Image.open('images/testImages/edgeDetectionResized/resizedImage0.jpeg')
  # img = Image.open('images/testImages/resized/picture3.jpeg')
  # croppedImg.save("croppedImage.jpeg")
  # img = croppedImage.resize((width, height))
  # img.save("resizedImage2.jpeg")

  # add N dim
  input_data = np.expand_dims(img, axis=0)
  input_data2 = []

  for i in range(len(input_data)):
      input_data2.append([])
      for j in range(len(input_data[i])):
          input_data2[i].append([])
          for k in range(len(input_data[i][j])):
              input_data2[i][j].append([input_data[i][j][k], input_data[i][j][k], input_data[i][j][k]])

  # print(len(input_data2))
  # print(len(input_data2[0]))
  # print(len(input_data2[0][0]))
  # print(input_data2[0][0][1])

  if floating_model:
    input_data = (np.float32(input_data))

  interpreter.set_tensor(input_details[0]['index'], input_data2)

  interpreter.invoke()

  output_data = interpreter.get_tensor(output_details[0]['index'])
  results = np.squeeze(output_data)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels('models/' + modelName + '/dict.txt')
  print(labels[top_k[0]] + ": " + str(results[top_k[0]]/255.0))
  print(labels[top_k[0]])
  for i in top_k:
    print(i)
    # if floating_model:
    #   print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
    # else:
    #   print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
    # print(results[i] + ": " + labels[i])
