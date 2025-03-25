from ninja import NinjaAPI, Schema
from typing import Optional

api = NinjaAPI()

class ReviewPullRequest(Schema):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

@api.post("/start-task")
async def start_task_endpoint(request, task_request: ReviewPullRequest):
    data = {
        "repo_url": task_request.repo_url,
        "pr_number": task_request.pr_number,
        "github_token": task_request.github_token
    }
    print(data)
    return {"task_id": "714", "status": "Task Started"}
