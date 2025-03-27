from ninja import NinjaAPI, Schema, Router
from typing import Optional
import aiohttp

api = NinjaAPI()
router = Router()

class AnalyzePullRequest(Schema):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None


async def post_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json(), response.status

async def get_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json(), response.status


class PullRequestAnalysisAPI:
    @router.post("/analyze-pr/")
    async def start_analysis(self, request, analysis_request: AnalyzePullRequest):
        """Handles PR analysis request"""
        data = {
            "repo_url": analysis_request.repo_url,
            "pr_number": analysis_request.pr_number,
            "github_token": analysis_request.github_token,
        }
        response_data, status_code = await post_request("http://127.0.0.1:8000/analyze-pr/", data)

        if status_code != 200:
            return {"error": "Failed to initiate analysis", "details": response_data}

        analysis_id = response_data.get("analysis_id")
        return {"analysis_id": analysis_id, "status": "Analysis initiated"}

    @router.get("/view-status/{analysis_id}/")
    async def analysis_status(self, request, analysis_id: str):
        """Fetches PR analysis status"""
        response_data, status_code = await get_request(f"http://127.0.0.1:8000/view-status/{analysis_id}/")

        if status_code != 200:
            return {"error": "Failed to retrieve analysis status", "details": response_data}

        return response_data


api.add_router("", router)
