import os
import datetime
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
# from django.conf import settings


AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# if settings.FORCE_SANDBOX or os.environ.get("I_AM_IN_DEV_ENV"):
#     HOST = 'mechanicalturk.sandbox.amazonaws.com'
# else:
HOST = 'mechanicalturk.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             host=HOST)
TARGET_TITLE = "Crop a Video to Frame a Demonstrator"
REVIEWABLE_STATUS = "Reviewable"

all_hits = [hit for hit in connection.get_all_hits() if hit.Title == TARGET_TITLE]
reviewable_hits = [hit for hit in all_hits if hit.HITStatus == REVIEWABLE_STATUS]

'''
for hit in reviewable_hits:
    assignments = connection.get_assignments(hit.HITId)
    for assignment in assignments:
        # don't ask me why this is a 2D list
        question_form_answers = assignment.answers[0]
        for question_form_answer in question_form_answers:
            # "user-input" is the field I created and the only one I care about
            if question_form_answer.qid == "user-input":
                user_response = question_form_answer.fields[0]
                print "<li>%s</li>" % user_response
        connection.approve_assignment(assignment.AssignmentId)
'''

FILENAME_DIR = '/Users/slobdell/Movies/Miro Video Converter/'
for filename in os.listdir(FILENAME_DIR):
    video_name = filename.replace(".mp4.webmsd.webm", "")
    url = "https://mturk-demonstration.herokuapp.com/crop/%s/" % video_name
    print url
    title = "Crop a Video to Frame a Demonstrator"
    description = "Crop a video to best frame all of the movements of the demonstrator"
    keywords = ["video editing", "video", "crop"]
    frame_height = 800
    amount = 0.05

    questionform = ExternalQuestion(url, frame_height)

    create_hit_result = connection.create_hit(
        title=title,
        description=description,
        keywords=keywords,
        max_assignments=1,
        question=questionform,
        duration=datetime.timedelta(minutes=3),
        reward=Price(amount=amount),
        response_groups=('Minimal', 'HITDetail'),  # I don't know what response groups are
    )
