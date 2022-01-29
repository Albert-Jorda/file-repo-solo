from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from repo.models import File, Folder, HeirData, User

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(HeirData)