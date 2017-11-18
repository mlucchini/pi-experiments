import RPi.GPIO as GPIO
import time


def set_angle(pin, angle):
    duty_cycle = float(angle) / 18.0 + 2
    GPIO.output(12, True)
    pin.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    GPIO.output(12, False)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setwarnings(False)

p = GPIO.PWM(12, 50)
p.start(0)

try:
    set_angle(p, 0)
    set_angle(p, 180)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
