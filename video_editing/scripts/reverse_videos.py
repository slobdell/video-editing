import cv2
# import numpy as np
import os

FRAMES_PER_SEC_KEY = 5
INTRO = True
OUTRO = False


RESIZE_WIDTH = 360


def resized_frame(frame):
    height, width = frame.shape[0: 2]
    import pdb; pdb.set_trace()
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
    new_filename = "reversed_" + original_filename + ".avi"
    video_writer = cv2.VideoWriter(new_filename, codec, frames_per_sec, (width, height))
    return video_writer


input_directory = '/Users/slobdell/Dropbox/WorkoutGen_Stuff/videos/copy/consolidated/'
for filename in os.listdir(input_directory):
# for filename in ["-6yv9ihhJ8w.mp4"]:
    if "mp4" not in filename:
        continue
    capture_path = input_directory + filename
    print capture_path
    capture = cv2.VideoCapture(capture_path)
    frames_per_sec = capture.get(FRAMES_PER_SEC_KEY)
    reversed_frames = list(reversed(list(generate_valid_frames(capture))))
    height, width = reversed_frames[0].shape[0: 2]
    video_writer = create_video_writer(filename, height, width, frames_per_sec)
    for frame in reversed_frames:
        video_writer.write(frame)
    video_writer.release()
    print "finished %s" % filename
