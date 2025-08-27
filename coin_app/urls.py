from django.urls import path
from coin_app.views import upload_file,list_file,view_file,delete_file

urlpatterns = [
    path('upload/', upload_file, name = 'upload_file'),
    path('files/', list_file, name = 'list_file'),
    path('file/<int:file_id>/', view_file, name = 'view_file'),
    path('file/<int:file_id>/delete/', delete_file, name = 'delete_file'),
]