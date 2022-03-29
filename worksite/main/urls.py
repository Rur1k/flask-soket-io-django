from django.urls import path, include
from .views import CreateUserAPIView

urlpatterns = [
    path('create', CreateUserAPIView.as_view()),
]
