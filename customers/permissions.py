from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

list_group = ['managers', 'operators', 'supervisors', 'customers']


def add_all_permission_of_app(app_label, group):
    content_types = ContentType.objects.filter(app_label=app_label)
    for content_type in content_types:
        model_name = content_type.model
        type_perms = ['add', 'change', 'delete', 'view']
        for type_perm in type_perms:
            permission_codename = f'{type_perm}_{model_name}'
            permission = Permission.objects.get(content_type=content_type, codename=permission_codename)
            group.permissions.add(permission)
    return group


def add_view_permission_to_group(group, type_perm):
    content_types = ContentType.objects.all()
    for content_type in content_types:
        model_name = content_type.model
        permission_codename = f'{type_perm}_{model_name.lower()}'
        permission = Permission.objects.get(content_type=content_type, codename=permission_codename)
        group.permissions.add(permission)
    return group


def add_full_permission(group):
    content_types = ContentType.objects.all()
    for content_type in content_types:
        model_name = content_type.model
        type_perms = ['add', 'change', 'delete', 'view']
        for type_perm in type_perms:
            permission_codename = f'{type_perm}_{model_name}'
            permission = Permission.objects.get(content_type=content_type, codename=permission_codename)
            group.permissions.add(permission)
    return group
