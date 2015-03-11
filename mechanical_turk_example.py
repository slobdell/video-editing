import os
import datetime
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

if False and os.environ.get("I_AM_IN_DEV_ENV"):
    HOST = 'mechanicalturk.sandbox.amazonaws.com'
else:
    HOST = 'mechanicalturk.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             host=HOST)

all_hits = [hit for hit in connection.get_all_hits()]

for hit in all_hits:
    assignments = connection.get_assignments(hit.HITId)
    for assignment in assignments:
        # don't ask me why this is a 2D list
        question_form_answers = assignment.answers[0]
        for question_form_answer in question_form_answers:
            # "user-input" is the field I created and the only one I care about
            if question_form_answer.qid == "user-input":
                user_response = question_form_answer.fields[0]
                print "<li>%s</li>" % user_response
        try:
            connection.approve_assignment(assignment.AssignmentId)
        except Exception as e:
            print e

url = "https://mturk-demonstration.herokuapp.com/"
title = "Describe a picture in your own words (COMPLETE THIS TASK ONLY ONCE!)"
description = "COMPLETE THIS TASK ONLY ONCE! All submissions after the first will be rejected"
keywords = ["easy"]
frame_height = 800
amount = 0.05

questionform = ExternalQuestion(url, frame_height)


for _ in xrange(0):
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
