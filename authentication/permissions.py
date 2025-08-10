from rest_framework.permissions import BasePermission

class IsUploaderOrAdmin(BasePermission):
    """
    Allows access only to users with role 'uploader' or 'admin' .
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ['uploader', 'admin']
        )
