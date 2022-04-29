from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from api.models import Category, Expenses, Income, Source
from plans.models import Notifications


@receiver([pre_save], sender=Expenses)
def add_notification_for_expense(sender, instance,  **kwags):
    expense = Expenses.objects.filter(pk=instance.pk)

    if not expense:
        Notifications.objects.create(
            user=instance.user, title=f"spent {instance.amount} on {instance}", status="created")


@receiver([pre_save], sender=Income)
def add_notification_for_income(sender, instance,  **kwags):
    income = Income.objects.filter(pk=instance.pk)

    if not income:
        Notifications.objects.create(
            user=instance.user, title=f"Got {instance.amount} from {instance}", status="created")


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
            user=instance.user, title=f"Created Source {instance}", status="created")
    else:
        Notifications.objects.create(
            user=instance.user, title=f"Updated Source {instance}", status="updated")


@receiver([pre_save], sender=Category)
def add_notification_for_category(sender, instance, **kwags):
    category = Category.objects.filter(pk=instance.pk)

    if not category:
        Notifications.objects.create(
            user=instance.user, title=f"Created catergory {instance}", status="created")
    else:
        Notifications.objects.create(
            user=instance.user, title=f"Updated category {instance}", status="updated")
