import atexit
import threading

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor


class Worker(threading.Thread):
    def __init__(self, stepper, update_steps_event):
        super(Worker, self).__init__()
        self.lock = threading.Lock()
        self.update_steps_event = update_steps_event
        self.stepper = stepper
        self.current_steps = 0
        self.target_steps = 0

    def update_steps(self, target_steps):
        with self.lock:
            self.target_steps = target_steps

    def one_step(self):
        if self.current_steps < self.target_steps:
            direction = Adafruit_MotorHAT.FORWARD
            self.current_steps += 1
        else:
            direction = Adafruit_MotorHAT.BACKWARD
            self.current_steps -= 1
        self.stepper.oneStep(direction, Adafruit_MotorHAT.DOUBLE)

    def run(self):
        while True:
            self.lock.acquire()
            try:
                if self.current_steps != self.target_steps:
                    self.one_step()
                    self.lock.release()
                else:
                    self.update_steps_event.clear()
                    self.lock.release()
                    self.update_steps_event.wait()
            finally:
                self.lock.release()


class StepperMotorDriver:
    def __init__(self, motor_index, motor_steps_per_revolution=200):
        self.motor_index = motor_index
        self.motor_steps_per_revolution = motor_steps_per_revolution
        self.mh = Adafruit_MotorHAT()
        atexit.register(self.turn_off_motor)
        self.stepper = self.mh.getStepper(motor_steps_per_revolution, motor_index)
        self.update_steps_event = threading.Event()
        self.worker = Worker(self.stepper, self.update_steps_event)
        self.worker.daemon = True
        self.worker.start()

    def turn_off_motor(self):
        self.mh.getMotor(self.motor_index).run(Adafruit_MotorHAT.RELEASE)

    def angle_to_steps(self, angle):
        return int(angle * self.motor_steps_per_revolution / 360.0)

    def move(self, angle):
        steps = self.angle_to_steps(angle)
        self.worker.update_steps(steps)
        self.update_steps_event.set()
