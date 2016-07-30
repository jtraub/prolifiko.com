from metrics.management.commands import ReportCommand
from metrics import reports


class Command(ReportCommand):
    help = 'Shows active users'

    def handle(self, *args, **options):
        reports.user_journey(self.writer)
