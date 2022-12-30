from django.db import models


class NotificationActions(models.TextChoices):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    BLANK = 'blank'


class NotificationSignalChoices(models.TextChoices):
    EXPENSE = "expense"
    INCOME = "income"
    SOURCE = "source"
    CATEGORY = "category"
    BUDGET = "budget"
    GOAL = "goal"
    PROFILE = "profile"
    UNKNOWN = "unknown"
