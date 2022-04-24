from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from .models import Goal
from api.models import Category, Expenses


@receiver([pre_save], sender=Goal)
def create_category_if_not_exists(sender, instance, **kwargs):
    goal_categories = Category.objects.filter(
        user=instance.user, title="goals").first()
    if not goal_categories:
        Category.objects.create(user=instance.user, title="goals")


@receiver([post_save], sender=Goal)
def create_a_new_expense(sender, instance, created, **kwargs):
    # if instance.is_accomplised():
    #     expense = Expenses.objects.create(user=instance.user,amount=instance.amount)
    pass
