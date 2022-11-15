from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class CartPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated())