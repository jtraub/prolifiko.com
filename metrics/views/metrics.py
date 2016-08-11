from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import os
from app.models import Email, Goal
from metrics import data


@staff_member_required
def dashboard(request):
    return render(request, 'dashboard.html')


@staff_member_required
def conversion(request):
    users = data.real_users()
    emails = [user.email for user in users]

    registered = users.count()
    n7 = Email.objects.filter(name='n7_goal_complete',
                              recipient__email__in=emails).count()
    dr3 = Email.objects.filter(name='dr3',
                               recipient__email__in=emails).count()
    d3 = Email.objects.filter(name='d3',
                              recipient__email__in=emails).count()

    return render(request, 'conversion.html', {
        'project_id': os.environ['KEEN_PROJECT_ID'],
        'read_key': os.environ['KEEN_READ_KEY'],
        'real_users': [user.email for user in users],
        'excluded_goals': [goal.id.hex for goal in data.excluded_goals()],
        'conversion': {
            'registered': registered,
            'n7': n7,
            'dr3':  dr3,
            'd3':  d3,
            'sum': n7 + dr3 + d3,
            'completion': (n7 / registered) * 100
        }
    })
