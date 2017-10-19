import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor


mh = Adafruit_MotorHAT()
mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
atexit.register(lambda: mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE))
myStepper = mh.getStepper(200, 1)
myStepper.setSpeed(60)

while True:
    myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
