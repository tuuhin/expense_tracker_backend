from django.dispatch import receiver
from django.db.models.signals import pre_save

from .models import Goal


@receiver([pre_save], sender=Goal)
def create_category_if_not_exists(sender, instance, **kwargs):
    pass
