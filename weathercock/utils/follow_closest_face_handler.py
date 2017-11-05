import atexit
import numpy as np

from utils.simulated_stepper_motor_driver import SimulatedStepperMotorDriver
from utils.stepper_motor_driver import StepperMotorDriver
from utils.geometry_helper import get_angle


class FollowClosestFaceHandler:
    def __init__(self, camera_fov, simulation=False):
        self.camera_fov = camera_fov
        self.simulation = simulation
        atexit.register(self.__turn_off_motor)
        if simulation:
            self.h_stepper_motor_driver = SimulatedStepperMotorDriver(2)
            self.v_stepper_motor_driver = SimulatedStepperMotorDriver(1)
        else:
            from Adafruit_MotorHAT import Adafruit_MotorHAT
            self.mh = Adafruit_MotorHAT()
            self.h_stepper_motor_driver = StepperMotorDriver(self.mh, 2)
            self.v_stepper_motor_driver = StepperMotorDriver(self.mh, 1)

    def handle(self, user, location, frame):
        angle = get_angle(location, frame, self.camera_fov)
        self.h_stepper_motor_driver.move(angle[0])
        self.v_stepper_motor_driver.move(angle[1])

        print('Face tracking:')
        print('   Angle to center: %s' % np.rint(angle))

    def __turn_off_motor(self):
        if not self.simulation:
            from Adafruit_MotorHAT import Adafruit_MotorHAT
            self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
            self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
            self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
            self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
