import atexit
import threading
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor


mh = Adafruit_MotorHAT()


def turn_off_motors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


def stepper_worker(stepper, direction):
    for _ in range(1000):
        stepper.oneStep(direction, Adafruit_MotorHAT.DOUBLE)


atexit.register(turn_off_motors)
myStepper1 = mh.getStepper(200, 1)
myStepper2 = mh.getStepper(200, 2)

st1 = threading.Thread(target=stepper_worker, args=(myStepper1, Adafruit_MotorHAT.FORWARD,))
st1.start()

st2 = threading.Thread(target=stepper_worker, args=(myStepper2, Adafruit_MotorHAT.BACKWARD,))
st2.start()
