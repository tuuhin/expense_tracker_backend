from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from expense_tracker.utils import resize_photo, delete_photoURL


class Profile(models.Model):

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    firstName = models.CharField(max_length=50, blank=True, null=True)
    lastName = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=250, null=True, blank=True)
    photoURL = models.ImageField(
        upload_to="profile/", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=timezone.now)

    def save(self, *args, **kwargs):

        if self.photoURL:
            resize_photo(self.photoURL, self.user)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        if self.photoURL:
            delete_photoURL(self.photoURL, self.user)

        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.user.username}'
