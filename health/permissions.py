from rest_framework import permissions


class IsCatOwnerOrReadOnly(permissions.BasePermission):
    """Только владелец кота может создавать/изменять/удалять записи его здоровья."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.cat.owner == request.user
