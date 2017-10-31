import sys
from utils.log_user_on_face_recognized_handler import LogUserOnFaceRecognizedHandler
from utils.follow_closest_face_handler import FollowClosestFaceHandler
from utils.video_face_recognizer import VideoFaceRecognizer


CAMERA_FOV = (53.50, 41.41)  # https://thepihut.com/products/zerocam-camera-for-raspberry-pi-zero#desc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s src_dir [--simulation]' % sys.argv[0])
        sys.exit()

    src_dir = sys.argv[1]
    simulation = len(sys.argv) > 2 and sys.argv[2] == '--simulation'

    face_recognizer = VideoFaceRecognizer(src_dir)
    face_recognizer.load()
    face_recognizer.add_face_recognized_handler(LogUserOnFaceRecognizedHandler())

    if simulation:
        from utils.simulated_fire_closest_face_handler import SimulatedFireClosestFaceHandler
        face_recognizer.add_face_recognized_handler(FollowClosestFaceHandler(CAMERA_FOV, simulate=True))
        face_recognizer.add_face_recognized_handler(SimulatedFireClosestFaceHandler(CAMERA_FOV))
    else:
        from utils.fire_closest_face_handler import FireClosestFaceHandler
        face_recognizer.add_face_recognized_handler(FollowClosestFaceHandler(CAMERA_FOV))
        face_recognizer.add_face_recognized_handler(FireClosestFaceHandler(CAMERA_FOV))

    face_recognizer.start_capture()
