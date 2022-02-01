from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from repo.models import File, Folder, HeirData, User

# fields and filters


class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in File._meta.get_fields()]
    list_filter = [field.name for field in File._meta.get_fields()]


class FolderAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "name", "is_root", "is_shared"]
    list_filter = ["id", "owner", "name", "is_root", "is_shared"]


class HeirDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HeirData._meta.get_fields()]
    list_filter = [field.name for field in HeirData._meta.get_fields()]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(HeirData, HeirDataAdmin)
