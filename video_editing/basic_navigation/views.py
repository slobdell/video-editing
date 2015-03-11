# import datetime
import json
import os

# from django.conf import settings
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response


if os.environ.get("I_AM_IN_DEV_ENV"):
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"


def render_to_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="application/json", status=status)


def crop(request, video_name):
    if request.GET.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # worker hasn't accepted the HIT (task) yet
        pass
    else:
        # worked accepted the task
        pass

    worker_id = request.GET.get("workerId", "")
    if worker_id in []:
        # you might want to guard against this case somehow
        pass

    # TODO: need to add Amazon S3 stuff and push to production
    render_data = {
        "worker_id": request.GET.get("workerId", ""),
        "assignment_id": request.GET.get("assignmentId", ""),
        "amazon_host": AMAZON_HOST,
        "video_name": video_name,
        "hit_id": request.GET.get("hitId", ""),
    }

    response = render_to_response("base.html", render_data)
    # without this header, your iFrame will not render in Amazon
    response['x-frame-options'] = 'this_can_be_anything'
    return response
