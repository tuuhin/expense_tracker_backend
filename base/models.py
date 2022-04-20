from datetime import datetime
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
import boto3
from io import BytesIO


class Profile(models.Model):

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    firstName = models.CharField(max_length=50, blank=True, default='')
    lastName = models.CharField(max_length=50, blank=True, default='')
    photoURL = models.ImageField(upload_to="profiles/", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=datetime.now)

    def save(self, *args, **kwargs):
        # overrideing the save method to change the dimmesion of the image
        profile = Profile.objects.get(user=self.user)

        if self.photoURL and not profile.photoURL == self.photoURL:

            img = Image.open(self.photoURL)
            source_image = img.convert('RGB')
            source_image.thumbnail((200, 200))  # Resize to size
            output = BytesIO()
            # Save resize image to bytes
            source_image.save(output, format='JPEG')
            output.seek(0)
            # Read output and create ContentFile in memory
            content_file = ContentFile(output.read())
            file = File(content_file)
            self.photoURL.save(
                f"{self.photoURL}.jpeg", file, save=False)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photoURL:
            self.delete_photoURL()

        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}'

    def delete_photoURL(self):
        try:
            botoClient = boto3.client('s3')
            botoClient.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"{self.photoURL}")
            print(f"{self.photoURL} has been deleted")
        except Exception as e:
            print(f"{e} is the exception\n")
            print("There was some error due to which the photoURL can't be deleted.")
