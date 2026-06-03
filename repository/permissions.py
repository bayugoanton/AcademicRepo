from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author', None) == request.user or getattr(obj, 'uploader', None) == request.user or getattr(obj, 'user', None) == request.user or request.user.is_staff