from celery import Celery, shared_task
from utils.analyzer import pr_analysis

app = Celery("core")
app.config_from_object('django.conf:settings', namespace='CELERY')

@shared_task
def pr_analysis_task(repo_url, pr_number, github_token=None):
    result = pr_analysis(repo_url, pr_number, github_token)
    return result
    