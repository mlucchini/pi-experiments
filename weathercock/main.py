import sys
from utils.log_user_on_face_recognized_handler import LogUserOnFaceRecognizedHandler
from utils.video_face_recognizer import VideoFaceRecognizer
from utils.follow_closest_face_handler import FollowClosestFaceHandler

CAMERA_FOV = (53.50, 41.41)  # https://thepihut.com/products/zerocam-camera-for-raspberry-pi-zero#desc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s src_dir' % sys.argv[0])
        sys.exit()

    src_dir = sys.argv[1]

    face_recognizer = VideoFaceRecognizer(src_dir)
    face_recognizer.load()
    face_recognizer.add_face_recognized_handler(LogUserOnFaceRecognizedHandler())
    face_recognizer.add_face_recognized_handler(FollowClosestFaceHandler(CAMERA_FOV, simulate=True))
    face_recognizer.start_capture()
