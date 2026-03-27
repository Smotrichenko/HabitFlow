from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Права доступа: CRUD только свои"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
