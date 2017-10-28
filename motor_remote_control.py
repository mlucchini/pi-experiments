import atexit
import threading
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor


mh = Adafruit_MotorHAT()


def turn_off_motors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


atexit.register(turn_off_motors)
myStepper1 = mh.getStepper(200, 1)
myStepper2 = mh.getStepper(200, 2)


def move_worker(stepper, direction, steps):
    for _ in range(steps):
        stepper.oneStep(direction, Adafruit_MotorHAT.DOUBLE)


def move(stepper, direction, steps):
    st = threading.Thread(target=move_worker, args=(stepper, direction, steps,))
    st.start()
    st.join()


def input_move():
    user_input = input("Choose a motor: (1) or (2) and a number of steps (n)\n")

    stepper_index, steps = user_input.split(" ")
    stepper = myStepper1 if stepper_index == "1" else myStepper2
    direction = Adafruit_MotorHAT.FORWARD if int(steps) > 0 else Adafruit_MotorHAT.BACKWARD
    steps = abs(int(steps))

    move(stepper, direction, steps)


while True:
    input_move()
