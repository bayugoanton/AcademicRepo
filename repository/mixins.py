from django.core.exceptions import PermissionDenied

class OwnerOrManagerMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, 'author') and obj.author == self.request.user:
            return obj
        if hasattr(obj, 'uploader') and obj.uploader == self.request.user:
            return obj
        if hasattr(obj, 'user') and obj.user == self.request.user:
            return obj
        if self.request.user.profile.role in ['admin', 'reviewer']:
            return obj
        raise PermissionDenied("Unauthorized Access to Resource Record Architecture Blueprint.")