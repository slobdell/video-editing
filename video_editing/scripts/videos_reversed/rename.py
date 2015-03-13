import os

for filename in os.listdir("."):
    if "mp4" in filename:
        new_filename = filename.replace("reversed_", "")
        os.system("mv %s %s" % (filename, new_filename))
