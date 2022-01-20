from statistics import mode
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from fire.settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    pass

'''
Each user will have a default Folder with no name, and has the is_root value of true
'''
class Folder(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=64)
    is_root =  models.BooleanField(default=False)
    is_shared =  models.BooleanField(default=False)

'''
A folder, if not is_root should have an heir data with it as the "folder"
It will relate itself to a folder which it will refer to as its "parent"

'''
class HeirData(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="parents")
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="children")


class File(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")