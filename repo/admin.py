from django.contrib import admin
from repo.models import File, Folder, HeirData
# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(HeirData)