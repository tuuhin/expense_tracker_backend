from django.urls import path
from .views import goals, upgrade_goals


urlpatterns = [

    path('goals', goals, name="goals"),  # to create or vist the goals
    path('goals/<int:pk>', upgrade_goals,
         name="upgrade_goals")  # to upgrade the goals

]
