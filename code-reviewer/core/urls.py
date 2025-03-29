from django.contrib import admin
from django.urls import path
from main.views import AnalyzePullRequest, AnalysisStatus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze-pr/', AnalyzePullRequest.as_view()),
    path('view-status/<analysis_id>/', AnalysisStatus.as_view())
]
