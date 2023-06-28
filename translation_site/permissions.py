from rest_framework.permissions import BasePermission

__all__ = [
    "AllowAny",
    "IsSuperUser",
]


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return True if request.user and request.user.is_superuser else False
