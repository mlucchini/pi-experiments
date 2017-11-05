import cv2
import time

from utils.system import is_pi
from utils.threaded_generator import ThreadedGenerator


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
        return ThreadedGenerator(self.__iterator_worker())

    def release(self):
        self.video_capture.release()

    def __iterator_worker(self):
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                yield frame


class PiCamera:
    def __init__(self, frame_rate, resolution):
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = frame_rate
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        time.sleep(1.0)  # Warm up camera

    def iterator(self):
        return ThreadedGenerator(self.__iterator_worker())

    def release(self):
        self.camera.release()

    def __iterator_worker(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            frame.array.setflags(write=1)
            yield frame.array
            self.rawCapture.truncate(0)
