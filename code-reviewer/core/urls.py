from django.contrib import admin
from django.urls import path
from main.views import home, AnalyzePullRequest, AnalysisStatus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('analyze-pr/', AnalyzePullRequest.as_view()),
    path('view-status/<analysis_id>/', AnalysisStatus.as_view())
]
