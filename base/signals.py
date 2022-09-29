from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from plans.models import Notifications


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Create a profile for the  user and 
    '''
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def remove_profile(sender, instance, **kwags):
    ''' 
    Delete the profile if the user  delete itself
    '''
    users_profile = Profile.objects.filter(user=instance)

    if users_profile:
        users_profile.delete()
