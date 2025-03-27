from django.contrib import admin
from django.urls import path
from main.views import AnalyzePullRequest, AnalysisStatus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze-pr', AnalyzePullRequest.as_view()),
    path('view-status', AnalysisStatus.as_view())
]
