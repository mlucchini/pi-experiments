from utils.geometry_helper import is_target_locked


class SimulatedFireClosestFaceHandler:
    def __init__(self, camera_fov):
        self.camera_fov = camera_fov

    def handle(self, user, location, frame):
        if is_target_locked(location, frame, self.camera_fov):
            print('Fire!')
