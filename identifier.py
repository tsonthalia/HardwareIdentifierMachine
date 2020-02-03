from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np

from picamera import PiCamera
from time import sleep

from PIL import Image

import tflite_runtime.interpreter as tflite # TF2

camera = PiCamera()
# camera.start_preview()
# sleep(5)
camera.capture('picture.jpg')
# camera.stop_preview()

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


if __name__ == '__main__':

  interpreter = tflite.Interpreter(model_path='standardizedModel/model.tflite')
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]
  img = Image.open('picture.jpg').resize((width, height))

  # add N dim
  input_data = np.expand_dims(img, axis=0)

  if floating_model:
    input_data = (np.float32(input_data))

  interpreter.set_tensor(input_details[0]['index'], input_data)

  interpreter.invoke()

  output_data = interpreter.get_tensor(output_details[0]['index'])
  results = np.squeeze(output_data)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels('standardizedModel/dict.txt')
  for i in top_k:
    if floating_model:
      print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
    else:
      print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
