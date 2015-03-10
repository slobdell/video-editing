# import datetime
import json
# import os

# from django.conf import settings
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response


def render_to_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="application/json", status=status)


def home(request):
    render_data = {}
    if request.GET.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # worker hasn't accepted the HIT (task) yet
        pass
    else:
        # worked accepted the task
        pass
    hit_id = request.GET.get("hitId", "")
    render_data = {
        "assignment_id": request.GET.get("assignmentId"),
        "hit_id": hit_id
    }

    return render_to_response("base.html", render_data)