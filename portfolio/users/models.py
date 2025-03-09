from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
import shutil 

def user_directory_path(instance, filename):
    # This function will generate a unique upload path based on the username
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f'users/{instance.user.username}/{instance.user.username}{extension}'
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.user.username