from django.urls import path
from .views import (
    PredictAPIView,
    HealthAPIView,
    LanguageDetectAPIView,
    LogsAPIView
)

urlpatterns = [
    path("predict/", PredictAPIView.as_view()),
    path("health/", HealthAPIView.as_view()),
    path("detect-language/", LanguageDetectAPIView.as_view()),
    path("logs/", LogsAPIView.as_view()),
]
