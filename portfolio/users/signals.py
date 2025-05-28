import os
import shutil
import stat
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Profile

# def delete_file_and_parent_folder(file_path):
#     """Safely delete a file and its parent folder if empty."""
#     try:
#         if os.path.isfile(file_path):
#             os.remove(file_path)

#             # Get parent folder
#             parent_folder = os.path.dirname(file_path)

#             # Make parent folder writable just in case
#             os.chmod(parent_folder, stat.S_IWRITE)

#             # Delete parent folder if empty
#             if os.path.exists(parent_folder) and not os.listdir(parent_folder):
#                 shutil.rmtree(parent_folder)

#     except Exception as e:
#         # Optionally log the error, or ignore
#         pass

def delete_file_safely(file_path):
    """Safely delete a file if it exists."""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
    except Exception:
        pass


@receiver(post_delete, sender=Profile)
def delete_profile_image_on_delete(sender, instance, **kwargs):
    """Delete profile image from filesystem when a Profile is deleted."""
    if instance.image and instance.image.name:
        delete_file_safely(instance.image.path)

@receiver(pre_save, sender=Profile)
def delete_old_profile_image_on_update(sender, instance, **kwargs):
    """Delete old profile image when a Profile is updated with a new image."""
    if not instance.pk:
        return False  # No previous file if new object

    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return False

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        delete_file_safely(old_image.path)
