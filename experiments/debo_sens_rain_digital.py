import RPi.GPIO as GPIO
import time
import math

# Define GPIO pin and setup
DO = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(DO, GPIO.IN)

# Read digital signal every 2 seconds and print
while True:
    status = GPIO.input(DO)
    if status == 1:
        print("DRY")
    if status == 0:
        print("WET")
    time.sleep(2)
        
