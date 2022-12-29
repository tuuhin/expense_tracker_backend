from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save

from api.models import Category, Expenses, Income, Source
from plans.models import Notifications, Budget
from plans.choices import NotificationActions, NotificationSignalChoices


@receiver([post_save], sender=Expenses)
def add_notification_for_expense(sender, instance: Expenses, created: bool,  **kwags):

    if created:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.CREATED,
            signal=NotificationSignalChoices.EXPENSE
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.UPDATED,
            signal=NotificationSignalChoices.EXPENSE
        )


@receiver([pre_delete], sender=Expenses)
def expense_delete(sender: Expenses, instance: Expenses, **kwags):
    Notifications.objects.create(
        user=instance.user,
        title=f"{instance}",
        status=NotificationActions.DELETED,
        signal=NotificationSignalChoices.EXPENSE
    )


@receiver([post_save], sender=Income)
def add_notification_for_income(sender, instance: Income, created: bool, **kwags):

    if not created:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.UPDATED,
            signal=NotificationSignalChoices.INCOME
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.CREATED,
            signal=NotificationSignalChoices.INCOME
        )


@receiver([pre_delete], sender=Income)
def remove_notification_for_income(sender: Income, instance: Income,  **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"{instance}",
        status=NotificationActions.DELETED,
        signal=NotificationSignalChoices.INCOME
    )


@receiver([post_save], sender=Source)
def add_notification_for_source(sender: Source, instance: Source, created: bool,  **kwags):

    if created:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.CREATED,
            signal=NotificationSignalChoices.SOURCE
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.UPDATED,
            signal=NotificationSignalChoices.SOURCE
        )


@receiver([pre_save], sender=Category)
def add_notification_for_category(sender, instance: Category, **kwags):
    category = Category.objects.filter(pk=instance.pk).first()

    if not category:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.CREATED,
            signal=NotificationSignalChoices.CATEGORY
        )
    else:
        Notifications.objects.create(
            user=instance.user,
            title=f"{instance}",
            status=NotificationActions.UPDATED,
            signal=NotificationSignalChoices.CATEGORY
        )


@receiver([pre_delete], sender=Source)
def remove_source_notification(sender: Category, instance: Category, **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"{instance}",
        status=NotificationActions.DELETED,
        signal=NotificationSignalChoices.SOURCE
    )


@receiver([pre_delete], sender=Category)
def remove_category_notification(sender, instance: Category, **kwags):

    Notifications.objects.create(
        user=instance.user,
        title=f"{instance}",
        status=NotificationActions.DELETED,
        signal=NotificationSignalChoices.CATEGORY
    )
