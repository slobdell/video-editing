import json
import os
import requests
import time


BASE_API_URL = "http://upload.gfycat.com/transcode?fetchUrl=%s"
QUERY_URL = "http://gfycat.com/cajax/get/%s"  # where %s becomes the AdjectiveAdjectiveNoun
AMAZON_URL = "https://s3-us-west-1.amazonaws.com/workout-generator-exercises/filtered/%s"

video_id_to_gfy_name = {}
filenames = os.listdir("/Users/slobdell/projects/workout-generator/workout_generator/scripts/video_scripts/test")
counter = 1
video_id_to_error = {}
for filename in reversed(filenames):
    if "avi" not in filename:
        continue
    file_url = AMAZON_URL % filename
    response = requests.get(BASE_API_URL % file_url)
    json_response = json.loads(response.content)
    video_id = filename.replace("filtered_", "").replace(".avi", "")
    if "error" in json_response:
        video_id_to_error[video_id] = json_response["error"]
        print json_response["error"]
        time.sleep(2)
        continue
    gfy_name = json_response["gfyName"]
    video_id_to_gfy_name[video_id] = gfy_name
    print counter, gfy_name
    counter += 1


with open("video_output.json", "w+") as f:
    f.write(json.dumps(video_id_to_gfy_name, indent=4))
    f.write("\n")
    f.write(json.dumps(video_id_to_error, indent=4))
