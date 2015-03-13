import cv2
# import numpy as np
import os

FRAMES_PER_SEC_KEY = 5
RESIZE_WIDTH = 300


def resized_frame(frame):
    height, width = frame.shape[0: 2]
    desired_width = RESIZE_WIDTH
    desired_to_actual = float(desired_width) / width
    new_width = int(width * desired_to_actual)
    new_height = int(height * desired_to_actual)
    return cv2.resize(frame, (new_width, new_height))


def generate_valid_frames(capture):

    while True:
        success, frame = capture.read()
        if not success:
            break
        frame = resized_frame(frame)
        yield frame


def create_video_writer(original_filename, height, width, frames_per_sec):
    codec = cv2.cv.FOURCC('M', 'J', 'P', 'G')
    original_filename = original_filename.replace(".mp4", "")
    video_writer = cv2.VideoWriter(original_filename, codec, frames_per_sec, (width, height))
    return video_writer


input_directory = "."
for filename in os.listdir(input_directory):
# for filename in ["-6yv9ihhJ8w.mp4"]:
    if "avi" not in filename:
        continue
    capture_path = filename
    capture = cv2.VideoCapture(capture_path)
    frames_per_sec = capture.get(FRAMES_PER_SEC_KEY)
    success, frame = capture.read()
    if not success:
        continue
    frame = resized_frame(frame)
    height, width = frame.shape[0: 2]
    new_filename = "small_" + filename.replace("filtered_", "")
    video_writer = create_video_writer(new_filename, height, width, frames_per_sec)
    for good_frame in generate_valid_frames(capture):
        video_writer.write(good_frame)
    video_writer.release()
    print "finished %s" % new_filename
