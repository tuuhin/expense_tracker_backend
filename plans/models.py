from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from expense_tracker.utils import delete_photoURL, resize_photo
from expense_tracker.validators import number_lt_zero


class Goal(models.Model):

    title = models.CharField(max_length=50, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    collected = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=timezone.now)
    price = models.FloatField(null=False, validators=[number_lt_zero])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accomplished = models.BooleanField(
        default=False, editable=False)
    image = models.ImageField(upload_to="", null=True, blank=True)

    class Meta:
        ordering = ('-updated_at',)

    def save(self, *args, **kwags):

        if self.image:
            resize_photo(self.image)

        return super().save(*args, **kwags)

    def delete(self, *args, **kwargs):

        if self.image:
            delete_photoURL(self.image)
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Budget(models.Model):

    title = models.CharField(max_length=50, null=False, blank=False)
    desc = models.TextField(blank=True, null=True)
    _from = models.DateTimeField(verbose_name="from", default=timezone.now)
    to = models.DateTimeField()
    total_amount = models.FloatField(
        null=False, blank=False, validators=[number_lt_zero])
    amount_used = models.FloatField(
        default=0.0, null=False, blank=False, validators=[number_lt_zero])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    has_expired = models.BooleanField(default=False, editable=False)

    class Meta:
        ordering = ('-issued_at',)

    def __str__(self):
        return f"{self.title}"


class NotificationActions(models.TextChoices):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    BLANK = 'blank'


class Notifications(models.Model):

    title = models.CharField(max_length=50, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=NotificationActions.choices, default=NotificationActions.BLANK)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-at',)

    def __str__(self):
        return f"{self.title}"
