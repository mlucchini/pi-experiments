import cv2

from utils.system import is_pi


class Camera:
    def __init__(self, frame_rate, resolution):
        self.driver = PiCamera(frame_rate, resolution) if is_pi() else CvCamera(frame_rate, resolution)

    def iterator(self):
        return self.driver.iterator()

    def release(self):
        return self.driver.release()


class CvCamera:
    def __init__(self, frame_rate, resolution):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FPS, frame_rate)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    def iterator(self):
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                yield frame

    def release(self):
        self.video_capture.release()


class PiCamera:
    def __init__(self, frame_rate, resolution):
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = frame_rate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)

    def iterator(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            frame = frame.array
            self.rawCapture.truncate(0)
            yield frame

    def release(self):
        self.camera.release()
