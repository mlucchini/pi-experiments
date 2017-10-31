import face_recognition
import numpy as np
import os
import sys


class FaceEncoder:
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def encode(self):
        self.__create_dest_dirs()

        images = self.__images_from_dir()
        for image in images:
            image_full_path = self.src_dir + '/' + image
            face_encodings = face_recognition.face_encodings(face_recognition.load_image_file(image_full_path))
            if len(face_encodings) > 0:
                self.__save_encodings(image, face_encodings)

    def __create_dest_dirs(self):
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)

    def __images_from_dir(self):
        files = os.listdir(self.src_dir)
        return [image for image in files if image.endswith('.jpg')]

    def __save_encodings(self, path, arr):
        face_encoding_path = self.dest_dir + '/' + path.replace('.jpg', '.npy')
        print('Saving face encoding for %s' % face_encoding_path)
        np.save(face_encoding_path, arr)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: %s src_dir dest_dir' % sys.argv[0])
        sys.exit()

    face_encoder = FaceEncoder(sys.argv[1], sys.argv[2])
    face_encoder.encode()
