from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np

# import cv2

import tensorflow as tf # TF2

from PIL import Image

def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

if __name__ == '__main__':

  interpreter = tf.lite.Interpreter(model_path='models/modelEdgeDetectionResized/model.tflite')
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]

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
  for i in top_k:
       if floating_model:
           print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
       else:
            print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
  print('\n')




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
  for i in top_k:
       if floating_model:
           print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
       else:
            print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
  print('\n')
