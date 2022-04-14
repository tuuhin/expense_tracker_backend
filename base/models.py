from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=datetime.now)

    phoneNumber = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
