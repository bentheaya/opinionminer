from django.urls import path
from . import views
from .views import SentimentAnalysisAPI, AnalysisHistoryAPI

app_name = 'sentiment'

urlpatterns = [
    path('', views.sentiment_analysis, name='analyze'),
    path('result/<int:pk>/', views.sentiment_result, name='result'),
    path('history/', views.analysis_history, name='history'), 
    path('api/analyze/', SentimentAnalysisAPI.as_view(), name='api_analyze'),
    path('api/history/', AnalysisHistoryAPI.as_view(), name='api_history'),
]
