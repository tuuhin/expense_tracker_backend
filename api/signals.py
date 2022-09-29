from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save
from api.models import Category, Expenses, Income, Source
from plans.models import Notifications, Budget
from django.db.models.base import ModelBase


@receiver([pre_save], sender=Expenses)
def add_notification_for_expense(sender, instance: Expenses,  **kwags):

    Notifications.objects.create(
        user=instance.user, title=f"spent {instance.amount} on {instance}", status="created")


@receiver([post_save], sender=Expenses)
def update_budget_amount_on_add(sender: ModelBase, instance: Expenses, created: bool, **kwags):
    budget: Budget = instance.budget
    budget.amount_used += instance.amount
    budget.save()


@receiver([pre_delete], sender=Expenses)
def update_budget_amount_on_delete(sender: ModelBase, instance: Expenses, **kwags):
    budget: Budget = instance.budget
    budget.amount_used -= instance.amount
    budget.save()


@receiver([pre_save], sender=Income)
def add_notification_for_income(sender, instance,  **kwags):
    income = Income.objects.filter(pk=instance.pk)

    if not income:
        Notifications.objects.create(
            user=instance.user, title=f"Got {instance.amount} for {instance}", status="created")


@receiver([pre_delete], sender=Income)
def add_notification_for_income(sender, instance,  **kwags):
    income = Income.objects.filter(pk=instance.pk)

    if not income:
        Notifications.objects.create(
            user=instance.user, title=f"Removed {instance.amount} from {instance}", status="removed")


@receiver([pre_save], sender=Source)
def add_notification_for_source(sender, instance,  **kwags):
    source = Source.objects.filter(pk=instance.pk)

    if not source:
        Notifications.objects.create(
            user=instance.user, title=f"Created new source {instance}", status="created")
    else:
        Notifications.objects.create(
            user=instance.user, title=f"Updated source {instance}", status="updated")


@receiver([pre_save], sender=Category)
def add_notification_for_category(sender, instance, **kwags):
    category = Category.objects.filter(pk=instance.pk)

    if not category:
        Notifications.objects.create(
            user=instance.user, title=f"Created catergory {instance}", status="created")
    else:
        Notifications.objects.create(
            user=instance.user, title=f"Updated category {instance}", status="updated")
