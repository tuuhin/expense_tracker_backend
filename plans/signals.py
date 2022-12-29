from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save

from .models import Budget, Goal, Notifications, NotificationSignalChoices
from .choices import NotificationActions


@receiver([post_save], sender=Goal)
def goals_notifications(sender: Goal, instance: Goal, created: bool, **kwags):

    if created:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.CREATED,
            signal=NotificationSignalChoices.GOAL,
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.UPDATED,
            signal=NotificationSignalChoices.GOAL
        )


@receiver([pre_delete], sender=Goal)
def remove_goal(sender: Goal, instance: Goal, **kwags):
    Notifications.objects.create(
        user=instance.user,
        title=f"{instance}",
        status=NotificationActions.DELETED,
        signal=NotificationSignalChoices.GOAL
    )


@receiver([post_save], sender=Budget)
def add_budget(sender: Budget, instance: Budget, created: bool, **kwags):

    if created:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.CREATED,
            signal=NotificationSignalChoices.BUDGET
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.UPDATED,
            signal=NotificationSignalChoices.BUDGET
        )


@receiver([pre_delete], sender=Budget)
def remove_budget(sender: Budget, instance: Budget, **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"{instance}",
        status=NotificationActions.DELETED,
        signal=NotificationSignalChoices.BUDGET
    )
