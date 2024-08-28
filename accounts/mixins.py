from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Allow access to superusers only
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect to login if user is not authenticated
        if not self.request.user.is_authenticated:
            return redirect('login')
        # Raise PermissionDenied if user is authenticated but not authorized
        else:
            raise PermissionDenied