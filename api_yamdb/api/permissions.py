from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions


class IsAdminOrSuperuserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_superuser or request.user.is_admin)
        return False


class IsStuffOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.user and request.user.is_authenticated:
            if request.user.is_admin:
                return True
            else:
                raise PermissionDenied(request.method)
