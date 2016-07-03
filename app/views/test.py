from django.http import HttpResponse
from app import utils
from app.models import Goal


def render_email(request, name):
    goal = Goal.objects.filter(user=request.user).first()

    (html, text) = utils.render_email(name, request.user, goal)
    return HttpResponse(html)
