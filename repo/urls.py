from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from fire import settings
from repo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),

    # Auth
    path('login', views.login_request, name='login'),
    path('register', views.register_request, name='register'),
    path('logout', views.logout_request, name='logout'),

    # File/Folder views
    path('repo/view', views.view_repo, name='view-repo'),
    path('repo/view/folder/<int:folder_id>',
         views.view_folder, name='view-folder'),
    path('repo/view/archive',
         views.view_archive, name='view-archive'),
    path('repo/view/file/<int:file_id>', views.view_file, name='view-file'),

    # File Upload
    path('repo/upload/file-to-folder/<int:folder_id>',
         views.upload_file_to_folder, name='upload-file-to-folder'),
    path('repo/upload/file', views.upload_file, name='upload-file'),

    # File repo
    path('repo/create/folder/<int:parent_folder_id>',
         views.create_folder, name='create-folder'),
    path('repo/delete/folder/<int:folder_id>',
         views.delete_folder, name='delete-folder'),
    path('repo/delete/file/<int:file_id>',
         views.delete_file, name='delete-file'),
    path('repo/rename/folder/<int:folder_id>',
         views.rename_folder, name='rename-folder'),
    path('repo/rename/file/<int:file_id>',
         views.rename_file, name='rename-file'),
    path('repo/add/archive/<int:file_id>', views.archive_file, name="archive-file"),
    path('repo/remove/archive/<int:file_id>', views.restore_file, name="restore-file"),

    # Profile
    path('profile/change', views.view_profile, name="view-profile"),
    path('profile/change/password', views.change_password, name='change-password'),
    path('profile/change/username', views.change_username, name='change-username'),
    path('profile/change/email', views.change_email, name='change-email'),
    path('profile/change/profile_picture',
         views.change_profile_picture, name='change-profile-picture'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
