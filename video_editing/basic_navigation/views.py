# import datetime
import json
import os

from django.conf import settings
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response

from boto.mturk.connection import MTurkConnection


AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


if settings.FORCE_SANDBOX or os.environ.get("I_AM_IN_DEV_ENV"):
    AMAZON_HOST = "https://workersandbox.mturk.com/mturk/externalSubmit"
else:
    AMAZON_HOST = "https://www.mturk.com/mturk/externalSubmit"
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


def secret_review(request):
    HOST = 'mechanicalturk.amazonaws.com'
    connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                host=HOST)
    if request.method == "POST":
        hit = connection.get_hit(request.POST["hit_id"])[0]
        assignments = connection.get_assignments(hit.HITId)
        if request.POST['execute'] == 'approve':
            for assignment in assignments:
                connection.approve_assignment(assignment.AssignmentId)
        elif request.POST['execute'] == 'deny':
            for assignment in assignments:
                connection.reject_assignment(assignment.AssignmentId)
    TARGET_TITLE = "Crop a Video to Frame a Demonstrator"
    REVIEWABLE_STATUS = "Reviewable"
    render_data = {}
    for hit in connection.get_all_hits():
        if hit.Title != TARGET_TITLE:
            continue
        if hit.HITStatus != REVIEWABLE_STATUS:
            continue
        assignments = connection.get_assignments(hit.HITId)
        for assignment in assignments:
            if assignment.AssignmentStatus in ("Approved", "Rejected"):
                continue
            question_form_answers = assignment.answers[0]
            response_dict = {q.qid: q.fields[0] for q in question_form_answers}
            render_data.update(response_dict)
            render_data["hit_id"] = hit.HITId
            return render_to_response("review.html", render_data)
    return HttpResponse("End of the Line")
