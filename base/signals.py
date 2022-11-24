from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from plans.models import Notifications, Budget, Goal
from api.models import Category, Expenses, Income, Source


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,firstName=instance.username)


@receiver(pre_delete, sender=User)
def remove_profile(sender, instance: User, **kwags):
    profile = Profile.objects.filter(user=instance).first()
    if profile:
        Notifications.objects.filter(user=instance.pk).delete()
        Category.objects.filter(user=instance.pk).delete()
        profile.delete()
