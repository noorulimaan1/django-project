from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
        )


class IsAgentOrAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                hasattr(request.user, "agent_profile")
                or hasattr(request.user, "admin_profile")
            )
        )
