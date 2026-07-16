import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newmoonhome.config.settings.development')

try:
    from celery import Celery
    app = Celery('newmoonhome')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()

    @app.task(bind=True)
    def debug_task(self):
        print(f'Request: {self.request!r}')
except ImportError:
    app = None
