from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from expense_tracker.utils import delete_photoURL, resize_photo


class Goal(models.Model):

    title = models.CharField(max_length=50, null=False, blank=False)
    desc = models.TextField(null=True, blank=True)
    collected = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=datetime.now)
    actual_price = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accomplished = models.BooleanField(
        default=collected == actual_price, editable=False)
    image = models.ImageField(upload_to="goals", null=True)

    @property
    def is_accomplished(self):
        return self.is_accomplished

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
    amount = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f""


class Saving(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
