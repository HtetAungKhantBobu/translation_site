from rest_framework.permissions import BasePermission

__all__ = [
    "AllowAny",
    "IsStaff",
    "IsSuperUser",
    "IsTranslatorOrReadOnly",
]

SAFE_METHODS = ["GET", "HEAD", "OPTION"]


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return True if request.user and request.user.is_superuser else False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return True if request.user and request.user.is_staff else False


class IsTranslatorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_superuser:
            return True
        return False
