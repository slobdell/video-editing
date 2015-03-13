import cv2
import numpy as np
import os

FRAMES_PER_SEC_KEY = 5
INTRO = True
OUTRO = False


def generate_valid_frames(capture):
    global INTRO
    global OUTRO

    while True:
        success, frame = capture.read()
        if not success:
            break
        if OUTRO:
            return
        # print np.std(frame[0]), np.average(frame[0])
        if np.std(frame[0]) <= 2 and np.average(frame[0]) < 20:
            if not INTRO:
                OUTRO = True
            pass
        else:
            INTRO = False
            yield frame


def create_video_writer(original_filename, height, width, frames_per_sec):
    codec = cv2.cv.FOURCC('M', 'J', 'P', 'G')
    original_filename = original_filename.replace(".mp4", "")
    new_filename = "filtered_" + original_filename + ".avi"
    video_writer = cv2.VideoWriter(new_filename, codec, frames_per_sec, (width, height))
    return video_writer


input_directory = '/Users/slobdell/Dropbox/WorkoutGen_Stuff/videos/copy/consolidated'
for filename in os.listdir(input_directory):
# for filename in ["-6yv9ihhJ8w.mp4"]:
    INTRO = True
    OUTRO = False
    if "mp4" not in filename:
        continue
    capture_path = input_directory + filename
    # capture_path = filename
    capture = cv2.VideoCapture(capture_path)
    frames_per_sec = capture.get(FRAMES_PER_SEC_KEY)
    _, frame = capture.read()
    height, width = frame.shape[0: 2]
    video_writer = create_video_writer(filename, height, width, frames_per_sec)
    for good_frame in generate_valid_frames(capture):
        video_writer.write(good_frame)
    video_writer.release()
    print "finished %s" % filename
