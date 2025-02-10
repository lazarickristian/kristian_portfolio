from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Profile
import os
import shutil
import stat

@receiver(post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes the file and its parent directory (if empty) when the corresponding `Profile` object is deleted.
    """
    if instance.image:
        # Get the file path
        file_path = instance.image.path

        # Check if the file exists
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)

            # Get the parent directory
            parent_directory = os.path.dirname(file_path)

            # Check if the parent directory is empty
            if os.path.exists(parent_directory) and not os.listdir(parent_directory):
                # Delete the parent directory if it's empty
                os.chmod(parent_directory, stat.S_IWRITE)  # Allow write permissions
                shutil.rmtree(parent_directory)

@receiver(pre_save, sender=Profile)
def auto_delete_file_on_update(sender, instance, **kwargs):
    """
    Deletes the previous image file when the `Profile` instance is updated with a new image.
    """

    if not instance.pk:
        # If the instance is being created (not updated), do nothing
        return False

    try:
        # Get the existing instance from the database
        old_instance = Profile.objects.get(pk=instance.pk)

        # Check if the image field has changed
        if old_instance.image and old_instance.image != instance.image:
            # Delete the old image file
            
            if os.path.isfile(old_instance.image.path):
                os.remove(old_instance.image.path)

                # Optionally, delete the parent directory if it's empty
                parent_directory = os.path.dirname(old_instance.image.path)
                if os.path.exists(parent_directory) and not os.listdir(parent_directory):
                    os.chmod(parent_directory, stat.S_IWRITE)  # Allow write permissions
                    shutil.rmtree(parent_directory)
    except Profile.DoesNotExist:
        # If the instance doesn't exist in the database, do nothing
        return False