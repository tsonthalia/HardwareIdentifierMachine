# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
from picamera import PiCamera #Imports Pi Camera
import os
import sys

GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

camera = PiCamera()
print(sys.argv)

imagesPath = 'images/'
os.mkdir(imagesPath + "" + sys.argv[1])
os.mkdir(imagesPath + "" + sys.argv[1] + "/uncroppedImages")
imageSavePath = imagesPath + "" + sys.argv[1] + "/uncroppedImages/"
#camera.start_preview()

# Set up pin 11 for PWM
GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0

# Move the servo back and forth
count = 0
for i in range(330):
    p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
    sleep(2)                 # Wait 1 second
    p.ChangeDutyCycle(8)    # Changes the pulse width to 12 (so moves the servo)
    sleep(1)
    camera.capture(imageSavePath + "picture" + str(count) + ".jpeg")
    print("picture" + str(count) + ".jpeg")
    count=count+1
    p.ChangeDutyCycle(12)
    sleep(1)

# Clean up everything
#camera.stop_preview()
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults
