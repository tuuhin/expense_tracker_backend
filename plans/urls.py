from django.urls import path
from .views import budget, goals, remove_budget, show_notifications, upgrade_goals


urlpatterns = [

    path('goals', goals, name="goals"),  # to create or get the goals
    path('goals/<int:pk>', upgrade_goals,
         name="upgrade_goals"),  # to upgrade the goals
    path("notifications", show_notifications,
         name="notifications"),  # get all the notifications
    path('budget', budget, name="budget"),  # create or get budget
    path("budget/<int:pk>", remove_budget,
         name="remove_budget")  # remove budget

]
