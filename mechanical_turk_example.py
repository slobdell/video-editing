import os
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# HOST = 'mechanicalturk.amazonaws.com'
HOST = 'mechanicalturk.sandbox.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             host=HOST)

# hit = connection.get_hit("3S8A4GJRD22XNRRHHX41B0AX8ES6VF")[0]

url = "https://mturk-demonstration.herokuapp.com/"
title = "Tell me your favorite actor/actress"
description = "This is a really simple question. That's it."
keywords = ["easy"]
frame_height = 500  # the height of the iframe holding the external hit
amount = .05

questionform = ExternalQuestion(url, frame_height)


create_hit_result = connection.create_hit(
    title=title,
    description=description,
    keywords=keywords,
    question=questionform,
    reward=Price(amount=amount),
    response_groups=('Minimal', 'HITDetail'),  # I don't know what response groups are
)

task = create_hit_result[0]
print task.HITId

# POST back to:
# https://www.mturk.com/mturk/externalSubmit
# OR
# https://workersandbox.mturk.com/mturk/externalSubmit

# assignmentId must be included in POST parameters
