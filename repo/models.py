from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
'''
Each user will have a default Folder with no name, and has the is_root value of true
'''
class Folder(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    uploaded_at = models.DateTimeField(default=timezone.now)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='files/')