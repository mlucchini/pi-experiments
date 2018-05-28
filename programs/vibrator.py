import RPi.GPIO as GPIO
import time


CHANNEL = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL,GPIO.OUT)
pwm=GPIO.PWM(CHANNEL, 100)
pwm.start(100)

while True:
  pwm.ChangeDutyCycle(10)
  time.sleep(1)
  pwm.ChangeDutyCycle(50)
  time.sleep(1)
  pwm.ChangeDutyCycle(100)
  time.sleep(1)
