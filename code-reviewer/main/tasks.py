from celery import Celery, shared_task
from .utils.analyzer import pr_analysis

@shared_task
def pr_analysis_task(repo_url: str, pr_branch: str, pr_number: int, github_token: str = None):
    result = pr_analysis(repo_url, pr_branch, pr_number, github_token)
    
    return result
    