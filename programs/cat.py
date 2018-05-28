import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import threading
import time

from pyvirtualdisplay import Display
from selenium import webdriver


class StrokeSensor(threading.Thread):
    def __init__(self, callback):
        super(StrokeSensor, self).__init__()
        self.daemon = True
        self.flex_sensor = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(port=0, device=0))
        self.callback = callback

    def __read_flex_sensor(self):
        return self.flex_sensor.read_adc(0)

    def run(self):
        while True:
            value = self.__read_flex_sensor()
            print(value)
            self.callback(value)
            time.sleep(0.5)


class Vibration(threading.Thread):
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(25, GPIO.OUT)
        self.daemon = True
        self.pwm = GPIO.PWM(25, 100)

    def start(self):
        self.pwm.start(0)

    def update(self, percentage):
        self.pwm.ChangeDutyCycle(percentage)


class Cat:
    def __init__(self):
        self.display = Display(visible=0, size=(800, 600))
        self.browser = None
        self.stroke_sensor = StrokeSensor(self.adjust_stroke)
        self.vibration = Vibration()
        self.strokes = []

    def volume(self):
        levels = self.browser.find_element_by_css_selector('#levelBars')
        return float(levels.get_attribute('src')[-5]) * 20

    def adjust_volume(self, units):
        selector = 'body > div.tile1 > div.ctrSection > img:nth-child(' + ('1' if units < 0 else '3') + ')'
        element = self.browser.find_element_by_css_selector(selector)
        for unit in range(abs(units)):
            element.click()
            print('Adjusted volume to ' + str(self.volume()))

    def adjust_stroke(self, stroke):
        print(stroke)
        self.strokes.append(stroke)

        if len(self.strokes) < 10:
            return

        current_strokes = self.strokes[-10:]
        current_intensity = max(current_strokes) - min(current_strokes)
        if current_intensity > 100:
            self.adjust_volume(1)
        elif self.volume() > 0:
            self.adjust_volume(-1)
        self.vibration.update(self.volume())

    def start(self):
        self.display.start()
        print('Display started')

        self.browser = webdriver.Firefox()
        print('Browser started')

        self.browser.get('https://purrli.com')
        print('Web page loaded')

        self.stroke_sensor.start()
        print('Stroke sensor started')

        self.vibration.start()
        print('Vibration started')

    def stop(self):
        self.browser.quit()
        self.display.stop()


def keyboard_input(c):
    user_input = None
    while user_input is not 'q':
        user_input = input('Volume (+) or (-). Or quit (q)\n')
        c.adjust_volume(1) if user_input == '+' else c.adjust_volume(-1)


cat = Cat()
try:
    cat.start()
    cat.stroke_sensor.join()
except:
    cat.stop()
