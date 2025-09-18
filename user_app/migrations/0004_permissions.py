from django.db import migrations


def create_global_content_type_and_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')

    # создаем или получаем content_type
    content_type, _ = ContentType.objects.get_or_create(
        app_label='user_app',
        model='global'
    )

    # список прав
    perms = [
        ('can_manage_users', 'Can manage users'),
        ('can_add_permission_users', 'Can add permissions for users'),
        ('can_access_users_list', 'Can access users list'),
    ]

    for codename, name in perms:
        Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type
        )


def rollback_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')

    try:
        content_type = ContentType.objects.get(app_label='user_app', model='global')
        Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                'can_manage_users',
                'can_add_permission_users',
                'can_access_users_list'
            ]
        ).delete()
    except ContentType.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_adminuser_date_joined'),  # замени на реальную предыдущую миграцию
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(
            create_global_content_type_and_permissions,
            rollback_permissions
        ),
    ]