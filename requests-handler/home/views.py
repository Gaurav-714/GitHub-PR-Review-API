from ninja import NinjaAPI, Schema, Router
from typing import Optional
import aiohttp
import asyncio

api = NinjaAPI()
router = Router()

CODE_REVIEWER_URL = "http://code-reviewer:8001/"


class AnalyzePullRequest(Schema):
    repo_url: str
    pr_branch: str
    pr_number: int
    github_token: Optional[str] = None


async def post_request(url, data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                return await response.json(), response.status
            
    except aiohttp.ClientConnectorError:
        return {"error": "Service unavailable", "message": f"Cannot connect to {url}"}, 503
    except asyncio.TimeoutError:
        return {"error": "Request timed out", "message": f"Timeout when connecting to {url}"}, 504
    except Exception as ex:
        return {"error": "Unexpected error", "message": str(ex)}, 500


async def get_request(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json(), response.status
            
    except aiohttp.ClientConnectorError:
        return {"error": "Service unavailable", "message": f"Cannot connect to {url}"}, 503
    except asyncio.TimeoutError:
        return {"error": "Request timed out", "message": f"Timeout when connecting to {url}"}, 504
    except Exception as e:
        return {"error": "Unexpected error", "message": str(e)}, 500


class PullRequestAnalysisAPI:
    @router.post("/analyze-pr/")
    async def start_analysis(request, analysis_request: AnalyzePullRequest):
        """Handles PR analysis request"""
        data = {
            "repo_url": analysis_request.repo_url,
            "pr_branch": analysis_request.pr_branch,
            "pr_number": analysis_request.pr_number,
            "github_token": analysis_request.github_token,
        }
        response_data, status_code = await post_request(f"{CODE_REVIEWER_URL}/analyze-pr/", data)

        if status_code != 200:
            return {"error": "Failed to initiate analysis", "details": response_data}

        return {"message": "You can check the results using analysis id.", "details": response_data}

    @router.get("/view-status/{analysis_id}/")
    async def analysis_status(request, analysis_id: str):
        """Fetches PR analysis status"""
        analysis_id = str(analysis_id)
        response_data, status_code = await get_request(f"{CODE_REVIEWER_URL}/view-status/{analysis_id}/")

        if status_code != 200:
            return {"error": "Failed to retrieve analysis status", "details": response_data}
        return response_data


api.add_router("", router)
