from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from customers.forms import UserChangeForm, UserCreationForm
from customers.models import CustomUser, Address


class UserAdmin(BaseUserAdmin):
    """manage panel of admin"""

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["phonenumber", "firstname", "lastname", "is_active",
                    "is_admin", "is_deleted"]
    search_field = ["phonenumber", "is_admin", "is_active"]
    list_filter = ["is_admin", "created", "is_active", "is_deleted"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["phonenumber", "firstname", "lastname", ]}),
        # ("Address info", {"fields": ["user_city", "user_address", "user_postcode", ]}),
        ("General info", {"fields": ["how_know_us", "is_deleted"]}),
        ("Permissions", {"fields": ["is_active", "is_admin", "groups", "user_permissions"]}),
    ]

    add_fieldsets = [
        (None, {"classes": ["wide"],
                "fields": ["phonenumber", "email", "firstname", "lastname",
                           "password1", "password2", "how_know_us", "is_active", "is_admin"], },),
        ("Permissions", {"fields": ["is_active", "is_admin", "groups", "user_permissions"],
                         },),
    ]
    ordering = ["is_admin", "created"]
    filter_horizontal = []

    def get_queryset(self, request):
        return CustomUser._base_manager.all()


admin.site.unregister(Group)


class CustomGroupAdmin(GroupAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.user = None

    def has_permission(request):
        return request.user.is_authenticated and request.user.is_admin


class AddressAdmin(admin.ModelAdmin):
    list_display = ["city", "address", "postcode", ]


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Group)
admin.site.register(Address, AddressAdmin)
