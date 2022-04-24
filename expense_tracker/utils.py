from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
import boto3


def delete_photoURL(photoURL):
    try:
        botoClient = boto3.client('s3')
        botoClient.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=f"{photoURL}")
        print(f"{photoURL} has been deleted")
    except Exception as e:
        print(f"{e} is the exception\n")
        print("There was some error due to which the photoURL can't be deleted.")


def resize_photo(photo):
    img = Image.open(photo)
    source_image = img.convert('RGB')
    source_image.thumbnail((200, 200))  # Resize to size
    output = BytesIO()
    # Save resize image to bytes
    source_image.save(output, format='JPEG')
    output.seek(0)
    # Read output and create ContentFile in memory
    content_file = ContentFile(output.read())
    file = File(content_file)
    photo.save(f"{photo}", file, save=False)
