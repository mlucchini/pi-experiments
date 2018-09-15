import RPi.GPIO as GPIO
import threading
import time


RED = 25
GREEN = 24
BLUE = 23

RGB_OFF = [GPIO.LOW, GPIO.LOW, GPIO.LOW]


class RgbLed(threading.Thread):
    def __init__(self):
        super(RgbLed, self).__init__()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RED, GPIO.OUT)
        GPIO.setup(GREEN, GPIO.OUT)
        GPIO.setup(BLUE, GPIO.OUT)
        self.daemon = True
        self.rgb = RGB_OFF
        self.blinking = False

    def __color_output(self, rgb):
      GPIO.output(RED, rgb[0])
      GPIO.output(GREEN, rgb[1])
      GPIO.output(BLUE, rgb[2])
    
    def __pause(self):
      time.sleep(1)

    def run(self):
      while(True):
        self.__color_output(self.rgb)
        self.__pause()
        if self.blinking:
          self.__color_output(RGB_OFF)
          self.__pause()
    
    def color(self, rgb):
      self.rgb = rgb

    def blink(self, blinking):
      self.blinking = blinking

    def keyboard_input(self):
      while(True):
        rgb = raw_input('RGB( ) -> ')
        if (len(rgb) >= 3):
          blink = len(rgb) == 4
          color = [int(rgb[0]), int(rgb[1]), int(rgb[2])]
          self.color(color)
          self.blink(blink)
        else:
          print('Wrong format')


if __name__ == '__main__':
  try:
    rgbLed = RgbLed()
    rgbLed.start()
    while(True):
      rgbLed.keyboard_input()
  except KeyboardInterrupt:
    GPIO.cleanup()
