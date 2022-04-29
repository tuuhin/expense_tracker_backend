from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from expense_tracker.utils import resize_photo, delete_photoURL


def profile_path_with_node():
    pass


class Profile(models.Model):

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    firstName = models.CharField(max_length=50, blank=True,)
    lastName = models.CharField(max_length=50, blank=True,)
    photoURL = models.ImageField(
        upload_to="", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=datetime.now)

    def save(self, *args, **kwargs):

        if self.photoURL:
            resize_photo(self.photoURL)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        if self.photoURL:
            delete_photoURL(self.photoURL)

        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}'
