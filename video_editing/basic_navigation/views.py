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


def trimreverse(request, video_name):
    render_data = {
        "worker_id": request.GET.get("workerId", ""),
        "assignment_id": request.GET.get("assignmentId", ""),
        "amazon_host": AMAZON_HOST,
        "video_name": video_name,
        "hit_id": request.GET.get("hitId", ""),
    }

    response = render_to_response("trimreverse.html", render_data)
    response['x-frame-options'] = 'this_can_be_anything'
    return response


def trim(request, video_name):
    render_data = {
        "worker_id": request.GET.get("workerId", ""),
        "assignment_id": request.GET.get("assignmentId", ""),
        "amazon_host": AMAZON_HOST,
        "video_name": video_name,
        "hit_id": request.GET.get("hitId", ""),
    }

    response = render_to_response("trim.html", render_data)
    # without this header, your iFrame will not render in Amazon
    response['x-frame-options'] = 'this_can_be_anything'
    return response


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


def _find_next_video_name():
    with open("responses.json", "rb") as f:
        user_responses = json.loads(f.read())
    with open("reviews.json", "rb") as f:
        reviews = json.loads(f.read())
    available_video_names = {item["video_name"] for item in user_responses}
    finished_video_names = {item["video_name"] for item in reviews}
    unfinished_video_names = available_video_names - finished_video_names
    for video_name in unfinished_video_names:
        return video_name
    raise ValueError("ALL DONE")


def _find_next_trim_video_name():
    with open("trim_responses.json", "rb") as f:
        user_responses = json.loads(f.read())
    with open("trim_reviews.json", "rb") as f:
        reviews = json.loads(f.read())
    available_video_names = {item["video_name"] for item in user_responses}
    finished_video_names = {item["video_name"] for item in reviews}
    unfinished_video_names = available_video_names - finished_video_names
    for video_name in unfinished_video_names:
        return video_name
    raise ValueError("ALL DONE")


def trim_review(request, video_name=None):
    if request.method == "POST":
        with open("trim_reviews.json", "rb") as f:
            current_reviews = json.loads(f.read())
        new_review_keys = ("start", "from_end", "video_name")
        new_review = {key: request.POST[key] for key in new_review_keys}

        existing_reviews = [item for item in current_reviews if item["video_name"] == video_name]
        if existing_reviews:
            existing_review = existing_reviews[0]
            existing_review.update(new_review)
        else:
            current_reviews.append(new_review)
        with open("trim_reviews.json", "w+") as f:
            f.write(json.dumps(current_reviews, indent=4))

    if video_name is None:
        video_name = _find_next_trim_video_name()
    with open("trim_responses.json", "rb") as f:
        user_responses = json.loads(f.read())
        video_data = [item for item in user_responses if item["video_name"] == video_name][0]
    with open("trim_reverse_responses.json", "rb") as f:
        user_reverse_responses = json.loads(f.read())
        video_end_data = [item for item in user_reverse_responses if item["video_name"] == video_name][0]

    with open("trim_reviews.json", "rb") as f:
        reviews = json.loads(f.read())
        finished_reviews = [item for item in reviews if item["video_name"] == video_name]
        if finished_reviews:
            video_data = finished_reviews[0]

    render_data = {
        "worker_id": request.GET.get("workerId", ""),
        "assignment_id": request.GET.get("assignmentId", ""),
        "amazon_host": AMAZON_HOST,
        "video_name": video_name,
        "hit_id": request.GET.get("hitId", ""),
    }
    render_data.update(video_data)
    render_data.update(video_end_data)
    render_data["start"] = render_data["start"] or 0
    render_data["from_end"] = render_data["from_end"] or 0

    return render_to_response("trimreview.html", render_data)


def local_review(request, video_name=None):

    if request.method == "POST":
        with open("reviews.json", "rb") as f:
            reviews = json.loads(f.read())
        new_review_keys = ("video_name", "width", "height", "offset_x", "offset_y")
        new_review = {key: request.POST[key] for key in new_review_keys}

        existing_reviews = [item for item in reviews if item["video_name"] == video_name]
        if existing_reviews:
            existing_review = existing_reviews[0]
            existing_review.update(new_review)
        else:
            reviews.append(new_review)
        with open("reviews.json", "w+") as f:
            f.write(json.dumps(reviews, indent=4))

    if video_name is None:
        video_name = _find_next_video_name()
    with open("responses.json", "rb") as f:
        user_responses = json.loads(f.read())
        video_data = [item for item in user_responses if item["video_name"] == video_name][0]
    with open("reviews.json", "rb") as f:
        reviews = json.loads(f.read())
        finished_reviews = [item for item in reviews if item["video_name"] == video_name]
        if finished_reviews:
            video_data = finished_reviews[0]

    render_data = {
        "worker_id": request.GET.get("workerId", ""),
        "assignment_id": request.GET.get("assignmentId", ""),
        "amazon_host": AMAZON_HOST,
        "video_name": video_name,
        "hit_id": request.GET.get("hitId", ""),
    }
    render_data.update(video_data)

    return render_to_response("self.html", render_data)


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
