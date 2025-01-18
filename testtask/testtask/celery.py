import os

from celery import Celery
CELERY_IMPORTS = ('comment.task',)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testtask.settings")
app = Celery("testtask")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
