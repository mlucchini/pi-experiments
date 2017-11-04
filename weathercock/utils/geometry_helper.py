import numpy as np


TARGET_LOCK_THRESHOLD_IN_DEGREES = 1


def get_angle(location, frame, camera_fov):
    top, right, bottom, left = location
    height, width, _ = frame.shape

    frame_center = (width / 2.0, height / 2.0)
    face_center = (left + (right - left) / 2.0, bottom + (top - bottom) / 2.0)

    pixels_offset = tuple(np.subtract(face_center, frame_center))
    percentage_offset = (pixels_offset[0] / width, pixels_offset[1] / height)
    angle_offset = tuple(np.multiply(percentage_offset, camera_fov))

    return angle_offset


def is_target_locked(location, frame, camera_fov):
    angle = get_angle(location, frame, camera_fov)
    return abs(angle[0]) < TARGET_LOCK_THRESHOLD_IN_DEGREES and abs(angle[1] < TARGET_LOCK_THRESHOLD_IN_DEGREES)
