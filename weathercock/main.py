import argparse

from utils.log_user_on_face_recognized_handler import LogUserOnFaceRecognizedHandler
from utils.follow_closest_face_handler import FollowClosestFaceHandler
from utils.video_face_recognizer import VideoFaceRecognizer, Recognizer

#  CAMERA_FOV = (53.50, 41.41)  # https://thepihut.com/products/zerocam-camera-for-raspberry-pi-zero#desc
CAMERA_FOV = (120, 100)  # https://thepihut.com/products/zerocam-camera-for-raspberry-pi-zero#desc

FRAME_RATE = 15
RESOLUTION = (640, 480)


def parse_args():
    parser = argparse.ArgumentParser(description='Launches face detection or recognition and shoots detected targets.')
    parser.add_argument('--src_dir', required=True, help='the directory containing the face encodings')
    parser.add_argument('--simulation', action='store_true', help='simulates motors and triggers')
    parser.add_argument('--headless', action='store_true', help='do not display camera capture on screen')
    parser.add_argument('--recognizer', default='recognition', choices=['recognition', 'detection'], help='algorithm')
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    src_dir = args['src_dir']
    simulation = args['simulation']
    headless = args['headless']
    recognizer = Recognizer.DETECTION if args['recognizer'] == 'detection' else 'recognition'

    face_recognizer = VideoFaceRecognizer(src_dir, FRAME_RATE, RESOLUTION, recognizer, headless)
    face_recognizer.load()
    face_recognizer.add_face_recognized_handler(LogUserOnFaceRecognizedHandler())

    if simulation:
        from utils.simulated_fire_closest_face_handler import SimulatedFireClosestFaceHandler
        face_recognizer.add_face_recognized_handler(FollowClosestFaceHandler(camera_fov=CAMERA_FOV, simulation=True))
        face_recognizer.add_face_recognized_handler(SimulatedFireClosestFaceHandler(CAMERA_FOV))
    else:
        from utils.fire_closest_face_handler import FireClosestFaceHandler
        face_recognizer.add_face_recognized_handler(FollowClosestFaceHandler(CAMERA_FOV))
        face_recognizer.add_face_recognized_handler(FireClosestFaceHandler(CAMERA_FOV))

    face_recognizer.start_capture()
