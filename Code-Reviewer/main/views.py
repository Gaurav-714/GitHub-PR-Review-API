from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from .tasks import pr_analysis_task


class AnalyzePullRequest(APIView):
    def post(self, request):
        data = request.data 
        repo_url = data.get("repo_url")
        pr_number = data.get("pr_number")
        github_token = data.get("github_token")
        task_result = pr_analysis_task(repo_url, pr_number, github_token)

        return Response({
            "analysis_id": task_result.id,
            "status": "Started Analyzing Pull Request"
        })
    

class AnalysisStatus(APIView):
    def get(self, request, analysis_id):
        result = AsyncResult(analysis_id)
        return Response({
            "analysis_id": analysis_id,
            "status": result.state
        })