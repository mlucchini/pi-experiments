import RPi.GPIO as GPIO
import threading
import time


RGB_OFF = [GPIO.LOW, GPIO.LOW, GPIO.LOW]


class RgbLed(threading.Thread):
    def __init__(self, red=25, green=24, blue=23):
        super(RgbLed, self).__init__()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)
        self.daemon = True
        self.rgb = RGB_OFF
        self.blinking = False
        self.red = red
        self.green = green
        self.blue = blue

    def __color_output(self, rgb):
      GPIO.output(self.red, rgb[0])
      GPIO.output(self.green, rgb[1])
      GPIO.output(self.blue, rgb[2])
    
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
