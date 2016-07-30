from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
import os
import json
from metrics import data


@staff_member_required
def user_journey(request):
    return render(request, 'user_journey.html', {
        'project_id': os.environ['KEEN_PROJECT_ID'],
        'read_key': os.environ['KEEN_READ_KEY'],
        'real_users': [user.email for user in data.real_users()],
    })


@staff_member_required
def active_users(request):
    return render(request, 'active_users.html', {
        'active_users': data.active_users()
    })
