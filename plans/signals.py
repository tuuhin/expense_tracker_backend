from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from plans.models import Goal, Notifications
from api.models import Category, Expenses


# @receiver([pre_save], sender=Goal)
# def create_category_if_not_exists(sender, instance, **kwargs):
#     goal_categories = Category.objects.filter(
#         user=instance.user, title="goals").first()
#     if not goal_categories:
#         Category.objects.create(user=instance.user, title="goals")


@receiver([post_save], sender=Goal)
def create_a_new_expense(sender, instance, created, **kwargs):
    print(sender)

    if instance.is_accomplised() and created:
        category = Category.objects.filter(user=instance.user, title="goals")

        if not category:
            category = Category.objects.create(
                user=instance.user, title="goals")
        expense = Expenses.objects.create(
            user=instance.user, amount=instance.amount)
        expense.category.add(category)


@receiver([pre_save], sender=Goal)
def add_goals_to_notifications(sender, instance, **kwags):
    goal_exists = Goal.objects.filter(
        user=instance.user, title=instance.title).first()
    if not goal_exists:
        Notifications.objects.create(
            user=instance.user, title=f"Created Goal {instance}")
    else:
        Notifications.objects.create(
            user=instance.user, title=f"Updated Goal {instance}")
