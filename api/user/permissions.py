from rest_framework.permissions import IsAuthenticated


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_admin or request.user.is_superuser
        return False
