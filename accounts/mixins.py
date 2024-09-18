from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from accounts.constants import ADMIN

class RoleRequiredMixin(UserPassesTestMixin):
    required_role = None

    def test_func(self):
        user_role = self.request.user.role
        return user_role and user_role.name == self.required_role

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            raise PermissionDenied

class AdminRequiredMixin(RoleRequiredMixin):
    required_role = 'Admin'

    def dispatch(self, request, *args, **kwargs):
        # Check if user is staff as well
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Allow access to superusers only
        return self.request.user.role == ADMIN

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        # authenticated, not authorized
        else:
            raise PermissionDenied
