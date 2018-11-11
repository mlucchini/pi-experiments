import RPi.GPIO as GPIO
import time
from rgb_led import RgbLed
from lib import SimpleMFRC522


RGB_OFF = [GPIO.LOW, GPIO.LOW, GPIO.LOW]
RGB_GREEN = [GPIO.LOW, GPIO.HIGH, GPIO.LOW]


try:
    reader = SimpleMFRC522.SimpleMFRC522()
    rgbLed = RgbLed(red=14, green=15, blue=18)
    rgbLed.start()
    while True:
        id, data = reader.read()
        print('id: %s, data: %s' % (id, data))
        rgbLed.color(RGB_GREEN)
        time.sleep(0.5)
        rgbLed.color(RGB_OFF)
        time.sleep(0.5)
finally:
    GPIO.cleanup()
