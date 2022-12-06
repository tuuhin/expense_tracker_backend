from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from expense_tracker.utils import delete_photoURL, resize_photo
from expense_tracker.validators import number_lt_zero
from .choices import NotificationActions, ReminderChoices


class Goal(models.Model):

    title = models.CharField(max_length=50, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    collected = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=timezone.now)
    price = models.FloatField(null=False, validators=[number_lt_zero])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="goals", null=True, blank=True)

    @property
    def is_accomplished(self):
        return self.collected >= self.price

    class Meta:
        ordering = '-updated_at',

    def save(self, *args, **kwags):

        if self.image:
            resize_photo(self.image, self.user, resize=True)

        return super().save(*args, **kwags)

    def delete(self, *args, **kwargs):

        if self.image:
            delete_photoURL(self.image, self.user)
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Budget(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    desc = models.TextField(blank=True, null=True)
    _from = models.DateTimeField(verbose_name="from", default=timezone.now)
    to = models.DateTimeField(verbose_name="to")
    total_amount = models.FloatField(
        null=False, blank=False, validators=[number_lt_zero])
    amount_used = models.FloatField(
        default=0.0, null=False, blank=False, validators=[number_lt_zero],editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=timezone.now)

    @property
    def has_expired(self):
        return not self.to > timezone.now()

    @property
    def amount_left(self):
        return self.total_amount-self.amount_used

    class Meta:
        ordering = '-issued_at',

    def __str__(self):
        return f"{self.title}"


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


class Reminder(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=ReminderChoices.choices, default=ReminderChoices.INFO)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
