from django.db import models


class NotificationActions(models.TextChoices):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    BLANK = 'blank'


class ReminderChoices(models.TextChoices):
    INFO = 'info'
    WARNING = 'warning'
    ALERT = 'alert'
