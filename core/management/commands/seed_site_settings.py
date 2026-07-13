from django.core.management.base import BaseCommand
from core.models import SiteSetting


class Command(BaseCommand):
    help = 'ایجاد تنظیمات اولیه سایت'

    def handle(self, *args, **options):
        SiteSetting.objects.get_or_create(site_name='NEWMOON HOME')
        self.stdout.write(self.style.SUCCESS('Site settings seeded successfully.'))
