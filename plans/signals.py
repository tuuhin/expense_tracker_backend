from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from .models import Budget, Goal, Notifications
from .choices import NotificationActions

from api.models import Category


@receiver([pre_save], sender=Goal)
def create_category_if_not_exists(sender: Goal, instance: Goal, **kwargs):
    goal_categories = Category.objects.filter(
        user=instance.user, title="goals").first()
    if not goal_categories:
        Category.objects.create(user=instance.user, title="goals")


@receiver([pre_save], sender=Goal)
def goals_notifications(sender: Goal, instance: Goal, **kwags):

    goal_exists = Goal.objects.filter(pk=instance.pk).exists()

    if not goal_exists:
        Notifications.objects.create(
            user=instance.user,
            title=f"Created Goal {instance}",
            status=NotificationActions.CREATED
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"Updated Goal {instance}",
            status=NotificationActions.UPDATED,
        )


@receiver([pre_delete], sender=Goal)
def remove_goal(sender: Goal, instance: Goal, **kwags):
    Notifications.objects.create(
        user=instance.user,
        title=f"Removed Goal {instance}",
        status=NotificationActions.DELETED
    )


@receiver([pre_save], sender=Budget)
def add_budget(sender: Budget, instance: Budget, **kwags):
    budget_exists = Budget.objects.filter(pk=instance.pk).exists()
    if not budget_exists:
        Notifications.objects.create(
            user=instance.user,
            title=f"Created a Budget {instance}",
            status=NotificationActions.CREATED
        )


@receiver([pre_delete], sender=Budget)
def remove_budget(sender: Budget, instance: Budget, **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"Removed Budget {instance}",
        status=NotificationActions.DELETED
    )
