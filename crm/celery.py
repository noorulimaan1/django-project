
from __future__ import absolute_import, unicode_literals
from django.conf import settings

import os

from celery import Celery

from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'test-every-1-hour': {
        'task': 'demo',
        'schedule': 5.0,
    },
}
