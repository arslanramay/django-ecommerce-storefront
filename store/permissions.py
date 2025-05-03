from rest_framework import permissions
# from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """
    def has_permission(self, request, view):
        # Allow read-only access for all users
        # if request.method in ['GET', 'HEAD', 'OPTIONS']:
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only for admin users
        return bool(request.user and request.user.is_staff)