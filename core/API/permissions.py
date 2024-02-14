from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnerOrReadonly(BasePermission):
    message = 'permission denied, you are not allowed'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
