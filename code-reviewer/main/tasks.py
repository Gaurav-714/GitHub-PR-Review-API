from celery import Celery, shared_task
from .utils.analyzer import pr_analysis

app = Celery("core")
app.config_from_object('django.conf:settings', namespace='CELERY')

@shared_task
def pr_analysis_task(repo_url: str, pr_branch: str, pr_number: int, github_token: str = None):
    result = pr_analysis(repo_url, pr_branch, pr_number, github_token)

    if hasattr(result, "values"):  
        result = list(result.values()) 

    return result
    