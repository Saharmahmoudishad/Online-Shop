from datetime import timedelta, datetime
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
import pytz


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=86400)
        Session.objects.filter(expire_date__lt=expired_time).delete()
        # self.stdout.write(self.style.Successfully closed poll "%s" % poll_id)
        self.stdout.write('all expireed session is_deleted')
