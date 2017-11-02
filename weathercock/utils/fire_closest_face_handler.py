import RPi.GPIO as GPIO
import time

from utils.geometry_helper import is_target_locked


SERVO_PIN_NUMBER = 12
SERVO_PWM_FREQUENCY = 50


class FireClosestFaceHandler:
    def __init__(self, camera_fov):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(SERVO_PIN_NUMBER, GPIO.OUT)
        GPIO.setwarnings(False)
        self.camera_fov = camera_fov
        self.servo_pin = GPIO.PWM(SERVO_PIN_NUMBER, SERVO_PWM_FREQUENCY)
        self.servo_pin.start()

    def handle(self, user, location, frame):
        if is_target_locked(location, frame, self.camera_fov):
            self.__fire()

    def __rotate(self, angle):
        duty_cycle = float(angle) / 18.0 + 2
        GPIO.output(SERVO_PIN_NUMBER, True)
        self.servo_pin.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)
        GPIO.output(SERVO_PIN_NUMBER, False)

    def __fire(self):
        try:
            self.__rotate(0)
            self.__rotate(180)
        except KeyboardInterrupt:
            self.servo_pin.stop()
            GPIO.cleanup()
