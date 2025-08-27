from django.contrib import admin
from  .models import AdminUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = AdminUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('email',)
    list_filter = ['is_active', 'is_staff', 'date_joined']
    fieldsets = (
        (None,{'fields': ('email', 'first_name', 'last_name', 'password','phone_number','date_of_birth')}),
        ('Permissions',{'fields': ('is_active', 'is_staff', 'is_superuser', 'groups','user_permissions')}),
    )

    add_fieldsets = (
        ('User_creation',{
            'classes': ('wide',),
            'fields': ('email', 'password1','password2','first_name', 'last_name', 'phone_number','date_of_birth'),
        }),)
    

admin.site.register(AdminUser, CustomUserAdmin)