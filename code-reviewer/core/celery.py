import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

broker_url = 'redis://redis:6379/0' # os.getenv("CELERY_BROKER_URL")
result_backend = 'redis://redis:6379/0' # os.getenv("CELERY_RESULT_BACKEND")

if not broker_url or not result_backend:
    raise ValueError("CELERY_BROKER_URL or CELERY_RESULT_BACKEND is not set properly!")

app.conf.broker_url = broker_url
app.conf.result_backend = result_backend

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
