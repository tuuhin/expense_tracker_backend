from datetime import datetime
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import boto3


class Profile(models.Model):

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    firstName = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    photoURL = models.ImageField(upload_to="profiles/", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=datetime.now)

    def save(self, *args, **kwargs):

        if self.photoURL:
            img = Image.open(self.photoURL)
            if img.width > 300 or img.height > 300:
                img.thumbnail((300, 300))
                img.save(self.photoURL)

        return super().save()

    def delete(self, *args, **kwargs):
        print("triggering delete method...")

        if self.photoURL:

            try:
                botoClient = boto3.client('s3')
                botoClient.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"profile/{self.photoURL}")
                print(f"{self.user.username}/{self.photoURL.name} has been deleted")
            except Exception as e:
                print(f"{e} is the exception")

        return super().delete()

    def __str__(self):
        return f'{self.user.username}'
