from django.urls import path
from .views import (budget, delete_reminders, goals,
                    reminders, remove_budget, upgrade_goals)
from .notifications import NotificationView

urlpatterns = [

    path('goals', goals, name="goals"),
    path('goals/<int:pk>', upgrade_goals, name="upgrade_goals"),
    path("notification", NotificationView.as_view(), name="notifications"),
    path('budget', budget, name="budget"),
    path("budget/<int:pk>", remove_budget, name="remove_budget"),
    path('reminders', reminders, name='reminders'),
    path('reminders/<int:pk>', delete_reminders)

]
