import csv
import sys
from django.core.management import BaseCommand


class ReportCommand(BaseCommand):
    writer = csv.writer(sys.stdout)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            'subclasses of ReportCommand must provide a handle() method')
