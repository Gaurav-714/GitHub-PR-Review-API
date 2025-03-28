from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import pr_analysis_task


class AnalyzePullRequest(APIView):
    def post(self, request):
        try:
            data = request.data 
            repo_url = data.get("repo_url")
            pr_number = data.get("pr_number")
            github_token = data.get("github_token")
            task_result = pr_analysis_task(repo_url, pr_number, github_token)

            return Response({
                "success": True,
                "analysis_id": task_result.id,
                "status": "Started Analyzing Pull Request"
            }, status=status.HTTP_102_PROCESSING)
        
        except Exception as ex:
            return Response({
                "success": False,
                "message": "something went wrong",
                "details": str(ex)
            })
    

class AnalysisStatus(APIView):
    def get(self, request, analysis_id):
        try:
            result = AsyncResult(analysis_id)
            response_data = {
                'analysis_id': analysis_id,
                'status': result.state,
            }
            if result.state == 'SUCCESS':
                response_data['result'] = result.result
            elif result.state == 'FAILURE':
                response_data['error'] = str(result.result)

            return JsonResponse(response_data)
        
        except Exception as ex:
            return Response({
                "success": False,
                "message": "something went wrong",
                "details": str(ex)
            })
    