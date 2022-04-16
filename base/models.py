from datetime import datetime
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import boto3


class Profile(models.Model):

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    photoURL = models.ImageField(
        upload_to="profiles/", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=datetime.now)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.photoURL:
            print(self.photoURL.path)
            img = Image.open(self.photoURL.path)
            if img.width > 300 or img.height > 300:
                img.thumbnail((300, 300))
                img.save(self.photoURL.path)

    def delete(self, *args, **kwargs):

        if self.photoURL:
            boto3.client('s3').delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f'profiles/{self.photoURL.name}')
            print(f"{self.user.username}/{self.photoURL.name} has been deleted")

        return super().delete()

    def __str__(self):
        return f'Profile {self.user.username}'
