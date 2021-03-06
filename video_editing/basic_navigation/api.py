import json
import requests

from django.http import Http404
from django.http import HttpResponse


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
    # DELETE
    post_data = post_data or {}
    hit_id = post_data.get("hitId", "")
    assignment_id = post_data.get("assignmentId", "")
    post_data = {
        "hitId": hit_id,
        "workerId": post_data.get("workerId", ""),
        "assignmentId": assignment_id,
        "actor": post_data.get("actor", "")
    }
    final_url = ""
    response = requests.post(final_url, post_data)
    print final_url
    print response.content
    print response.status_code
    return render_to_json({"content": response.content}, status=200)
