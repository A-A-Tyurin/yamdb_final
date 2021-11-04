from rest_framework.permissions import IsAuthenticated


class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        is_admin = False
        if is_authenticated:
            is_admin = (request.user.is_admin or request.user.is_superuser)
        return is_admin
