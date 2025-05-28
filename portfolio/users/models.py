from django.db import models
from django.conf import settings
import os
from datetime import datetime


# def user_directory_path(instance, filename):
#     # This function will generate a unique upload path based on the username
#     #print(filename[-4:])
#     return f'users/{instance.user.username}/{instance.user.username}{filename[-4:]}'
    
def user_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]  # Get file extension (.jpg, .png, etc.)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f'users/{instance.user.username}/{instance.user.username}_{timestamp}{extension}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return self.user.username