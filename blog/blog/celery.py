import os

from celery import Celery
from celery.schedules import crontab

from django.contrib.auth import get_user_model

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task
def print_count_of_users_registrated():
    users = get_user_model().objects.all()
    l = len(users)
    print("registrated users count is: ", l)
    return l


app.conf.beat_schedule = {
    'print-count-of-users-registrated': {
        'task': 'blog.celery.print_count_of_users_registrated',
        'schedule': crontab(),
    },
}
