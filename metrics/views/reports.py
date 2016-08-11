from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from metrics import data, reports
import csv


@staff_member_required
def csv_report(request, name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % name

    getattr(reports, name)(csv.writer(response))

    return response
