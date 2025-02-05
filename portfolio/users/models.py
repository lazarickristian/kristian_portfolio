from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def user_directory_path(instance, filename):
    # This function will generate a unique upload path based on the username
    return f'users/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.user.username