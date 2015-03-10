import json
import os
import requests

from django.http import Http404
from django.http import HttpResponse


if True or os.environ.get("I_AM_IN_DEV_ENV"):
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"


def render_to_json(response_obj, context={}, content_type="application/json", status=200):
    json_str = json.dumps(response_obj, indent=4)
    return HttpResponse(json_str, content_type=content_type, status=status)


def requires_post(fn):
    def inner(request, *args, **kwargs):
        if request.method != "POST":
            return Http404
        post_data = request.POST or json.loads(request.body)
        kwargs["post_data"] = post_data
        return fn(request, *args, **kwargs)
    return inner


@requires_post
def submit(request, post_data=None):
    post_data = post_data or {}
    hit_id = post_data.get("hitId", "")
    assignment_id = post_data.get("assignmentId", "")
    post_data = {
        # "hitId": hit_id,
        "assignmentId": assignment_id,
        "actor": post_data.get("actor", "")
    }
    response = requests.post(AMAZON_HOST, post_data)
    return render_to_json({"content": response.content}, status=200)
