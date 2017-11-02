import numpy as np

from utils.simulated_stepper_motor_driver import SimulatedStepperMotorDriver
from utils.stepper_motor_driver import StepperMotorDriver
from utils.geometry_helper import get_angle


class FollowClosestFaceHandler:
    def __init__(self, camera_fov, simulation=False):
        self.camera_fov = camera_fov
        self.h_stepper_motor_driver = SimulatedStepperMotorDriver(1) if simulation else StepperMotorDriver(1)
        self.v_stepper_motor_driver = SimulatedStepperMotorDriver(2) if simulation else StepperMotorDriver(2)

    def handle(self, user, location, frame):
        angle = get_angle(location, frame, self.camera_fov)
        self.h_stepper_motor_driver.move(angle[0])
        self.v_stepper_motor_driver.move(angle[1])

        print('Face tracking:')
        print('   Angle to center: %s' % np.rint(angle))
