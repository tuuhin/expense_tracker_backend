from io import BytesIO

from boto3 import client as AWSClient
from PIL import Image

from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile


def delete_photoURL(photoURL: ImageFieldFile, user: User):
    try:
        botoClient = AWSClient('s3')
        botoClient.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"{user.username}/{photoURL.name}")
        print(f"{photoURL} has been deleted")
    except Exception as e:
        print(f"{e} is the exception\n")
        print("There was some error due to which the photoURL can't be deleted.")


def resize_photo(photo: ImageFieldFile, user: User, resize: bool = True):
    img = Image.open(photo).convert("RGB")
    if img.size > (512, 512) and resize:
        img.thumbnail((512, 512))  # Resize to size
    output = BytesIO()
    # Save resize image to bytes
    img.save(output, format="JPEG")
    output.seek(0)
    # Read output and create ContentFile in memory
    content_file = ContentFile(output.read())
    file = File(content_file)
    # get only the name of the photo
    photo_name = photo.name.split("/")[-1]
    photo.save(f"{user.username}/{photo_name}", file, save=False)
