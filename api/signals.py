from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save

from api.models import Category, Expenses, Income, Source
from plans.models import Notifications, Budget
from plans.choices import NotificationActions


@receiver([pre_save], sender=Expenses)
def add_notification_for_expense(sender, instance: Expenses,  **kwags):
    exp = Expenses.objects.filter(pk=instance.pk).exists()
    if not exp:
        Notifications.objects.create(
            user=instance.user,
            title=f"spent {instance.amount} on {instance}",
            status=NotificationActions.CREATED
        )


@receiver([post_save], sender=Expenses)
def update_budget_amount_on_add(sender, instance: Expenses, created: bool, **kwags):

    budget: Budget = instance.budget
    budget.amount_used += instance.amount
    budget.save()


@receiver([pre_delete], sender=Expenses)
def expense_delete(sender: Expenses, instance: Expenses, **kwags):
    Notifications.objects.create(
        user=instance.user,
        title=f"Removed {instance}",
        status=NotificationActions.DELETED
    )
    budget: Budget = instance.budget
    budget.amount_used -= instance.amount
    budget.save()


@receiver([post_save], sender=Income)
def add_notification_for_income(sender, instance: Income,  **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"Got {instance.amount} for {instance}",
        status=NotificationActions.CREATED,
    )


@receiver([pre_delete], sender=Income)
def remove_notification_for_income(sender: Income, instance: Income,  **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"Removed {instance.amount} from {instance}",
        status=NotificationActions.DELETED
    )


@receiver([pre_save], sender=Source)
def add_notification_for_source(sender: Source, instance: Source,  **kwags):
    source = Source.objects.filter(pk=instance.pk)

    if not source:
        Notifications.objects.create(
            user=instance.user,
            title=f"Created new source {instance}",
            status=NotificationActions.CREATED
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"Updated source {instance}",
            status=NotificationActions.UPDATED
        )


@receiver([pre_save], sender=Category)
def add_notification_for_category(sender, instance: Category, **kwags):
    category = Category.objects.filter(pk=instance.pk).first()

    if not category:
        Notifications.objects.create(
            user=instance.user,
            title=f"Created catergory {instance}",
            status=NotificationActions.CREATED
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"Updated category {instance}",
            status=NotificationActions.UPDATED
        )


@receiver([pre_delete], sender=Source)
def remove_source_notification(sender: Category, instance: Category, **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"Source:{instance} deleted",
        status=NotificationActions.DELETED
    )


@receiver([pre_delete], sender=Category)
def remove_category_notification(sender, instance: Category, **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"Category: {instance} deleted",
        status=NotificationActions.DELETED
    )
