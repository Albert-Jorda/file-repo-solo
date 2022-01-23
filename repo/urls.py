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

    # File Repo
    path('repo/view', views.view_repo, name='view-repo'),
    path('repo/view/folder/<int:folder_id>', views.view_folder, name='view-folder'),
    path('repo/view/file/<int:file_id>', views.view_file, name='view-file'),

    path('repo/create/folder/<int:parent_folder_id>', views.create_folder, name='create-folder'),
    path('repo/upload/file-to-folder/<int:folder_id>', views.upload_file_to_folder, name='upload-file-to-folder'),
    path('repo/upload/file', views.upload_file, name='upload-file')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

