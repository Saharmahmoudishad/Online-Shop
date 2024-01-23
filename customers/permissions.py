# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
#
#
# class CustomPermission:
#
#     @staticmethod
#     def create_one_type_permission_in_all_models(type_prem: str):
#         codename = f'{type_prem}_all_models'
#         name = f'Can {type_prem.capitalize()} All Models'
#         print("3" * 40, name)
#         permission, created = Permission.objects.get_or_create(codename=codename, name=name)
#         print("3"*40,permission)
#         return permission
#
#     @staticmethod
#     def create_full_permission_for_app(app_name: str):
#         print("5" * 40, ContentType.objects.all())
#         content_type = ContentType.objects.get_for_models(app_name=app_name)
#         print("4" * 40, content_type)
#         permission_codename = f'can_access_{app_name}_app'
#         permission_name = f'Can Access {app_name.capitalize()} App'
#         print("3" * 40, permission_name)
#         permission, created = Permission.objects.get_or_create(
#             codename=permission_codename,
#             name=permission_name,
#             content_type=content_type,
#         )
#         print("3" * 40, permission)
#         return permission

    # @staticmethod
    # def create_customer_management_permission():
    #     content_type = ContentType.objects.get_for_model("CustomUser")
    #     permission_codename = 'manage_customers'
    #     permission_name = 'Can Add, Edit, and Delete Customers'
    #     permission, created = Permission.objects.get_or_create(
    #         codename=permission_codename,
    #         name=permission_name,
    #         content_type=content_type,
    #     )
    #     return permission
