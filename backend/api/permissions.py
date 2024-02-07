from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedAuthorOrReadOnly(BasePermission):
    """Разрешение дляа аутентифицированного автора или только для чтения"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author
