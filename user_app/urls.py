from django.urls import path
from .views import manage_user_permissions

urlpatterns = [
    path('manage-permissions/', view = manage_user_permissions, name = 'manage_user_permissions' )
]