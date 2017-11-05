from enum import Enum

import face_recognition
import cv2
import numpy as np
import os
import sys

from utils.camera import Camera


class Recognizer(Enum):
    RECOGNITION = 0
    DETECTION = 1


class VideoFaceRecognizer:
    def __init__(self, src_dir, frame_rate, resolution, recognizer=Recognizer.RECOGNITION, headless=False):
        self.src_dir = src_dir
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.recognizer = recognizer
        self.headless = headless
        self.cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.face_encodings = []
        self.users = []
        self.face_recognized_handlers = []
        self.camera = Camera(frame_rate, resolution)

    def load(self):
        self.__load_encodings()

    def add_face_recognized_handler(self, handler):
        self.face_recognized_handlers.append(handler)

    def start_capture(self):
        process_this_frame = True
        frame_face_locations = []
        frame_face_users = []

        for frame in self.camera.iterator():
            if process_this_frame:
                frame_face_locations, frame_face_users = self.__extract_faces(frame)
                closest_face_index = self.__find_closest_face_index(frame_face_locations, frame_face_users)
                if closest_face_index is not None:
                    self.__process_handlers(frame_face_users[closest_face_index],
                                            frame_face_locations[closest_face_index],
                                            frame)
            self.__draw_rectangles(frame, frame_face_locations, frame_face_users, closest_face_index)
            process_this_frame = not process_this_frame
            if not self.headless:
                cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.camera.release()
        cv2.destroyAllWindows()

    def __load_encodings(self):
        files = [path for path in os.listdir(self.src_dir) if path.endswith('.npy')]
        for path in files:
            encodings = np.load(self.src_dir + '/' + path)
            if len(encodings) > 0:
                print('Loaded face encoding for %s' % path)
                self.face_encodings.append(encodings[0])
                self.users.append({'id': path.split('-')[0], 'name': path.split('-')[1].split('.')[0]})
        print('Loaded %d face encodings' % len(self.users))

    def __extract_faces(self, frame):
        if self.recognizer is Recognizer.DETECTION:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.cascade.detectMultiScale(gray, 1.3, 5)
            locations = [(y.item(), x.item() + w.item(), y.item() + h.item(), x.item()) for (x, y, w, h) in faces]
            return locations, [{'id': '0', 'name': 'Unknown'} for _ in locations]
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.cascade.detectMultiScale(gray, 1.3, 5)
            frame_face_locations = [(y.item(), x.item() + w.item(), y.item() + h.item(), x.item()) for (x, y, w, h) in faces]
            #  frame_face_locations = face_recognition.face_locations(frame)
            frame_face_encodings = face_recognition.face_encodings(frame, frame_face_locations)
            frame_face_users = []
            for face_encoding in frame_face_encodings:
                distances = face_recognition.face_distance(self.face_encodings, face_encoding)
                if distances.any():
                    closest_index = (np.abs(distances)).argmin()
                    frame_face_users.append(self.users[closest_index])
            return frame_face_locations, frame_face_users

    @staticmethod
    def __find_closest_face_index(frame_face_locations, frame_face_users):
        max_face_length = 0
        closest_face_index = None
        for i, ((top, right, bottom, left), _) in enumerate(zip(frame_face_locations, frame_face_users)):
            face_length = abs(top - bottom)
            if face_length > max_face_length:
                max_face_length = face_length
                closest_face_index = i
        return closest_face_index

    @staticmethod
    def __draw_rectangles(frame, frame_face_locations, frame_face_users, closest_face_index):
        for i, ((top, right, bottom, left), user) in enumerate(zip(frame_face_locations, frame_face_users)):
            rect_colour = (255, 0, 0) if i == closest_face_index else (0, 0, 255)
            center = (int(left + (right - left) / 2), int(bottom + (top - bottom) / 2))

            cv2.rectangle(frame, (left, top), (right, bottom), rect_colour, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), rect_colour, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, user['name'], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, 'x', center, font, 1.0, (255, 255, 255), 1)

    def __process_handlers(self, user, location, frame):
        for handler in self.face_recognized_handlers:
            handler.handle(user, location, frame)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: %s src_dir' % sys.argv[0])
        sys.exit()

    face_recognizer = VideoFaceRecognizer(sys.argv[1])
    face_recognizer.load()
    face_recognizer.start_capture()
