from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user and (request.user.is_staff or request.user.is_superuser)) or request.method in SAFE_METHODS
