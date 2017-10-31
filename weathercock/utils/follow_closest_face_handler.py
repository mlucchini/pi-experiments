import numpy as np

from utils.simulated_stepper_motor_driver import SimulatedStepperMotorDriver
from utils.stepper_motor_driver import StepperMotorDriver


class FollowClosestFaceHandler:
    def __init__(self, camera_fov, simulate=False):
        self.camera_fov = camera_fov
        self.h_stepper_motor_driver = SimulatedStepperMotorDriver(1) if simulate else StepperMotorDriver(1)
        self.v_stepper_motor_driver = SimulatedStepperMotorDriver(2) if simulate else StepperMotorDriver(2)

    def get_angle(self, location, frame):
        top, right, bottom, left = location
        height, width, _ = frame.shape

        frame_center = (width / 2.0, height / 2.0)
        face_center = (left + (right - left) / 2.0, bottom + (top - bottom) / 2.0)

        pixels_offset = tuple(np.subtract(frame_center, face_center))
        percentage_offset = (pixels_offset[0] / width, pixels_offset[1] / height)
        angle_offset = tuple(np.multiply(percentage_offset, self.camera_fov))

        return angle_offset

    def handle(self, user, location, frame):
        angle = self.get_angle(location, frame)
        self.h_stepper_motor_driver.move(angle[0])
        self.v_stepper_motor_driver.move(angle[1])

        print('Face tracking:')
        print('   Angle to center: %s' % np.rint(angle))
