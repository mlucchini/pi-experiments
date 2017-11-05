import threading


class Worker(threading.Thread):
    def __init__(self, motor_index, update_steps_event):
        super(Worker, self).__init__()
        self.lock = threading.Lock()
        self.update_steps_event = update_steps_event
        self.motor_index = motor_index
        self.current_steps = 0
        self.target_steps = 0

    def update_steps(self, target_steps):
        with self.lock:
            self.target_steps = target_steps

    def run(self):
        while True:
            self.lock.acquire()
            try:
                if self.current_steps != self.target_steps:
                    self.__one_step()
                    self.lock.release()
                else:
                    self.update_steps_event.clear()
                    self.lock.release()
                    self.update_steps_event.wait()
            except RuntimeError:
                self.lock.release()

    def __one_step(self):
        if self.current_steps < self.target_steps:
            direction = 'FORWARD'
            self.current_steps += 1
        else:
            direction = 'BACKWARD'
            self.current_steps -= 1
        steps = abs(self.target_steps - self.current_steps)
        print('   Moving motor %s in direction %s for %d steps' % (self.motor_index, direction, steps))


class SimulatedStepperMotorDriver:
    def __init__(self, motor_index, motor_steps_per_revolution=200):
        self.motor_steps_per_revolution = motor_steps_per_revolution
        self.motor_index = motor_index
        self.update_steps_event = threading.Event()
        self.worker = Worker(motor_index, self.update_steps_event)
        self.worker.daemon = True
        self.worker.start()

    def move(self, angle):
        steps = self.__angle_to_steps(angle)
        self.worker.update_steps(steps)
        self.update_steps_event.set()

    def __angle_to_steps(self, angle):
        return int(angle * self.motor_steps_per_revolution / 360.0)
