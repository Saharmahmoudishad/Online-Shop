from datetime import datetime, timedelta
import pytz
from django.core.management.base import BaseCommand
from customers.models import CustomUser


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=86400)
        CustomUser.objects.filter(last_login__lt=expired_time).logical_delete()
        # self.stdout.write(self.style.Successfully closed poll "%s" % poll_id)
        self.stdout.write('all inactive user is_deleted')
