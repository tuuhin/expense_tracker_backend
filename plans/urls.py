from django.urls import path
from .views import budget, goals, change_budget, upgrade_goals, create_goal
from .notifications import NotificationView

urlpatterns = [

    path('goals', goals, name="goals"),
    path('create-goal', create_goal, name="create-goal"),
    path('goals/<int:pk>', upgrade_goals, name="upgrade_goals"),
    path("notification", NotificationView.as_view(), name="notifications"),
    path('budget', budget, name="budget"),
    path("budget/<int:pk>", change_budget, name="change_budget"),

]
