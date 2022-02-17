from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Folder, User

@receiver(post_save, sender=User)
def create_folder(sender, instance, created, **kwargs):
    if created:
        new_root_folder = Folder(
            owner=instance,
            name="root",
            is_root=True
        )
        new_root_folder.save()