from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import httpx

app = FastAPI()

class ReviewPullRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None


@app.post('/analyze-pr/')
async def start_analysis_endpoint(task_request: ReviewPullRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/analyze-pr/",
            data={
                "repo_url": task_request.repo_url,
                "pr_number": task_request.pr_number,
                "github_token": task_request.github_token,
            }
        )
        if response.status_code != 200:
            return {"error": "Failed to initiate task", "details": response.text}
        
        analysis_id = response.json().get("analysis_id")
        return {"analysis_id": analysis_id, "status": "Task started"}


@app.get("/view-status/{analysis_id}/")
async def analysis_status_endpoint(analysis_id: str):
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8000/view-status/{analysis_id}/")
        print(response)
        return response.json()
    
    return {"message": "something went wrong",}