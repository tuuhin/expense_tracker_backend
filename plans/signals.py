from typing import Union
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.db.models.base import ModelBase
from django.utils import timezone
from .models import Budget, Goal, Notifications
from api.models import Category


@receiver([pre_save], sender=Budget)
def check_expiry(sender: ModelBase, instance: Budget, **kwags):
    if not instance.has_expired and instance.amount_used > instance.total_amount or timezone.now() > instance.to:
        instance.has_expired = True


@receiver([pre_save], sender=Goal)
def check_full_fillness(sender: ModelBase, instance: Goal, **kwags):
    if not instance.is_accomplished and instance.collected > instance.price:
        instance.is_accomplished = True


@receiver([pre_save], sender=Goal)
def create_category_if_not_exists(sender, instance, **kwargs):
    goal_categories = Category.objects.filter(
        user=instance.user, title="goals").first()
    if not goal_categories:
        Category.objects.create(user=instance.user, title="goals")


@receiver([pre_save], sender=Goal)
def add_goals_to_notifications(sender: ModelBase, instance: Goal, **kwags):
    goal_exists: Union[Goal, None] = Goal.objects.filter(pk=instance.pk)

    if not goal_exists:
        Notifications.objects.create(
            user=instance.user, title=f"Created Goal {instance}", status="created")
    else:
        Notifications.objects.create(
            user=instance.user, title=f"Updated Goal {instance}", status="updated")


@receiver([pre_delete], sender=Goal)
def add_remove_goal_notification(sender, instance, **kwags):
    goal_exists = Goal.objects.filter(pk=instance.pk)

    if goal_exists:
        Notifications.objects.create(
            user=instance.user, title=f"Removed Goal {instance}", status="deleted")


@receiver([pre_save], sender=Budget)
def add_budget_to_notification(sender, instance, **kwags):
    budget_exists = Budget.objects.filter(pk=instance.pk).first()
    if not budget_exists:
        Notifications.objects.create(
            user=instance.user, title=f"Created a Budget {instance}", status="created")


@receiver([pre_delete], sender=Budget)
def add_remove_budget_notification(sender, instance, **kwags):
    budget_exists = Budget.objects.filter(pk=instance.pk).first()
    if budget_exists:
        Notifications.objects.create(
            user=instance.user, title=f"Removed Budget {instance}", status="deleted")
