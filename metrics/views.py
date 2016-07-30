from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import os
from metrics import data, reports
import csv


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


@staff_member_required
def list_reports(request):
    return render(request, 'reports.html')


@staff_member_required
def csv_report(request, name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % name

    getattr(reports, name)(csv.writer(response))

    return response
