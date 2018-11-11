import RPi.GPIO as GPIO
from lib import SimpleMFRC522

RGB_OFF = [GPIO.LOW, GPIO.LOW, GPIO.LOW]


reader = SimpleMFRC522.SimpleMFRC522()

try:
    text = raw_input('New data:')
    print('Now place your tag to write')
    reader.write(text)
    print('Written')
finally:
    GPIO.cleanup()
