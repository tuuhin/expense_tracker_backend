from django.urls import path
from .views import goals


urlpatterns = [
    path('goals', goals, name="goals"),
]
